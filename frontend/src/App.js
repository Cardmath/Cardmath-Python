import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'primereact/resources/themes/soho-dark/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import AuthPage from './pages/AuthPage';
import LandingPageComponent from './pages/LandingPage';
import TeamPage from './pages/TeamPage';
import DashboardPage from './pages/DashboardPage';
import CreditCardDatabase from './pages/CreditCardDatabase';
import ResetPassword from './pages/ResetPasswordPage';
import OnboardingFlow from './pages/OnboardingFlowPage';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPageComponent />}/>
                <Route path="/contact-us" element={<TeamPage />} />
                <Route path="/creditcards" element={<CreditCardDatabase />} />
                <Route path="/dashboard" element={ <DashboardPage /> } />
                <Route path="/login" element={<AuthPage userHasAccount={true} />} />
                <Route path="/register" element={<OnboardingFlow />} />
                <Route path="/reset-password" element={<ResetPassword />} />
            </Routes>
        </Router>
    );
};

export default App;