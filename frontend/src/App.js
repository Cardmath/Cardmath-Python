import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'primereact/resources/themes/soho-dark/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import AuthPage from './pages/AuthPage';
import LandingPageComponent from './pages/LandingPage';
import TellerConnectComponent from './pages/TellerConnect';
import TeamPage from './pages/TeamPage';
import PreferencesPage from './pages/PreferencesPage';
import DashboardPage from './pages/DashboardPage';
import CreditCardDatabase from './pages/CreditCardDatabase';
import ContactUsPage from './pages/ContactUsPage';
import ResetPassword from './pages/ResetPasswordPage';
import RegistrationFlowPage from './pages/RegistrationFlowPage';
import ArticleDetailPage from './components/articles/ArticleDetailPage';
import BlogPage from './pages/BlogPage';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPageComponent />}/>
                <Route path="/connect" element={<TellerConnectComponent />} />
                <Route path="/dashboard" element={ <DashboardPage /> } />
                <Route path="/login" element={<AuthPage userHasAccount={true} />} />
                <Route path="/preferences" element={<PreferencesPage />} />
                <Route path="/register" element={<AuthPage userHasAccount={false} />} />
                <Route path="/team" element={<TeamPage />} />
                <Route path='/creditcards' element={<CreditCardDatabase />} />
                <Route path='/contact-us' element={<ContactUsPage />} />
                <Route path="/reset-password" element={<ResetPassword />} />
                <Route path="/registration-steps" element={<RegistrationFlowPage />} />
                <Route path="/articles/:id" element={<ArticleDetailPage/>} />
                <Route path="/blog" element={<BlogPage/>} />
            </Routes>
        </Router>
    );
};

export default App;