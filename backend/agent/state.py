from typing import Annotated, TypedDict, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):

    messages: Annotated[List[BaseMessage], add_messages]
    user_id: int
    order_id: Optional[int]
    sentiment: str  
    needs_human: bool 
    agent_info: Optional[dict] 
