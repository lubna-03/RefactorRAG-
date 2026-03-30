import os
import subprocess
import shutil
import typing
if typing.TYPE_CHECKING:
    from src.graph import GraphState

def qa_judge_node(state: 'GraphState') -> dict:
    """
    The QA Judge takes the new code, runs it in a sandboxed directory,
    captures errors, and updates the execution_errors state.
    """
    print("--- QA JUDGE: Testing code ---")
    generated_code = state.generated_code
    iteration_count = state.iteration_count + 1
    
    # Extract files
    sandbox_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sandbox")
    if os.path.exists(sandbox_dir):
        shutil.rmtree(sandbox_dir)
    os.makedirs(sandbox_dir, exist_ok=True)
    
    # Simple parse based on "# --- filename.py ---"
    files = {}
    current_file = "main.py"
    current_content = []
    
    for line in generated_code.split('\n'):
        if line.startswith("# ---") and line.endswith("---"):
            if current_content:
                files[current_file] = '\n'.join(current_content)
                current_content = []
            current_file = line.replace("# ---", "").replace("---", "").strip()
        else:
            current_content.append(line)
            
    if current_content:
        files[current_file] = '\n'.join(current_content)
        
    # Write files to sandbox
    for filename, content in files.items():
        filepath = os.path.join(sandbox_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    main_file = "main.py" if "main.py" in files else (list(files.keys())[0] if files else "main.py")
        
    print(f"  > Executing {main_file} in sandbox... (Iteration {iteration_count})")
    try:
        result = subprocess.run(
            ["python", main_file],
            cwd=sandbox_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("  > Execution successful!")
            return {"execution_errors": "", "iteration_count": iteration_count}
        else:
            errors = result.stderr if result.stderr else result.stdout
            print(f"  > Execution failed. Errors:\n{errors[:200]}...")
            return {"execution_errors": errors, "iteration_count": iteration_count}
            
    except subprocess.TimeoutExpired:
        print("  > Execution timed out.")
        return {"execution_errors": "Execution timed out.", "iteration_count": iteration_count}
    except Exception as e:
        print(f"  > Execution error: {e}")
        return {"execution_errors": str(e), "iteration_count": iteration_count}
