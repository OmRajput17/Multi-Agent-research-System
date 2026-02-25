from src.utils.get_llm import LLMConfig
from src.graphs.state import ResearchState
from langchain_core.prompts import ChatPromptTemplate
import json


class FilterAgent:
    def __init__(self):
        self.llm = LLMConfig().get_llm()
        self.prompt = ChatPromptTemplate.from_template(
            """Rate the relevance of EACH result to the query on a scale of 0 to 1.
            Return ONLY valid JSON with a list of scores, one per result.

            Query: {query}

            Results:
            {results}

            Return format: {{"scores": [0.8, 0.3, 0.9, ...]}}"""
        )
        self.chain = self.prompt | self.llm

    def filter(self, state: ResearchState) -> ResearchState:
        query = state['query']
        results = state['search_results']

        # Step 1: Format all results as numbered list
        results_text = '\n\n'.join([
            f"[{i+1}] {r['title']}\n{r['content'][:300]}"
            for i, r in enumerate(results)
        ])

        # Step 2: One LLM call to score ALL results
        try:
            response = self.chain.invoke({
                "query": query,
                "results": results_text
            })
            scores = json.loads(response.content)['scores']
        except Exception as e:
            print(f"Error batch scoring: {e}")
            scores = [0.5] * len(results)  # default all to 0.5

        # Step 3: Filter by threshold
        scored = []
        for i, result in enumerate(results):
            score = scores[i] if i < len(scores) else 0.5
            if score >= 0.6:
                scored.append({**result, 'score': score})

        # Step 4: Deduplicate by URL
        seen = set()
        filtered = []
        for r in scored:
            if r['url'] not in seen:
                seen.add(r['url'])
                filtered.append(r)

        return {**state, 'filtered_results': filtered}