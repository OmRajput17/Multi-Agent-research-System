"""
WARNING: This module is NOT used in the graph. It is dead code kept for reference only.
- The `human_review` function is never added as a node in research_graph.py.
- It uses `input()` which blocks and will crash in a web API (FastAPI/Streamlit) context.
- To properly implement HITL, use LangGraph's `interrupt()` / checkpointer pattern instead.
"""
from src.graphs.state import ResearchState

def human_review(state: ResearchState) -> ResearchState:
    """Pauses the graph for human feedback.
    
    NOTE: This function is NOT connected to the graph (see research_graph.py).
    It uses blocking input() which is incompatible with web deployments.
    For proper HITL, use LangGraph's interrupt() with a checkpointer."""
    print("\n" + "=" * 60)
    print("HUMAN REVIEW")
    print("=" * 60)
    print(f"\nSummary:\n{state['summary'][:500]}...")
    print(f"\nFact-Check Scores:")
    for claim, score in state['fact_check'].items():
        print(f"  - {claim}: {score}")
    
    feedback = input("\nProvide feedback (or press Enter to approve): ")
    if feedback:
        return {
            **state,
            'user_feedback': feedback,
            'iteration': state['iteration'] + 1
        }
    else:
        return {
            **state,
            'user_feedback': 'approved'
        }

