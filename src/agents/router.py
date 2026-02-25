from src.graphs.state import ResearchState
from typing import Literal

def route(state: ResearchState) -> Literal['academic', 'web', 'mixed']:
    if state['route'] == 'academic':
        return 'academic'
    elif state['route'] == 'web':
        return 'web'
    else:
        return 'mixed'

