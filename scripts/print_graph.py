import sys
import os

# Add parent directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.graph import graph

def main():
    print("=== Multi-Agent Graph Diagram ===")
    
    # 1. Print ASCII Diagram to the terminal
    ascii_graph = graph.get_graph().draw_ascii()
    print("\n" + ascii_graph + "\n")
    
    # 2. Save a PNG diagram to the root folder using Mermaid API
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        with open("graph_diagram.png", "wb") as f:
            f.write(png_data)
        print("Successfully saved diagram to 'graph_diagram.png'.")
    except Exception as e:
        print(f"Could not generate PNG: {e}")

if __name__ == "__main__":
    main()
