import os
import json
import hashlib
import csv
import fitz

def get_hash(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f: h.update(f.read())
    return h.hexdigest()

def normalize_name(name):
    return name.replace('_', ' ').strip()

def process():
    base_dir = 'ResearchMind_Dataset'
    output_dir = 'ResearchMind_LocalKB'
    metadata_dir = os.path.join(output_dir, 'metadata')
    manifests_dir = os.path.join(output_dir, 'manifests')
    reports_dir = os.path.join(output_dir, 'reports')
    
    os.makedirs(metadata_dir, exist_ok=True)
    os.makedirs(manifests_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    stats = {
        'total_pdfs': 0, 'valid_pdfs': 0, 'invalid_pdfs': 0,
        'domains': set(), 'subdomains': set(), 'topics': set(), 'collections': set(),
        'json_count': 0, 'metadata_complete': 0, 'metadata_only': 0, 'duplicates': 0
    }
    
    tree_report = []
    failed_papers = []
    manifest = []
    
    seen_hashes = {}
    
    csv_metadata = {}
    # First pass: find all CSVs
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.csv'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        key = row.get('pdf_filename') or row.get('file_name') or row.get('id')
                        if not key and list(row.values()): key = list(row.values())[0]
                        if key: csv_metadata[key] = row
                        
    validation_issues = []

    for root, dirs, files in os.walk(base_dir):
        rel_path = os.path.relpath(root, base_dir)
        if rel_path == '.':
            parts = []
        else:
            parts = rel_path.split(os.sep)
            
        pdf_files = [f for f in files if f.lower().endswith('.pdf')]
        tree_report.append({'path': parts, 'pdfs': len(pdf_files), 'dirs': dirs, 'files': files})
        
        for file in pdf_files:
            filepath = os.path.join(root, file)
            stats['total_pdfs'] += 1
            
            domain = normalize_name(parts[0]) if len(parts) > 0 else 'Unknown'
            subdomain = normalize_name(parts[1]) if len(parts) > 1 else None
            topic = normalize_name(parts[2]) if len(parts) > 2 else None
            collection = normalize_name(parts[3]) if len(parts) > 3 else None
            
            stats['domains'].add(domain)
            if subdomain: stats['subdomains'].add(subdomain)
            if topic: stats['topics'].add(topic)
            if collection: stats['collections'].add(collection)
            
            file_hash = get_hash(filepath)
            if file_hash in seen_hashes:
                stats['duplicates'] += 1
                validation_issues.append(f'Duplicate content hash: {filepath} equals {seen_hashes[file_hash]}')
            else:
                seen_hashes[file_hash] = filepath
                
            readable = False
            page_count = 0
            text_len = 0
            try:
                doc = fitz.open(filepath)
                page_count = doc.page_count
                if page_count > 0:
                    readable = True
                    text_len = len(doc[0].get_text())
                doc.close()
            except Exception as e:
                pass
                
            if not readable:
                stats['invalid_pdfs'] += 1
                failed_papers.append({'path': filepath, 'reason': 'unreadable'})
                continue
                
            stats['valid_pdfs'] += 1
            
            norm_rel_path = rel_path.replace(os.sep, '/')
            paper_id = f'local:{domain}:{file_hash}'
            
            row_meta = csv_metadata.get(file, {})
            title = row_meta.get('title', file)
            abstract = row_meta.get('abstract')
            
            authors_raw = row_meta.get('authors', '')
            authors_list = [{'name': a.strip(), 'orcid': None, 'affiliation': None} for a in authors_raw.split(';')] if authors_raw else []
            
            meta = {
                'paper_id': paper_id,
                'title': title,
                'authors': authors_list,
                'abstract': abstract if abstract else None,
                'keywords': row_meta.get('keywords', '').split(';') if row_meta.get('keywords') else [],
                'domain': domain,
                'subdomain': subdomain,
                'topic': topic,
                'collection': collection,
                'publication_year': row_meta.get('publication_year'),
                'publication_date': row_meta.get('publication_date'),
                'journal': row_meta.get('journal'),
                'conference': row_meta.get('conference'),
                'publisher': row_meta.get('publisher'),
                'doi': row_meta.get('doi'),
                'source_repository': 'local_curated',
                'source_id': file,
                'url': None,
                'pdf_url': None,
                'pdf_path': filepath.replace('\\', '/'),
                'processing_status': 'discovered',
                'processing_error': None,
                'evidence_status': 'metadata_only' if not abstract else 'metadata_complete',
                'embedding_status': 'pending',
                'embedding_model': None,
                'embedding_reference': None,
                'ingestion_date': None
            }
            
            if abstract:
                stats['metadata_complete'] += 1
            else:
                stats['metadata_only'] += 1
                
            out_dir = os.path.join(metadata_dir, *parts)
            os.makedirs(out_dir, exist_ok=True)
            safe_paper_id = paper_id.replace(':', '_')
            with open(os.path.join(out_dir, f'{safe_paper_id}.json'), 'w', encoding='utf-8') as f:
                json.dump(meta, f, indent=2)
                
            manifest.append(meta)
            stats['json_count'] += 1

    with open(os.path.join(reports_dir, 'dataset_structure_report.md'), 'w') as f:
        f.write('# Dataset Structure Report\n\n')
        for node in tree_report:
            f.write(f'- Path: {os.sep.join(node["path"]) if node["path"] else "Root"} | PDFs: {node["pdfs"]} | Subdirs: {len(node["dirs"])} | Other files: {len(node["files"]) - node["pdfs"]}\n')
            
    with open(os.path.join(reports_dir, 'metadata_validation_report.md'), 'w') as f:
        f.write('# Metadata Validation Report\n\n')
        for issue in validation_issues:
            f.write(f'- {issue}\n')
            
    with open(os.path.join(reports_dir, 'failed_papers.json'), 'w') as f:
        json.dump(failed_papers, f, indent=2)
        
    with open(os.path.join(manifests_dir, 'corpus_manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=2)
        
    print(json.dumps({
        'domains': len(stats['domains']),
        'subdomains': len(stats['subdomains']),
        'topics': len(stats['topics']),
        'collections': len(stats['collections']),
        'total_pdfs': stats['total_pdfs'],
        'valid_pdfs': stats['valid_pdfs'],
        'invalid_pdfs': stats['invalid_pdfs'],
        'json_count': stats['json_count'],
        'metadata_complete': stats['metadata_complete'],
        'metadata_only': stats['metadata_only'],
        'duplicates': stats['duplicates'],
        'domain_list': list(stats['domains'])
    }))

if __name__ == '__main__':
    process()
