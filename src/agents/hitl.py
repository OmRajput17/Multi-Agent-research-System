from src.graphs.state import ResearchState

def human_review(state: ResearchState) -> ResearchState:
    """Pauses the graph for human feedback.
    In production, this is handled by the API (user submits feedback via frontend).
    For testing, we use input() to simulate."""
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

