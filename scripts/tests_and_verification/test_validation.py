import os
import sys

# Load .env manually to avoid pydantic validation errors
env_path = os.path.join(os.path.dirname(__file__), "backend", ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        # if it's UTF-16, decode correctly or strip nulls
        if "\x00" in content:
            content = content.replace("\x00", "")
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.services.assistant.context_manager import ContextManager

def test_context_manager():
    print("Testing ContextManager validation combinations...")
    
    # 1. Invalid mode
    try:
        ContextManager.validate_and_resolve(session_id="123", mode="unknown", scope="all_research")
        print("FAIL: Expected invalid mode to fail")
    except ValueError as e:
        print(f"PASS: {str(e)}")

    # 2. Invalid scope
    try:
        ContextManager.validate_and_resolve(session_id="123", mode="research", scope="unknown")
        print("FAIL: Expected invalid scope to fail")
    except ValueError as e:
        print(f"PASS: {str(e)}")

    # 3. Paper mode with all_research scope
    try:
        ContextManager.validate_and_resolve(session_id="123", mode="paper", scope="all_research")
        print("FAIL: Expected paper mode + all_research to fail")
    except ValueError as e:
        print(f"PASS: {str(e)}")

    # 4. Compare mode with <2 papers
    try:
        ContextManager.validate_and_resolve(session_id="123", mode="compare", scope="selected_papers", paper_ids=["p1"])
        print("FAIL: Expected compare with 1 paper to fail")
    except ValueError as e:
        print(f"PASS: {str(e)}")

    # 5. Compare mode with >5 papers
    try:
        ContextManager.validate_and_resolve(session_id="123", mode="compare", scope="selected_papers", paper_ids=["p1","p2","p3","p4","p5","p6"])
        print("FAIL: Expected compare with 6 papers to fail")
    except ValueError as e:
        print(f"PASS: {str(e)}")

    # 6. Single paper with missing paper_id
    try:
        ContextManager.validate_and_resolve(session_id="123", mode="paper", scope="single_paper", paper_id=None)
        print("FAIL: Expected single paper with missing paper_id to fail")
    except ValueError as e:
        print(f"PASS: {str(e)}")

if __name__ == "__main__":
    test_context_manager()
