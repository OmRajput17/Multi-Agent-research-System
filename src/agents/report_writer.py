from src.utils.get_llm import LLMConfig
from src.graphs.state import ResearchState
from langchain_core.prompts import ChatPromptTemplate

class ReportWriterAgent:
    def __init__(self):
        self.llm = LLMConfig().get_llm()
        self.prompt = ChatPromptTemplate.from_template(
            """You are a senior research analyst. Write a comprehensive, detailed markdown report.

            Query: {query}

            Research Summary: {summary}

            Fact-Check Results:
            {fact_check}

            References (use these inline):
            {references}

            Write a thorough research report in markdown with these sections:
            # Research Report: [Topic]
            ## Executive Summary (2-3 paragraphs)
            ## Key Findings (bullet points with details)
            ## Detailed Analysis (in-depth discussion, multiple paragraphs)
            ## Methodology (which sources were used and why)
            ## Confidence Assessment (use fact-check scores, explain reliability)
            ## Limitations & Future Research
            ## References

            IMPORTANT CITATION RULES:
            - Place citations INLINE next to the claim they support, like: "Transformers use attention mechanisms [1]"
            - Use the reference numbers [1], [2], etc. that match the References list
            - Every major claim MUST have an inline citation
            - Still include a numbered References section at the end for the full URLs
            - Be detailed and thorough. Each section should have substantial content."""
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

