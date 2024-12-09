import React from 'react';
import CreditCard from './CreditCard';

const GetStartedCallToAction = () => {
    return (
        <div className='pt-6 pr-8 w-full bg-gray-900'>
            <div className="flex flex-column md:flex-row align-items-center">
                <div className="flex justify-content-center md:w-6 md:mb-0">
                    <CreditCard />
                </div>
                <div className="text-center text-xl lg:text-left md:text-left call-to-action-font lg:ml-8 md:w-6 p-4 md:p-0">
                    <div className="text-white font-bold text-3xl md:text-6xl">
                        Ready to find
                    </div>
                    <div className="text-green-300 font-bold text-3xl md:text-6xl mb-4 md:mb-6">
                        your next Credit Card?
                    </div>
                    <div className="text-gray-200 text-2xl font-medium mb-4 md:mb-6">
                        We compute the optimal set of credit cards for your spending habits, so that you can earn the most rewards. 
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GetStartedCallToAction;
