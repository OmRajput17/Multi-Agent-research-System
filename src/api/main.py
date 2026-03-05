from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.graphs.research_graph import build_graph
import asyncio

app = FastAPI(title = "Multi-Agent Research Assistant")

# Allow cross-origin requests from any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy load — build graph only on first request, not at startup
_graph = None

def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Multi-Agent Research Assistant API", "docs": "/docs"}

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

    try:
        result = await get_graph().ainvoke(initial_state)

        return {
            "report": result["final_report"],
            "citations": result["citations"],
            "fact_check": result["fact_check"],
            "route": result["route"],
            "iterations": result["iteration"]
        }
    except Exception as e:
        error_msg = str(e)
        # Handle Groq rate limit errors
        if "rate_limit" in error_msg.lower() or "429" in error_msg:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit",
                    "message": "⏳ API rate limit reached. The free Groq tier allows 100K tokens/day. Please try again in a few minutes or upgrade at console.groq.com"
                }
            )
        # Handle all other errors
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal",
                "message": f"Something went wrong: {error_msg[:200]}"
            }
        )