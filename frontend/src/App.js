import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'primereact/resources/themes/soho-dark/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import AuthPage from './pages/AuthPage';
import LandingPageComponent from './pages/LandingPage';
import TeamPage from './pages/TeamPage';
import PreferencesPage from './pages/PreferencesPage';
import DashboardPage from './pages/DashboardPage';
import CreditCardDatabase from './pages/CreditCardDatabase';
import ResetPassword from './pages/ResetPasswordPage';
import ArticleDetailPage from './components/articles/ArticleDetailPage';
import OnboardingFlow from './pages/OnboardingFlowPage';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPageComponent />}/>
                <Route path="/articles/:id" element={<ArticleDetailPage/>} />
                <Route path="/contact-us" element={<TeamPage />} />
                <Route path="/creditcards" element={<CreditCardDatabase />} />
                <Route path="/dashboard" element={ <DashboardPage /> } />
                <Route path="/login" element={<AuthPage userHasAccount={true} />} />
                <Route path="/preferences" element={<PreferencesPage />} />
                <Route path="/register" element={<OnboardingFlow />} />
                <Route path="/reset-password" element={<ResetPassword />} />
                <Route path="/team" element={<TeamPage />} />
            </Routes>
        </Router>
    );
};

export default App;