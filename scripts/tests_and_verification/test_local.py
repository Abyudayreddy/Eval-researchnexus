import sys
import os

os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
os.environ['GEMINI_API_KEY'] = 'fake'

sys.path.insert(0, os.path.abspath('backend'))
from app.services.local_evidence import get_local_retriever

try:
    retriever = get_local_retriever()
    print('Init status:', retriever.init_status)
    evidence, is_suff, trace = retriever.retrieve('test query')
    print('Success:', len(evidence))
except Exception as e:
    import traceback
    traceback.print_exc()
