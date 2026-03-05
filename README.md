---
title: Research Assistant
emoji: 🔬
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# 🔬 Multi-Agent Research Assistant

An AI-powered research pipeline that uses multiple specialized agents to search, filter, summarize, fact-check, and generate comprehensive research reports.

## Features

- **Multi-source search** — Tavily, arXiv, DuckDuckGo
- **Smart routing** — Academic, web, mixed, or general conversation
- **Fact-checking** — Every claim verified against sources with confidence scores
- **Professional reports** — Publication-ready markdown with inline citations
- **Iterative refinement** — Loops up to 3x if fact-check scores are low

## Architecture

```
User Query → Planner → Router → Search Agents → Filter → Summarizer → Fact-Checker → Report Writer
                                                                              ↑                |
                                                                              └── (if low) ────┘
```

## Tech Stack

- **LangGraph** — Multi-agent orchestration
- **Groq (LLaMA 3.3 70B)** — LLM inference
- **FastAPI** — Backend API
- **Streamlit** — Frontend UI
- **Tavily / arXiv / DuckDuckGo** — Search tools
