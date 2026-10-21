with open("src/pages/HybridSearchPage.tsx", "r", encoding="utf-8") as f:
    content = f.read()

select_new = """          <div className="relative">
            <select 
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="appearance-none bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-700 py-1.5 pl-3 pr-8 outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 cursor-pointer shadow-sm hover:border-emerald-300 transition-colors"
            >
              <option value="relevance">Most Relevant</option>
              <option value="newest">Newest</option>
              <option value="oldest">Oldest</option>
            </select>
            <ChevronDown className="w-3 h-3 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>
        
        {/* SUMMARY & INDICATOR */}
        {hasSearched && !isLoading && retrievalMeta && (
          <div className="flex items-center justify-between text-xs font-medium border-t border-slate-100 pt-3">
            <div className="text-slate-500">
              {retrievalMeta.retrieval_source === 'local' && `Local Research • ${results.length} results`}
              {retrievalMeta.retrieval_source === 'online_fallback' && `Online Fallback • ${results.length} results`}
              {retrievalMeta.retrieval_source === 'mixed' && `Local Research + Online Sources • ${results.length} results`}
              {retrievalMeta.retrieval_source === 'online' && `Online Sources • ${results.length} results`}
            </div>
            <div>
              {retrievalMeta.retrieval_source === 'local' && <span className="text-emerald-600 font-bold">✓ Found in Local Research</span>}
              {retrievalMeta.retrieval_source === 'online_fallback' && <span className="text-blue-600 font-bold">Local evidence was insufficient. Searching trusted online academic sources...</span>}
            </div>
          </div>
        )}
      </div>"""

select_fixed = select_new + "\n      </div>"

content = content.replace(select_new, select_fixed)

with open("src/pages/HybridSearchPage.tsx", "w", encoding="utf-8") as f:
    f.write(content)
