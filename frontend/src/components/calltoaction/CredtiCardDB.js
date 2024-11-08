import React from 'react';
import { Button } from 'primereact/button';
import FadingImage from '../FadingImage';

const CreditCardDBCallToAction = () => {
    return (
        <div className="bg-gray-900 pb-2 md:pl-8 md:pr-1 lg:pl-9 flex flex-column md:flex-row align-items-center">
            {/* Text content on the left side for large screens, below the image on small screens */}
            <div className="lg:ml-8 text-center md:text-left w-full md:w-6">
                <div className="font-bold text-3xl md:text-6xl mb-2">
                    <div className="text-blue-300">Transparent</div>
                    <div className="text-white">Database of Credit Cards</div>
                </div>
                <div className="text-gray-300 mb-4 px-4 md:px-0">
                    We maintain a complete database of Credit Cards, and we pay you if you upload your Credit Card agreements!
                </div>
                <div className="flex flex-column md:flex-row justify-content-center md:justify-content-start align-items-center">
                    <Button
                        onClick={() => window.location.href = "https://cardmath.ai/creditcards"}
                        className="px-5 py-3 font-bold mb-3 md:mb-0 mx-4"
                        label="Explore the Database"
                    />
                    <Button
                        className="px-5 py-3 font-bold p-button-text mx-4"
                        label="Our Information Vetting Process"
                    />
                </div>
            </div>

            {/* Image above text on small screens, to the right on large screens */}
            <div className="w-full md:w-6 mb-4 md:mb-0">
                <FadingImage src="/cta-2.jpeg" alt="Credit Card" className="w-full" />
            </div>

            
        </div>
    );
};

export default CreditCardDBCallToAction;
