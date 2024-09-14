import React, { useEffect } from 'react';
import { useTellerConnect } from 'teller-connect-react';

const TellerConnectComponent = ({ onSuccess }) => {
    const config = {
        // Define your Teller Connect configuration here
        applicationId: 'your-app-id', // Replace with your actual application ID
        onSuccess: onSuccess,
    };

    const { open, ready } = useTellerConnect(config);

    useEffect(() => {
        if (ready) {
            open();
        }
    }, [ready, open]);

    return <></>;
};

export default TellerConnectComponent;