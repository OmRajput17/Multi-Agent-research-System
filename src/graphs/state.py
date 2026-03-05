from typing import TypedDict, List, Dict, Literal

class ResearchState(TypedDict):
    query: str ## User query
    sub_questions: List[str] ## Planner Output
    search_results: List[dict] ## Raw results from all sources
    filtered_results: List[dict] ## After relevance filtering
    summary: str ## Synthesized Answer
    fact_check: Dict[str, float] ## Claim -> confidence score
    final_report: str ## final markdown output
    citations: List[str] ## Sources url
    iteration: int ## Loop guard counter
    user_feedback: str ## Human in the loop input
    route: Literal['academic', 'web', 'mixed', 'general'] ## academic / mixed / web / general