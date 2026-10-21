#!/usr/bin/env python3
import glob
import re

target_dir = 'evaluation/module_03/revision_01'
forbidden_patterns = [
    r'100%\s+repair\s+safety',
    r'0%\s+false\s+positive',
    r'0%\s+repair\s+error',
    r'repair\s+safety\s+supported',
    r'repair\s+safety:\s+supported',
    r'repair\s+effectiveness\s*=\s*0',
    r'citation\s+repair\s+failed',
    r'citation\s+repair\s+is\s+ineffective',
    r'citation\s+improvement\s+was\s+proven',
    r'repair\s+safety\s+was\s+demonstrated',
    r'100%\s+safety'
]

clean = True
for filepath in glob.glob(f'{target_dir}/*.md'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for pat in forbidden_patterns:
        matches = list(re.finditer(pat, content, flags=re.IGNORECASE))
        for m in matches:
            if 'REVISION_CHANGELOG.md' in filepath:
                # Quoted historical comparison permitted in changelog table
                continue
            print(f'VIOLATION in {filepath}: {m.group(0)}')
            clean = False

if clean:
    print('ALL REVISION 01 ARTIFACTS ARE 100% CLEAN AND TERMINOLOGY-LOCKED.')
