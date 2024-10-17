import React, { useState } from 'react';
import SimpleSection from '../components/SimpleSection';
import PreferencesCard from '../components/PreferencesCard';
import Footer from '../components/Footer';
import Alert  from '../components/Alert';


const PreferencesPage = () => {
    const [alert, setAlert] = useState({visible: false, message: '', heading : '', type: 'error'});
    return (
        <div className='bg-gray-900' >
            <Alert visible={alert.visible} message={alert.message} type={alert.type} heading={alert.heading} setVisible={(visible) => setAlert({ ...alert, visible })}/>
            <SimpleSection sectionTitle="Preferences"
            tellerConnectButtonLabel={"Connect Banks with: "} tellerConnectButtonOnClick={() => window.location.href = '/connect'}
            dasboardButtonLabel="To Dashboard" dasboardButtonOnClick={() => window.location.href = '/dashboard'}/>
            <PreferencesCard setAlert={setAlert}/>
            <Footer />
        </div>
    );
};

export default PreferencesPage;