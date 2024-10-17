import React from 'react';
import { Button } from 'primereact/button';

const CreditCardDBCallToAction = () => {
    return (
        <div className="bg-gray-900 px-4 py-8 md:px-6 lg:px-8">
            <div className="flex justify-content-between align-items-center flex-wrap lg:flex-nowrap">
                <div className="pr-0 lg:pr-6 mb-5 lg:mb-0">
                    <div className="font-bold text-6xl font-bold mb-3">
                        <div className='text-blue-300'> 
                            Transparent
                        </div>
                        <div className='text-white'>
                            Database of Credit Cards
                        </div>
                    </div>
                    <div className="text-gray-300 line-height-3 mb-4">We maintain a complete database of Credit Cards, and we pay you if you upload your Credit Card agreements!</div>
                    <div className="flex flex-wrap lg:flex-nowrap">
                        <Button className="px-5 py-3 font-bold mr-3 white-space-nowrap mb-3 lg:mb-0 w-full lg:w-auto" label="Explore the Database" />
                        <Button className="px-5 py-3 font-bold mr-3 p-button-text white-space-nowrap w-full lg:w-auto" label="Our Information Vetting Process" />
                    </div>
                </div>
                <img src="/cta-2.png" alt="Image" className="block mx-auto lg:mx-0" />
            </div>
        </div>
    );
};

export default CreditCardDBCallToAction;