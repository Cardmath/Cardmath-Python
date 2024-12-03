import React from 'react';
import { Button } from 'primereact/button';
import IsometricCreditCard from './IsometricCreditCard';

const CreditCardDBCallToAction = () => {
    return (
        <div className="bg-gray-900 flex flex-column md:flex-row align-items-center p-6">
            <div className="ml-4 mb-4 lg:col-6 sm:col-12">
                <div className="font-bold text-3xl md:text-6xl mb-2 text-center lg:text-left">
                    <div className="text-blue-300">Transparent</div>
                    <div className="text-white">Database of Credit Cards</div>
                </div>
                <div className="text-gray-300 text-xl mb-4 px-4 md:px-0">
                    We maintain a completely transparent database of Credit Cards that is easily accessible!
                </div>
                <Button
                    onClick={() => window.location.href = "https://cardmath.ai/creditcards"}
                    className="px-5 py-3 font-bold mb-3"
                    label="Explore the Database"
                    size='large'
                />
            </div>
            <div className="lg:col-5 sm:col-12">
                <IsometricCreditCard />
            </div>            
        </div>
    );
};

export default CreditCardDBCallToAction;
