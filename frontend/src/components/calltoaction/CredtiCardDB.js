import React from 'react';
import { Button } from 'primereact/button';
import FadingImage from '../FadingImage';


const CreditCardDBCallToAction = () => {
    return (
        <div className="bg-gray-900 pt-2 md:pl-8 md:pr-1 lg:pl-9">
            <div className="flex justify-content-between align-items-center flex-wrap lg:flex-nowrap">
                <div className=" md:mb-5 lg:mb-0 lg:pl-6">
                    <div className="font-bold text-6xl font-bold mb-3">
                        <div className='text-blue-300'> 
                            Transparent
                        </div>
                        <div className='text-white'>
                            Database of Credit Cards
                        </div>
                    </div>
                    <div className="text-gray-300 line-height-3 mb-4 w-7">We maintain a complete database of Credit Cards, and we pay you if you upload your Credit Card agreements!</div>
                    <div className="flex flex-wrap lg:flex-nowrap">
                        <Button onClick={() => window.location.href="http://localhost:3000/creditcards" } className="px-5 py-3 font-bold mr-3 white-space-nowrap mb-3 lg:mb-0 w-full" label="Explore the Database" />
                        <Button className="px-5 py-3 font-bold md:mr-3 p-button-text white-space-nowrap w-full" label="Our Information Vetting Process" />
                    </div>
                </div>
                <FadingImage src="/cta-2.jpeg" alt="Image" className="block" />
            </div>
        </div>
    );
};

export default CreditCardDBCallToAction;