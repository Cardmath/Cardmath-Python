import React from 'react';

const FeaturesList = ({ features }) => {
    return (
        <div className="bg-gray-900 px-4 lg:py-4 sm:py-1 md:py-1 md:px-6 lg:px-8">
            <div className="grid">
                <div className="col-12 md:col-6">
                    <div className="pr-0 md:pr-8">
                        <div className="text-blue-500 font-bold text-5xl mb-5">Unlike Other Sites</div>

                        <div className="mb-5 border-blue-500 pl-3" style={{ borderLeft: '4px solid' }}>
                            <span className="text-white font-bold text-2xl">Independent</span>
                            <div className="text-gray-400 line-height-3 text-xl mt-3"> We have no affiliations with credit card companies, ensuring our recommendations are entirely data-driven and unbiased, focused solely on your best interest.</div>
                        </div>

                        <div className="mb-5 border-blue-500 pl-3">
                            <span className="text-white font-bold text-2xl">Data Driven</span>
                            <div className="text-gray-400 line-height-3 mt-3 text-xl">Tired of reading endless articles and sharing your data? Simply sign into your bank accounts, and we'll handle the numbers for you, delivering personalized insights without the hassle.</div>
                        </div>

                        <div className="mb-5 border-blue-500 pl-3">
                            <span className="text-white font-bold text-2xl">Privacy is our Priority</span>
                            <div className="text-gray-400 line-height-3 mt-3 text-xl">We only retain the data necessary to provide you with personalized insights, and once it's used, it’s securely discarded. With multiple layers of encryption, your information is always protected and kept private.</div>
                        </div>
                    </div>
                </div>
                <div className="col-12 md:col-6 relative" style={{padding: '10px', borderRadius: '8px' }}>
                    <img 
                        src="credit-cards.jpg" 
                        alt="Credit Cards" 
                        className="w-full" 
                        style={{
                            borderRadius: '8px', 
                            boxShadow: '0px 4px 15px rgba(0, 0, 0, 0.3)', 
                            opacity: 0.60
                        }} 
                    />
                </div>
            </div>
        </div>
    );
};

export default FeaturesList;