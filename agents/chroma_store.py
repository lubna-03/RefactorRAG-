import os
from chromadb import PersistentClient
from langchain_chroma import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_vector_store():
    # Provide the path for the persistent chroma DB
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
    client = PersistentClient(path=db_path)
    
    # We use FastEmbed which runs robust HuggingFace models locally without PyTorch overhead
    # using BAAI/bge-small-en-v1.5 by default which is highly rated for retrieval
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    vector_store = Chroma(
        client=client,
        collection_name="business_logic",
        embedding_function=embeddings,
    )
    
    return vector_store

def seed_database():
    """Seeds the database by loading, chunking, and indexing a documentation file."""
    print("Discarding old collections if they exist...")
    
    store = get_vector_store()
    try:
        store._client.delete_collection("business_logic")
        store = get_vector_store() # Recreate it
    except Exception:
        pass
        
    print("Loading business rules documentation...")
    rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "business_rules.md")
    loader = TextLoader(rules_path, encoding="utf-8")
    documents = loader.load()
    
    # Here we define the chunk size and overlap
    # A chunk_size of 300 characters ensures the retrieved context is dense and focused on single rules
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300, 
        chunk_overlap=50,
        separators=["\n## ", "\n\n", "\n", " ", ""]
    )
    
    docs = text_splitter.split_documents(documents)
    print(f"Split documentation into {len(docs)} chunks.")
    
    store.add_documents(docs)
    print("Database indexing complete with local HuggingFace equivalent (FastEmbed).")

if __name__ == "__main__":
    seed_database()
