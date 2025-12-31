import os 
from typing_extensions import Annotated ,Literal ,Optional
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage ,HumanMessage
from langgraph.graph import StateGraph 
from langgraph.graph import START ,END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from .tools import get_order_details, connect_to_human_agent,search_knowledge_base
from .state import AgentState

load_dotenv()

llm= ChatGroq(model="" ,api_key=os.getenv("GROQ_API_KEY"))

tools=[get_order_details ,connect_to_human_agent,search_knowledge_base]
llm_with_tools = llm.bind_tools(tools)



async def chatbot_node(state: AgentState):
    """
    The Brain: Receives messages and decides whether to respond 
    or call a tool (like checking an order).
    """
    response = await llm_with_tools.ainvoke(state["messages"])
    
    return {"messages": [response]}

async def analyze_sentiment_node(state: AgentState):
    """
    The Observer: Automatically updates sentiment and needs_human flag
    to make the project 'stand out'.
    """
    last_msg = state["messages"][-1].content.lower()
    
    frustration_keywords = ["angry", "bad service", "worst", "human", "scam"]
    is_angry = any(word in last_msg for word in frustration_keywords)
    
    return {
        "sentiment": "Angry" if is_angry else "Neutral",
        "needs_human": is_angry
    }


def route_logic(state: AgentState):
    """
    Determines where to go after the chatbot node.
    """
    last_message = state["messages"][-1]
    
    if last_message.tool_calls:
        return "tools"
    
    if state.get("needs_human"):
        return "human_handoff"
        
    return END


workflow = StateGraph(AgentState)

workflow.add_node("chatbot", chatbot_node)
workflow.add_node("analyzer", analyze_sentiment_node)
workflow.add_node("tools", ToolNode(tools))

async def human_handoff_node(state: AgentState):
    return {"messages": [HumanMessage(content="[SYSTEM]: Routing to human agent due to sentiment...")]}
workflow.add_node("human_handoff", human_handoff_node)

workflow.set_entry_point("chatbot")

workflow.add_edge("chatbot", "analyzer")

workflow.add_conditional_edges(
    "analyzer", 
    route_logic, 
    {
        "tools": "tools", 
        "human_handoff": "human_handoff", 
        "end": END
    }
)

workflow.add_edge("tools", "chatbot")
workflow.add_edge("human_handoff", END)


memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

