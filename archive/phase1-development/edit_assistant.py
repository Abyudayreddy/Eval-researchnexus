import re

with open('src/pages/AssistantPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Source interface
content = content.replace(
    "evidence_status?: 'evidence_ready' | 'metadata_only';",
    "evidence_status?: 'evidence_ready' | 'metadata_only';\n  retrieval_source?: string;"
)

# Render badge
old_badge = """                 <div className="text-[10px] font-bold text-emerald-600 mb-1 flex items-center justify-between">
                   <span>Source [{idx + 1}]</span>
                   <span className="text-slate-400">{source.source}</span>
                 </div>"""
                 
new_badge = """                 <div className="text-[10px] font-bold text-emerald-600 mb-1 flex items-center justify-between">
                   <div className="flex items-center gap-2">
                     <span>Source [{idx + 1}]</span>
                     {source.retrieval_source === 'local' && <span className="bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded uppercase tracking-widest text-[9px]">LOCAL</span>}
                     {source.retrieval_source === 'online' && <span className="bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded uppercase tracking-widest text-[9px]">ONLINE</span>}
                   </div>
                   <span className="text-slate-400">{source.source}</span>
                 </div>"""
                 
content = content.replace(old_badge, new_badge)

with open('src/pages/AssistantPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
