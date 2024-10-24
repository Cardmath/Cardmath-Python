import React from 'react';

const Footer = () => {
    return (
        <div className="bg-gray-900 px-4 py-6 md:px-6 lg:px-8 text-center">
            <img src="logos/svg/Color logo - no background.svg" alt="Image" height="50" />
            <div className="font-medium text-900 text-white mt-4 mb-3">&copy; 2024 Cardmath, Inc</div>
            <p className="text-600 line-height-3 mt-0 mb-4">
            Disclaimer: All information provided on this site is for general informational purposes only and is not guaranteed to be accurate or complete. CardMath, Inc. makes no representations or warranties of any kind, express or implied, regarding the accuracy, reliability, or availability of the information. Users are encouraged to independently verify any information before relying on it. Use of the site is at your own risk.    
            </p>
            <div className="flex align-items-center justify-content-center">
                <a className="cursor-pointer text-700 mr-5">
                    <i className="pi pi-twitter"></i>
                </a>
                <a className="cursor-pointer text-700 mr-5">
                    <i className="pi pi-facebook"></i>
                </a>
                <a className="cursor-pointer text-700">
                    <i className="pi pi-github"></i>
                </a>
            </div>
        </div>
    );
};

export default Footer;