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