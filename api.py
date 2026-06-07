import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from core.graph import graph

app = FastAPI(title="Retail AI Multi-Agent API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    user_input = request.message
    
    responses = []
    
    try:
        events = graph.stream(
            {"messages": [HumanMessage(content=user_input)]},
            {
                "recursion_limit": 50,
                "configurable": {"thread_id": request.session_id}
            }
        )
        
        for event in events:
            for node, state in event.items():
                if "messages" in state:
                    messages = state.get("messages", [])
                    if messages:
                        latest_message = messages[-1]
                        if hasattr(latest_message, "content") and latest_message.content:
                            responses.append({
                                "agent": node,
                                "content": latest_message.content
                            })
                elif node == "Orchestrator":
                    # Useful to show intermediate planning steps
                    next_agent = state.get("next_agent")
                    if next_agent != "FINISH":
                        responses.append({
                            "agent": "Orchestrator",
                            "content": f"Routing task to {next_agent} Agent..."
                        })
    except Exception as e:
        responses.append({
            "agent": "System (Error)",
            "content": f"Backend encountered an error during execution: {str(e)}"
        })
    
    # Generate the graph image dynamically at runtime
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        with open("graph_diagram_latest.png", "wb") as f:
            f.write(png_data)
    except Exception as e:
        print(f"Failed to generate runtime graph: {e}")
        
    return {"responses": responses}
