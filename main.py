from core.graph import graph
from langchain_core.messages import HumanMessage

def run_cli():
    print("=========================================")
    print("Retail Agentic AI Platform - Interactive CLI")
    print("=========================================")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        try:
            user_input = input("User: ")
        except (EOFError, KeyboardInterrupt):
            break
            
        if user_input.strip().lower() in ['exit', 'quit']:
            break
            
        events = graph.stream(
            {"messages": [HumanMessage(content=user_input)]},
            {"recursion_limit": 50}
        )
        
        for event in events:
            for node, state in event.items():
                if "messages" in state:
                    # In this setup, state["messages"] is the delta (if appended via Annotated)
                    # or the whole list. Let's just print the last one.
                    messages = state.get("messages", [])
                    if messages:
                        latest_message = messages[-1]
                        # Only print if it has content (some tool messages might be complex)
                        if hasattr(latest_message, "content") and latest_message.content:
                            print(f"\n[{node}]:\n{latest_message.content}\n")
                elif node == "Orchestrator":
                     print(f"[Orchestrator] routing to: {state.get('next_agent')}")

if __name__ == "__main__":
    run_cli()
