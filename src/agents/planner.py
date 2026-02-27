from src.utils.get_llm import LLMConfig
from src.graphs.state import ResearchState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class PlannerAgent:
    def __init__(self):
        self.llm = LLMConfig().get_llm()
        self.prompt = """
                You are a research planner. Given a user query, do two things:
                1. Break the query into 3-5 specific, detailed sub-questions that would help thoroughly research the topic. Make sub-questions targeted and researchable.

                2. Classify the search route based on these rules:
                - "academic" → scientific concepts, algorithms, papers, technical mechanisms (e.g., "How does attention work in transformers?")
                - "web" → current events, tutorials, comparisons, trends, opinions (e.g., "Best AI tools in 2024")
                - "mixed" → ONLY when the query genuinely needs both academic depth AND current web info (e.g., "Impact of quantum computing on cryptography")

                Query: {query}

                Return ONLY valid JSON:
                {{"sub_questions": ["detailed question 1", "detailed question 2", "detailed question 3"], "route": "academic"}}
        """

        self.prompt = ChatPromptTemplate.from_template(self.prompt)
        self.output_parsers = JsonOutputParser()
        self.chain = self.prompt | self.llm | self.output_parsers

    def plan(self, state: ResearchState):
        result = self.chain.invoke({"query":state['query']})
        return {
            **state,
            "sub_questions": result["sub_questions"],
            "route":result["route"],
            "iteration": 0
        }
