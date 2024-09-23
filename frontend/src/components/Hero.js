import React from 'react';

const Hero = () => {
    return (
        <div className="relative p-8 overflow-hidden">
            <img src="/hero-2.jpg" alt="hero-2" className="absolute top-0 left-0 w-auto h-full block md:w-full" />
            <div className="text-center my-6 relative">
                <div className="text-6xl text-white font-bold mb-1">Cardmath</div>
                <div className="text-6xl text-primary font-bold mb-4">We crunch the numbers.</div>
                <p className="mt-0 mb-4 line-height-3 text-center mx-auto text-white" style={{ maxWidth: '500px' }}>
                We provide independent, data-driven credit-card recommendations—just sign into your bank accounts for personalized insights, and rest assured your data is securely protected and only used as needed.                </p>
                <p className="text-sm mt-4 mb-4 line-height-3 text-white">Available for users in the United States Only</p>
            </div>
        </div>
    );
};

export default Hero;