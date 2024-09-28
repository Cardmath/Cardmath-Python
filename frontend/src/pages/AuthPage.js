import './AuthPage.css';  // Optional: for custom styles
import 'primeicons/primeicons.css';                        // Icons
import 'primereact/resources/primereact.min.css';          // Core CSS
import 'primereact/resources/themes/saga-blue/theme.css';  // Theme
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { Password } from 'primereact/password';
import { Checkbox } from 'primereact/checkbox';
import { Divider } from 'primereact/divider';
import React, { useState } from 'react';
import Alert  from '../components/Alert';

const AuthPage = ({ userHasAccount }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [checked3, setChecked3] = useState(false);
    const [passwordValid, setPasswordValid] = useState(false);
    const [usernameValid , setUsernameValid] = useState(false);
    const [alert, setAlert] = useState({visible: false, message: '', heading : '', type: 'error'});

    var endpoint = userHasAccount ? 'http://localhost:8000/token' : 'http://localhost:8000/register';  

    const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&,.])[A-Za-z\d@$!%*?&,.]{8,}$/;
    const isEmailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    const handlePasswordChange = (newPassword) => {
        setPassword(newPassword);

        if (strongPasswordRegex.test(newPassword)) {
            setPasswordValid(true);
        } else {
            setPasswordValid(false);
        }
    };

    const handleUsernameChange = (newUsername) => {
        setUsername(newUsername);

        if (isEmailRegex.test(newUsername)) {
            setUsernameValid(true)
        } else {
            setUsernameValid(false)
        }
    }

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

    const handleAuth = () => {
        if (!userHasAccount && !passwordValid) {
            console.log('Password is invalid');
            setAlert({visible: true, 
                message: 'Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, one digit, and one special character (@$!%*?&).',
                type: 'error',
                heading: 'Invalid Password'});
            return;
        }

        if (!usernameValid) {
            console.log('Email is invalid');
            setAlert({visible: true, 
                message: "Please enter a valid email address. Make sure it includes an '@' and a valid domain (e.g., example@domain.com).",
                type: 'error',
                heading: 'Invalid Email'});
            return;
        }

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
            } else if (response.status == 401) {
                if (!userHasAccount) {
                    setAlert({visible: true, 
                        message: 'Email already in use: An account is already associated with this email address. Please log in or use a different email to create a new account.',
                        type: 'error',
                        heading: 'Email already in use'})
                } else {
                    setAlert({visible: true, 
                        message: 'Incorrect email or password: Please check your email and password and try again.',
                        type: 'error',
                        heading: 'Incorrect Credentials'})
                }
            }
            throw new Error('Network response was not ok.');
        }).then(data => {
            localStorage.setItem('cardmath_access_token', data.access_token);
            if (userHasAccount) {
                window.location.href = '/preferences';
            } else {
                window.location.href = '/connect';
            }
        }).catch(error => {
            console.error('There was an error!', error)
        });
    };

    return (
        <div> 
            <Alert visible={alert.visible} message={alert.message} type={alert.type} heading={alert.heading} setVisible={(visible) => setAlert({ ...alert, visible })}/>
            <div style={{ background: 'url("signin-2.jpg") no-repeat', backgroundSize: 'cover' }} className="px-4 py-8 md:px-6 lg:px-8">
                <div className="flex flex-wrap">
                    <div className="w-full lg:w-6 p-4 lg:p-7" style={{ backgroundColor: 'rgba(255,255,255,.7)' }}>
                        <img src="hero-2.jpg" alt="Image" height="50" className="mb-6" />
                        <div className="text-xl text-black-alpha-90 font-500 mb-3">Welcome to Cardmath</div>
                        <p className="text-black-alpha-50 line-height-3 mt-0 mb-6">Quis vel eros donec ac odio tempor orci dapibus. In hac habitasse platea dictumst quisque.</p>
                        <ul className="list-none p-0 m-0">
                            <li className="flex align-items-start mb-4">
                                <div>
                                    <span className="flex align-items-center justify-content-center bg-purple-400" style={{ width: '38px', height: '38px', borderRadius: '10px' }}>
                                        <i className="text-xl text-white pi pi-inbox"></i>
                                    </span>
                                </div>
                                <div className="ml-3">
                                    <span className="font-medium text-black-alpha-90">Pick the Right Card</span>
                                    <p className="mt-2 mb-0 text-black-alpha-50 line-height-3">Cardmath analyzes your spending patterns to help you pick the right credit card, ensuring you get the best rewards and benefits tailored to your lifestyle.</p>
                                </div>
                            </li>
                            <li className="flex align-items-start mb-4">
                                <div>
                                    <span className="flex align-items-center justify-content-center bg-purple-400" style={{ width: '38px', height: '38px', borderRadius: '10px' }}>
                                        <i className="text-xl text-white pi pi-globe"></i>
                                    </span>
                                </div>
                                <div className="ml-3">
                                    <span className="font-medium text-black-alpha-90">Cloud Backups Inbox</span>
                                    <p className="mt-2 mb-0 text-black-alpha-50 line-height-3">Egestas sed tempus urna et. Auctor elit sed vulputate mi sit amet mauris commodo.</p>
                                </div>
                            </li>
                            <li className="flex align-items-start">
                                <div>
                                    <span className="flex align-items-center justify-content-center bg-purple-400" style={{ width: '38px', height: '38px', borderRadius: '10px' }}>
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
                    <div className="w-full lg:w-6 p-4 lg:p-7 surface-card">
                        <div className="text-900 text-2xl font-medium mb-6">{userHasAccount ? "Login" : "Register"}</div>

                        <label htmlFor="email" className="block text-900 font-medium mb-2">Email</label>
                        <InputText tabIndex={0} value={username} id="email" type="text" placeholder="Email address" className="w-full mb-4" onChange={(e) => handleUsernameChange(e.target.value)}/>

                        <label htmlFor="password" className="block text-900 font-medium mb-2">Password</label>
                        <Password footer={register_footer} tabIndex={0} value={password} feedback={!userHasAccount} id="password" type="text" placeholder="Password" className="w-full mb-4" onChange={(e) => handlePasswordChange(e.target.value)} toggleMask/>

                        <div className="flex align-items-center justify-content-between mb-6">
                            <div className="flex align-items-center">
                                <Checkbox id="rememberme3" className="mr-2" checked={checked3} onChange={(e) => setChecked3(e.checked)} />
                                <label htmlFor="rememberme3">Remember me</label>
                            </div>
                            <a className="font-medium no-underline ml-2 text-blue-500 text-right cursor-pointer">Forgot password?</a>
                        </div>

                        <Button label={userHasAccount ? "Login" : "Register"} icon="pi pi-user" className="w-full" onClick={handleAuth}/>

                        <Divider align="center" className="my-6">
                            <span className="text-600 font-normal text-sm">OR</span>
                        </Divider>

                        <Button label="Sign In with Google" icon="pi pi-google" className="w-full p-button-secondary" onClick={handleAuth}/>

                        <div className="mt-6 text-center text-600">
                            Don't have an account? <a href="/register" tabIndex="0" className="font-medium text-blue-500">Sign up</a>
                        </div>
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