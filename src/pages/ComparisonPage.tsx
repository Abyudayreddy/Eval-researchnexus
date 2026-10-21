import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../utils/api';
import { ComparisonArtifact } from '../models/ResearchContext';
import { ComparisonModalOverlay } from '../components/assistant/ComparisonModalOverlay';

export default function ComparisonPage() {
  const { comparisonId } = useParams<{ comparisonId: string }>();
  const navigate = useNavigate();

  const [comparisonData, setComparisonData] = useState<ComparisonArtifact | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!comparisonId) {
      setError("No comparison ID provided.");
      setIsLoading(false);
      return;
    }

    // First check localStorage for instant hydration
    const saved = localStorage.getItem('researchnexus_active_comparison');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (parsed.comparison_id === comparisonId) {
          setComparisonData(parsed);
          setIsLoading(false);
          return;
        }
      } catch (e) {
        // Fall through to API fetch
      }
    }

    // Fetch from backend
    api.ai.getComparison(comparisonId)
      .then(res => {
        setComparisonData(res);
        localStorage.setItem('researchnexus_active_comparison', JSON.stringify(res));
        setIsLoading(false);
      })
      .catch(err => {
        setError(err.message || "Failed to load comparison artifact.");
        setIsLoading(false);
      });
  }, [comparisonId]);

  return (
    <div className="h-screen w-screen bg-slate-900/30 flex items-center justify-center p-4">
      <ComparisonModalOverlay
        isOpen={true}
        onClose={() => navigate('/assistant')}
        comparisonData={comparisonData}
        isLoading={isLoading}
        loadingStage="Hydrating persisted comparison matrix..."
        error={error}
        onChangeSelection={() => navigate('/assistant')}
      />
    </div>
  );
}
