## Generative vs. Agentic: What is the fundamental difference between a standard Large Language Model (e.g., ChatGPT) and an AI Agent?

Generative AI is a type of artificial intelligence that can create new content like text, images, audio, or videos based on what a user asks. These systems usually use large language models like ChatGPT, Gemini, or Claude. They can take different kinds of inputs like text or images and give outputs in text, images, or videos. However, they only know what they were trained on and don’t have access to the latest information, tools like calculators, or live web searches. They can only respond based on their training data.

Agentic AI takes this a step further. In these systems, the language model acts as a “brain” that can not only generate content but also use tools, search for up-to-date information, and access databases. This allows the AI to reason, take actions, and solve problems, not just generate responses. We give functions as tools like calculators and web searches and the brain can use them to get better answers because the LLMs may not be good at some things like calculations.


## The Anatomy of an Agent: Describe the core components of an AI Agent.

The agent contains
1. The Brain - this the core Large Language Model like ChatGPT, Gemini, etc that creates the new content based on the query.
2. The Memory - LLMs in general do not have any kind of memory. What the agent does is append the previous conversations with the current one so that the LLM has the context of the whole conversations
3. The Tools - Agents make the LLMs access tools like calculators, live web searches, web apis, documentations, etc via rigid functions. 


## The ReAct Prompting Framework: What is "Reasoning and Acting" (ReAct) in the context of LLMs, and why is it crucial for building reliable agents?

The ReAct framework came in 2023. While LLMs were great at reasoning(chain-of-thought) and acting (action plan generation). In the ReAct framework, we try to do both in interleaved manner, to get a better synergy between reasoning and acting. Reasoning helps model track and update action plans as well as handle exceptions while actions help to gather external information. This framework helps in reducing hallucinations and error propogation in chain of thought. The loop goes like Thought -> Action -> Observation and it repeats until we get an answer. A loop would look like

**You:** What is the answer for (23-45) + (56*4)?

**Thought:** I need to calculate the value of the expression (23-45) + (56*4).
**First,** I will calculate the value of (23-45).
**Action:** calculate("23-45")
**Observation:** -22

**Thought:** Now I have the result of the first part, which is -22. Next, I will calculate the value of (56*4).
**Action:** calculate("56*4")
**Observation:** 224

**Thought:** Now I have the result of the second part, which is 224. Finally, I need to add the results of the two parts: -22 + 224.
**Action:** calculate("-22 + 224")
**Observation:** 202

**Final Answer:** The answer for (23-45) + (56*4) is 202.

🤖 Agent: The answer for (23-45) + (56*4) is 202.


## Failure Modes: What do you think is the most common reason a simple agent might fail or get stuck in an infinite loop?

On Implementation side, a failure mode can 
* **Lack of Proper EXIT Conditions** - If the agent does not know when to stop, it would just keep looping in.
* **LLM Hallucinations** - If the brain itself hallucinates, there can be cases when we cannot get a final answer or a wrong answer.
* **Lack of Tools** - If the brain lacks tools that it needs to get the final answer, we can be stuck in a loop or get a wrong answer.
* **Limited Context** - As LLMs can have only limited context, they can lose critical information that is necessary for the final answer.
* **Poor Task Decomposition** - If the agent is unable to break a complex task in different simpler tasks, the execution loop maybe wrong.



# Practical Implemntation

With Persistent Memory
```
(genai) tanishq.sharma@BLR-TanishqS Assignment 1 % clear
(genai) tanishq.sharma@BLR-TanishqS Assignment 1 % python atomic_agent.py
🤖 ReAct Agent (type 'exit' to quit)

You: what is the answer for (45+43)-(34+34)?
Thought: The user wants to know the answer to the expression (45+43)-(34+34). I will calculate the value of the expression using the `calculate` tool.
Action: calculate("(45+43)-(34+34)")
Observation: 20
Final Answer: The answer for (45+43)-(34+34) is 20.
🤖 Agent: The answer for (45+43)-(34+34) is 20.
--------------------------------------------------
You: quit    
👋 Goodbye!
```



Without Persistent Memory
```
(genai) tanishq.sharma@BLR-TanishqS Assignment 1 % python atomic_agent.py
🤖 ReAct Agent (type 'exit' to quit)

You: what is the answer for (45+43)-(34+34)?
Thought: The user wants to know the answer to the expression (45+43)-(34+34). I need to calculate the sum of the first set of numbers, then the sum of the second set of numbers, and finally subtract the second sum from the first sum.

First, I will calculate 45+43.
Action: calculate("45+43")
Observation: 88

Thought: Now I have the result of the first part, which is 88. Next, I need to calculate the sum of the second set of numbers, which is 34+34.
Action: calculate("34+34")
Observation: 68

Thought: I have both sums: 88 for the first part and 68 for the second part. Now I need to perform the subtraction: 88 - 68.
Action: calculate("88-68")
Observation: 20

Thought: I have calculated all parts of the expression and arrived at the final answer.
Final Answer: The answer for (45+43)-(34+34) is 20.
🤖 Agent: The answer for (45+43)-(34+34) is 20.
--------------------------------------------------
```