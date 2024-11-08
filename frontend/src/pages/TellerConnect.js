import React, { useEffect, useState } from 'react';
import { fetchWithAuth } from './AuthPage';
import { ProgressSpinner } from 'primereact/progressspinner';
import { ConfirmDialog } from 'primereact/confirmdialog';
import { confirmDialog } from 'primereact/confirmdialog';

const TellerConnectComponent = () => {

    const [showSpinner, setShowSpinner] = useState(false); 
    const [processingError, setProcessingError] = useState(false);

    const handleSuccess = async (data) => {
        setShowSpinner(true);
        var el = document.getElementById("teller-connect-window");
        el.style.display = 'none';
        try {
            let response = await fetchWithAuth('https://backend-dot-cardmath-llc.uc.r.appspot.com/receive_teller_enrollment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });   
            if (!response.ok) {
                confirmDialog({
                    message: `The server rejected your enrollment. Please confirm that you are logged in and try again.`,
                    header: 'Error sending Enrollment to Server',
                    icon: 'pi pi-exclamation-triangle',
                    accept: () => {
                        setProcessingError(false);
                        window.location.href = 'https://backend-dot-cardmath-llc.uc.r.appspot.com/dashboard';   
                    },
                    reject: () => {
                        window.location.reload();
                        setProcessingError(false);
                    }                
                })
                setProcessingError(true);
                console.log("The server rejected your enrollment. Please confirm that you are logged in and try again.");
            }
        } catch (error) {
            confirmDialog({
                message: `Error enrolling with Teller Connect. The enrollment was not sent to our server. Please try again.`,
                header: 'Error Enrolling with Teller Connect',
                icon: 'pi pi-exclamation-triangle',
                accept: () => {
                    setProcessingError(false);
                    window.location.href = 'https://cardmath.ai/dashboard';   
                },
                reject: () => {
                    window.location.reload();
                    setProcessingError(false);
                }
            })
            setProcessingError(true);
            console.log("Error enrolling with Teller Connect. The enrollment was not sent to our server. Please try again.");
        }     

        try {
            let response = await fetchWithAuth('https://backend-dot-cardmath-llc.uc.r.appspot.com/process_new_enrollment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            }); 
            if (!response.ok) {
                confirmDialog({
                    header: 'Error',
                    icon: 'pi pi-exclamation-triangle',
                    message: 'An error occurred while processing the enrollment. Please try again.',
                    accept: () => {
                        setProcessingError(false);
                        window.location.href = 'https://cardmath.ai/dashboard';   
                    },
                    reject: () => {
                        window.location.reload();
                    }                
                })
                setProcessingError(true);
                console.log("An error occurred while processing the enrollment. Please try again.");
            }
            window.location.href = 'https://cardmath.ai/dashboard';
        } catch (error) {   
            confirmDialog({
                header: 'Error',
                icon: 'pi pi-exclamation-triangle',
                message: 'An error occurred while processing the enrollment. Please try again.',
                accept: () => {
                    setProcessingError(false);
                    window.location.href = 'https://cardmath.ai/dashboard';   
                },
                reject: () => {
                    window.location.reload();
                }            
            })
            setProcessingError(true);
            console.log("An error occurred while processing the enrollment. Please try again.");
        }
};

    useEffect(() => {
        const script = document.createElement('script');
        script.src = "https://cdn.teller.io/connect/connect.js";        
        script.onload = () => {
            // Use TellerConnect directly after script loads
            if (window.TellerConnect) {
                var tellerConnect = window.TellerConnect.setup({
                    applicationId: "app_p3oodma27qfrj3hs8a000",
                    selectAccount: "disabled",
                    environment: 'sandbox',
                    onInit: function() {
                        console.log("Teller Connect has initialized");
                    },
                    onSuccess: function(enrollment) {
                        console.log("User enrolled successfully", enrollment.accessToken);
                        handleSuccess(enrollment);
                    },
                    onExit: function() {
                        console.log("User closed Teller Connect");
                        window.location.href = 'https://cardmath.ai/dashboard';
                    }
                });
                tellerConnect.open();
            } else {
                console.error("TellerConnect is not defined. Make sure the script is loaded correctly.");
            }
        };
        script.onerror = () => {
            console.error("Failed to load the Teller Connect script.");
        };
        document.body.appendChild(script);
    }, []);
    
    return (
        <div>
            <div id="teller-connect">

            </div>
            {showSpinner && !processingError && (
                <div className="bg-primary-reverse flex h-full h-screen flex-column justify-content-center">
                    <div className="flex align-content-evenly justify-content-center">
                        <ProgressSpinner />
                    </div>
                    <span className="flex align-content-evenly justify-content-center h-4rem font-bold border-round m-2 text-3xl font-medium text-gray-900 mt-4">
                        Hold tight while we process your information!
                    </span>
                </div>
            )}
            <ConfirmDialog />
        </div>
    );  
};



export default TellerConnectComponent;