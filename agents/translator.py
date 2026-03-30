from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import typing
if typing.TYPE_CHECKING:
    from src.graph import GraphState

def translator_node(state: 'GraphState') -> dict:
    """
    The Translator re-writes the code into the new modular design.
    If there are execution errors from a previous pass, it uses them to self-correct.
    """
    print("--- TRANSLATOR: Generating code ---")
    source_code = state.source_code
    business_context = state.business_context
    architecture_plan = state.architecture_plan
    execution_errors = state.execution_errors
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    
    user_message = """
Your task is to re-write the following monolithic code into a clean, modular structure 
based EXACTLY on the provided Architecture Plan and Business Logic.

=== BUSINESS LOGIC ===
{business_context}

=== ARCHITECTURE PLAN ===
{architecture_plan}

=== ORIGINAL SOURCE CODE ===
{source_code}
"""

    if execution_errors:
        user_message += """
=== PREVIOUS EXECUTION ERRORS ===
The code you generated previously failed with the following errors:
{execution_errors}
Please fix these errors in your new implementation.
"""

    user_message += """
Please output ONLY the final code. For multiple files, use comments like:
# --- filename.py ---
before each file's code. Do not include markdown formatting or explanations, just the code.
If there are multiple files, output them all in this single response. Include a main.py that runs the program.
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Software Engineer."),
        ("user", user_message)
    ])
    
    chain = prompt | llm

    try:
        response = chain.invoke({
            "business_context": business_context,
            "architecture_plan": architecture_plan,
            "source_code": source_code,
            "execution_errors": execution_errors
        })
        generated_code = response.content
        # Remove any leading/trailing markdown code blocks if the model still adds them
        if generated_code.startswith("```python"):
            generated_code = generated_code[9:]
        elif generated_code.startswith("```"):
            generated_code = generated_code[3:]
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]
            
        print("  > Code generation complete.")
    except Exception as e:
        print(f"  > Error generating code: {e}")
        generated_code = "Error generating code."
        
    return {"generated_code": generated_code.strip()}
