from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from src.chroma_store import get_vector_store
import typing
if typing.TYPE_CHECKING:
    from src.graph import GraphState

def context_retriever_node(state: 'GraphState') -> dict:
    """
    The Context Retriever queries the Vector DB for "Business Logic Documentation".
    """
    print("--- CONTEXT RETRIEVER: Scanning for business logic ---")
    source_code = state.source_code
    
    # Use Gemini to extract key concepts from the source code for better vector search
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    
    prompt_template = PromptTemplate(
        input_variables=["source_code"],
        template=(
            "You are an expert code analyst. Extract 3 to 5 highly specific "
            "search keywords from the following legacy code to query a business logic "
            "documentation database. Return ONLY the keywords separated by spaces.\n\n"
            "code:\n{source_code}"
        )
    )
    
    chain = prompt_template | llm
    
    try:
        query_response = chain.invoke({"source_code": source_code[:1500]})
        search_query = query_response.content
        print(f"  > Search query: {search_query}")
    except Exception as e:
        print(f"  > Error forming search query, using raw code block instead. Error: {e}")
        search_query = source_code[:500]
        
    # Query ChromaDB
    try:
        vector_store = get_vector_store()
        results = vector_store.similarity_search(search_query, k=3)
        context_str = "\n".join([f"- [Source: {doc.metadata.get('source', 'unknown')}] {doc.page_content}" for doc in results])
    except Exception as e:
        print(f"  > Error accessing ChromaDB: {e}")
        context_str = ""

    if not context_str.strip():
        context_str = "No specific business logic context found."
        
    print(f"  > Retrieved {len(results) if 'results' in locals() else 0} documents.")
    
    return {"business_context": context_str}
