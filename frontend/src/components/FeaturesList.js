import React, { useState } from 'react';

const FeaturesList = ({ features }) => {
    const [activeSection, setActiveSection] = useState('exhaustive');

    return (
        <div className="bg-gray-900 mt-8">
            <div className="grid">
                <div className="col-6">
                    <div className="pr-6">
                        <div className="text-blue-500 font-bold text-5xl mb-5">Sophisticated Algorithm</div>

                        <div 
                            className="mb-5"
                            style={{ 
                                borderLeft: activeSection === 'exhaustive' ? '4px solid #3B82F6' : '4px solid transparent',
                                paddingLeft: '1rem',
                                transition: 'border-color 0.3s ease'
                            }}
                            onMouseEnter={() => setActiveSection('exhaustive')}
                        >
                            <span className="text-white font-bold text-2xl">Exhaustive</span>
                            <div className="text-gray-400 line-height-3 text-xl mt-3">
                                There are roughly <span className='font-bold'> 42,000,000,000</span> ways to pick four credit cards. 
                                Our algorithm efficiently analyzes the value of everyone one of these combinations based on your 
                                purchase history and preferences.
                            </div>
                        </div>

                        <div 
                            className="mb-5"
                            style={{ 
                                borderLeft: activeSection === 'realtime' ? '4px solid #3B82F6' : '4px solid transparent',
                                paddingLeft: '1rem',
                                transition: 'border-color 0.3s ease'
                            }}
                            onMouseEnter={() => setActiveSection('realtime')}
                        >
                            <span className="text-white font-bold text-2xl">Real-time Recommendations</span>
                            <div className="text-gray-400 line-height-3 mt-3 text-xl">
                                Cardmath tracks your spending journey and notifies you when it's 
                                <span className='font-bold'> mathematically optimal</span> to get a new credit card or replace an existing one.
                            </div>
                        </div>

                        <div 
                            className="mb-5"
                            style={{ 
                                borderLeft: activeSection === 'know' ? '4px solid #3B82F6' : '4px solid transparent',
                                paddingLeft: '1rem',
                                transition: 'border-color 0.3s ease'
                            }}
                            onMouseEnter={() => setActiveSection('know')}
                        >
                            <span className="text-white font-bold text-2xl">Know Which Card to Use</span>
                            <div className="text-gray-400 line-height-3 mt-3 text-xl">
                                All of our recommendations come with a <span className="font-bold">spending strategy</span> that 
                                tells you which stores to use your cards at so you can realize your savings.
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-6" style={{ padding: '10px', borderRadius: '8px', height: '600px'}}>
                    {activeSection === 'exhaustive' && (
                        <img
                            src="exhaustive.jpg"
                            alt="Credit Cards"
                            style={{
                                maxWidth: '100%',
                                maxHeight: '100%',
                                height: 'auto',
                                width: 'auto',
                                zoom: '2',
                                borderRadius: '8px',
                                boxShadow: '0px 4px 15px rgba(0, 0, 0, 0.3)',
                                opacity: 0.6,
                                objectFit: 'contain',
                            }}
                        />
                    )}
                    {activeSection === 'realtime' && (
                        <img 
                            src="realtime.png" 
                            alt="iPhone notification" 
                            className="w-full h-full" 
                            style={{
                                borderRadius: '8px', 
                                opacity: 0.60,
                                objectFit: 'contain',
                                transform: 'scale(1.4)'
                            }} 
                        />
                    )}
                    {activeSection === 'know' && (
                        <img
                            src="know.jpg"
                            alt="Person paying"
                            style={{
                                maxWidth: '100%',
                                maxHeight: '100%',
                                height: 'auto',
                                width: 'auto',
                                borderRadius: '8px',
                                opacity: 0.6,
                                objectFit: 'contain',
                            }}
                        />
                    )}
                </div>
        </div>
    </div>
    );
};

export default FeaturesList;