import React from 'react';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import FeaturesList from '../components/FeaturesList';

const LandingPageComponent = () => {
    return (
        <div> 
            <Navbar/>
            <Hero/>
            <FeaturesList/>
        </div>
    );
};

export default LandingPageComponent;