import React, { useEffect, useState, useRef } from 'react';
import { fetchWithAuth } from './AuthPage';
import { ProgressSpinner } from 'primereact/progressspinner';
import { confirmDialog } from 'primereact/confirmdialog';
import { ConfirmDialog } from 'primereact/confirmdialog';
import { Button } from 'primereact/button';

const TellerConnectComponent = ({ onBack, onSuccess }) => {
    const [showSpinner, setShowSpinner] = useState(false);
    const [processingError, setProcessingError] = useState(false);
    const [tellerConnectReady, setTellerConnectReady] = useState(false);
    const [scriptLoadError, setScriptLoadError] = useState(false);
    const tellerConnectRef = useRef(null);

    const handleSuccess = async (data) => {
        setShowSpinner(true);
        var el = document.getElementById('teller-connect-window');
        if (el) {
            el.style.display = 'none';
        }
        try {
            let response = await fetchWithAuth(
                'https://backend-dot-cardmath-llc.uc.r.appspot.com/receive_teller_enrollment',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                }
            );
            if (!response.ok) {
                confirmDialog({
                    message: `The server rejected your enrollment. Please confirm that you are logged in and try again.`,
                    header: 'Error sending Enrollment to Server',
                    icon: 'pi pi-exclamation-triangle',
                    accept: () => {
                        setProcessingError(false);
                        window.location.href = 'https://cardmath.ai/dashboard';
                    },
                    reject: () => {
                        window.location.reload();
                        setProcessingError(false);
                    },
                });
                setProcessingError(true);
                console.log(
                    'The server rejected your enrollment. Please confirm that you are logged in and try again.'
                );
                return; // Exit the function if response is not ok
            }
        } catch (error) {
            confirmDialog({
                message: `A network error occurred while sending your enrollment data. Please check your internet connection and try again.`,
                header: 'Network Error',
                icon: 'pi pi-exclamation-triangle',
                accept: () => {
                    setProcessingError(false);
                    window.location.href = 'https://cardmath.ai/dashboard';
                },
                reject: () => {
                    window.location.reload();
                    setProcessingError(false);
                },
            });
            setProcessingError(true);
            console.log(
                'A network error occurred while sending your enrollment data. Please check your internet connection and try again.'
            );
            return; // Exit the function if there is an error
        }

        try {
            let response = await fetchWithAuth(
                'https://backend-dot-cardmath-llc.uc.r.appspot.com/process_new_enrollment',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }
            );
            if (!response.ok) {
                confirmDialog({
                    header: 'Error',
                    icon: 'pi pi-exclamation-triangle',
                    message:
                        'The server encountered an error while processing your enrollment. Please try again later.',
                    accept: () => {
                        setProcessingError(false);
                        window.location.href = 'https://cardmath.ai/dashboard';
                    },
                    reject: () => {
                        window.location.reload();
                    },
                });
                setProcessingError(true);
                console.log(
                    'The server encountered an error while processing your enrollment. Please try again later.'
                );
                return; // Exit the function if response is not ok
            }
            // Proceed to next step after successful processing
            onSuccess();
        } catch (error) {
            confirmDialog({
                header: 'Network Error',
                icon: 'pi pi-exclamation-triangle',
                message:
                    'A network error occurred while processing your enrollment. Please check your internet connection and try again.',
                accept: () => {
                    setProcessingError(false);
                    window.location.href = 'https://cardmath.ai/dashboard';
                },
                reject: () => {
                    window.location.reload();
                },
            });
            setProcessingError(true);
            console.log(
                'A network error occurred while processing your enrollment. Please check your internet connection and try again.'
            );
        }
    };

    useEffect(() => {
        const script = document.createElement('script');
        script.src = 'https://cdn.teller.io/connect/connect.js';
        script.onload = () => {
            // Initialize TellerConnect but do not open it yet
            if (window.TellerConnect) {
                const tellerConnect = window.TellerConnect.setup({
                    applicationId: 'app_p3oodma27qfrj3hs8a000',
                    selectAccount: 'disabled',
                    environment: 'sandbox', // Change to 'production' in production environment
                    products: ['transactions'],
                    onInit: function () {
                        console.log('Teller Connect has initialized');
                    },
                    onSuccess: function (enrollment) {
                        console.log('User enrolled successfully', enrollment.accessToken);
                        handleSuccess(enrollment);
                    },
                    onExit: function () {
                        console.log('User closed Teller Connect');
                        setProcessingError(true);
                        confirmDialog({
                            header: 'Enrollment Cancelled',
                            message:
                                'You have closed Teller Connect. Please try again to link your bank account.',
                            icon: 'pi pi-exclamation-triangle',
                            accept: () => {
                                setProcessingError(false);
                            },
                            reject: () => {
                                setProcessingError(false);
                            },
                        });
                    },
                });
                tellerConnectRef.current = tellerConnect;
                setTellerConnectReady(true);
            } else {
                console.error(
                    'TellerConnect is not defined. Make sure the script is loaded correctly.'
                );
                setScriptLoadError(true);
            }
        };
        script.onerror = () => {
            console.error('Failed to load the Teller Connect script.');
            setScriptLoadError(true);
        };
        document.body.appendChild(script);
    }, []);

    const openTellerConnect = () => {
        if (tellerConnectRef.current) {
            tellerConnectRef.current.open();
        } else {
            console.error('TellerConnect is not initialized.');
            confirmDialog({
                header: 'Error',
                message: 'Teller Connect is not initialized. Please try again later.',
                icon: 'pi pi-exclamation-triangle',
                accept: () => {
                    setProcessingError(false);
                    window.location.href = 'https://cardmath.ai/dashboard';
                },
                reject: () => {
                    setProcessingError(false);
                },
            });
            setProcessingError(true);
        }
    };

    return (
        <div>
            <div className="flex pt-6 pb-2 text-white font-bold text-6xl">
                Connect Your Bank Account
            </div>
            <div id="teller-connect"></div>
            {scriptLoadError && (
                <div className="error-message">
                    <p className="text-2xl text-red-500">
                        An error occurred while loading the Teller Connect component. Please check
                        your internet connection and try again.
                    </p>
                </div>
            )}
            {!scriptLoadError && !showSpinner && !processingError && (
                <div className="flex flex-column align-items-center">
                    <p className="text-2xl">
                        Cardmath utilizes Teller Connect to securely link users' bank accounts,
                        ensuring that only transaction data is accessed. Teller Connect is a
                        client-side UI component that facilitates the connection between users'
                        financial accounts and applications like Cardmath. It manages credential
                        validation, multi-factor authentication, account selection, and error
                        handling for various financial institutions.
                    </p>
                    <p className="text-2xl">
                        By integrating Teller Connect, Cardmath ensures that sensitive financial
                        information is handled securely and that users have control over their data.
                        Cardmath commits to never selling user data to third parties, and users
                        retain full rights to their information, deciding how it is utilized.
                    </p>
                    <Button
                        label="Connect Bank Account"
                        onClick={openTellerConnect}
                        disabled={!tellerConnectReady}
                        size="large"
                    />
                </div>
            )}
            {showSpinner && !processingError && (
                <div className="flex flex-column justify-content-center">
                    <div className="flex align-content-evenly justify-content-center mt-4">
                        <ProgressSpinner />
                    </div>
                    <span className="flex align-content-evenly justify-content-center h-4rem font-bold border-round m-2 text-3xl font-medium text-white mt-4">
                        Hold tight while we process your information!
                    </span>
                </div>
            )}
            <ConfirmDialog />
        </div>
    );
};

export default TellerConnectComponent;
