import os
import re
import time
from dotenv import load_dotenv
from openai import OpenAI
from colorama import Fore, Style

load_dotenv()

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# You can change this to "google/gemini-2.0-flash-001" or "anthropic/claude-3-haiku"
MODEL_NAME = "google/gemini-2.0-flash-001" 

# Initialize OpenAI client pointed at OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def calculate(expression: str) -> float:
    """Safe evaluation of arithmetic expressions."""
    # Basic sanitization: only allow numbers and math operators
    clean_expression = re.sub(r'[^0-9+\-*/(). ]', '', expression)
    try:
        return float(eval(clean_expression))
    except Exception as e:
        return f"Error: Invalid expression ({e})"

class ReActAgent:
    def __init__(self):
        self.system_prompt = """
        You are a reasoning agent that follows the ReAct pattern.
        You have access to one tool: calculate(expression: str)

        Follow this format EXACTLY:
        Thought: describe your reasoning.
        Action: calculate("expression")
        Observation: result of the tool
        ... (repeat if needed)
        Final Answer: your natural language response.

        Rules:
        - Use the calculator ONLY for math.
        - Strictly start with 'Thought' every time.
        """

    def call_llm(self, history):
        """Sends the conversation history to OpenRouter."""
        try:
            # Small delay to prevent rate-limiting (429 errors)
            time.sleep(1) 
            
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": history}
                ],
                temperature=0,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"API Error: {e}"

    def extract_action(self, text):
        match = re.search(r'Action:\s*calculate\("(.*?)"\)', text)
        return match.group(1) if match else None

    def run(self, query):
        history = f"User: {query}\n"
        
        for step in range(5):
            print(f"{Fore.YELLOW}--- Step {step + 1} ---{Style.RESET_ALL}")
            response = self.call_llm(history)
            print(response)

            if "Final Answer:" in response:
                return response.split("Final Answer:")[-1].strip()

            expression = self.extract_action(response)
            if expression:
                result = calculate(expression)
                print(f"{Fore.CYAN}Tool Result: {result}{Style.RESET_ALL}")
                # Append the LLM's thought/action AND the tool's result to history
                history += f"\n{response}\nObservation: {result}\n"
            else:
                # If the LLM stops without a Final Answer or Action
                return response

        return "Stopped: maximum reasoning steps reached."

# ---------------------------
# Execution
# ---------------------------
if __name__ == "__main__":
    agent = ReActAgent()
    print(f"🤖 ReAct Agent active (Model: {MODEL_NAME})")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        answer = agent.run(user_input)
        print(f"\n{Fore.GREEN}🤖 Agent: {answer}{Style.RESET_ALL}\n" + "-"*30)