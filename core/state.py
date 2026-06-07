import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """The state of the multi-agent system."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_agent: str
