import React, { useEffect, useState, useRef } from 'react';
import { fetchWithAuth } from './AuthPage';
import { ProgressSpinner } from 'primereact/progressspinner';
import { ConfirmDialog, confirmDialog } from 'primereact/confirmdialog';
import { Button } from 'primereact/button';
import { getBackendUrl } from '../utils/urlResolver';

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
                `${getBackendUrl()}/receive_teller_enrollment`,
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
                return;
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
            return;
        }

        try {
            let response = await fetchWithAuth(
                `${getBackendUrl()}/process_new_enrollment`,
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
                return;
            }
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
        }
    };

    useEffect(() => {
        const script = document.createElement('script');
        script.src = 'https://cdn.teller.io/connect/connect.js';
        script.onload = () => {
            if (window.TellerConnect) {
                const tellerConnect = window.TellerConnect.setup({
                    applicationId: 'app_p79ra9mqcims8r8gqa000',
                    selectAccount: 'disabled',
                    environment: 'development',
                    products: ["verify", "verify.instant", "transactions", "identity", "payments"],
                    onInit: function () {
                        console.log('Teller Connect has initialized');
                    },
                    onSuccess: function (enrollment) {
                        handleSuccess(enrollment);
                    },
                    onExit: function () {
                        console.log('User closed Teller Connect');
                        confirmDialog({
                            header: 'Enrollment Cancelled',
                            message:
                                'You have closed Teller Connect. Please try again to link your bank account.',
                            icon: 'pi pi-exclamation-triangle',
                            accept: () => {
                                setShowSpinner(false);
                                setProcessingError(false);
                            },
                            reject: () => {
                                setShowSpinner(false);
                                setProcessingError(false);
                            },
                        });
                    },
                });
                tellerConnectRef.current = tellerConnect;
                setTellerConnectReady(true);
            } else {
                console.error('TellerConnect is not defined.');
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

    const TellerInfo = () => (
        <div className="flex flex-column text-white align-items-center">
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
    );

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
            {!scriptLoadError && !showSpinner && <TellerInfo />}
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