import React from 'react';
import { Button } from 'primereact/button';
import IsometricCreditCard from './IsometricCreditCard';

const CreditCardDBCallToAction = () => {
    return (
        <div className="bg-gray-900 pb-2 h-28rem md:pl-8 md:pr-1 lg:pl-9 flex flex-column md:flex-row align-items-center">
            {/* Text content on the left side for large screens, below the image on small screens */}
            <div className="lg:ml-4 text-center md:text-left w-full md:w-6 lg:mr-4">
                <div className="font-bold text-3xl md:text-6xl mb-2">
                    <div className="text-blue-300">Transparent</div>
                    <div className="text-white">Database of Credit Cards</div>
                </div>
                <div className="text-gray-300 text-xl mb-4 px-4 md:px-0">
                    We maintain a completely transparent database of Credit Cards that is easily accessible!
                </div>
                <div className="flex flex-column md:flex-row justify-content-center md:justify-content-start align-items-center">
                    <Button
                        onClick={() => window.location.href = "https://cardmath.ai/creditcards"}
                        className="px-5 py-3 font-bold mb-3"
                        label="Explore the Database"
                        size='large'
                    />
                </div>
            </div>

            {/* Image above text on small screens, to the right on large screens */}
            <div className="max-h-15rem md:w-6 mb-4 md:mb-0 border-round shadow-5 pr-3" >
                <IsometricCreditCard />
            </div>

            
        </div>
    );
};

export default CreditCardDBCallToAction;
