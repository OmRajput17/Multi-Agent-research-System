from src.utils.get_llm import LLMConfig
from src.graphs.state import ResearchState
from langchain_core.prompts import ChatPromptTemplate

class SummarizerAgent:
    def __init__(self):
        self.llm = LLMConfig().get_llm()
        self.prompt = ChatPromptTemplate.from_template(
            """
                You are a research summarizer. Based on the following sources, 
                provide a comprehensive answer to the query.
                Cite sources inline using [1], [2], etc.

                Query: {query}

                Sources:{context}

                Provide a well structured summary with inline citations:
            """

        )
        self.chain = self.prompt | self.llm

    def summarize(self, state: ResearchState) -> ResearchState:
        # Guard: handle empty filtered results
        if not state['filtered_results']:
            return {
                'summary': 'No relevant sources were found for this query.',
                'citations': []
            }

        # Step 1: Format filtered results as numbered context
        context = '\n\n'.join([
            f'[{i+1}] {r["title"]}\n{r["content"][:1500]}'
            for i, r in enumerate(state['filtered_results'])
        ])

        # Step 2: Ask the LLM to synthesize with inline citations
        response = self.chain.invoke({
            "query": state['query'],
            "context": context
        })

        # Step 3: Extract the citation URLs
        citations = list(dict.fromkeys(r['url'] for r in state['filtered_results']))

        return {
            'summary': response.content,
            'citations': citations
        }
