# 🧠 Atomic ReAct Agent

A simple Python-based **ReAct agent** that can solve arithmetic problems using a **calculator tool**.  
The agent follows the **Thought → Action → Observation → Final Answer** reasoning framework.

---

## Features

- Step-by-step reasoning using the **ReAct pattern**  
- Uses a single tool: `calculate(expression)` for arithmetic  
- Friendly terminal interface with colored output  
- Supports interactive queries

---

## Requirements

- Python 3.8+  
- Dependencies listed in `requirements.txt`  

Install them using:

```bash
pip install -r requirements.txt
```

## How to Run

Run the agent in your terminal:

```bash
python atomic_agent.py
```

You will see a prompt:

```bash
🤖 ReAct Agent (type 'exit' to quit)
You:
```

Type any arithmetic question, e.g.:

``` 
You: What is (45+43)-(34+34)?
```

The agent will respond with step-by-step reasoning and the final answer.

To exit:
```
You: exit
```
## 🛠 Example
```You: What is 45 * 12?
Thought: I need to calculate 45 * 12. I will use the calculate tool.
Action: calculate("45*12")
Observation: 540
Final Answer: The result of 45 multiplied by 12 is 540.
🤖 Agent: The result of 45 multiplied by 12 is 540.
```

## 📂 Project Structure

```.
├── atomic_agent.py       # Main agent code
├── requirements.txt      # Python dependencies
└── README.md             # This file
```


# Thought behind the reasoning loop

I use the inspiration from the actual [ReAct](https://arxiv.org/pdf/2210.03629) loop. The LLM has a specific prompt that it needs to output in the exact format i.e., **Thought**, **Action**, **Observation** and repeat until It gets the **Final Answer**. In the reasoning loop, I take maximum 5 steps, but this can be changed to an infinite loop with better error handling considering that the LLM is not stuck in an infinite loop. Firstly, checks if we have the final answer. Otherwise, extract the action. If action exists, we use the calculate function to get the results and then append this with observation. Otherwise, we assume the answer is ready. 



# Example Outputs
```
You: "What is 15% of 450, and if I subtract that from 1000, what is left?"
--- Step 1 ---
Thought: First, I need to calculate 15% of 450. Then, I need to subtract that result from 1000.
Action: calculate("0.15 * 450")
Observation: 67.5
Thought: Now I need to subtract 67.5 from 1000.
Action: calculate("1000 - 67.5")
Observation: 932.5
Final Answer: 15% of 450 is 67.5. Subtracting that from 1000 leaves 932.5.


🤖 Agent: 15% of 450 is 67.5. Subtracting that from 1000 leaves 932.5.

```

```
You: "I have 12 boxes, each with 12 eggs. I broke 18 eggs. How many are left?"
--- Step 1 ---
Thought: First, I need to calculate the total number of eggs I started with. Then, I need to subtract the number of broken eggs from the total.
Action: calculate("12*12")

Tool Result: 144.0
--- Step 2 ---
Thought: Now I know I started with 144 eggs. I need to subtract the 18 broken eggs.
Action: calculate("144-18")
Observation: 126.0
Final Answer: You have 126 eggs left.


🤖 Agent: You have 126 eggs left.
```

```
You: "What is 50 plus 10, all multiplied by 2?"
--- Step 1 ---
Thought: I need to calculate (50 + 10) * 2. I will use the calculator to perform this calculation.
Action: calculate("(50 + 10) * 2")
Observation: 120.0
Final Answer: 50 plus 10, all multiplied by 2 is 120.


🤖 Agent: 50 plus 10, all multiplied by 2 is 120.
```

```
You: "Which is more: $25 \times 25$ or $20 \times 30$?"
--- Step 1 ---
Thought: I need to compare the results of two multiplication operations. I will use the calculator to find the value of each expression.
Action: calculate("25 * 25")
Observation: 625
Thought: Now I need to calculate the second expression.
Action: calculate("20 * 30")
Observation: 600
Thought: Now I can compare the two results. 625 is greater than 600.
Final Answer: $25 \times 25$ is more than $20 \times 30$.


🤖 Agent: $25 \times 25$ is more than $20 \times 30$.

```

```
You: "How many seconds are in 2.5 hours?"
--- Step 1 ---
Thought: To calculate the number of seconds in 2.5 hours, I need to multiply the number of hours by the number of minutes per hour and then by the number of seconds per minute.
Action: calculate("2.5*60*60")
Observation: 9000.0
Final Answer: There are 9000 seconds in 2.5 hours.


🤖 Agent: There are 9000 seconds in 2.5 hours.
```