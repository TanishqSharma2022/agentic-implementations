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