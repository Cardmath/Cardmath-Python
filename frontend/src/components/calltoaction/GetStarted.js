import React from 'react';
import { Button } from 'primereact/button';

const GetStartedCallToAction = () => {
    return (
        <div className="bg-gray-900 p-8 flex justify-content-center md:justify-content-end bg-no-repeat bg-cover md:bg-contain" style={{ backgroundImage: 'url("/cta-2.png")' }}>
            <div className="px-5">
                <div className="text-white font-bold text-6xl">Ready to find</div>
                <div className="text-green-300 font-bold text-6xl">your next Credit Card?</div>
                <div className="mt-3 mb-5 text-gray-200 font-medium line-height-3">Connect a bank account for free to earn more with what you spend.</div>
                <Button label="Get Started" className="bg-green-300 text-gray-900 font-bold px-5 py-3" />
            </div>
        </div> 
    );
};

export default GetStartedCallToAction;