import React, { useEffect, useState } from 'react';
import { useTellerConnect } from 'teller-connect-react';
import { fetchWithAuth } from './AuthPage';
import { ProgressSpinner } from 'primereact/progressspinner';

const TellerConnectComponent = () => {

    const [showSpinner, setShowSpinner] = useState(false); 

    const handleSuccess = async (data) => {
        setShowSpinner(true);
        try {
            let response = await fetchWithAuth('http://localhost:8000/enrollment', {
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

            window.location.href = '/preferences'; // TODO IMPLEMENT QUESTIONS 

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

    return (
        <div>
            {showSpinner && (
                <div className="bg-primary-reverse flex h-full h-screen flex-column justify-content-center">
                    <div className="flex align-content-evenly justify-content-center">
                        <ProgressSpinner />
                    </div>
                    <span className="flex align-content-evenly justify-content-center h-4rem font-bold border-round m-2 text-3xl font-medium text-gray-900 mt-4">
                        Hold tight while we process your information!
                    </span>
                </div>
            )}
        </div>
    );  
};



export default TellerConnectComponent;