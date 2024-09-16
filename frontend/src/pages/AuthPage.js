import './AuthPage.css';  // Optional: for custom styles
import 'primeicons/primeicons.css';                        // Icons
import 'primereact/resources/primereact.min.css';          // Core CSS
import 'primereact/resources/themes/saga-blue/theme.css';  // Theme
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { Password } from 'primereact/password';
import React, { useState } from 'react';

const AuthPage = ({ userHasAccount }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    var endpoint = userHasAccount ? 'http://localhost:8000/token' : 'http://localhost:8000/register';  

    const handleLogin = () => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        }).then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            localStorage.setItem('token', data.access_token);
            window.location.href = '/connect';
        })
        .catch(error => {
            console.error('There was an error!', error)
        });
    };

    return (
        <div className="login-container">
            <h2>{userHasAccount ? "Login" : "Register"}</h2>
            <div className="p-field">
                <label htmlFor="username">Email</label>
                <InputText id="username" value={username} onChange={(e) => setUsername(e.target.value)} />
            </div>
            <div className="p-field">
                <label htmlFor="password">Password</label>
                <Password id="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </div>
            <Button label="Login" icon="pi pi-sign-in" onClick={handleLogin} />
        </div>
    );
};

const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
};

export const fetchWithAuth = (url, options = {}) => {
    const headers = getAuthHeaders();
    return fetch(url, {
        ...options,
        headers: {
            ...headers,
            ...options.headers
        }
    });
};

export default AuthPage;