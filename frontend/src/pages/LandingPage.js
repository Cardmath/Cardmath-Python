import React from 'react';
import Navbar from '../components/Navbar';
import FeaturesList from '../components/FeaturesList';
import CreditCardDBCallToAction from '../components/calltoaction/CredtiCardDB';
import GetStartedCallToAction from '../components/calltoaction/GetStarted';
import Footer from '../components/Footer';
import FadeInSection from '../components/calltoaction/FadeInSection';
import AnimatedHero from '../components/hero/AnimatedHero';

const LandingPageComponent = () => {
    return (
        <div> 
            <Navbar/>
            <AnimatedHero/>
            <div style={{marginLeft: 'auto', marginRight: 'auto', maxWidth: '1100px'}}>
                <FadeInSection>
                    <GetStartedCallToAction/>
                </FadeInSection>
                <FadeInSection>
                    <FeaturesList/>    
                </FadeInSection>
                <FadeInSection>
                    <CreditCardDBCallToAction/>
                </FadeInSection>
            </div>
            <Footer/>
        </div>
    );
};

export default LandingPageComponent;