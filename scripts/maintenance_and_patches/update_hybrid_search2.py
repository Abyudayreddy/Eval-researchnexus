import re

with open("src/pages/HybridSearchPage.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the specific link block with the one guided by read_source
link_old = """              {selectedPaper.retrieval_source === 'local' ? (
                <a 
                  href={`http://localhost:8000/api/papers/${selectedPaper.id}/pdf`} 
                  target="_blank" 
                  rel="noreferrer"
                  className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm font-bold transition-colors flex items-center justify-center gap-2"
                >
                  <Maximize className="w-4 h-4" /> Open PDF
                </a>
              ) : selectedPaper.url ? (
                <a 
                  href={selectedPaper.url} 
                  target="_blank" 
                  rel="noreferrer"
                  className="w-full py-2.5 bg-slate-900 hover:bg-emerald-600 text-white rounded-lg text-sm font-bold transition-colors flex items-center justify-center gap-2"
                >
                  <Maximize className="w-4 h-4" /> Open Source
                </a>
              ) : (
                <button disabled className="w-full py-2.5 bg-slate-100 text-slate-400 rounded-lg text-sm font-bold flex items-center justify-center gap-2 cursor-not-allowed">
                  <Maximize className="w-4 h-4" /> Not Available
                </button>
              )}"""

link_new = """              {selectedPaper.read_source === 'online' || (selectedPaper.retrieval_source === 'online' && selectedPaper.url) ? (
                <a 
                  href={selectedPaper.paper_url || selectedPaper.url} 
                  target="_blank" 
                  rel="noreferrer"
                  className="w-full py-2.5 bg-slate-900 hover:bg-emerald-600 text-white rounded-lg text-sm font-bold transition-colors flex items-center justify-center gap-2"
                >
                  <Maximize className="w-4 h-4" /> Open Source
                </a>
              ) : selectedPaper.read_source === 'local_pdf' || (selectedPaper.retrieval_source === 'local' && selectedPaper.pdf_path) ? (
                <a 
                  href={`http://localhost:8000/api/papers/${selectedPaper.id}/pdf`} 
                  target="_blank" 
                  rel="noreferrer"
                  className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm font-bold transition-colors flex items-center justify-center gap-2"
                >
                  <Maximize className="w-4 h-4" /> Open PDF
                </a>
              ) : (
                <button disabled className="w-full py-2.5 bg-slate-100 text-slate-400 rounded-lg text-sm font-bold flex items-center justify-center gap-2 cursor-not-allowed">
                  <Maximize className="w-4 h-4" /> Full paper is not available.
                </button>
              )}"""
content = content.replace(link_old, link_new)

with open("src/pages/HybridSearchPage.tsx", "w", encoding="utf-8") as f:
    f.write(content)
