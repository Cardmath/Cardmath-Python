import './AuthPage.css';  // Optional: for custom styles
import 'primeicons/primeicons.css';                        // Icons
import 'primereact/resources/primereact.min.css';          // Core CSS
import 'primereact/resources/themes/saga-blue/theme.css';  // Theme
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { Password } from 'primereact/password';
import { Checkbox } from 'primereact/checkbox';
import React, { useState } from 'react';
import Alert from '../components/Alert';
import TermsOfUseDialog from '../components/TermsOfUseDialog';

const AuthPage = ({ userHasAccount }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [checked3, setChecked3] = useState(false);
    const [passwordValid, setPasswordValid] = useState(false);
    const [usernameValid, setUsernameValid] = useState(false);
    const [alert, setAlert] = useState({ visible: false, message: '', heading: '', type: 'error' });
    const [forgotPasswordMode, setForgotPasswordMode] = useState(false);
    const [showTermsDialog, setShowTermsDialog] = useState(false); // New state for Terms dialog visibility

    const authEndpoint = userHasAccount 
        ? 'https://backend-dot-cardmath-llc.uc.r.appspot.com/token' 
        : 'https://backend-dot-cardmath-llc.uc.r.appspot.com/register';
    const passwordRecoveryEndpoint = 'https://backend-dot-cardmath-llc.uc.r.appspot.com/password-recovery-email';

    const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&,.])[A-Za-z\d@$!%*?&,.]{8,}$/;
    const isEmailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const handlePasswordChange = (newPassword) => {
        setPassword(newPassword);
        setPasswordValid(strongPasswordRegex.test(newPassword));
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
                window.location.href = 'https://cardmath.ai/registration-steps';    
            } else {
                window.location.href = 'https://cardmath.ai/dashboard';
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
            <b>Pick a Strong password</b>
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
            style={{
                background: 'linear-gradient(120deg, hsl(146deg 96% 28%) 0%, hsl(147deg 95% 27%) 12%, hsl(148deg 95% 26%) 18%, hsl(149deg 95% 26%) 22%, hsl(150deg 96% 25%) 26%, hsl(151deg 96% 24%) 29%, hsl(152deg 97% 23%) 33%, hsl(153deg 94% 20%) 36%, hsl(154deg 92% 18%) 39%, hsl(156deg 91% 15%) 42%, hsl(159deg 91% 13%) 44%, hsl(163deg 92% 10%) 47%, hsl(169deg 95% 8%) 50%, hsl(171deg 95% 10%) 53%, hsl(172deg 95% 12%) 56%, hsl(173deg 95% 15%) 58%, hsl(173deg 96% 18%) 61%, hsl(174deg 96% 20%) 64%, hsl(174deg 97% 23%) 67%, hsl(174deg 96% 25%) 71%, hsl(174deg 96% 28%) 74%, hsl(174deg 96% 30%) 78%, hsl(174deg 96% 33%) 82%, hsl(174deg 96% 36%) 88%, hsl(174deg 96% 38%) 100%)',
                backgroundSize: 'cover',
                minHeight: '100vh',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center'
            }}
            className='flex flex-column'
        >
            <Alert visible={alert.visible} message={alert.message} type={alert.type} heading={alert.heading} setVisible={(visible) => setAlert({ ...alert, visible })}/>
            <div className="flex flex-wrap lg:flex-nowrap p-4">
                <div className="w-full lg:w-6 p-4 lg:p-7" style={{ backgroundColor: 'rgba(255,255,255,.7)' }}>
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
                <div className="w-full lg:w-6 p-4 lg:p-7 bg-gray-200">
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
                                footer={register_footer}
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

                            <div className="flex align-items-center justify-content-between mb-6">
                                <div className="flex align-items-center">
                                    <Checkbox id="rememberme3" className="mr-2" checked={checked3} onChange={(e) => setChecked3(e.checked)} />
                                    <label htmlFor="rememberme3">Remember me</label>
                                </div>
                                <a onClick={() => setForgotPasswordMode(true)} className="font-medium no-underline ml-2 text-blue-500 text-right cursor-pointer">
                                    Forgot password?
                                </a>
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
                            Don't have an account? <a href="/register" tabIndex="0" className="font-medium text-blue-500">Sign up</a>
                        </div>
                    )}
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