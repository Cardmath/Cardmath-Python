import React from 'react';
import SimpleSection from '../components/SimpleSection';
import PreferencesCard from '../components/PreferencesCard';
import Footer from '../components/Footer';

const PreferencesPage = () => {
    return (
        <div>
            <SimpleSection sectionTitle="Preferences"/>
            <PreferencesCard />
            <Footer />
        </div>
    );
};

export default PreferencesPage;