from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def get_knowledge_base_status():
    """
    Returns the status of the local 670-paper dataset.
    Currently hardcoded to 'awaiting_dataset' as per Phase 4A requirements.
    """
    # In the future, this will query ChromaDB and BM25 instances for their real states.
    return {
        "status": "awaiting_dataset",
        "documents": 0,
        "chunks": 0,
        "embeddings": 0,
        "vector_index": False,
        "bm25_index": False
    }
