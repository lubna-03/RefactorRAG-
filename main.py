import os
from src.graph import build_graph
from src.chroma_store import seed_database
from dotenv import load_dotenv

load_dotenv()

def main():
    db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
    if not os.path.exists(db_path):
        print("Seeding ChromaDB for the first time...")
        seed_database()
        
    with open("spaghetti.py", "r", encoding="utf-8") as f:
        source_code = f.read()
        
    app = build_graph()
    
    initial_state = {
        "source_code": source_code,
        "business_context": "",
        "architecture_plan": "",
        "generated_code": "",
        "execution_errors": "",
        "iteration_count": 0
    }
    
    print("Starting LangGraph Multi-Agent Refactoring Pipeline...\n")
    

    final_output = None
    for output in app.stream(initial_state):
        for key, value in output.items():
            print(f"Node '{key}' completed.")
            final_output = value
            
    print("\nPipeline Finished.")
    
    if final_output and "generated_code" in final_output:
        print("\n=== FINAL REFACTORED CODE ===")
        print(final_output["generated_code"])
        
if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY not found in .env. Please add it before running.")
        exit(1)
    main()
