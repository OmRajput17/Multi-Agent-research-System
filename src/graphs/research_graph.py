from langgraph.graph import StateGraph, END
from src.graphs.state import ResearchState
from src.agents.planner import PlannerAgent
from src.agents.router import route
from src.agents.search_agent import parallel_search_agent, web_search_agent, academic_search_agent
from src.agents.filter_agent import FilterAgent
from src.agents.summarizer import SummarizerAgent
from src.agents.fact_checker import FactCheckerAgent
from src.agents.report_writer import ReportWriterAgent


def should_continue(state: ResearchState) -> str:
    if state['iteration'] >= 3:
        return "write_report"
    for score in state['fact_check'].values():
        if score < 0.6:
            return 'planner'

    return 'write_report'

def build_graph():
    workflow = StateGraph(ResearchState)

    ## Creating Instances
    planner = PlannerAgent()
    filter_agent = FilterAgent()
    summarizer = SummarizerAgent()
    fact_checker = FactCheckerAgent()
    report_writer = ReportWriterAgent()

    ## Adding nodes 
    workflow.add_node("planner", planner.plan)
    workflow.add_node("filter", filter_agent.filter)
    workflow.add_node("summarizer", summarizer.summarize)
    workflow.add_node("fact_checker", fact_checker.fact_check)
    workflow.add_node("report_writer", report_writer.write_report)
    workflow.add_node("parallel_search", parallel_search_agent)
    workflow.add_node("web_search", web_search_agent)
    workflow.add_node("academic_search", academic_search_agent)

    ## Adding Edges
    workflow.set_entry_point("planner")

    ## Conditional Edge
    workflow.add_conditional_edges("planner", route,{
        "academic":"academic_search",
        "web":"web_search",
        "mixed":"parallel_search"
    })

    ## All search Node -> filter
    workflow.add_edge("academic_search", "filter")
    workflow.add_edge("web_search", "filter")
    workflow.add_edge("parallel_search", "filter")

    ## Filter -> summarizer
    workflow.add_edge("filter", "summarizer")

    ## Summarizer -> fact_checker
    workflow.add_edge("summarizer", "fact_checker")

    ## fact_checker -> loop or report
    workflow.add_conditional_edges("fact_checker", should_continue,{
        "planner":"planner",
        "write_report":"report_writer"
    })

    ## report_writer -> END
    workflow.add_edge("report_writer", END)

    return workflow.compile()



# Quick test — add to bottom of research_graph.py or run separately
if __name__ == "__main__":
    import asyncio
    graph = build_graph()
    result = asyncio.run(graph.ainvoke({
        "query": "What is quantum computing?",
        "sub_questions": [],
        "search_results": [],
        "filtered_results": [],
        "summary": "",
        "fact_check": {},
        "final_report": "",
        "citations": [],
        "iteration": 0,
        "user_feedback": "",
        "route": "mixed"
    }))
    print(result['final_report'])