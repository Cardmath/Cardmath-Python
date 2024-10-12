import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'primereact/resources/themes/soho-dark/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import AuthPage from './pages/AuthPage';
import QuestionsPage from './pages/QuestionsPage';
import LandingPageComponent from './pages/LandingPage';
import TellerConnectComponent from './pages/TellerConnect';
import TeamPage from './pages/TeamPage';
import PreferencesPage from './pages/PreferencesPage';
import DashboardPage from './pages/DashboardPage';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPageComponent />}/>
                <Route path="/connect" element={<TellerConnectComponent />} />
                <Route path="/dashboard" element={ <DashboardPage /> } />
                <Route path="/login" element={<AuthPage userHasAccount={true} />} />
                <Route path="/preferences" element={<PreferencesPage />} />
                <Route path="/questions" element={<QuestionsPage />} />
                <Route path="/register" element={<AuthPage userHasAccount={false} />} />
                <Route path="/team" element={<TeamPage />} />
            </Routes>
        </Router>
    );
};

export default App;