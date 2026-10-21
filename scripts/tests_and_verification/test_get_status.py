import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/researchnexus"
os.environ["GEMINI_API_KEY"] = "dummy"
from app.db.session import SessionLocal
from app.models.search_experiment import SearchExperiment

def main():
    db = SessionLocal()
    exp = db.query(SearchExperiment).order_by(SearchExperiment.search_id.desc()).first()
    if exp:
        print(f"Latest Search ID: {exp.search_id}")
        print(f"Query: {exp.query}")
        print(f"Local Trace keys: {exp.local_trace.keys() if exp.local_trace else None}")
        print(f"Combined Trace keys: {exp.combined_trace.keys() if exp.combined_trace else None}")
        print(f"Combined Trace Local Trace: {'local_trace' in exp.combined_trace if exp.combined_trace else False}")
    else:
        print("No search experiments found.")

if __name__ == "__main__":
    main()
