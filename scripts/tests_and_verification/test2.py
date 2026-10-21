import sys
import os

os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/researchnexus'
os.environ['GEMINI_API_KEY'] = 'fake'

sys.path.insert(0, os.path.abspath('backend'))
from app.services.local_evidence import get_local_retriever

try:
    retriever = get_local_retriever()
    print("STATUS", retriever.init_status)
    retriever.retrieve('retrieval augmented generation', deep_evidence=False)
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
