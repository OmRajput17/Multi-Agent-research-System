from src.utils.get_llm import LLMConfig
from src.graphs.state import ResearchState
from langchain_core.prompts import ChatPromptTemplate


class FilterAgent:
    def __init__(self):
        self.llm = LLMConfig().get_llm()
        self.prompt = ChatPromptTemplate.from_template(
            """
                Rate the relevance 0f the following content to the query on a scale of 0 to 1.
                Return ONLY a single number between 0 and 1, nothing else.

                Query: {query}
                Content: {content}

                Relevance Score:
            """

        )
        self.chain = self.prompt | self.llm

    def filter(self, state: ResearchState) -> ResearchState:
        query = state['query']
        scored = []

        for result in state['search_results']:
            try:
                response = self.chain.invoke({
                    "query": query,
                    "content": result['content'][:500]
                })
                score = float(response.content.strip())
                if score >= 0.6:
                    scored.append({**result, 'score':score})
            except (ValueError, Exception) as e:
                print(f"Error scoring result: {e}")
                continue
        
        ## Deduplicate by URL
        seen = set()
        filtered = []
        for r in scored:
            if r['url'] not in seen:
                seen.add(r['url'])
                filtered.append(r)
        
        return {**state, 'filtered_results': filtered}