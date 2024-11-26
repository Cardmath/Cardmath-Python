import React, { useState } from 'react';
import { Button } from 'primereact/button';
import { ConfirmDialog } from 'primereact/confirmdialog';
import { fetchWithAuth } from '../pages/AuthPage'; // Adjust the import path as needed
import { Toast } from 'primereact/toast';
import TellerConnectComponent from './TellerConnect'; // Import TellerConnectComponent
import { ProgressSpinner } from 'primereact/progressspinner';

const SettingsPage = () => {
    const [confirmVisible, setConfirmVisible] = useState(false);
    const [showTellerConnect, setShowTellerConnect] = useState(false); // State to control Teller Connect visibility
    const [isLoading, setIsLoading] = useState(false); // State for loading spinner
    const toast = React.useRef(null);

    const showConfirm = () => {
        setConfirmVisible(true);
    };

    const handleDelete = () => {
        fetchWithAuth(`https://backend-dot-cardmath-llc.uc.r.appspot.com/delete-user-data`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        })
            .then(response => {
                if (response.ok) {
                    toast.current.show({ severity: 'success', summary: 'Success', detail: 'Your transactions and any data related to your bank account has been deleted.' });
                } else {
                    toast.current.show({ severity: 'error', summary: 'Error', detail: 'Failed to delete your data. Please contact support@cardmath.ai if this issue persists.' });
                }
            })
            .catch(error => {
                console.error('Error deleting user data:', error);
                toast.current.show({ severity: 'error', summary: 'Error', detail: 'An unexpected error occurred. Please contact support@cardmath.ai if this issue persists.' });
            })
            .finally(() => {
                setConfirmVisible(false);
            });
    };

    const handleConnectMoreBanks = () => {
        setShowTellerConnect(true);
    };

    const handleTellerSuccess = () => {
        setShowTellerConnect(false);
        toast.current.show({ severity: 'success', summary: 'Success', detail: 'Bank account connected successfully.' });
    };

    const handleTellerBack = () => {
        setShowTellerConnect(false);
    };

    return (
        <div className="p-4 gap-4 surface-ground">
            <Toast ref={toast} />
            <ConfirmDialog
                visible={confirmVisible}
                onHide={() => setConfirmVisible(false)}
                message="Are you sure you want to delete your account and all saved data? You can restore your data at any time in the future by simply connecting your bank accounts."
                header="Confirmation"
                icon="pi pi-exclamation-triangle"
                accept={handleDelete}
                reject={() => setConfirmVisible(false)}
            />
            {!showTellerConnect && (
                <div className="grid">
                    <div className="col-12 flex justify-content-center mb-4">
                        <Button label="Upgrade your subscription plan" className="p-button-lg" />
                    </div>
                    <div className="col-12 flex justify-content-center mb-4">
                        <Button
                            label="Connect more bank accounts"
                            className="p-button-lg"
                            onClick={handleConnectMoreBanks}
                        />
                    </div>
                    <div className="col-12 flex justify-content-center">
                        <Button
                            label="Delete your account, saved data"
                            className="p-button-lg p-button-danger"
                            onClick={showConfirm}
                        />
                    </div>
                </div>
            )}
            {showTellerConnect && (
                <div className="mt-5">
                    {isLoading && <ProgressSpinner />}
                    <TellerConnectComponent
                        onBack={handleTellerBack}
                        onSuccess={handleTellerSuccess}
                    />
                </div>
            )}
        </div>
    );
};

export default SettingsPage;
