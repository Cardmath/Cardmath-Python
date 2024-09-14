import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Button } from 'primereact/button';
import 'primereact/resources/themes/saga-blue/theme.css';  // Theme
import 'primereact/resources/primereact.min.css';          // Core CSS
import 'primeicons/primeicons.css';                        // Icons
import LoginPage from './pages/LoginPage';
import TellerConnectComponent from './pages/TellerConnect';

const App = () => {
    const handleSuccess = (data) => {
      console.log('Success:', data);
    };

    window.intercomSettings = {
      app_id: 'your-app-id',
      cookie: {
          sameSite: 'None',
          secure: true
      }
    };

    return (
        <Router>
            <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/teller-connect" element={<TellerConnectComponent onSuccess={handleSuccess}/>} />
                <Route path="/" element={
                    <div className="landing-page">
                        <h1>Welcome to Cardmath</h1>
                        <div className="button-group">
                            <Button label="Login" icon="pi pi-sign-in" onClick={() => window.location.href = '/login'} />
                            <Button label="Teller Connect" icon="pi pi-check" onClick={() => window.location.href = '/teller-connect'} />
                        </div>
                    </div>
                } />
            </Routes>
        </Router>
    );
};

export default App;