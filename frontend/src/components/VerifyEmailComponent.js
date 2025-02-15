import React, { useState, useEffect } from 'react';
import { Button } from 'primereact/button';
import { useLocation } from 'react-router-dom';
import Alert from './Alert';
import { getBackendUrl } from '../utils/urlResolver';


const VerifyEmailComponent = ({ onSuccess }) => {
    const [alert, setAlert] = useState({
        visible: false,
        message: '',
        heading: '',
        type: 'info',
    });
    const location = useLocation();

    // Extract token from URL
    const token = new URLSearchParams(location.search).get('token');

    useEffect(() => {
        if (!token) {
            setAlert({
                visible: true,
                message: 'Check your email for the verification link.',
                type: 'info',
                heading: 'Verification Email Sent',
            });
            return;
        }

        // Send token to backend to verify email
        fetch(`${getBackendUrl()}/verify-email?token=` + encodeURIComponent(token))
            .then((response) => response.json())
            .then((data) => {
                if (data.msg === 'Email verified successfully') {
                    setAlert({
                        visible: true,
                        message: 'Your email has been verified successfully!',
                        type: 'success',
                        heading: 'Success',
                    });
                    setTimeout(() => onSuccess(), 2000); // Proceed to next step
                } else {
                    throw new Error(data.detail || 'Email verification failed');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                setAlert({
                    visible: true,
                    message:
                        error.message ||
                        'Email verification failed. Please try again or contact support.',
                    type: 'error',
                    heading: 'Error',
                });
            });
    }, [token, onSuccess]);

    const retryVerification = () => {
        fetch(`${getBackendUrl()}/retry-email-verification`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.msg === 'Verification email resent successfully') {
                    setAlert({
                        visible: true,
                        message: 'Verification email resent successfully!',
                        type: 'success',
                        heading: 'Success',
                    });
                } else {
                    throw new Error(data.detail || 'Failed to resend verification email. Please contact support@cardmath.ai if this issue persists.');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                setAlert({
                    visible: true,
                    message: error.message || 'Failed to resend verification email. Please try again later. Please contact support@cardmath.ai if this issue persists.',
                    type: 'error',
                    heading: 'Error',
                });
            });
    };
    return (
        <div className='flex flex-column'>
            <div className="flex pt-6 pb-4 text-white font-bold text-6xl">Verify Your Email</div>
            <Alert
                visible={alert.visible}
                message={alert.message}
                type={alert.type}
                heading={alert.heading}
                setVisible={(visible) => setAlert({ ...alert, visible })}
            />
            <div className="w-4 mt-4">
                <Button
                        className="p-button p-component"
                        onClick={() => retryVerification()}
                        label="Retry Verification"
                        size='large'
                    />
            </div>
        </div>
    );
};

export default VerifyEmailComponent;
