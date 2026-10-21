import re

with open('src/utils/apiAdapter.ts', 'r', encoding='utf-8') as f:
    content = f.read()

new_logic = """
export function normalizeSearchId(value: any): string | null {
  if (typeof value !== 'string') return null;
  const trimmed = value.trim();
  if (!trimmed || trimmed === 'null' || trimmed === 'undefined' || trimmed === '[object Object]') return null;
  
  // Basic UUID validation
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  if (!uuidRegex.test(trimmed)) return null;
  return trimmed;
}
"""
if 'normalizeSearchId' not in content:
    content += new_logic

with open('src/utils/apiAdapter.ts', 'w', encoding='utf-8') as f:
    f.write(content)
