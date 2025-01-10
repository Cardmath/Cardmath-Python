import React from 'react';
import CreditCard from './CreditCard';

const GetStartedCallToAction = () => {
    return (
        <div className='w-full my-8 grid bg-gray-900'>
                <div className="flex col-6">
                    <CreditCard />
                </div>
                <div className="col-6 font-bold text-3xl md:text-6xl mb-2 text-center">
                    <div className="text-green-300">Personalized</div>
                    <div className="text-white">Recommendations based on your spending habits   </div>
                </div>
        </div>
    );
};

export default GetStartedCallToAction;
