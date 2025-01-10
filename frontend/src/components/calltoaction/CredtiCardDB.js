import React from 'react';
import { Button } from 'primereact/button';
import IsometricCreditCard from './IsometricCreditCard';

const CreditCardDBCallToAction = () => {
    return (
        <div className="w-full my-8 bg-gray-900 mt-6">
            <div className="grid">
                <div className="col-12 font-bold text-3xl md:text-6xl mb-2 text-center ">
                    <div className="text-blue-300">Comprehensive</div>
                    <div className="text-white">Database of Credit Cards</div>
                </div>
                <div className="col-12 text-gray-300 text-xl text-center lg:text-left mb-4 sm:px-0 lg:px-4 md:px-0 text-2xl lg:line-height-4 ">
                    We maintain a completely transparent database of Credit Cards that is easily accessible!
                </div>
                <Button
                    onClick={() => window.location.href = "https://cardmath.ai/creditcards"}
                    className="mb-3 text-2xl"
                    label="Explore the Database"
                    style={{marginLeft: 'auto', marginRight: 'auto'}}
                    size='large'
                />
                <div className="col-12" style={{marginLeft: 'auto', marginRight: 'auto'}}>
                    <IsometricCreditCard />
                </div>          
            </div> 
              
        </div>
    );
};

export default CreditCardDBCallToAction;
