import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import HumanMessage
from core.graph import graph

def run_debug():
    events = graph.stream(
        {"messages": [HumanMessage(content="Compare sales vs inventory levels for the top 50 products.")]},
        {"recursion_limit": 5}
    )
    for event in events:
        for node, state in event.items():
            print(f"--- NODE: {node} ---")
            if "messages" in state:
                for msg in state["messages"]:
                    print(f"[{type(msg).__name__}]: {msg.content[:100]}")
            if "next_agent" in state:
                print(f"Routing to: {state['next_agent']}")
            print("\n")

if __name__ == "__main__":
    run_debug()
