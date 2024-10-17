import React, { useRef } from 'react';
import { StyleClass } from 'primereact/styleclass';
import { Ripple } from 'primereact/ripple';
import { Button } from 'primereact/button'; // Import Button component
import "./Navbar.css";

const Navbar = () => {
    const rootBtnRef6 = useRef(null);
    const btnRef10 = useRef(null);


    return (    
        <div className="navbar-container bg-gray-900 py-3 px-4 shadow-2 flex align-items-center justify-content-between relative">
            <div className="flex align-items-center cursor-pointer" onClick={() => window.location.href="http://localhost:3000/"}>
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
                <ul className="list-none p-0 m-0 flex lg:align-items-zcenter text-gray-400 select-none flex-column lg:flex-row">
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
                                        <div className="px-0 lg:px-3 py-3 cursor-pointer" onClick={() => {window.location.href="http://localhost:3000/creditcards"}}>
                                            <span className="text-white">All</span>
                                            <p className="text-sm text-gray-400 mt-2 mb-0 line-height-3">Porta lorem mollis aliquam ut porttitor leo a diam.</p>
                                        </div>
                                        <div className="px-0 lg:px-3 py-3">
                                            <span className="text-white">Travel</span>
                                            <p className="text-sm text-gray-400 mt-2 mb-0 line-height-3">Amet purus gravida quis blandit.</p>
                                        </div>
                                        <div className="px-0 lg:px-3 py-3">
                                            <span className="text-white">Student</span>
                                            <p className="text-sm text-gray-400 mt-2 mb-0 line-height-3">Aenean vel elit scelerisque mauris.</p>
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
                    <li onClick={()=>window.location.href ='/team'}>
                        <a className="p-ripple flex px-0 lg:px-5 py-3 hover:text-blue-600 font-medium transition-colors transition-duration-150 cursor-pointer">
                            <span>Our Team </span>
                            <Ripple />
                        </a>
                    </li>
                    <li>
                        <a className="p-ripple flex px-0 lg:px-5 py-3 hover:text-blue-600 font-medium transition-colors transition-duration-150 cursor-pointer">
                            <span>Contact Us</span>
                            <Ripple />
                        </a>
                    </li>
                </ul>
                <div className="flex justify-content-between lg:block border-top-1 lg:border-top-none border-gray-800 py-3 lg:py-0 mt-3 lg:mt-0">
                    <Button label="Login" className="hover:bg-green-400 p-button-text text-white font-bold" onClick={()=>window.location.href ='/login'} />
                    <Button label="Register" className="ml-3 font-bold" onClick={()=>window.location.href ='/register'}/>
                </div>
            </div>
        </div>
    );
};

export default Navbar;