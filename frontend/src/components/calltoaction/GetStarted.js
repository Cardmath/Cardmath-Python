import React from 'react';
import { Button } from 'primereact/button';
import FadingImage from '../FadingImage';
import CreditCard from './CreditCard';

const GetStartedCallToAction = () => {
    return (
        <div className="w-full bg-gray-900 pb-2 pt-6 md:pb-2 flex flex-column md:flex-row align-items-center">
            {/* Image above text on small screens, to the left on large screens */}
            <div className="flex justify-content-center w-full md:w-6 md:mb-0">
                <CreditCard />
            </div>

            {/* Text content on the right side for large screens, below the image on small screens */}
            <div className="text-center text-xl lg:text-left md:text-left lg:ml-8 w-full md:w-6 p-4 md:p-0">
                <div className="text-white font-bold text-3xl md:text-6xl">
                    Ready to find
                </div>
                <div className="text-green-300 font-bold text-3xl md:text-6xl mb-4 md:mb-6">
                    your next Credit Card?
                </div>
                <div className="text-gray-200 font-medium mb-4 md:mb-6">
                    Connect a bank account for free to earn more with what you spend.
                </div>
                <Button size="large" label="Get Started" className="bg-green-300 text-gray-900 font-bold px-5 py-3" />
            </div>
        </div>
    );
};

export default GetStartedCallToAction;
