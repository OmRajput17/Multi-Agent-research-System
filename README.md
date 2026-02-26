---
title: Multi-Agent Research Assistant
emoji: 🔬
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 8000
pinned: false
---

# Multi-Agent Research Assistant

AI-powered research pipeline using LangGraph with multiple specialized agents:
- **Planner** — breaks queries into sub-questions
- **Search** — async parallel search across Tavily, arxiv, DuckDuckGo
- **Filter** — LLM-based batch relevance scoring
- **Summarizer** — synthesizes findings with citations
- **Fact-Checker** — cross-references claims against sources
- **Report Writer** — generates structured markdown reports
