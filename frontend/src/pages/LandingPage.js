import React from 'react';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import FeaturesList from '../components/FeaturesList';
import CreditCardDBCallToAction from '../components/calltoaction/CredtiCardDB';
import GetStartedCallToAction from '../components/calltoaction/GetStarted';
import Footer from '../components/Footer';

const LandingPageComponent = () => {
    return (
        <div> 
            <Navbar/>
            <Hero/>
            <GetStartedCallToAction/>
            <CreditCardDBCallToAction/>
            <FeaturesList/>
            <Footer/>
        </div>
    );
};

export default LandingPageComponent;