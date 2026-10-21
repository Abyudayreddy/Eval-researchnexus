import re

with open('src/pages/XaiPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix XaiDetail header
new_header = """
        <header className="px-6 py-4 border-b border-slate-200 bg-white shrink-0 z-10">
          <button onClick={onBack} className="text-xs font-bold text-slate-500 hover:text-slate-800 flex items-center gap-1 mb-2 transition-colors uppercase tracking-wider">
            <ArrowLeft className="w-3.5 h-3.5" /> Back to Queries
          </button>
          <h1 className="text-2xl font-black text-blue-900 mb-1">
            Online Retrieval Timeline
          </h1>
        </header>
"""
content = re.sub(r'<header className="px-6 py-4 border-b border-slate-200 bg-white shrink-0 z-10">[\s\S]*?</header>', new_header, content, count=1)

# Add "Online Retrieval Summary" to XaiDetail
# We will just append it after the timeline. The timeline is in `<div className="w-full overflow-x-auto pb-6 shrink-0">`
# Actually, the quickest way is to just inject it before the closing `</div>` of the `flex-1` container.
summary = """
        <div className="p-6 shrink-0">
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-5">
            <h3 className="font-black text-blue-900 text-lg mb-3">Online Retrieval Summary</h3>
            <div className="flex justify-between items-start gap-4 mb-2">
              <span className="font-bold text-slate-500 min-w-[140px] text-xs">Candidate Count</span>
              <span className="text-slate-800 text-right flex-1 break-words">{trace.raw_result_count ?? <span className="italic text-slate-400">Not available from source trace.</span>}</span>
            </div>
            <div className="flex justify-between items-start gap-4 mb-2">
              <span className="font-bold text-slate-500 min-w-[140px] text-xs">Final Count</span>
              <span className="text-slate-800 text-right flex-1 break-words">{trace.final_result_count ?? <span className="italic text-slate-400">Not available from source trace.</span>}</span>
            </div>
            <div className="flex justify-between items-start gap-4 mb-2">
              <span className="font-bold text-slate-500 min-w-[140px] text-xs">Latency</span>
              <span className="text-slate-800 text-right flex-1 break-words">{trace.latency ? `${trace.latency}ms` : <span className="italic text-slate-400">Not available from source trace.</span>}</span>
            </div>
          </div>
        </div>
      </div>
"""
content = content.replace("</div>\n\n      {/* OVERLAYS */}", summary + "\n      {/* OVERLAYS */}")

# Fix XaiPage header so we don't have duplicated nested headers if possible.
# Actually, the user says "XAI page title: Research Explainability Timeline. Under it show two tabs: [ LOCAL RETRIEVAL ] [ ONLINE RETRIEVAL ]"
# It's better if `XaiPage` renders the main header, and `XaiDetail`/`LocalXaiDetail` just render the tabs and content.
# I'll just change the text of the headers in `LocalXaiDetail` and `XaiDetail` to be subsections.

with open('src/pages/XaiPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
