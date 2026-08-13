# 🤖 AI Agent — Project 5

A simple AI Agent built from scratch using **Python + Ollama + Qwen3 8B**.

The goal of this project is to understand how an AI Agent works internally before using frameworks such as **LangGraph** or **MCP**.

---

## 🎯 Goal

Understand:

- What is an AI Agent?
- How an Agent makes decisions
- How an Agent uses tools
- Agent loops
- Tool Registry
- Agent state
- Tool execution
- How multiple tools can be added later

---

## 🔄 Application Flow

**Single Tool Flow:**
```
         User Question
               │
               ▼
            Agent
               │
               ▼
              LLM
               │
        ┌──────┴──────┐
        │             │
     ANSWER          TOOL
        │             │
        │             ▼
        │       Tool Registry
        │             │
        │             ▼
        │        Calculator
        │             │
        │             ▼
        │         Tool Result
        │             │
        └─────────────┘
               │
               ▼
             Agent
               │
               ▼
              LLM
               │
               ▼
         Final Answer
```

**Multi-Tool Flow:**
```
                 USER
                   │
                   ▼
                 AGENT
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
 Calculator    CSV Analyzer   Web Search
      │            │            │
      ▼            ▼            ▼
   Math          Pandas       Internet
      │            │            │
      └────────────┼────────────┘
                   ▼
                 RESULT
                   │
                   ▼
                  LLM
                   │
                   ▼
             FINAL ANSWER
```

---

## 🛠️ Tools

### 1. Calculator

Used for mathematical calculations.

**Example:**
```
What is 25 * 48?
```

The Agent can select: `calculator`

---

### 2. CSV Analyzer

Used to analyze the CSV dataset.

**Supported operations include:**
- Average
- Maximum
- Minimum
- Average by Group
- Other supported CSV operations

**Example:**
```
What is the average salary?
```
or:
```
Which department has the highest average salary?
```

The Agent can call: `csv_analyzer`

---

### 3. Web Search

Used for questions that require current or external information.

**Example:**
```
What is the latest Python version?
```

The Agent can select: `web_search`

---

## 🔁 Agent Loop

The Agent works in multiple steps.

**Example:**

> **User:** Which department has the highest average salary?

| Step | Action |
|------|--------|
| **Step 1** | LLM decides to use CSV Analyzer |
| **Step 2** | CSV Analyzer returns average salary for each department |
| **Step 3** | LLM analyzes the result |
| **Final Answer** | Engineering has the highest average salary. |

> The Agent supports up to **5 steps** for a single question.

---

## 📋 Tool Registry

Tools are registered centrally using `ToolRegistry`.

```python
self.registry.register(CalculatorTool)
self.registry.register(CSVTool)
self.registry.register(WebSearchTool)
```

The Agent does not need to contain the implementation of every tool. The registry is responsible for managing available tools.

---

## 🧠 Conversation Memory

The project includes a `MemoryManager`.

**Memory stores:**

**Recent Conversation**
- Recent user questions, tool calls, and tool results.

**Important Facts**
- Successful tool results can also be stored as facts.

```
IMPORTANT FACTS:

- csv_analyzer:
  average Salary = 88500
```

This allows useful information to remain available even when older conversation messages are removed.

### Memory Limit

The Agent keeps a maximum number of recent messages.

```python
MemoryManager(max_messages=12)
```

When the limit is exceeded, older conversation messages are removed. The system prompt is preserved.

| Type | Behavior |
|------|----------|
| System Prompt | Always retained |
| Recent Messages | Retained |
| Old Messages | Removed when limit is exceeded |
| Important Facts | Retained separately |

---

## ⚠️ Error Handling

The Agent does not immediately stop when a tool fails.

**Example:**

> **User:** What is the average of EmployeeName?

If the CSV tool reports that the column does not exist, the Agent can inspect the error and decide what to do next.

> The Agent is instructed **not** to blindly repeat the same failed tool call.

---

## 📁 Project Structure

```
AI_AGENT/
│
├── agent/
│   ├── agent.py
│   └── prompts.py
│
├── memory/
│   ├── memory_manager.py
│   └── __init__.py
│
├── tools/
│   ├── registry.py
│   ├── calculator.py
│   ├── csv_tool.py
│   ├── web_search.py
│   └── __init__.py
│
├── llm/
│   ├── llm.py
│   └── __init__.py
│
├── data/
│   └── employees.csv
│
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

## 📄 Important Files

| File | Description |
|------|-------------|
| `app.py` | Application entry point. Starts the Agent and accepts user questions. |
| `agent/agent.py` | Main Agent orchestration logic — calling the LLM, selecting tools, executing tools, managing the loop, returning the final answer. |
| `agent/prompts.py` | System instructions given to the LLM — available tools, expected response format, tool usage rules, agent behavior. |
| `tools/registry.py` | Maintains the list of available tools. The Agent uses the registry to discover and execute tools. |
| `tools/calculator.py` | Provides calculator functionality. |
| `tools/csv_tool.py` | Provides CSV analysis functionality. |
| `tools/web_search.py` | Provides web search functionality. |
| `memory/memory_manager.py` | Manages recent conversation, message limits, important facts, and system prompt preservation. |
| `llm/llm.py` | Connects the Agent to Ollama. Currently uses **Qwen3 8B**. |

---

## 💬 Example Questions

### 🔢 Calculator
```
What is 125 * 48?
```

### 📊 CSV
```
What is the average salary?
Which department has the highest average salary?
What about Engineering?
What about Finance?
```

### 🌐 Web Search
```
What is the latest Python version?
```

### 🧵 Conversation Memory
```
What is the average salary?
```
Then:
```
What about Engineering?
```
Then:
```
Which one is higher?
```

The Agent can use the previous conversation context.

---

## 🚀 How to Run

**1. Create and activate a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Make sure Ollama is running and the required model is available:**
```bash
ollama list
```

> This project uses: `qwen3:8b`

**4. Run:**
```bash
python3 app.py
```

You should see:
```
============================================================
                     AI AGENT
============================================================

Ask a question (type exit to quit):
```

---

## 📚 What You Learn From This Project

By completing this project, you learn the fundamentals of Agentic AI:

- What an AI Agent is
- LLM-based decision making
- Agent loops
- Tool calling
- Tool selection
- Tool registries
- Tool chaining
- Error handling
- Conversation memory
- Short-term memory management
- Important facts
- LLM + external tools
- Modular Agent architecture

---

## 🗺️ Projects Built Before This

This project is part of a progressive AI learning roadmap.

```
Project 1 — Local Multi-Document RAG Chatbot
        │
        ▼
Project 2 — Enterprise AI Database Assistant
        │
        ▼
Project 3 — AI CSV Assistant
        │
        ▼
Project 4 — AI Data Analyst
        │
        ▼
Project 5 — AI Agent  ← You are here
```

Each project introduces a new AI concept. Project 5 combines several concepts learned in the previous projects and introduces **autonomous tool selection**.

---

## ⏭️ Next Step

The next project will introduce **MCP (Model Context Protocol)**.

**Current architecture:**
```
Agent
  │
  ▼
Tool Registry
  │
  ├── CSV
  ├── Calculator
  └── Web Search
```

**MCP architecture:**
```
Agent
  │
  ▼
MCP Client
  │
  ▼
MCP Servers
  │
  ├── CSV Server
  ├── Calculator Server
  └── Web/API Server
```

This will introduce a **standardized way** for AI applications to communicate with external tools and data sources.