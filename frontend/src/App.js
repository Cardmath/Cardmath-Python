import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Button } from 'primereact/button';
import 'primereact/resources/themes/saga-blue/theme.css';  // Theme
import 'primereact/resources/primereact.min.css';          // Core CSS
import 'primeicons/primeicons.css';                        // Icons
import AuthPage from './pages/AuthPage';
import TellerConnectComponent from './pages/TellerConnect';

const App = () => {
    const handleSuccess = (data) => {
      console.log('Success:', data);
    };

    window.intercomSettings = {
      cookie: {
          sameSite: 'None',
          secure: true
      }
    };

    return (
        <Router>
            <Routes>
                <Route path="/login" element={<AuthPage userHasAccount={true} />} />
                <Route path="/register" element={<AuthPage userHasAccount={false} />} />
                <Route path="/connect" element={<TellerConnectComponent />} />
                <Route path="/" element={
                    <div className="landing-page">
                        <h1>Welcome to Cardmath</h1>
                        <div className="button-group">
                            <Button label="Login" icon="pi pi-sign-in" onClick={() => window.location.href = '/login'} />
                            <Button label="Sign Up" icon="pi pi-user-plus" onClick={() => window.location.href = '/register'} />
                        </div>
                    </div>
                } />
            </Routes>
        </Router>
    );
};

export default App;