# Autonomous Multi-Agent Refactoring Pipeline (with RAG)

This project automatically transforms legacy, monolithic "spaghetti" Python code into clean, modular microservices using AI.

What makes this project special is **Agentic RAG (Retrieval-Augmented Generation)**. Instead of just blindly rewriting the code, the AI pulls actual rules from your company documentation (`docs/business_rules.md`) and enforces them in the new architecture!

## How It Works

The system uses a **LangGraph** workflow with four specialized AI agents:

### 1. The Context Retriever (RAG Agent)
- Looks at the raw spaghetti code (`spaghetti.py`).
- Generates intelligent search keywords.
- Queries a local vector database (**ChromaDB**) to pull the exact business logic rules that apply to that code (from your `docs/`).

### 2. The Architecture Planner (Staff Engineer Agent)
- Takes the **code** AND the **business rules** retrieved from the database.
- Designs a microservice blueprint. For example, it might decide to create `models.py`, `services/`, and `config.py` to securely handle the code without violating the retrieved business rules.

### 3. The Translator (Coding Agent)
- Writes the actual Python code for the new architecture.
- If the system encounters errors in previous runs, this agent automatically reads the traceback and self-corrects the bugs.

### 4. The QA Judge (Testing Agent)
- Takes the code written by the Translator and physically saves it into the `src/sandbox/` folder.
- Executes the code in the background to physically test it.
- If the execution crashes, it tells the Translator to try again (up to 3 times). If it succeeds, the pipeline finishes!


## Usage

You can test the pipeline by running it locally on the dummy `spaghetti.py` script:

```powershell
# 1. Ensure your Google API Key is set in your .env file
# GEMINI_API_KEY=your_key_here

# 2. Run the pipeline orchestrator
uv run python main.py
```

Once the pipeline completes, check the `src/sandbox/` directory. You will find that the spaghetti code has been perfectly separated into modular files, and all logical bugs (like wrong tax rates or local disk saving) have been completely fixed according to your explicit documentation!
