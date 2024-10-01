import React, { useState } from 'react';
import SimpleSection from '../components/SimpleSection';
import PreferencesCard from '../components/PreferencesCard';
import Footer from '../components/Footer';
import Alert  from '../components/Alert';

const PreferencesPage = () => {
    const [alert, setAlert] = useState({visible: false, message: '', heading : '', type: 'error'});
    return (
        <div>
            <Alert visible={alert.visible} message={alert.message} type={alert.type} heading={alert.heading} setVisible={(visible) => setAlert({ ...alert, visible })}/>
            <SimpleSection sectionTitle="Preferences"/>
            <PreferencesCard setAlert={setAlert}/>
            <Footer />
        </div>
    );
};

export default PreferencesPage;