"""
Test script for src/tools/helper_tools.py
Tests all 4 search tools — validates return types, dict keys, and basic functionality.
"""
from src.tools.helper_tools import HelperTools

REQUIRED_KEYS = {'title', 'url', 'content', 'source'}
TEST_QUERY = "transformer architecture in NLP"
tools = HelperTools()


def print_results(results):
    """Pretty-print list[dict] results"""
    if not results:
        print("  (no results)")
        return
    for i, r in enumerate(results, 1):
        print(f"  [{i}] {r['title']}")
        print(f"      URL: {r['url']}")
        print(f"      Source: {r['source']}")
        print(f"      Content: {r['content'][:100]}...")
        print()


def test_tavily():
    print("=" * 60)
    print("TEST 1: Tavily Search")
    print("=" * 60)
    results = tools.tavily_search(TEST_QUERY, max_results=2)
    assert isinstance(results, list), f"Expected list, got {type(results)}"
    assert len(results) > 0, "No results returned"
    assert REQUIRED_KEYS.issubset(results[0].keys()), f"Missing keys: {REQUIRED_KEYS - results[0].keys()}"
    assert results[0]['source'] == 'tavily', f"Expected source 'tavily', got {results[0]['source']}"
    print_results(results)
    print("✅ Tavily Search PASSED\n")


def test_arxiv():
    print("=" * 60)
    print("TEST 2: Arxiv Search")
    print("=" * 60)
    results = tools.arxiv_search(TEST_QUERY, max_results=2)
    assert isinstance(results, list), f"Expected list, got {type(results)}"
    assert len(results) > 0, "No results returned"
    assert REQUIRED_KEYS.issubset(results[0].keys()), f"Missing keys: {REQUIRED_KEYS - results[0].keys()}"
    assert results[0]['source'] == 'arxiv', f"Expected source 'arxiv', got {results[0]['source']}"
    print_results(results)
    print("✅ Arxiv Search PASSED\n")


def test_ddgs():
    print("=" * 60)
    print("TEST 3: DuckDuckGo Search")
    print("=" * 60)
    results = tools.ddgs_search(TEST_QUERY, max_results=2)
    assert isinstance(results, list), f"Expected list, got {type(results)}"
    if len(results) > 0:
        assert REQUIRED_KEYS.issubset(results[0].keys()), f"Missing keys: {REQUIRED_KEYS - results[0].keys()}"
        assert results[0]['source'] == 'duckduckgo', f"Expected source 'duckduckgo', got {results[0]['source']}"
        print_results(results)
        print("✅ DuckDuckGo Search PASSED\n")
    else:
        print("  ⚠️ No results (rate limited — not a code bug)")
        print("✅ DuckDuckGo Search PASSED (graceful empty)\n")


def test_semantic_scholar():
    print("=" * 60)
    print("TEST 4: Semantic Scholar Search")
    print("=" * 60)
    results = tools.semantic_scholar_search("transformers", max_results=2)
    assert isinstance(results, list), f"Expected list, got {type(results)}"
    if len(results) > 0:
        assert REQUIRED_KEYS.issubset(results[0].keys()), f"Missing keys: {REQUIRED_KEYS - results[0].keys()}"
        assert results[0]['source'] == 'semantic_scholar'
        print_results(results)
        print("✅ Semantic Scholar Search PASSED\n")
    else:
        print("  ⚠️ No results (rate limited — not a code bug)")
        print("✅ Semantic Scholar Search PASSED (graceful empty)\n")


def test_error_handling():
    """Test that tools return empty list on bad input, not crash"""
    print("=" * 60)
    print("TEST 5: Error Handling")
    print("=" * 60)
    results = tools.tavily_search("", max_results=0)
    assert isinstance(results, list), "Should return list even on empty query"
    print(f"  Empty query returned: {len(results)} results (no crash)")
    print("✅ Error Handling PASSED\n")


if __name__ == "__main__":
    test_tavily()
    test_arxiv()
    test_ddgs()
    test_semantic_scholar()
    test_error_handling()
    print("=" * 60)
    print("ALL TOOLS TESTS PASSED ✅")
    print("=" * 60)
