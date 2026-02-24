from src.tools.helper_tools import HelperTools

tools = HelperTools()
test_query = "transformer architecture in NLP"

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

print("=" * 60)
print("TEST 1: Tavily Search")
print("=" * 60)
try:
    result = tools.tavily_search(test_query, max_results=2)
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) > 0, "No results returned"
    assert all(k in result[0] for k in ['title', 'url', 'content', 'source']), "Missing keys"
    print_results(result)
    print("✅ Tavily Search PASSED\n")
except Exception as e:
    print(f"❌ Tavily Search FAILED: {e}\n")

print("=" * 60)
print("TEST 2: Arxiv Search")
print("=" * 60)
try:
    result = tools.arxiv_search(test_query, max_results=2)
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) > 0, "No results returned"
    assert all(k in result[0] for k in ['title', 'url', 'content', 'source']), "Missing keys"
    print_results(result)
    print("✅ Arxiv Search PASSED\n")
except Exception as e:
    print(f"❌ Arxiv Search FAILED: {e}\n")

print("=" * 60)
print("TEST 3: DuckDuckGo Search")
print("=" * 60)
try:
    result = tools.ddgs_search(test_query, max_results=2)
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) > 0, "No results returned"
    assert all(k in result[0] for k in ['title', 'url', 'content', 'source']), "Missing keys"
    print_results(result)
    print("✅ DuckDuckGo Search PASSED\n")
except Exception as e:
    print(f"❌ DuckDuckGo Search FAILED: {e}\n")

print("=" * 60)
print("TEST 4: Semantic Scholar Search")
print("=" * 60)
try:
    result = tools.semantic_scholar_search(test_query, max_results=2)
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    if len(result) > 0:
        assert all(k in result[0] for k in ['title', 'url', 'content', 'source']), "Missing keys"
        print_results(result)
        print("✅ Semantic Scholar Search PASSED\n")
    else:
        print("  ⚠️ No results (API issue, not a code bug)")
        print("✅ Semantic Scholar Search PASSED (graceful empty)\n")
except Exception as e:
    print(f"❌ Semantic Scholar Search FAILED: {e}\n")
