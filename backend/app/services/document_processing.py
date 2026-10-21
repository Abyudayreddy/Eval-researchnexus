import io
from pypdf import PdfReader
from typing import List, Dict, Any

try:
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.core import Document
except ImportError:
    SentenceSplitter = None
    Document = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

# Load real BGE embedding model or fallback mock generator for tests
embed_model = None

def get_embed_model():
    global embed_model
    if embed_model is None and SentenceTransformer is not None:
        try:
            embed_model = SentenceTransformer("BAAI/bge-base-en-v1.5")
        except Exception:
            embed_model = None
    return embed_model

def get_bge_embeddings(texts: List[str]) -> List[List[float]]:
    model = get_embed_model()
    if model is not None:
        embeddings = model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()
    else:
        # Fallback 768-dim mock vector generator for standalone test runs
        return [[0.01 * (i + 1) for i in range(768)] for _ in texts]

def extract_text_pymupdf(pdf_bytes: bytes) -> str:
    """
    Extracts text from PDF bytes using PyPDF.
    """
    text = ""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error parsing PDF: {e}")
    return text

def process_and_chunk_document(text: str, paper_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Processes the raw text, applies semantic chunking via LlamaIndex,
    generates embeddings, and returns the chunks ready for ChromaDB.
    """
    if not text.strip():
        return []
        
    # 1. Metadata / Section processing
    cleaned_text = text.replace('\n', ' ')
    
    # 2. Semantic Chunking (LlamaIndex SentenceSplitter)
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    document = Document(text=cleaned_text)
    nodes = splitter.get_nodes_from_documents([document])
    
    chunks = []
    if not nodes:
        return chunks
        
    model = get_embed_model()
    # Batch compute embeddings for efficiency
    texts_to_embed = [node.get_content() for node in nodes]
    embeddings = model.encode(texts_to_embed, normalize_embeddings=True)
    
    for i, (node, embedding) in enumerate(zip(nodes, embeddings)):
        chunk_data = {
            "chunk_id": f"{paper_metadata.get('id', 'unknown')}_chunk_{i}",
            "text": node.get_content(),
            "embedding": embedding.tolist(),
            "metadata": {
                "paper_id": paper_metadata.get("id", "unknown"),
                "domain": paper_metadata.get("domain", "General"),
                "title": paper_metadata.get("title", ""),
            }
        }
        chunks.append(chunk_data)
        
    return chunks
