from src.utils.get_llm import LLMConfig
from src.graphs.state import ResearchState
from langchain_core.prompts import ChatPromptTemplate
import json
import re

class FactCheckerAgent:
    def __init__(self):
        self.llm = LLMConfig().get_llm()
        # Step 1 prompt: Extract claims from summary
        self.extract_prompt = ChatPromptTemplate.from_template(
            """Extract the key factual claims from this summary as a JSON list.
            Return ONLY valid JSON, no extra text.
            Summary: {summary}
            Example output: {{"claims": ["claim 1", "claim 2", "claim 3"]}}"""
        )

        # Step 2 prompt: Score each claim against sources
        self.verify_prompt = ChatPromptTemplate.from_template(
            """Given these sources, rate the confidence of this claim from 0 to 1.
            Return ONLY a single number between 0 and 1.
            Claim: {claim}
            Sources: {sources}
            Confidence score:"""
        )

        self.extract_chain = self.extract_prompt | self.llm
        self.verify_chain = self.verify_prompt |  self.llm

    def _parse_score(self, text: str) -> float:
        """Robustly extract a float score from LLM response text."""
        # Try to find a decimal number between 0 and 1
        match = re.search(r'\b(0(?:\.\d+)?|1(?:\.0+)?)\b', text.strip())
        if match:
            return round(float(match.group(1)), 2)
        return 0.5  # default fallback

    def fact_check(self, state: ResearchState) -> ResearchState:

        # Step 1: Extract Claims from summary
        try:
            result = self.extract_chain.invoke({
                "summary": state['summary']
            })
            claims = json.loads(result.content)['claims']
        
        except Exception as e:
            print(f"Error extracting claims: {e}")
            claims = []
    
        # Step2 : Score each claim against the filtered sources
        sources = '\n'.join([
            f"- {r['title']} : {r['content'][:300]}"
            for r in state['filtered_results']
        ])

        fact_check = {}

        for claim in claims:
            try:
                response = self.verify_chain.invoke({
                    "claim": claim,
                    "sources": sources
                })

                score = self._parse_score(response.content)
                fact_check[claim] = score
            except Exception:
                fact_check[claim] = 0.5
            
        return {
            'fact_check': fact_check
        }
