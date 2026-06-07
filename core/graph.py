from typing import Literal
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

from core.state import AgentState
from core.llm import get_llm
from agents.specialists import (
    inventory_agent, sales_agent, order_agent, 
    finance_agent, supply_chain_agent, analytics_agent
)

members = ["Inventory", "Sales", "Order", "Finance", "SupplyChain", "Analytics"]
system_prompt = (
    "You are a supervisor managing a conversation between the following workers: {members}. "
    "Given the user request, respond with the worker to act next. Each worker will perform a "
    "task and respond with their results. "
    "CRITICAL RULES: "
    "1. If the user's request has been fully answered, respond with FINISH. "
    "2. If a worker agent asks a clarifying question to the user, respond with FINISH so the user can see it and reply. Do not route back to the worker."
)

options = ["FINISH"] + members

class Router(BaseModel):
    next_agent: str = Field(description=f"The next agent to route to. Must be one of: {', '.join(options)}")

llm = get_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
    ("system", "Given the conversation above, who should act next? Select one of: {options}. "
               "CRITICAL: If the request is fulfilled OR if a worker just asked the user a question, you MUST select FINISH.")
])

def supervisor_node(state: AgentState):
    messages = state["messages"]
    supervisor_chain = prompt | llm.with_structured_output(Router)
    response = supervisor_chain.invoke({
        "messages": messages,
        "members": ", ".join(members),
        "options": ", ".join(options)
    })
    return {"next_agent": response.next_agent}

# Create Graph
workflow = StateGraph(AgentState)

# Node wrapper to format outputs correctly
def make_node(agent, name):
    def node(state: AgentState):
        # We invoke the underlying agent
        result = agent.invoke({"messages": state["messages"]})
        # The react agent returns the full updated list of messages.
        # We append a tag so the supervisor knows who replied
        last_message = result["messages"][-1]
        
        # In a robust implementation we might change the name of the AIMessage to the node name
        # We just return the new messages appended by the agent
        # The new messages are those in result that were not in state
        new_messages = result["messages"][len(state["messages"]):]
        return {"messages": new_messages}
    return node

workflow.add_node("Orchestrator", supervisor_node)
workflow.add_node("Inventory", make_node(inventory_agent, "Inventory"))
workflow.add_node("Sales", make_node(sales_agent, "Sales"))
workflow.add_node("Order", make_node(order_agent, "Order"))
workflow.add_node("Finance", make_node(finance_agent, "Finance"))
workflow.add_node("SupplyChain", make_node(supply_chain_agent, "SupplyChain"))
workflow.add_node("Analytics", make_node(analytics_agent, "Analytics"))

# Routing
for member in members:
    workflow.add_edge(member, "Orchestrator")

def router(state: AgentState) -> str:
    next_node = state["next_agent"]
    # Fallback checking
    if next_node not in options:
        return "FINISH"
    return next_node

workflow.add_conditional_edges("Orchestrator", router, {m: m for m in members} | {"FINISH": END})
workflow.add_edge(START, "Orchestrator")

import os
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.memory import MemorySaver
from psycopg_pool import ConnectionPool

db_url = os.environ.get("DATABASE_URL")
checkpointer = MemorySaver()

if db_url:
    try:
        # Added timeout=5 to prevent the container from hanging indefinitely if the DB is unreachable
        pool = ConnectionPool(db_url, timeout=5, max_size=5)
        checkpointer = PostgresSaver(pool)
        checkpointer.setup()
        print("Enabled persistent Postgres checkpointer for memory.")
    except Exception as e:
        print(f"CRITICAL ERROR connecting to Postgres checkpointer: {e}")
        print("Falling back to MemorySaver to prevent crash.")
        checkpointer = MemorySaver()
else:
    print("Warning: DATABASE_URL not set. Using in-memory checkpointer.")

graph = workflow.compile(checkpointer=checkpointer)
