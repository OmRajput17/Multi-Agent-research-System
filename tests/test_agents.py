"""
Test script for all agents in src/agents/
Tests planner, router, search_agent, filter, summarizer, fact_checker, and report_writer.
Runs end-to-end through the full pipeline.
"""
import asyncio
from src.agents.planner import PlannerAgent
from src.agents.router import route
from src.agents.search_agent import parallel_search_agent, web_search_agent, academic_search_agent
from src.agents.filter_agent import FilterAgent
from src.agents.summarizer import SummarizerAgent
from src.agents.fact_checker import FactCheckerAgent
from src.agents.report_writer import ReportWriterAgent


# Shared test state — starts minimal, gets filled as each agent runs
TEST_QUERY = "What is the transformer architecture in NLP?"

def make_initial_state():
    return {
        'query': TEST_QUERY,
        'sub_questions': [],
        'search_results': [],
        'filtered_results': [],
        'summary': '',
        'fact_check': {},
        'final_report': '',
        'citations': [],
        'iteration': 0,
        'user_feedback': '',
        'route': 'mixed'
    }


def test_planner():
    print("=" * 60)
    print("TEST 1: Planner Agent")
    print("=" * 60)
    state = make_initial_state()
    planner = PlannerAgent()
    result = planner.plan(state)

    assert 'sub_questions' in result, "Missing sub_questions"
    assert isinstance(result['sub_questions'], list), "sub_questions should be a list"
    assert len(result['sub_questions']) > 0, "sub_questions should not be empty"
    assert 'route' in result, "Missing route"
    assert result['route'] in ['academic', 'web', 'mixed'], f"Invalid route: {result['route']}"
    assert result['iteration'] == 0, "Iteration should be 0"

    print(f"  Route: {result['route']}")
    print(f"  Sub-questions ({len(result['sub_questions'])}):")
    for i, q in enumerate(result['sub_questions'], 1):
        print(f"    {i}. {q}")
    print("✅ Planner Agent PASSED\n")
    return result


def test_router(state):
    print("=" * 60)
    print("TEST 2: Router")
    print("=" * 60)
    result = route(state)
    assert result in ['academic', 'web', 'mixed'], f"Invalid route result: {result}"
    print(f"  Route decision: {result}")
    print("✅ Router PASSED\n")
    return result


async def test_search_agent(state, route_decision):
    print("=" * 60)
    print("TEST 3: Search Agent")
    print("=" * 60)
    
    if route_decision == 'academic':
        result = await academic_search_agent(state)
        agent_name = "academic_search_agent"
    elif route_decision == 'web':
        result = await web_search_agent(state)
        agent_name = "web_search_agent"
    else:
        result = await parallel_search_agent(state)
        agent_name = "parallel_search_agent"

    assert isinstance(result['search_results'], list), "search_results should be a list"
    assert len(result['search_results']) > 0, "search_results should not be empty"

    # Verify dict structure
    for r in result['search_results'][:1]:
        assert 'title' in r, "Missing 'title' key"
        assert 'url' in r, "Missing 'url' key"
        assert 'content' in r, "Missing 'content' key"
        assert 'source' in r, "Missing 'source' key"

    sources = set(r['source'] for r in result['search_results'])
    print(f"  Agent used: {agent_name}")
    print(f"  Total results: {len(result['search_results'])}")
    print(f"  Sources: {sources}")
    print("✅ Search Agent PASSED\n")
    return result


def test_filter(state):
    print("=" * 60)
    print("TEST 4: Filter Agent")
    print("=" * 60)
    filter_agent = FilterAgent()
    result = filter_agent.filter(state)

    assert isinstance(result['filtered_results'], list), "filtered_results should be a list"
    
    # Check deduplication — no duplicate URLs
    urls = [r['url'] for r in result['filtered_results']]
    assert len(urls) == len(set(urls)), "Duplicate URLs found!"

    # Check score key exists
    if len(result['filtered_results']) > 0:
        assert 'score' in result['filtered_results'][0], "Missing 'score' key"
        assert result['filtered_results'][0]['score'] >= 0.6, "Score below threshold"

    print(f"  Input: {len(state['search_results'])} results")
    print(f"  Output: {len(result['filtered_results'])} filtered results")
    for r in result['filtered_results'][:3]:
        print(f"    - [{r['score']}] {r['title'][:50]}...")
    print("✅ Filter Agent PASSED\n")
    return result


def test_summarizer(state):
    print("=" * 60)
    print("TEST 5: Summarizer Agent")
    print("=" * 60)
    summarizer = SummarizerAgent()
    result = summarizer.summarize(state)

    assert isinstance(result['summary'], str), "summary should be a string"
    assert len(result['summary']) > 50, "Summary too short"
    assert isinstance(result['citations'], list), "citations should be a list"
    assert len(result['citations']) > 0, "citations should not be empty"

    print(f"  Summary length: {len(result['summary'])} chars")
    print(f"  Preview: {result['summary'][:200]}...")
    print(f"  Citations: {len(result['citations'])}")
    print("✅ Summarizer Agent PASSED\n")
    return result


def test_fact_checker(state):
    print("=" * 60)
    print("TEST 6: Fact-Checker Agent")
    print("=" * 60)
    checker = FactCheckerAgent()
    result = checker.fact_check(state)

    assert isinstance(result['fact_check'], dict), "fact_check should be a dict"
    
    if len(result['fact_check']) > 0:
        for claim, score in result['fact_check'].items():
            assert isinstance(score, float), f"Score should be float, got {type(score)}"
            assert 0 <= score <= 1, f"Score out of range: {score}"
    
    print(f"  Claims checked: {len(result['fact_check'])}")
    for claim, score in list(result['fact_check'].items())[:3]:
        print(f"    - [{score}] {claim[:60]}...")
    print("✅ Fact-Checker Agent PASSED\n")
    return result


def test_report_writer(state):
    print("=" * 60)
    print("TEST 7: Report Writer Agent")
    print("=" * 60)
    writer = ReportWriterAgent()
    result = writer.write_report(state)

    assert isinstance(result['final_report'], str), "final_report should be a string"
    assert len(result['final_report']) > 100, "Report too short"
    assert '#' in result['final_report'], "Report should contain markdown headers"

    print(f"  Report length: {len(result['final_report'])} chars")
    print(f"  Preview:\n{result['final_report'][:300]}...")
    print("✅ Report Writer Agent PASSED\n")
    return result


async def run_all_tests():
    print("\n" + "🚀 " * 20)
    print("RUNNING FULL AGENT PIPELINE TEST")
    print("🚀 " * 20 + "\n")

    # 1. Planner
    state = test_planner()

    # 2. Router
    route_decision = test_router(state)

    # 3. Search Agent (async)
    state = await test_search_agent(state, route_decision)

    # 4. Filter
    state = test_filter(state)

    # 5. Summarizer
    state = test_summarizer(state)

    # 6. Fact-Checker
    state = test_fact_checker(state)

    # 7. Report Writer
    state = test_report_writer(state)

    print("=" * 60)
    print("🎉 ALL AGENT TESTS PASSED ✅")
    print("=" * 60)
    print(f"\nFinal state keys: {list(state.keys())}")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
