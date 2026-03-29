from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import re


load_dotenv()

# Access environment variables using os.getenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Get the client ready for gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# TOOL calculate function that LLM would use
def calculate(expression: str) -> float:
    result = eval(expression)
    return float(result)




class ReActAgent:
    def __init__(self):
        self.system_prompt = """
            You are a reasoning agent that follows the ReAct pattern.

            You have access to one tool:
            calculate(expression: str)

            Follow this format EXACTLY:

            Thought: think about the problem. For example, I need to calculate 453 * 89. I will use the calculate tool. 
            Action: calculate("expression")   # only if needed
            Observation: result of the tool
            ... (you can repeat Thought/Action/Observation multiple times)

            When you are done:
            Final Answer: your natural language answer. For example, The result of 453 multiplied by 89 is 40,317.

            Rules:
            - Use the calculator ONLY for math
            - Always show your reasoning steps
            - Strictly start with Thought every time.
        """
        self.memory = ""

    def call_llm(self, prompt):
        # get response based on prompt from gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=types.Part.from_text(text=prompt),
            config=types.GenerateContentConfig(
                temperature=0,
                top_p=0.95,
                top_k=20,
            ))
        return response.candidates[0].content.parts[0].text

    def extract_action(self, text):
        # Extract action from LLM output
        match = re.search(r'Action:\s*calculate\("(.*?)"\)', text)
        if match:
            return match.group(1)
        return None

    def run(self, query):

        prompt = f"{self.system_prompt}\n\nUser: {query}\n"
        # persistant memory to give to LLM that is used in actual ReAct code implementation
        # prompt = self.system_prompt + "\n" + self.memory + f"\nUser: {query}\n"
        history = prompt

        for step in range(5):  # max steps

            response = self.call_llm(history)
            print(response)

            # Check if final answer
            if "Final Answer:" in response:
                answer = response.split("Final Answer:")[-1].strip()
                # self.memory += f"\nUser: {query}\n{response}\n"
                return answer

            # Extract tool call
            expression = self.extract_action(response)

            if expression:
                result = calculate(expression)
                print("Tool Result:", result)

                # Append observation and continue loop
                history += response + f"\nObservation: {result}\n"
            else:
                # No tool call, assume it's final-ish
                # self.memory += f"\nUser: {query}\n{response}\n"
                return response

        return "Stopped: too many steps"


# ---------------------------
# TEST
# ---------------------------
if __name__ == "__main__":
    agent = ReActAgent()

    print("🤖 ReAct Agent (type 'exit' to quit)\n")
    
    from colorama import Fore, Style
    while True:
        try:
            query = input("You: ")

            if query.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break

            answer = agent.run(query)


            print(Fore.GREEN + "🤖 Agent: " + answer + Style.RESET_ALL)
            print("-" * 50)

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Exiting...")
            break