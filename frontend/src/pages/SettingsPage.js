import React from 'react';
import { Button } from 'primereact/button';

const SettingsPage = () => {
    return (
        <div className="p-4 gap-4 surface-ground">
            <div className="grid">
                <div className="col-12 flex justify-content-center mb-4">
                    <Button label="Upgrade your subscription plan" className="p-button-lg" />
                </div>
                <div className="col-12 flex justify-content-center mb-4">
                    <Button label="Connect more bank accounts" className="p-button-lg" />
                </div>
                <div className="col-12 flex justify-content-center">
                    <Button label="Delete your account, saved data" className="p-button-lg p-button-danger" />
                </div>
            </div>
        </div>
    );
};

export default SettingsPage;
