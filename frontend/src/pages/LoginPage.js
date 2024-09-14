import React, { useState } from 'react';
import { InputText } from 'primereact/inputtext';
import { Password } from 'primereact/password';
import { Button } from 'primereact/button';
import 'primereact/resources/themes/saga-blue/theme.css';  // Theme
import 'primereact/resources/primereact.min.css';          // Core CSS
import 'primeicons/primeicons.css';                        // Icons
import './LoginPage.css';  // Optional: for custom styles

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = () => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        fetch('http://localhost:8000/register', {
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
        }).then(data => {
            // Handle the data
            window.location.href = '/account-linking';
        })
        .catch(error => {
            console.error('There was an error!', error)
        });
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            <div className="p-field">
                <label htmlFor="username">Username</label>
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

export default LoginPage;