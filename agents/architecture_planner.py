from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import typing
if typing.TYPE_CHECKING:
    from src.graph import GraphState

def architecture_planner_node(state: 'GraphState') -> dict:
    """
    The Architecture Planner decomposes spaghetti code into clean, modular components.
    It takes the raw code and the business context and produces an architecture plan.
    """
    print("--- ARCHITECTURE PLANNER: Planning modularization ---")
    source_code = state.source_code
    business_context = state.business_context
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Software Architect."),
        ("user", """
Your task is to decompose the following monolithic "spaghetti" code into clean, modular 
microservices or decoupled modules based on the provided business logic context.

=== BUSINESS LOGIC CONTEXT ===
{business_context}

=== ORIGINAL SOURCE CODE ===
{source_code}

Produce a detailed "Architecture Plan" that describes how the code should be broken down.
Your output should act as a blueprint. Focus on identifying separate concerns, data flow, 
and functional boundaries.
Do NOT write the actual final application code. Provide a structured plan detailing:
1. Which logical files or modules to create.
2. What classes/functions go where.
3. How they will interact.
""")
    ])
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({
            "business_context": business_context,
            "source_code": source_code
        })
        architecture_plan = response.content
        print("  > Architecture plan generated successfully.")
    except Exception as e:
        print(f"  > Error generating architecture plan: {e}")
        architecture_plan = "Error generating plan."
        
    return {"architecture_plan": architecture_plan}
