import React from 'react';
import { Button } from 'primereact/button';

const SimpleSection = ( {sectionTitle, dasboardButtonLabel, dasboardButtonOnClick, tellerConnectButtonLabel, tellerConnectButtonOnClick} ) => {
    return (
        <div className="flex justify-content-between align-items-center bg-surface-ground px-4 py-5 md:px-6 lg:px-8">
            <div className="flex border-bottom-1 surface-border">
                <span className="block text-4xl text-white text-900 mb-4">{sectionTitle}</span>
            </div>
            <div className="flex justify-content-end flex-wrap gap-3">
                <Button label={dasboardButtonLabel} onClick={dasboardButtonOnClick} className="p-button-lg p-button-rounded p-button-primary mr-3" />
                <Button label={tellerConnectButtonLabel} onClick={tellerConnectButtonOnClick} className="p-button-lg p-button-rounded p-button-secondary ">
                    <img src="/teller.svg" alt="Image" className="p-1 h-2rem" />
                </Button>
            </div>
        </div>
    );
};

export default SimpleSection;