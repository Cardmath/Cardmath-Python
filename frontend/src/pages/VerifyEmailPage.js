import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Button } from 'primereact/button';
import Alert from '../components/Alert';

const VerifyEmailPage = () => {
    const [alert, setAlert] = useState({ visible: false, message: '', heading: '', type: 'info' });
    const navigate = useNavigate();
    const location = useLocation();

    // Extract token from URL
    const token = new URLSearchParams(location.search).get('token');

    useEffect(() => {
        if (!token) {
            setAlert({
                visible: true,
                message: 'Verification token is missing.',
                type: 'error',
                heading: 'Error'
            });
            return;
        }

        // Send token to backend to verify email
        fetch('http://localhost:8000/verify-email?token=' + encodeURIComponent(token))
            .then((response) => response.json())
            .then((data) => {
                if (data.msg === 'Email verified successfully') {
                    setAlert({
                        visible: true,
                        message: 'Your email has been verified successfully! You will be redirected to login.',
                        type: 'success',
                        heading: 'Success'
                    });
                    setTimeout(() => navigate('/login'), 3000);
                } else {
                    throw new Error(data.detail || 'Email verification failed');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                setAlert({
                    visible: true,
                    message: error.message || 'Email verification failed. Please try again or contact support.',
                    type: 'error',
                    heading: 'Error'
                });
            });
    }, [token, navigate]);

    return (
        <div className="verify-email-container flex flex-column justify-content-center align-items-center">
            <Alert
                visible={alert.visible}
                message={alert.message}
                type={alert.type}
                heading={alert.heading}
                setVisible={(visible) => setAlert({ ...alert, visible })}
            />
            <div className="card">
                <h2>Email Verification</h2>
                {alert.visible && alert.type === 'info' && (
                    <p>Please wait while we verify your email...</p>
                )}
                {(!alert.visible || alert.type !== 'info') && (
                    <Button label="Go to Login" icon="pi pi-sign-in" className="w-full" onClick={() => navigate('/login')} />
                )}
            </div>
        </div>
    );
};

export default VerifyEmailPage;
