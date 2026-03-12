from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from app.ai.llm import get_llm
from app.ai.prompts import LOG_ANALYSIS_PROMPT, NLQ_PROMPT

class AgentState(TypedDict):
    logs_summary: str
    question: str
    result: str

def analysis_node(state: AgentState):
    llm = get_llm()
    prompt = LOG_ANALYSIS_PROMPT.format(logs_summary=state['logs_summary'])
    response = llm.invoke(prompt)
    return {"result": response.content}

def nlq_node(state: AgentState):
    llm = get_llm()
    prompt = NLQ_PROMPT.format(logs_summary=state['logs_summary'], question=state['question'])
    response = llm.invoke(prompt)
    return {"result": response.content}

# Basic logic to decide flow (single step for now)
def create_analysis_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("analyze", analysis_node)
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", END)
    return workflow.compile()

def create_nlq_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("query", nlq_node)
    workflow.set_entry_point("query")
    workflow.add_edge("query", END)
    return workflow.compile()
