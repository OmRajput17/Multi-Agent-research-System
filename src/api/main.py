from fastapi import FastAPI
from pydantic import BaseModel
from src.graphs.research_graph import build_graph
import asyncio

app = FastAPI(title = "Multi-Agent Research Assistant")

graph = build_graph()

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/research")
async def research(request: QueryRequest):
    initial_state = {
        "query": request.query,
        "sub_questions": [],
        "search_results": [],
        "filtered_results": [],
        "summary": "",
        "fact_check": {},
        "final_report": "",
        "citations": [],
        "iteration": 0,
        "user_feedback": "",
        "route": "mixed"
    }

    result = await graph.ainvoke(initial_state)

    return {
        "report": result["final_report"],
        "citations": result["citations"],
        "fact_check": result["fact_check"],
        "route": result["route"],
        "iterations": result["iteration"]
    }