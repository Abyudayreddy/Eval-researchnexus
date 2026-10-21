import json

cells = [
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': ['# Phase 4B.4 Embedding Generation\n', 'Mount Google Drive to access `ResearchMind_LocalKB/chunks`']
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'from google.colab import drive\n',
            'drive.mount("/content/drive")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': ['Install Dependencies']
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            '!pip install -q sentence-transformers'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': ['Verify Environment and Hardware']
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'import torch\n',
            'import sentence_transformers\n',
            'print(f"PyTorch: {torch.__version__}")\n',
            'print(f"Sentence Transformers: {sentence_transformers.__version__}")\n',
            'print(f"CUDA available: {torch.cuda.is_available()}")\n',
            'if torch.cuda.is_available():\n',
            '    print(f"GPU: {torch.cuda.get_device_name(0)}")\n'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': ['Embedding Configuration and Paths']
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'import os\n',
            'import json\n',
            'import time\n',
            'from datetime import datetime\n',
            'from sentence_transformers import SentenceTransformer\n',
            '\n',
            '# UPDATE THIS PATH to where ResearchMind_LocalKB is located in your Drive\n',
            'BASE_DIR = "/content/drive/MyDrive/ResearchMind_LocalKB"\n',
            'CHUNKS_DIR = os.path.join(BASE_DIR, "chunks")\n',
            'EMBEDDINGS_DIR = os.path.join(BASE_DIR, "embeddings")\n',
            'VECTORS_DIR = os.path.join(EMBEDDINGS_DIR, "vectors")\n',
            'os.makedirs(VECTORS_DIR, exist_ok=True)\n',
            '\n',
            'MODEL_NAME = "BAAI/bge-base-en-v1.5"\n',
            'BATCH_SIZE = 64  # Good default for T4\n',
            'DEVICE = "cuda" if torch.cuda.is_available() else "cpu"\n',
            '\n',
            'print(f"Loading {MODEL_NAME} on {DEVICE}...")\n',
            'model = SentenceTransformer(MODEL_NAME, device=DEVICE)\n',
            'DIMENSION = model.get_sentence_embedding_dimension()\n',
            'print(f"Dimension: {DIMENSION}")\n'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': ['Process Embeddings']
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            '# Gather chunks\n',
            'chunk_files = []\n',
            'for r, d, f_list in os.walk(CHUNKS_DIR):\n',
            '    for f in f_list:\n',
            '        if f.endswith(".json"):\n',
            '            chunk_files.append(os.path.join(r, f))\n',
            '\n',
            'all_chunks = []\n',
            'for filepath in chunk_files:\n',
            '    with open(filepath, "r", encoding="utf-8") as fp:\n',
            '        all_chunks.extend(json.load(fp))\n',
            '\n',
            'total_eligible = len(all_chunks)\n',
            'print(f"Found {total_eligible} eligible chunks.")\n',
            '\n',
            '# Check existing shards to support resumability\n',
            'processed_chunk_ids = set()\n',
            'if os.path.exists(VECTORS_DIR):\n',
            '    for r, d, f_list in os.walk(VECTORS_DIR):\n',
            '        for f in f_list:\n',
            '            if f.endswith(".jsonl"):\n',
            '                with open(os.path.join(r, f), "r", encoding="utf-8") as fp:\n',
            '                    for line in fp:\n',
            '                        record = json.loads(line)\n',
            '                        processed_chunk_ids.add(record["chunk_id"])\n',
            '\n',
            'print(f"Found {len(processed_chunk_ids)} already processed chunks. Resuming...")\n',
            '\n',
            'chunks_to_process = [c for c in all_chunks if c["chunk_id"] not in processed_chunk_ids]\n',
            'print(f"{len(chunks_to_process)} chunks left to process.")\n',
            '\n',
            'failures = []\n',
            'start_time = time.time()\n',
            'generated_count = 0\n',
            '\n',
            'for i in range(0, len(chunks_to_process), BATCH_SIZE):\n',
            '    batch = chunks_to_process[i:i+BATCH_SIZE]\n',
            '    texts = [c["text"] for c in batch]\n',
            '    \n',
            '    try:\n',
            '        # We do NOT manually truncate. Full texts are encoded.\n',
            '        embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)\n',
            '        \n',
            '        for j, emb in enumerate(embeddings):\n',
            '            chunk = batch[j]\n',
            '            emb_id = chunk["chunk_id"].replace("#", "_").replace(":", "_")\n',
            '            safe_pid = chunk["paper_id"].replace(":", "_")\n',
            '            out_path = os.path.join(VECTORS_DIR, f"{safe_pid}.jsonl")\n',
            '            \n',
            '            record = {\n',
            '                "embedding_id": f"emb_{emb_id}",\n',
            '                "chunk_id": chunk["chunk_id"],\n',
            '                "paper_id": chunk["paper_id"],\n',
            '                "domain": chunk.get("domain"),\n',
            '                "subdomain": chunk.get("subdomain"),\n',
            '                "section": chunk.get("section"),\n',
            '                "model": MODEL_NAME,\n',
            '                "dimension": DIMENSION,\n',
            '                "vector": [float(x) for x in emb],\n',
            '                "created_at": datetime.now().isoformat()\n',
            '            }\n',
            '            \n',
            '            with open(out_path, "a", encoding="utf-8") as f_out:\n',
            '                f_out.write(json.dumps(record) + "\\n")\n',
            '                \n',
            '            generated_count += 1\n',
            '            \n',
            '    except Exception as e:\n',
            '        for c in batch:\n',
            '            failures.append({\n',
            '                "chunk_id": c["chunk_id"],\n',
            '                "error_type": "BatchEmbeddingError",\n',
            '                "error_message": str(e)\n',
            '            })\n',
            '            \n',
            '    if (i + BATCH_SIZE) % (BATCH_SIZE * 5) == 0:\n',
            '        print(f"Processed {i + BATCH_SIZE}/{len(chunks_to_process)}...")\n',
            '\n',
            'end_time = time.time()\n',
            'total_time = end_time - start_time\n',
            'print(f"Generation complete in {total_time:.2f} seconds.")\n',
            '\n',
            'manifest = {\n',
            '    "corpus_version": "1.0",\n',
            '    "chunk_count": total_eligible,\n',
            '    "embedded_count": len(processed_chunk_ids) + generated_count,\n',
            '    "failed_count": len(failures),\n',
            '    "skipped_zero_chunk_count": 13,\n',
            '    "embedding_model": MODEL_NAME,\n',
            '    "embedding_dimension": DIMENSION,\n',
            '    "normalization": True,\n',
            '    "device": DEVICE,\n',
            '    "batch_size": BATCH_SIZE,\n',
            '    "generated_at": datetime.now().isoformat(),\n',
            '    "embedding_format": "jsonl_shards_by_paper"\n',
            '}\n',
            'with open(os.path.join(EMBEDDINGS_DIR, "embedding_manifest.json"), "w") as fp:\n',
            '    json.dump(manifest, fp, indent=2)\n'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': ['Package Artifacts']
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            '!cd /content/drive/MyDrive && zip -r ResearchMind_LocalKB_embeddings.zip ResearchMind_LocalKB/embeddings -x "*/.*" -x "*/__pycache__/*"\n',
            'print("Done! You can now download ResearchMind_LocalKB_embeddings.zip from your Google Drive.")'
        ]
    }
]

notebook = {
    'cells': cells,
    'metadata': {
        'colab': {'name': 'phase_4b_04_embeddings_colab.ipynb'},
        'kernelspec': {'display_name': 'Python 3', 'name': 'python3'}
    },
    'nbformat': 4,
    'nbformat_minor': 4
}

with open('phase_4b_04_embeddings_colab.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)
