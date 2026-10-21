import os
import json
import csv
import pandas as pd
from glob import glob

metadata_dir = "ResearchMind_LocalKB/metadata"
dataset_dir = "ResearchMind_Dataset"

# 1. Discover all JSON files
json_files = glob(f"{metadata_dir}/**/*.json", recursive=True)

# 2. Discover all CSV files
csv_files = glob(f"{dataset_dir}/**/*.csv", recursive=True)

print(f"Discovered {len(csv_files)} CSV files.")

# Load all CSV data into a dictionary indexed by filename
csv_metadata = {}
for csv_file in csv_files:
    try:
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            # Normalize keys to lowercase
            row_dict_lower = {str(k).strip().lower(): v for k, v in row_dict.items()}
            
            # Find the filename column
            filename = None
            for key in ['file_name', 'filename', 'file', 'pdf', 'id', 'paper_id']:
                if key in row_dict_lower and pd.notna(row_dict_lower[key]):
                    val = str(row_dict_lower[key]).strip()
                    if '.pdf' in val.lower():
                        filename = val
                        break
                    elif key in ['file_name', 'filename']:
                        filename = val
                        break
                        
            if filename:
                if not filename.endswith('.pdf'):
                    filename += '.pdf'
                csv_metadata[filename] = row_dict_lower
    except Exception as e:
        print(f"Failed to parse {csv_file}: {e}")

print(f"Loaded {len(csv_metadata)} rows from CSV files.")

# 3. Update Canonical JSONs
papers_updated = 0
total_canonical_papers = 0
metadata_fields = {
    'title': 0, 'authors': 0, 'abstract': 0, 'doi': 0,
    'online_url': 0, 'local_pdf': 0, 'both': 0, 'neither': 0,
    'unknown_title': 0, 'fake_default': 0
}

canonical_papers_map = {}

for json_file in json_files:
    if "canonical_papers.json" in json_file:
        continue
    # Read
    with open(json_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception:
            continue
            
    # Normalize to list
    is_list = isinstance(data, list)
    records = data if is_list else [data]
    
    modified_records = []
    
    for record in records:
        total_canonical_papers += 1
        
        # Identity
        paper_id = record.get('id') or record.get('paper_id')
        filename = record.get('source_id')
        
        # Merge if filename matches CSV
        if filename and filename in csv_metadata:
            csv_row = csv_metadata[filename]
            
            # Title
            if 'title' in csv_row and pd.notna(csv_row['title']):
                record['title'] = str(csv_row['title']).strip()
                record['title_source'] = 'csv'
                
            # Authors
            if 'authors' in csv_row and pd.notna(csv_row['authors']):
                auth_str = str(csv_row['authors'])
                record['authors'] = [{'name': a.strip(), 'orcid': None, 'affiliation': None} for a in auth_str.split(';') if a.strip()]
                if len(record['authors']) <= 1 and ',' in auth_str:
                    record['authors'] = [{'name': a.strip(), 'orcid': None, 'affiliation': None} for a in auth_str.split(',') if a.strip()]
                
            # Year
            if 'year' in csv_row and pd.notna(csv_row['year']):
                record['publication_year'] = str(csv_row['year']).strip()
                if record['publication_year'].endswith('.0'):
                    record['publication_year'] = record['publication_year'][:-2]
            elif 'date' in csv_row and pd.notna(csv_row['date']):
                record['publication_date'] = str(csv_row['date']).strip()
                
            # URL
            if 'source_url' in csv_row and pd.notna(csv_row['source_url']):
                record['paper_url'] = str(csv_row['source_url']).strip()
            elif 'url' in csv_row and pd.notna(csv_row['url']):
                record['paper_url'] = str(csv_row['url']).strip()
            elif 'link' in csv_row and pd.notna(csv_row['link']):
                record['paper_url'] = str(csv_row['link']).strip()
                
            # Abstract
            if 'abstract' in csv_row and pd.notna(csv_row['abstract']):
                record['abstract'] = str(csv_row['abstract']).strip()
                
            # DOI
            if 'doi' in csv_row and pd.notna(csv_row['doi']):
                record['doi'] = str(csv_row['doi']).strip()
                
        # Remove fabricated defaults
        if record.get('title') in ['Unknown', 'Untitled', '', None]:
            record['title'] = None
            metadata_fields['unknown_title'] += 1
            
        # Fix authors if it's "Authors unavailable" or string
        if isinstance(record.get('authors'), str):
            if "unavailable" in record['authors'].lower():
                record['authors'] = []
                metadata_fields['fake_default'] += 1
            else:
                record['authors'] = [{'name': record['authors']}]
        elif isinstance(record.get('authors'), list):
            if len(record['authors']) == 1 and isinstance(record['authors'][0], dict) and "unavailable" in record['authors'][0].get('name', '').lower():
                record['authors'] = []
                metadata_fields['fake_default'] += 1
                
        # Fix year fabricated
        if record.get('publication_year') == '2023' and record.get('title_source') != 'csv':
            record['publication_year'] = None
            metadata_fields['fake_default'] += 1
        if record.get('publication_date') == '2023-01-01':
            record['publication_date'] = None
            metadata_fields['fake_default'] += 1
            
        # Determine read_source and URLs
        has_url = bool(record.get('paper_url') or record.get('url'))
        has_pdf = bool(record.get('pdf_path'))
        
        # Ensure 'paper_url' is canonical
        if not record.get('paper_url') and record.get('url'):
            record['paper_url'] = record.get('url')
            
        if has_url:
            record['read_source'] = 'online'
        elif has_pdf:
            record['read_source'] = 'local_pdf'
        else:
            record['read_source'] = 'unavailable'
            
        # Track stats
        if record.get('title'): metadata_fields['title'] += 1
        if record.get('authors') and len(record.get('authors')) > 0: metadata_fields['authors'] += 1
        if record.get('abstract'): metadata_fields['abstract'] += 1
        if record.get('doi'): metadata_fields['doi'] += 1
        
        if has_url and has_pdf: metadata_fields['both'] += 1
        elif has_url: metadata_fields['online_url'] += 1
        elif has_pdf: metadata_fields['local_pdf'] += 1
        else: metadata_fields['neither'] += 1
        
        modified_records.append(record)
        canonical_papers_map[paper_id] = record
        papers_updated += 1

    # Write back
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(modified_records if is_list else modified_records[0], f, indent=2)

# Save Master canonical_papers.json
with open(os.path.join(metadata_dir, "canonical_papers.json"), 'w', encoding='utf-8') as f:
    json.dump(canonical_papers_map, f, indent=2)

print(f"Total Canonical Papers: {total_canonical_papers}")
print("Coverage Stats:", metadata_fields)
