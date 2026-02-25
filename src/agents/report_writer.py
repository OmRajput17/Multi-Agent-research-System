from src.utils.get_llm import LLMConfig
from src.graphs.state import ResearchState
from langchain_core.prompts import ChatPromptTemplate

class ReportWriterAgent:
    def __init__(self):
        self.llm = LLMConfig().get_llm()
        self.prompt = ChatPromptTemplate.from_template(
            """You are a research report writer. Generate a well-structured markdown report.
            Query: {query}
            Summary: {summary}
            Fact-Check Results:
            {fact_check}
            References:
            {references}
            Write a complete research report in markdown with these sections:
            # Research Report: [Topic]
            ## Introduction
            ## Key Findings
            ## Detailed Analysis
            ## Confidence Assessment
            ## References
            Use the fact-check scores to highlight which findings are most reliable.
            Include numbered references at the end."""
        )
        self.chain = self.prompt | self.llm

    def write_report(self, state: ResearchState) -> ResearchState:
        ## Format fact check scores as readable text
        fact_check_text = "\n".join([
            f"- \"{claim}\": {score}"
            for claim, score in state['fact_check'].items()
        ])

        ## format citations as numbered refrences
        references  = '\n'.join([
            f"[{i+1}] {url}"
            for i, url in enumerate(state['citations'])
        ])

        response = self.chain.invoke({
            "query": state['query'],
            "summary": state["summary"],
            "fact_check": fact_check_text,
            "references": references
        })

        return {
            **state,
            'final_report': response.content
        }

