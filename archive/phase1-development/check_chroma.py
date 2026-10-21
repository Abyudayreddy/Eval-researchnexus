import os
import chromadb

def main():
    root_dir = os.path.abspath("C:/Users/Abyureddy/OneDrive/Desktop/SDC2")
    kb_dir = os.path.join(root_dir, "ResearchMind_LocalKB")
    chroma_path = os.path.join(kb_dir, "indexes", "chroma")
    
    try:
        chroma_client = chromadb.PersistentClient(path=chroma_path)
        collection = chroma_client.get_collection("researchnexus_local_v1_bgebase")
        res = collection.get(include=[])
        print("Current Chroma DB Count:", len(res['ids']))
    except Exception as e:
        print("Error checking chroma:", e)

if __name__ == "__main__":
    main()
