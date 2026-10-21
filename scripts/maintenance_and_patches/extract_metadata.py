import os
import json
import hashlib
import csv
import re
from datetime import datetime
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
        'json_count': 0, 'metadata_complete': 0, 'metadata_partial': 0, 'metadata_missing': 0,
        'evidence_ready': 0, 'metadata_only': 0, 'duplicates': 0,
        'title_extracted': 0, 'title_fallback': 0,
        'author_available': 0, 'abstract_available': 0, 'doi_available': 0,
        'ocr_candidates': 0
    }
    
    csv_metadata = {}
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.csv'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        key = row.get('pdf_filename') or row.get('file_name') or row.get('id')
                        if not key and list(row.values()): key = list(row.values())[0]
                        if key: csv_metadata[key] = row

    seen_hashes = {}
    duplicates_mapping = []
    unreadable_analysis = []
    
    domain_counts = {}
    subdomain_counts = {}
    topic_counts = {}

    for root, dirs, files in os.walk(base_dir):
        rel_path = os.path.relpath(root, base_dir)
        if rel_path == '.': parts = []
        else: parts = rel_path.split(os.sep)
            
        pdf_files = [f for f in files if f.lower().endswith('.pdf')]
        
        for file in pdf_files:
            filepath = os.path.join(root, file)
            stats['total_pdfs'] += 1
            
            domain = normalize_name(parts[0]) if len(parts) > 0 else 'Unknown'
            subdomain = normalize_name(parts[1]) if len(parts) > 1 else 'Unknown'
            topic = normalize_name(parts[2]) if len(parts) > 2 else 'Unknown'
            collection = normalize_name(parts[3]) if len(parts) > 3 else 'Unknown'
            
            stats['domains'].add(domain)
            stats['subdomains'].add(subdomain)
            stats['topics'].add(topic)
            stats['collections'].add(collection)
            
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
            subdomain_counts[subdomain] = subdomain_counts.get(subdomain, 0) + 1
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            file_hash = get_hash(filepath)
            paper_id = f'local:{domain.replace(" ", "_")}:{file_hash}'
            
            if file_hash in seen_hashes:
                stats['duplicates'] += 1
                canonical_path = seen_hashes[file_hash]
                canonical_domain = canonical_path['domain']
                canonical_id = f'local:{canonical_domain.replace(" ", "_")}:{file_hash}'
                duplicates_mapping.append({
                    'duplicate_hash': file_hash,
                    'canonical_paper_id': canonical_id,
                    'duplicate_path': filepath.replace('\\\\', '/'),
                    'canonical_path': canonical_path['path'].replace('\\\\', '/')
                })
                continue
            else:
                seen_hashes[file_hash] = {'path': filepath, 'domain': domain}
                
            readable = False
            unreadable_status = None
            page_count = 0
            text_len = 0
            pdf_metadata = {}
            first_page_text = ""
            full_text = ""
            
            try:
                doc = fitz.open(filepath)
                page_count = doc.page_count
                if page_count == 0:
                    unreadable_status = 'zero-page'
                else:
                    pdf_metadata = doc.metadata
                    for page in doc:
                        text = page.get_text()
                        if not first_page_text: first_page_text = text
                        full_text += text + "\n"
                        
                    text_len = len(full_text.strip())
                    if text_len == 0:
                        # might be scanned/image
                        unreadable_status = 'zero-text'
                        if any(page.get_images() for page in doc):
                            unreadable_status = 'image/scanned'
                    else:
                        readable = True
                doc.close()
            except Exception as e:
                unreadable_status = 'corrupt'
                
            if not readable:
                stats['invalid_pdfs'] += 1
                unreadable_analysis.append({
                    'path': filepath.replace('\\\\', '/'),
                    'status': unreadable_status,
                    'reason': unreadable_status,
                    'ocr_candidate': (unreadable_status == 'image/scanned')
                })
                if unreadable_status == 'image/scanned': stats['ocr_candidates'] += 1
                continue
                
            stats['valid_pdfs'] += 1
            
            row_meta = csv_metadata.get(file, {})
            
            # TITLE EXTRACTION
            title = None
            title_source = None
            if row_meta.get('title'):
                title = row_meta.get('title')
                title_source = 'trusted_metadata'
            elif pdf_metadata.get('title'):
                title = pdf_metadata.get('title').strip()
                if title: title_source = 'pdf_metadata'
                
            if not title and first_page_text:
                lines = [l.strip() for l in first_page_text.split('\n') if l.strip()]
                if lines:
                    title = lines[0][:200] # Take first line as title candidate
                    title_source = 'first_page_extraction'
            
            if not title:
                title = file
                title_source = 'filename_fallback'
                stats['title_fallback'] += 1
            else:
                stats['title_extracted'] += 1
                
            # AUTHORS
            authors_raw = row_meta.get('authors', '')
            if not authors_raw and pdf_metadata.get('author'):
                authors_raw = pdf_metadata.get('author')
            authors_list = [{'name': a.strip(), 'orcid': None, 'affiliation': None} for a in authors_raw.split(';') if a.strip()] if authors_raw else []
            if authors_list: stats['author_available'] += 1
                
            # ABSTRACT
            abstract = row_meta.get('abstract')
            abstract_source = None
            if abstract:
                abstract_source = 'trusted_metadata'
            else:
                abstract_match = re.search(r'(?i)(?:abstract|summary)\s*[\n\:]+(.*?)(?:\n\s*\n|\n(?:introduction|keywords|index terms))', full_text, re.DOTALL)
                if abstract_match:
                    abstract = abstract_match.group(1).strip()
                    abstract_source = 'text_extraction'
            
            if abstract: stats['abstract_available'] += 1
            
            # DOI
            doi = row_meta.get('doi')
            doi_source = None
            if doi:
                doi_source = 'trusted_metadata'
            else:
                doi_match = re.search(r'(10\.\d{4,9}/[-._;()/:A-Z0-9]+)', full_text, re.IGNORECASE)
                if doi_match:
                    doi = doi_match.group(1)
                    doi_source = 'text_extraction'
                    
            if doi: stats['doi_available'] += 1
                    
            evidence_status = 'evidence_ready' if (abstract or text_len > 500) else 'metadata_only'
            if evidence_status == 'evidence_ready': stats['evidence_ready'] += 1
            else: stats['metadata_only'] += 1
                
            fields_present = sum([1 for x in [title_source != 'filename_fallback', bool(authors_list), bool(abstract), bool(doi)] if x])
            if fields_present == 4:
                metadata_completeness = 'complete'
                stats['metadata_complete'] += 1
            elif fields_present > 0:
                metadata_completeness = 'partial'
                stats['metadata_partial'] += 1
            else:
                metadata_completeness = 'missing'
                stats['metadata_missing'] += 1

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
                'doi': doi,
                'source_repository': 'local_curated',
                'source_id': file,
                'url': None,
                'pdf_url': None,
                'pdf_path': filepath.replace('\\\\', '/'),
                'processing_status': 'discovered',
                'processing_error': None,
                'metadata_completeness': metadata_completeness,
                'evidence_status': evidence_status,
                'embedding_status': 'pending',
                'embedding_model': None,
                'embedding_reference': None,
                'ingestion_date': datetime.now().isoformat(),
                'title_source': title_source,
                'abstract_source': abstract_source,
                'doi_source': doi_source
            }
                
            out_dir = os.path.join(metadata_dir, *parts)
            os.makedirs(out_dir, exist_ok=True)
            safe_paper_id = paper_id.replace(':', '_')
            with open(os.path.join(out_dir, f'{safe_paper_id}.json'), 'w', encoding='utf-8') as f:
                json.dump(meta, f, indent=2)
                
            stats['json_count'] += 1

    with open(os.path.join(reports_dir, 'metadata_validation_report.md'), 'w') as f:
        f.write('# Metadata Validation Report\n\n')
        f.write(f'- Total papers: {stats["valid_pdfs"]}\n')
        f.write(f'- Metadata complete: {stats["metadata_complete"]}\n')
        f.write(f'- Metadata partial: {stats["metadata_partial"]}\n')
        f.write(f'- Metadata missing: {stats["metadata_missing"]}\n')
        f.write(f'- Evidence-ready: {stats["evidence_ready"]}\n')
        f.write(f'- Metadata-only: {stats["metadata_only"]}\n')
        f.write(f'- DOI available: {stats["doi_available"]}\n')
        f.write(f'- Abstract available: {stats["abstract_available"]}\n')
        f.write(f'- Author available: {stats["author_available"]}\n')
        f.write(f'- Title extracted: {stats["title_extracted"]}\n')
        f.write(f'- Filename fallback: {stats["title_fallback"]}\n')
        f.write(f'- Duplicates: {stats["duplicates"]}\n')
        f.write(f'- Unreadable: {stats["invalid_pdfs"]}\n')
        f.write(f'- OCR candidates: {stats["ocr_candidates"]}\n')
        f.write('\n## Duplicates\n')
        for dup in duplicates_mapping:
            f.write(f'- {dup["duplicate_path"]} points to canonical {dup["canonical_paper_id"]} ({dup["canonical_path"]})\n')
            
    with open(os.path.join(reports_dir, 'failed_papers.json'), 'w') as f:
        json.dump(unreadable_analysis, f, indent=2)
        
    manifest_summary = {
        'corpus_version': '1.0',
        'generated_at': datetime.now().isoformat(),
        'total_papers': stats['total_pdfs'],
        'canonical_papers': stats['valid_pdfs'],
        'duplicate_files': stats['duplicates'],
        'unreadable_papers': stats['invalid_pdfs'],
        'metadata_complete': stats['metadata_complete'],
        'metadata_partial': stats['metadata_partial'],
        'metadata_missing': stats['metadata_missing'],
        'evidence_ready': stats['evidence_ready'],
        'metadata_only': stats['metadata_only'],
        'domain_counts': domain_counts,
        'subdomain_counts': subdomain_counts,
        'topic_counts': topic_counts
    }
    with open(os.path.join(manifests_dir, 'corpus_manifest.json'), 'w') as f:
        json.dump(manifest_summary, f, indent=2)
        
    mapping_md = '''# Online to Canonical Mapping
    
| Online field | Local source | Canonical field |
| --- | --- | --- |
| id | deterministic local hash | paper_id |
| title | pdf metadata / extracted | title |
| authors | csv / pdf metadata | authors |
| abstract | csv / text extraction | abstract |
| keywords | csv keywords | keywords |
| doi | csv / text extraction | doi |
| journal | csv journal | journal |
'''
    with open(os.path.join(reports_dir, 'online_to_canonical_mapping.md'), 'w') as f:
        f.write(mapping_md)
        
    print(json.dumps(stats))

if __name__ == '__main__':
    process()
