from src.graphs.state import ResearchState
from typing import Literal

def route(state: ResearchState) -> Literal['academic', 'web', 'mixed', 'general']:
    if state['route'] == 'academic':
        return 'academic'
    elif state['route'] == 'web':
        return 'web'
    elif state['route'] == 'general':
        return 'general'
    else:
        return 'mixed'

