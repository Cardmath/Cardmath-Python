import React, { useRef, useState, useEffect } from 'react';
import { StyleClass } from 'primereact/styleclass';
import { Ripple } from 'primereact/ripple';
import { Button } from 'primereact/button';
import "./Navbar.css";
import { fetchWithAuth } from '../pages/AuthPage';

const Navbar = () => {
    const rootBtnRef6 = useRef(null);
    const btnRef10 = useRef(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        // Check if user is authenticated
        fetchWithAuth('https://backend-dot-cardmath-llc.uc.r.appspot.com/api/is_user_logged_in', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else if (response.status === 401) {
                console.warn('User is not authenticated');
                setIsAuthenticated(false);
                return null;
            } else {
                console.error('Error checking authentication status');
                setIsAuthenticated(false);
                return null;
            }
        })
        .then(data => {
            if (data && data.detail === "cardmath_user_authenticated") {
                setIsAuthenticated(true);
                console.log('User is authenticated');
            }
        })
        .catch(err => {
            console.error('Network related Fetch error', err);
            setIsAuthenticated(false);
        });
    }, []);

    // Logout functionality
    const handleLogout = () => {
        localStorage.removeItem('cardmath_access_token'); // Remove token
        setIsAuthenticated(false); // Update state to reflect logged-out status
    };

    return (
        <div className="navbar-container bg-gray-900 py-3 px-4 shadow-2 flex align-items-center justify-content-between relative">
            <div className="flex align-items-center cursor-pointer" onClick={() => window.location.href="https://cardmath.ai"}>
                <img src="logos/svg/Color logo - no background.svg" alt="Image" height="50"/>
            </div>
            <StyleClass nodeRef={rootBtnRef6} selector="@next" enterClassName="hidden" leaveToClassName="hidden" hideOnOutsideClick>
                <a ref={rootBtnRef6} className="p-ripple cursor-pointer block lg:hidden text-gray-400">
                    <i className="pi pi-bars text-4xl"></i>
                    <Ripple />
                </a>
            </StyleClass>
            <div className="align-items-center flex-grow-1 justify-content-between hidden lg:flex absolute lg:static w-full bg-gray-900 left-0 top-100 px-6 lg:px-0 shadow-2 lg:shadow-none">
                <section></section>
                <ul className="list-none p-0 m-0 flex lg:align-items-center text-gray-400 select-none flex-column lg:flex-row">
                    <li>
                        <StyleClass nodeRef={btnRef10} selector="@next" enterClassName="hidden" enterActiveClassName="scalein" leaveToClassName="hidden" leaveActiveClassName="fadeout" hideOnOutsideClick>
                            <a ref={btnRef10} className="p-ripple flex px-0 lg:px-5 py-3 align-items-center hover:text-blue-600 font-medium transition-colors transition-duration-150 cursor-pointer" >
                                <span>Credit Cards</span>
                                <i className="pi pi-chevron-down ml-auto lg:ml-3"></i>
                                <Ripple />
                            </a>
                        </StyleClass>
                        <div className="lg:absolute bg-gray-800 hidden origin-top left-0 top-100 w-full">
                            <div className="flex flex-wrap p-6">
                                <div className="w-full lg:w-6 mb-4 lg:mb-0">
                                    <span className="block font-normal text-2xl mb-4 text-white">Credit Cards</span>
                                    <p className="line-height-3 m-0 text-gray-400">We maintain a completely transparent database of credit cards. Submit feedback and corrections for anything you see!</p>
                                </div>
                                <div className="w-full lg:w-6">
                                    <div className="flex flex-wrap border-bottom-1 border-gray-700 pb-3 mb-3">
                                        <div className="px-0 lg:px-3 py-3 cursor-pointer hover:bg-gray-700 transition-duration-150" onClick={() => {window.location.href="https://cardmath.ai/creditcards"}}>
                                            <span className="text-white">All</span>
                                            <p className="text-sm text-gray-400 mt-2 mb-0 line-height-3">Every single credit card we could find.</p>
                                        </div>
                                        <div className="px-0 lg:px-3 py-3 hover:bg-gray-700 transition-duration-150">
                                            <span className="text-white">Travel</span>
                                            <p className="text-sm text-gray-400 mt-2 mb-0 line-height-3">Best credit cards for travel points</p>
                                        </div>
                                        <div className="px-0 lg:px-3 py-3 hover:bg-gray-700 transition-duration-150">
                                            <span className="text-white">Student</span>
                                            <p className="text-sm text-gray-400 mt-2 mb-0 line-height-3">Best credit cards for college students</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li>
                        <a className="p-ripple flex px-0 lg:px-5 py-3 hover:text-blue-600 font-medium transition-colors transition-duration-150 cursor-pointer">
                            <span>Blog</span>
                            <Ripple />
                        </a>
                    </li>
                    <li>
                        <a className="p-ripple flex px-0 lg:px-5 py-3 hover:text-blue-600 font-medium transition-colors transition-duration-150 cursor-pointer">
                            <span>Legal</span>
                            <Ripple />
                        </a>
                    </li>
                    <li onClick={()=>window.location.href ='https://cardmath.ai/team'}>
                        <a className="p-ripple flex px-0 lg:px-5 py-3 hover:text-blue-600 font-medium transition-colors transition-duration-150 cursor-pointer">
                            <span>Our Team </span>
                            <Ripple />
                        </a>
                    </li>
                    <li onClick={()=>window.location.href ='https://cardmath.ai/contact-us'}>
                        <a className="p-ripple flex px-0 lg:px-5 py-3 hover:text-blue-600 font-medium transition-colors transition-duration-150 cursor-pointer">
                            <span>Contact Us</span>
                            <Ripple />
                        </a>
                    </li>
                </ul>
                <div className="flex justify-content-between lg:block border-top-1 lg:border-top-none border-gray-800 py-3 lg:py-0 mt-3 lg:mt-0">
                    {isAuthenticated ? (
                        <>
                            <Button label="To Dashboard" className="hover:bg-green-400 p-button-text text-white font-bold" onClick={() => window.location.href ='https://cardmath.ai/dashboard'} />
                            <Button label="Log out" className="ml-3 font-bold" onClick={handleLogout} />
                        </>
                    ) : (
                        <>
                            <Button label="Login" className="hover:bg-green-400 p-button-text text-white font-bold" onClick={() => window.location.href ='https://cardmath.ai/login'} />
                            <Button label="Register" className="ml-3 font-bold" onClick={() => window.location.href ='https://cardmath.ai/register'} />
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Navbar;