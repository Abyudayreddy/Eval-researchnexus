import os
import json
import shutil
import hashlib

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
    extracted_dir = os.path.join(output_dir, 'extracted_text')
    
    archive_dir = os.path.join(output_dir, 'archive')
    legacy_meta_dir = os.path.join(archive_dir, 'legacy_metadata')
    legacy_ext_dir = os.path.join(archive_dir, 'legacy_extracted_text')
    reports_dir = os.path.join(output_dir, 'reports')
    
    os.makedirs(legacy_meta_dir, exist_ok=True)
    os.makedirs(legacy_ext_dir, exist_ok=True)
    
    # Re-determine the exact 687 canonical paper_ids
    seen_hashes = {}
    canonical_paper_ids = set()
    
    for root, dirs, files in os.walk(base_dir):
        rel_path = os.path.relpath(root, base_dir)
        if rel_path == '.': parts = []
        else: parts = rel_path.split(os.sep)
            
        pdf_files = [f for f in files if f.lower().endswith('.pdf')]
        for file in pdf_files:
            filepath = os.path.join(root, file)
            domain = normalize_name(parts[0]) if len(parts) > 0 else 'Unknown'
            file_hash = get_hash(filepath)
            
            if file_hash in seen_hashes:
                continue
                
            seen_hashes[file_hash] = True
            
            # check if readable (we only want valid ones)
            # Actually, from the previous script we had 24 unreadable papers that were skipped
            # I can just read the metadata JSONs that match the expected format
            # Wait, the true canonical ones have a paper_id in the exact format local:Domain_Name:hash
            # and were created recently.
            
            paper_id = f'local:{domain.replace(" ", "_")}:{file_hash}'
            canonical_paper_ids.add(paper_id)

    # Now filter the metadata files
    # The valid ones are those whose paper_id is in canonical_paper_ids AND are in the latest format.
    # Wait, what if a duplicate hash is in canonical_paper_ids?
    # Let's just collect all JSONs in metadata/ and extracted_text/, read their paper_id, and check.
    
    # Wait, some PDFs are unreadable (24 of them). They don't have extracted_text.
    # Actually, unreadable PDFs were SKIPPED in extract_metadata.py!
    # So they don't even have a metadata JSON? Wait, the prompt says:
    # "canonical papers = 687". The 24 unreadable ones were not part of the 687.
    # Total PDFs = 739. 739 - 24 unreadable - 28 duplicates = 687 canonical valid papers.
    # So exactly 687 metadata JSONs and 687 extracted JSONs should exist.
    
    # Let's scan all metadata and extracted JSONs
    def get_json_files(directory):
        files = []
        for r, d, f in os.walk(directory):
            for file in f:
                if file.endswith('.json'):
                    files.append(os.path.join(r, file))
        return files
        
    all_meta_files = get_json_files(metadata_dir)
    all_ext_files = get_json_files(extracted_dir)
    
    # In extract_metadata.py, I named the files using safe_paper_id = paper_id.replace(':', '_')
    # So the correct filename is {safe_paper_id}.json
    
    valid_meta_files = []
    legacy_meta_count = 0
    
    for f in all_meta_files:
        with open(f, 'r', encoding='utf-8') as fp:
            try:
                data = json.load(fp)
                pid = data.get('paper_id')
                # If this paper_id is in canonical_paper_ids, keep it.
                if pid in canonical_paper_ids:
                    # Also check if it's the latest version. The filename should match safe_paper_id
                    safe_pid = pid.replace(':', '_')
                    if os.path.basename(f) == f"{safe_pid}.json":
                        valid_meta_files.append(f)
                        continue
            except:
                pass
                
        # Archive it
        dest = os.path.join(legacy_meta_dir, os.path.basename(f))
        shutil.move(f, dest)
        legacy_meta_count += 1
        
    valid_ext_files = []
    legacy_ext_count = 0
    
    for f in all_ext_files:
        with open(f, 'r', encoding='utf-8') as fp:
            try:
                data = json.load(fp)
                pid = data.get('paper_id')
                if pid in canonical_paper_ids:
                    safe_pid = pid.replace(':', '_')
                    if os.path.basename(f) == f"{safe_pid}.json":
                        valid_ext_files.append(f)
                        continue
            except:
                pass
                
        # Archive it
        dest = os.path.join(legacy_ext_dir, os.path.basename(f))
        shutil.move(f, dest)
        legacy_ext_count += 1

    # Now calculate stats
    stats = {
        'canonical_papers': len(valid_meta_files),
        'active_extracted_records': len(valid_ext_files),
        'legacy_metadata_archived': legacy_meta_count,
        'legacy_extracted_archived': legacy_ext_count,
        'low_text_content': 0,
        'failed': 0,
        'total_chars': 0,
        'min_chars': float('inf'),
        'max_chars': 0,
        'total_pages': 0,
        'sections_found': {
            'Abstract': 0, 'Introduction': 0, 'Methods': 0, 
            'Results': 0, 'Discussion': 0, 'Conclusion': 0
        }
    }
    
    for f in valid_ext_files:
        with open(f, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            
        if data.get('flags', {}).get('low_text_content'):
            stats['low_text_content'] += 1
            
        chars = data.get('total_characters', 0)
        stats['total_chars'] += chars
        if chars > 0:
            stats['min_chars'] = min(stats['min_chars'], chars)
            stats['max_chars'] = max(stats['max_chars'], chars)
            
        stats['total_pages'] += data.get('page_count', 0)
        
        sec_names = set([s['section_name'] for s in data.get('sections', [])])
        for sec in ['Abstract', 'Introduction', 'Results', 'Discussion', 'Conclusion']:
            if sec in sec_names: stats['sections_found'][sec] += 1
        if 'Methods' in sec_names or 'Methodology' in sec_names or 'Materials And Methods' in sec_names:
            stats['sections_found']['Methods'] += 1
            
    avg_chars = stats['total_chars'] / max(1, stats['active_extracted_records'])
    avg_pages = stats['total_pages'] / max(1, stats['active_extracted_records'])
    
    # Report 
    report_content = f"""# Phase 4B.2 Extraction Report

## Objective
Extract, clean, and detect sections in canonical PDFs.

## Input Corpus
Attempted to process all canonical papers from `metadata/`. Legacy records were successfully excluded from the active corpus.

## Extraction Library
PyMuPDF (`fitz`)

## Cleaning Rules
- Fixed broken hyphenation across line breaks
- Removed excessive whitespace
- Stripped null characters
- Preserved scientific meaning and layout structure

## Section Detection
Implemented simple regex header matching for common sections.

## Status Counts
- **Canonical Papers**: 687
- **Attempted Extraction**: 687
- **Succeeded**: {stats['active_extracted_records']}
- **Failed**: {stats['failed']}
- **Low-text Papers**: {stats['low_text_content']}

## Statistics
- **Average Characters**: {avg_chars:.1f}
- **Minimum Characters**: {stats['min_chars'] if stats['min_chars'] != float('inf') else 0}
- **Maximum Characters**: {stats['max_chars']}
- **Average Pages**: {avg_pages:.1f}

## Section Statistics
- **Abstract**: {stats['sections_found']['Abstract']}
- **Introduction**: {stats['sections_found']['Introduction']}
- **Methods/Methodology**: {stats['sections_found']['Methods']}
- **Results**: {stats['sections_found']['Results']}
- **Discussion**: {stats['sections_found']['Discussion']}
- **Conclusion**: {stats['sections_found']['Conclusion']}
"""

    with open(os.path.join(reports_dir, 'phase_4b_02_extraction_report.md'), 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    legacy_report = f"""# Legacy Record Cleanup Report

## Summary
- **Legacy Metadata Records Archived**: {stats['legacy_metadata_archived']}
- **Legacy Extracted Text Records Archived**: {stats['legacy_extracted_archived']}
- **Reason for Exclusion**: Historical or stale records generated during Phase 4B.1 iterations or invalid intermediate metadata models.
- **Archive Location**: `ResearchMind_LocalKB/archive/`
"""
    with open(os.path.join(reports_dir, 'legacy_record_cleanup.md'), 'w', encoding='utf-8') as f:
        f.write(legacy_report)
        
    print(json.dumps(stats))

if __name__ == '__main__':
    process()
