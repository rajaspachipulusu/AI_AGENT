# 🤖 AI Agent — Project 5

A simple AI Agent built from scratch using **Python + Ollama + Qwen3 8B**.

The goal of this project is to understand how an AI Agent works internally before using frameworks such as LangGraph or MCP.

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

```text
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