import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from app.services.local_evidence import get_local_retriever

def main():
    try:
        print("Getting retriever...")
        retriever = get_local_retriever()
        print(f"Status: {retriever.init_status}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
