import asyncio
from src.tools.helper_tools import HelperTools
from src.graphs.state import ResearchState

# Single shared instance — avoids recreating API clients per call
tools = HelperTools()

async def parallel_search_agent(state: ResearchState) -> ResearchState:
    """Runs All 4 tools for every subquestion concurrently"""
    queries = state['sub_questions']

    tasks = []

    for q in queries:
        tasks.append(asyncio.to_thread(tools.tavily_search, q, 7))
        tasks.append(asyncio.to_thread(tools.arxiv_search, q, 7))
        tasks.append(asyncio.to_thread(tools.ddgs_search, q, 7))
        # tasks.append(asyncio.to_thread(tools.semantic_scholar_search, q))

    all_results = await asyncio.gather(*tasks, return_exceptions=True)

    flat = [r for sublist in all_results if isinstance(sublist, list) for r in sublist]

    return {**state, 'search_results': flat}


async def web_search_agent(state: ResearchState) -> ResearchState:
    """Only web tools: Tavily + DuckDuckGO."""
    queries = state['sub_questions']

    tasks = []
    for q in queries:
        tasks.append(asyncio.to_thread(tools.tavily_search, q))
        tasks.append(asyncio.to_thread(tools.ddgs_search, q))

    all_results = await asyncio.gather(*tasks, return_exceptions=True)
    flat = [r for sublist in all_results if isinstance(sublist, list) for r in sublist]

    return {**state, 'search_results': flat}

async def academic_search_agent(state: ResearchState) -> ResearchState:
    """Only academic tools: arxiv + Semantic Scholar."""
    queries = state['sub_questions']
    
    tasks = []
    for q in queries:
        tasks.append(asyncio.to_thread(tools.arxiv_search, q))
        # tasks.append(asyncio.to_thread(tools.semantic_scholar_search, q))
    
    all_results = await asyncio.gather(*tasks, return_exceptions=True)
    flat = [r for sublist in all_results if isinstance(sublist, list) for r in sublist]
    
    return {**state, 'search_results': flat}