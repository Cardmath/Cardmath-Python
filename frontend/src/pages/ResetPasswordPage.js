import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Password } from 'primereact/password';
import { Button } from 'primereact/button';
import Alert from '../components/Alert';
import { getBackendUrl } from '../utils/urlResolver';

const ResetPassword = () => {
    const [newPassword, setNewPassword] = useState('');
    const [passwordValid, setPasswordValid] = useState(false);
    const [alert, setAlert] = useState({ visible: false, message: '', heading: '', type: 'error' });
    const navigate = useNavigate();
    const location = useLocation();
    const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&,.])[A-Za-z\d@$!%*?&,.]{8,}$/;

    // Extract token from URL
    const token = new URLSearchParams(location.search).get('token');

    // Validate password strength
    const handlePasswordChange = (newPassword) => {
        setNewPassword(newPassword);
        setPasswordValid(strongPasswordRegex.test(newPassword));
    };

    const handleResetPassword = () => {
        if (!passwordValid) {
            setAlert({
                visible: true,
                message: 'Password must be at least 8 characters long, include uppercase, lowercase, a digit, and a special character.',
                type: 'error',
                heading: 'Invalid Password'
            });
            return;
        }

        fetch(`${getBackendUrl()}/reset-password/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ token, new_password: newPassword })
        })
            .then((response) => {
                if (response.ok) {
                    setAlert({
                        visible: true,
                        message: 'Password reset successfully! You will be redirected to login.',
                        type: 'success',
                        heading: 'Success'
                    });
                    setTimeout(() => navigate('/login'), 3000);
                } else {
                    throw new Error('Failed to reset password');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                setAlert({
                    visible: true,
                    message: 'Password reset failed. Please try again or contact support.',
                    type: 'error',
                    heading: 'Error'
                });
            });
    };

    return (
        <div className="reset-password-container flex flex-column justify-content-center align-items-center">
            <Alert visible={alert.visible} message={alert.message} type={alert.type} heading={alert.heading} setVisible={(visible) => setAlert({ ...alert, visible })} />
            <div >
                <h2 className='col-12 text-center text-white'>Set Your Cardmath Password</h2>
                <label htmlFor="newPassword" className="block text-900 font-medium mb-2">New Password</label>
                <Password
                    id="newPassword"
                    value={newPassword}
                    onChange={(e) => handlePasswordChange(e.target.value)}
                    className="w-full mb-3"
                    footer={
                        <div>
                            <p>Password must be at least 8 characters long and contain uppercase, lowercase, a digit, and a special character.</p>
                        </div>
                    }
                />
                <Button label="Reset Password" icon="pi pi-check" className="w-full" onClick={handleResetPassword} />
            </div>
        </div>
    );
};

export default ResetPassword;
