import './AuthPage.css';  // Optional: for custom styles
import 'primeicons/primeicons.css';                        // Icons
import 'primereact/resources/primereact.min.css';          // Core CSS
import 'primereact/resources/themes/saga-blue/theme.css';  // Theme
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { Password } from 'primereact/password';
import React, { useState } from 'react';
import Alert from '../components/Alert';
import TermsOfUseDialog from '../components/TermsOfUseDialog';
import { useNavigate } from 'react-router-dom';
import { getBackendUrl } from '../utils/urlResolver';

const AuthPage = ({ userHasAccount }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState(''); // New state variable
    const [passwordValid, setPasswordValid] = useState(false);
    const [usernameValid, setUsernameValid] = useState(false);
    const [alert, setAlert] = useState({ visible: false, message: '', heading: '', type: 'error' });
    const [forgotPasswordMode, setForgotPasswordMode] = useState(false);
    const [showTermsDialog, setShowTermsDialog] = useState(false); // For Terms dialog visibility
    const navigate = useNavigate();
    

    const authEndpoint = userHasAccount 
        ? `${getBackendUrl()}/token` 
        : `${getBackendUrl()}/register`;
    const passwordRecoveryEndpoint = `${getBackendUrl()}/password-recovery-email`;

    const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&,.])[A-Za-z\d@$!%*?&,.]{8,}$/;
    const isEmailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const handlePasswordChange = (newPassword) => {
        setPassword(newPassword);
        setPasswordValid(strongPasswordRegex.test(newPassword));
    };

    const handleConfirmPasswordChange = (newPassword) => {
        setConfirmPassword(newPassword);
    };

    const handleUsernameChange = (newUsername) => {
        setUsername(newUsername);
        setUsernameValid(isEmailRegex.test(newUsername));
    };

    const handleAuth = () => {
        if (!userHasAccount && !passwordValid) {
            setAlert({ visible: true, 
                message: 'Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, one digit, and one special character (@$!%*?&).',
                type: 'error',
                heading: 'Invalid Password'});
            return;
        }

        if (!usernameValid) {
            setAlert({ visible: true, 
                message: "Please enter a valid email address. Make sure it includes an '@' and a valid domain (e.g., example@domain.com).",
                type: 'error',
                heading: 'Invalid Email'});
            return;
        }

        if (!userHasAccount) {
            // Check if passwords match
            if (password !== confirmPassword) {
                setAlert({
                    visible: true,
                    message: 'Passwords do not match. Please make sure both passwords are identical.',
                    type: 'error',
                    heading: 'Password Mismatch',
                });
                return;
            }
            setShowTermsDialog(true);
            return;
        }

        performAuth();
    };

    const performAuth = () => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        fetch(authEndpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                handleAuthError(response);
                throw new Error('Network response was not ok.');
            }
        }).then(data => {
            localStorage.setItem('cardmath_access_token', data.access_token);
            if (!userHasAccount) {
                navigate('/registration-steps');
            } else {
                navigate('/dashboard');
            }
        }).catch(error => {
            console.error('There was an error!', error);
        });
    };

    const handleAuthError = (response) => {
        if (response.status === 401) {
            const message = userHasAccount 
                ? 'Incorrect email or password: Please check your email and password and try again.'
                : 'Email already in use: An account is already associated with this email address. Please log in or use a different email.';
            setAlert({ visible: true, message, type: 'error', heading: 'Authentication Error' });
        }
    };
    
    const handlePasswordResetRequest = () => {
        if (!usernameValid) {
            setAlert({
                visible: true,
                message: "Please enter a valid email address.",
                type: 'error',
                heading: 'Invalid Email'
            });
            return;
        }
    
        fetch(passwordRecoveryEndpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: username })        
        }).then(response => {
            if (response.ok) {
                setAlert({
                    visible: true,
                    message: 'Password reset link sent. Check your email.',
                    type: 'success',
                    heading: 'Email Sent'
                });
                setForgotPasswordMode(false);
            } else {
                setAlert({
                    visible: true,
                    message: 'Unable to send password reset email. Try again later.',
                    type: 'error',
                    heading: 'Error'
                });
            }
        }).catch(error => {
            setAlert({
                visible: true,
                message: 'There was an error with the request.',
                type: 'error',
                heading: 'Request Error'
            });
        });
    };    

    const register_footer = (
        <div className='pt-2'>
            <b>Pick a Strong Password</b>
            <ul>
                <li>Password must be at least 8 characters long</li>
                <li>Include at least one uppercase letter</li>
                <li>Include at least one lowercase letter</li>
                <li>Include at least one digit</li>
                <li>Include at least one special character (@$!%*?&)</li>
            </ul>
        </div>
    );

    return (
        <div
            className="h-screen w-screen overflow-hidden flex flex-column align-items-center justify-content-center"
            style={{
                background: `linear-gradient(
                    135deg,
                    hsl(157deg 99% 48%) 0%,
                    hsl(159deg 100% 48%) 4%,
                    hsl(161deg 100% 47%) 8%,
                    hsl(162deg 100% 47%) 13%,
                    hsl(164deg 100% 46%) 17%,
                    hsl(166deg 100% 46%) 21%,
                    hsl(167deg 100% 45%) 25%,
                    hsl(169deg 100% 44%) 29%,
                    hsl(170deg 100% 44%) 33%,
                    hsl(172deg 100% 43%) 37%,
                    hsl(173deg 100% 43%) 42%,
                    hsl(175deg 100% 42%) 46%,
                    hsl(176deg 100% 41%) 50%,
                    hsl(178deg 100% 41%) 54%,
                    hsl(181deg 100% 41%) 58%,
                    hsl(184deg 100% 42%) 63%,
                    hsl(186deg 100% 44%) 67%,
                    hsl(188deg 100% 45%) 71%,
                    hsl(190deg 100% 46%) 75%,
                    hsl(192deg 100% 47%) 79%,
                    hsl(194deg 100% 47%) 83%,
                    hsl(196deg 100% 48%) 87%,
                    hsl(197deg 100% 48%) 92%,
                    hsl(198deg 100% 48%) 96%,
                    hsl(200deg 100% 48%) 100%
                )`,
                animation: 'bg-pan-diagonal-reverse 8s ease-in-out infinite',
                backgroundSize: '200% 200%',
                position: 'relative',
                zIndex: 0,
            }}
        >
            <style>
                {`
                /* Diagonal animation from bottom-right to top-left */
                @keyframes bg-pan-diagonal-reverse {
                    0% { background-position: 100% 100%; }
                    50% { background-position: 0% 0%; }
                    100% { background-position: 100% 100%; }
                }

                /* Text animation for Cardmath */
                @keyframes tracking-in-expand {
                    0% { letter-spacing: -0.5em; opacity: 0; }
                    40% { opacity: 0.6; }
                    100% { letter-spacing: normal; opacity: 1; }
                }
                `}
            </style>
            <div
                style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: `
                        radial-gradient(circle at top right, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0) 50%),
                        radial-gradient(circle at bottom left, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0) 50%)
                    `,
                    zIndex: -1,
                }} />
            <div style={{zIndex: 2}}>
            <Alert className ='py-8' visible={alert.visible} message={alert.message} type={alert.type} heading={alert.heading} setVisible={(visible) => setAlert({ ...alert, visible })}/>
            <div className="grid px-6 mt-5">
                    <div className="col p-4 lg:p-7" style={{ backgroundColor: 'rgba(255,255,255,.7)' }}>
                    <img src="logos/svg/Black logo - no background.svg" alt="Cardmath Logo" height="50" className="mb-6" />
                        <div className="text-xl text-black-alpha-90 font-medium mb-3">Welcome to Cardmath</div>
                        <p className="text-black-alpha-50 line-height-3 mt-0 mb-6">
                            Choose your credit card more intelligently by matching it to your spending habits and lifestyle needs.
                        </p>
                        <ul className="list-none p-0 m-0">
                            <li className="flex align-items-start mb-4">
                                <div>
                                    <span className="flex align-items-center justify-content-center bg-green-500 shadow-2" style={{ width: '38px', height: '38px', borderRadius: '10px' }}>
                                        <i className="text-xl text-white pi pi-credit-card"></i>
                                    </span>
                                </div>
                                <div className="ml-3">
                                    <span className="font-medium text-black-alpha-90">Pick the Right Card</span>
                                    <p className="mt-2 mb-0 text-black-alpha-50 line-height-3">Cardmath analyzes your spending patterns to help you pick the right credit card, ensuring you get the best rewards and benefits tailored to your lifestyle.</p>
                                </div>
                            </li>
                            <li className="flex align-items-start mb-4">
                                <div>
                                    <span className="flex align-items-center justify-content-center bg-green-500 shadow-2" style={{ width: '38px', height: '38px', borderRadius: '10px' }}>
                                        <i className="text-xl text-white pi pi-calculator"></i>
                                    </span>
                                </div>
                                <div className="ml-3">
                                    <span className="font-medium text-black-alpha-90">Track Your Spending</span>
                                    <p className="mt-2 mb-0 text-black-alpha-50 line-height-3">Track your spending and rewards to avoid fees and make the most of your cards.</p>
                                </div>
                            </li>
                            <li className="flex align-items-start">
                                <div>
                                    <span className="flex align-items-center justify-content-center bg-green-500 shadow-2" style={{ width: '38px', height: '38px', borderRadius: '10px' }}>
                                        <i className="text-xl text-white pi pi-shield"></i>
                                    </span>
                                </div>
                                <div className="ml-3">
                                    <span className="font-medium text-black-alpha-90">Premium Security</span>
                                    <p className="mt-2 mb-0 text-black-alpha-50 line-height-3">Cardmath prioritizes your security with robust encryption and never sells or shares your data, ensuring your financial information stays private and protected.</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <div className="col lg:p-7 bg-gray-200">
                        <div className="text-900 text-2xl font-medium mb-6">
                            {forgotPasswordMode ? "Reset Password" : (userHasAccount ? "Login" : "Register")}
                        </div>
    
                        <label htmlFor="email" className="block text-900 font-medium mb-2">Email</label>
                        <InputText
                            tabIndex={0}
                            value={username}
                            id="email"
                            type="text"
                            placeholder="Email address"
                            className="w-full mb-4"
                            onChange={(e) => handleUsernameChange(e.target.value)}
                        />
    
                        {!forgotPasswordMode && (
                            <>
                                <label htmlFor="password" className="block text-900 font-medium mb-2">Password</label>
                                <Password
                                    footer={userHasAccount ? null : register_footer}
                                    tabIndex={0}
                                    value={password}
                                    feedback={!userHasAccount}
                                    id="password"
                                    type="text"
                                    placeholder="Password"
                                    className="w-full mb-4"
                                    onChange={(e) => handlePasswordChange(e.target.value)}
                                    toggleMask
                                />
    
                                {/* Confirm Password Field for Registration */}
                                {!userHasAccount && (
                                    <>
                                        <label htmlFor="confirmPassword" className="block text-900 font-medium mb-2">Confirm Password</label>
                                        <Password
                                            tabIndex={0}
                                            value={confirmPassword}
                                            feedback={false}
                                            id="confirmPassword"
                                            type="text"
                                            placeholder="Confirm Password"
                                            className="w-full mb-4"
                                            onChange={(e) => handleConfirmPasswordChange(e.target.value)}
                                            toggleMask
                                        />
                                    </>
                                )}
    
                                <div className="pb-6">
                                    {userHasAccount && (
                                        <a onClick={() => setForgotPasswordMode(true)} className="font-medium no-underline ml-2 text-blue-500 text-right cursor-pointer">
                                            Forgot password?
                                        </a>
                                    )}
                                </div>
    
                                <Button label={userHasAccount ? "Login" : "Register"} icon="pi pi-user" className="bg-blue-500 text-white w-full" onClick={handleAuth}/>
                                
                                {/* Terms of Use dialog */}
                                {showTermsDialog && (
                                    <TermsOfUseDialog
                                        pdfUrl="/Cardmath, LLC - Terms of Use.docx.pdf"
                                        onConfirm={() => {
                                            setShowTermsDialog(false);
                                            performAuth();  // Proceed with authentication after terms are accepted
                                        }}
                                    />
                                )}
                            </>
                        )}
    
                        {forgotPasswordMode && (
                            <Button label="Send Reset Link" icon="pi pi-envelope" className="bg-blue-500 text-white w-full" onClick={handlePasswordResetRequest}/>
                        )}
    
                        {!forgotPasswordMode && (
                            <div className="mt-6 text-center text-600">
                                {userHasAccount ? (
                                    <>Don't have an account? <a href="/register" tabIndex="0" className="font-medium text-blue-500">Sign up</a></>
                                ) : (
                                    <>Already have an account? <a href="/login" tabIndex="0" className="font-medium text-blue-500">Login</a></>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

const getAuthHeaders = () => {
    const token = localStorage.getItem('cardmath_access_token');
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