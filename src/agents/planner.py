from src.utils.get_llm import LLMConfig
from src.graphs.state import ResearchState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class PlannerAgent:
    def __init__(self):
        self.llm = LLMConfig().get_llm()
        self.prompt = """
            You are a research planner. Given the query: {query}
            Break it into 3-5 specific sub-questions for research.
            Also classify the query route as: academic, web, or mixed.
            Return ONLY valid JSON in this exact format:
            {{"sub_questions": ["q1", "q2", "q3"], "route": "mixed"}}
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
