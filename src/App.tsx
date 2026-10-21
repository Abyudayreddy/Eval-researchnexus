import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import DashboardPage from './pages/DashboardPage';
import ResearchPage from './pages/ResearchPage';
import ResearchDomainsPage from './pages/ResearchDomainsPage';
import DomainWorkspacePage from './pages/DomainWorkspacePage';
import LiteratureReviewPage from './pages/LiteratureReviewPage';
import NotebookPage from './pages/NotebookPage';
import XaiPage from './pages/XaiPage';
import AnalyticsPage from './pages/AnalyticsPage';
import HybridSearchPage from './pages/HybridSearchPage';
import AssistantPage from './pages/AssistantPage';
import DiscussionsPage from './pages/DiscussionsPage';
import PaperLibraryPage from './pages/PaperLibraryPage';
import NotificationsPage from './pages/NotificationsPage';
import SettingsPage from './pages/SettingsPage';
import ResearchOverviewPage from './pages/ResearchOverviewPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import PaperReaderPage from './pages/PaperReaderPage';
import ComparisonPage from './pages/ComparisonPage';
import { useAuthStore } from './store/authStore';
import React, { useEffect } from 'react';

import LandingPage from './pages/LandingPage';

// Protected Route Wrapper
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, checkAuth, isLoading } = useAuthStore();
  
  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  if (isLoading) {
    return <div className="h-screen flex items-center justify-center bg-[#F8FAFC]">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        <Route element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }>
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="research-overview/:id" element={<ResearchOverviewPage />} />
          <Route path="research" element={<ResearchPage />} />
          <Route path="research-domains" element={<ResearchDomainsPage />} />
          <Route path="research-domains/:domainId" element={<DomainWorkspacePage />} />
          <Route path="literature-review" element={<LiteratureReviewPage />} />
          <Route path="notebook" element={<NotebookPage />}>
            <Route path=":noteId" element={<NotebookPage />} />
          </Route>
          <Route path="xai" element={<XaiPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="hybrid-search" element={<HybridSearchPage />} />
          <Route path="assistant" element={<AssistantPage />} />
          <Route path="comparison/:comparisonId" element={<ComparisonPage />} />
          <Route path="read" element={<PaperReaderPage />} />
          <Route path="paper-library" element={<PaperLibraryPage />} />
          <Route path="notifications" element={<NotificationsPage />} />
          <Route path="profile" element={<Navigate to="/settings" replace />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="settings/research-review-toolkit" element={<Navigate to="/settings" replace />} />
          <Route path="discussions" element={<DiscussionsPage />}>
            <Route path=":id" element={<DiscussionsPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
