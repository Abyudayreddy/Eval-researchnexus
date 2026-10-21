import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'LiteratureReviewPage' in filepath:
        content = re.sub(r"import\s*\{\s*normalizeSearchId\s*\}\s*from\s*'../utils/apiAdapter';\n", "", content)
        content = content.replace("import { normalizeSearchId, apiAdapter }", "import { apiAdapter }")
    if 'XaiPage' in filepath:
        # We might have imported it twice
        content = re.sub(r"import\s*\{\s*normalizeSearchId\s*\}\s*from\s*'../utils/apiAdapter';\n", "", content)
        # Ensure only one is in the named imports
        content = content.replace("normalizeSearchExperimentResponse, ExperimentStatus, normalizeSearchId, normalizeSearchId", "normalizeSearchExperimentResponse, ExperimentStatus, normalizeSearchId")
        content = content.replace("normalizeSearchExperimentResponse, ExperimentStatus, normalizeSearchId", "normalizeSearchExperimentResponse, ExperimentStatus, normalizeSearchId")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

clean_file('src/pages/LiteratureReviewPage.tsx')
clean_file('src/pages/XaiPage.tsx')

# Let's double check XaiPage explicitly
with open('src/pages/XaiPage.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
deduped_lines = []
seen_imports = set()
for line in lines:
    if line.startswith('import {') and 'normalizeSearchId' in line:
        if line in seen_imports:
            continue
        seen_imports.add(line)
        # remove duplicate words in line
        if line.count('normalizeSearchId') > 1:
            line = line.replace(', normalizeSearchId', '', line.count('normalizeSearchId') - 1)
    deduped_lines.append(line)

with open('src/pages/XaiPage.tsx', 'w', encoding='utf-8') as f:
    f.writelines(deduped_lines)

