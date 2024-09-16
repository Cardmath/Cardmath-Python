import React, { useEffect } from 'react';
import { useTellerConnect } from 'teller-connect-react';
import { fetchWithAuth } from './AuthPage';

const TellerConnectComponent = () => {
    const handleSuccess = async (data) => {
        try {
            const response = await fetchWithAuth('http://localhost:8000/enrollment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });            
            
            if (!response.ok) {
                throw new Error('Failed sending Teller enrollment to server.');
            }

            response = await fetchWithAuth('http://localhost:8000/get_transactions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            }); 
            
            if (!response.ok) {
                throw new Error('Failed prefetching Teller transactions.');
            }

            window.location.href = '/questions'; // TODO IMPLEMENT QUESTIONS 

        } catch (error) {
            console.error('Error sending enrollment to server:', error);
        }
    };

    const config = {
        // Teller Connect configuration
        selectAccount: "disabled",
        environment: 'sandbox',
        applicationId: 'app_p3oodma27qfrj3hs8a000',
        onSuccess: handleSuccess,
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