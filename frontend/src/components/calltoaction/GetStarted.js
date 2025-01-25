import React from 'react';
import CreditCard from './CreditCard';

const GetStartedCallToAction = () => {
    return (
        <div className='w-full my-8 grid row-gap-8 bg-gray-900 '>
                <div className="flex xl:col-6 sm:col-12" style={{ marginLeft: window.innerWidth < 768 ? "1.5rem" : "0rem" }}>                    
                    <CreditCard />
                </div>
                <div className="xl:col-6 sm:col-12 font-bold text-3xl md:text-6xl text-center" style={{ marginLeft: window.innerWidth < 768 ? "1rem" : "0rem" }}>
                    <div className="text-green-300">Personalized</div>
                    <div className="text-white">Recommendations based on your spending habits   </div>
                </div>
        </div>
    );
};

export default GetStartedCallToAction;
