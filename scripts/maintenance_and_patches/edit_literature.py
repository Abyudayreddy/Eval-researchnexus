import re

with open('src/pages/LiteratureReviewPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
"""  const projectId = location.state?.projectId;""",
"""  const projectId = location.state?.projectId;
  const searchId = location.state?.search_id;
  const initialPapers = location.state?.selected_papers;"""
)

content = content.replace(
"""  useEffect(() => {
    loadBookmarks();
  }, []);

  const loadBookmarks = async () => {
    setIsLoading(true);
    try {
      if (projectId) {
        const data = await api.projects.getPapers(projectId);
        setBookmarks(data);
      } else {
        const data = await api.bookmarks.getAll();
        setBookmarks(data);
      }
    } catch (err) {
      console.error("Failed to load papers", err);
    } finally {
      setIsLoading(false);
    }
  };""",
"""  useEffect(() => {
    if (initialPapers && initialPapers.length > 0) {
      // If we arrived from a search with pre-selected papers, use them directly
      // Mapping them to look like bookmark objects so the rest of the UI works
      setBookmarks(initialPapers.map((p: any) => ({ paper: p })));
      setSelectedPaperIds(new Set(initialPapers.map((p: any) => p.id)));
      setIsLoading(false);
    } else {
      loadBookmarks();
    }
  }, [initialPapers]);

  const loadBookmarks = async () => {
    setIsLoading(true);
    try {
      if (projectId) {
        const data = await api.projects.getPapers(projectId);
        setBookmarks(data);
      } else {
        const data = await api.bookmarks.getAll();
        setBookmarks(data);
      }
    } catch (err) {
      console.error("Failed to load papers", err);
    } finally {
      setIsLoading(false);
    }
  };"""
)

with open('src/pages/LiteratureReviewPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
