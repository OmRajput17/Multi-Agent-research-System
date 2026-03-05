from src.utils.get_llm import LLMConfig
from src.graphs.state import ResearchState
from langchain_core.prompts import ChatPromptTemplate

class DirectResponderAgent:
    def __init__(self):
        self.llm = LLMConfig().get_llm()
        self.prompt = ChatPromptTemplate.from_template(
            """You are a helpful Research Assistant AI. A user has sent you a conversational message rather than a research query.
            
            User's message: {query}
            
            Respond politely, conversationally, and briefly. If they are just saying hello, greet them back and ask what they would like to research today. 
            Do not make up facts or write a long report. Keep it under 3 sentences."""
        )
        self.chain = self.prompt | self.llm

    def respond(self, state: ResearchState) -> ResearchState:
        response = self.chain.invoke({
            "query": state['query']
        })

        return {
            'final_report': response.content,
            'citations': [],
            'fact_check': {},
        }
