from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END

# Define state here instead of state.py
class GraphState(BaseModel):
    """
    Represents the state of our multi-agent refactoring system.
    """
    source_code: str = Field(default="")
    business_context: str = Field(default="")
    architecture_plan: str = Field(default="")
    generated_code: str = Field(default="")
    execution_errors: str = Field(default="")
    iteration_count: int = Field(default=0)

# Import the technical nodes
from src.agents.context_retriever import context_retriever_node
from src.agents.architecture_planner import architecture_planner_node
from src.agents.translator import translator_node
from src.agents.qa_judge import qa_judge_node

def should_continue(state: GraphState):
    """
    Conditional edge logic after the QA Judge runs.
    """
    errors = state.execution_errors
    iterations = state.iteration_count
    
    if not errors:
        print("--- SUCCESS: Code passed QA testing! ---")
        return "end"
        
    if iterations >= 3:
        print("--- FAILURE: Max iterations reached. Giving up. ---")
        return "end"
        
    print(f"--- RETRY: Code failed testing. Routing back to Translator (Iteration {iterations}) ---")
    return "translator"

def build_graph():
    # 1. Initialize StateGraph with the Pydantic schema
    workflow = StateGraph(GraphState)
    
    # 2. Add Nodes
    workflow.add_node("context_retriever", context_retriever_node)
    workflow.add_node("architecture_planner", architecture_planner_node)
    workflow.add_node("translator", translator_node)
    workflow.add_node("qa_judge", qa_judge_node)
    
    # 3. Add Edges
    workflow.set_entry_point("context_retriever")
    workflow.add_edge("context_retriever", "architecture_planner")
    workflow.add_edge("architecture_planner", "translator")
    workflow.add_edge("translator", "qa_judge")
    
    # 4. Add Conditional Edges
    workflow.add_conditional_edges(
        "qa_judge",
        should_continue,
        {
            "translator": "translator",
            "end": END
        }
    )
    
    # 5. Compile Graph
    app = workflow.compile()
    
    return app
