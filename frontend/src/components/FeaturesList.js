import React, { useState, useEffect } from 'react';

const FeaturesList = ({ features }) => {
    const [activeSection, setActiveSection] = useState('exhaustive');
    const [isMobile, setIsMobile] = useState(false);

    useEffect(() => {
        const checkMobile = () => setIsMobile(window.innerWidth < 768);
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    const sections = [
        {
            id: 'exhaustive',
            title: 'Exhaustive',
            description: 'There are roughly 42,000,000,000 ways to pick four credit cards. Our algorithm efficiently analyzes the value of everyone one of these combinations based on your purchase history and preferences.',
            image: 'exhaustive.jpg',
            imageProps: {
                opacity: 0.6,
                scale: 2
            }
        },
        {
            id: 'realtime',
            title: 'Real-time Recommendations',
            description: 'Cardmath tracks your spending journey and notifies you when it\'s mathematically optimal to get a new credit card or replace an existing one.',
            image: 'realtime.png',
            imageProps: {
                opacity: 0.6,
                scale: 1.4
            }
        },
        {
            id: 'know',
            title: 'Know Which Card to Use',
            description: 'All of our recommendations come with a spending strategy that tells you which stores to use your cards at so you can realize your savings.',
            image: 'know.jpg',
            imageProps: {
                opacity: 0.6
            }
        }
    ];

    const containerStyle = {
        display: 'grid',
        gridTemplateColumns: isMobile ? '1fr' : '1fr 1fr',
        gap: '1.5rem'
    };

    return (
        <div className="bg-gray-900 mt-8">
            <div style={containerStyle}>
                <div className={`${isMobile ? 'px-4' : 'pr-6'}`}>
                    <h2 className={`text-blue-500 font-bold ${isMobile ? 'text-3xl' : 'text-5xl'} mb-5`}>
                        Sophisticated Algorithm
                    </h2>

                    <div className="space-y-8">
                        {sections.map(section => (
                            <div
                                key={section.id}
                                className={`cursor-pointer transition-all duration-300 ${isMobile ? 'mb-8' : ''}`}
                                style={{
                                    borderLeft: activeSection === section.id ? '4px solid #3B82F6' : '4px solid transparent',
                                    paddingLeft: '1rem'
                                }}
                                onClick={() => setActiveSection(section.id)}
                                onTouchStart={() => setActiveSection(section.id)}
                                onMouseEnter={() => !isMobile && setActiveSection(section.id)}
                            >
                                <h3 className={`text-white font-bold ${isMobile ? 'text-xl' : 'text-2xl'}`}>
                                    {section.title}
                                </h3>
                                <p className={`text-gray-400 line-height-3 mt-3 ${isMobile ? 'text-lg' : 'text-xl'}`}>
                                    {section.description}
                                </p>
                                
                                {isMobile && activeSection === section.id && (
                                    <div className="mt-4 overflow-hidden h-[400px] flex items-center justify-center">
                                        <img
                                            src={section.image}
                                            alt={section.title}
                                            className="rounded-lg"
                                            style={{
                                                opacity: section.imageProps.opacity,
                                                transform: section.imageProps.scale ? `scale(${section.imageProps.scale})` : 'none',
                                                height: '100%',
                                                width: 'auto',
                                                maxHeight: '400px'
                                            }}
                                        />
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {!isMobile && (
                    <div className="h-[600px] p-3 rounded-lg overflow-hidden flex items-center justify-center">
                        {sections.map(section => (
                            activeSection === section.id && (
                                <img
                                    key={section.id}
                                    src={section.image}
                                    alt={section.title}
                                    className="rounded-lg"
                                    style={{
                                        opacity: section.imageProps.opacity,
                                        transform: section.imageProps.scale ? `scale(${section.imageProps.scale})` : 'none',
                                        height: '100%',
                                        width: 'auto',
                                        maxHeight: '600px'
                                    }}
                                />
                            )
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default FeaturesList;