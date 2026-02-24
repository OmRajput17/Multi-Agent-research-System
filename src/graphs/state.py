from typing import TypedDict, Annotated, List, Dict
from langgraph.graph.message import add_messages

class ResearchState(TypedDict):
    query: str ## User query
    sub_questions: List[str] ## Planner Output
    search_results: List[dict] ## Raw results from all sources
    filtered_results: List[dict] ## After relevanve filtering
    summary: str ## Synthesized Answer
    fact_check: Dict[str, float] ## Clain -> confidence score
    final_report: str ## final markdown output
    citations: List[str] ## Sources url
    iteration: int ## Loop guard counter
    user_feedback: str ## Human in the loop input
    route: str ## academic / mixed / web