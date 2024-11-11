import React, { useState } from 'react';
import { Dialog } from 'primereact/dialog';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';

const TermsOfUseDialog = ({ pdfUrl, onConfirm }) => {
    const [visible, setVisible] = useState(true);
    const [checked, setChecked] = useState(false);

    const handleConfirm = () => {
        if (checked) {
            onConfirm();
            setVisible(false);
        } else {
            alert("Please accept the Terms of Use to proceed.");
        }
    };

    return (
        <Dialog header="Terms of Use" visible={visible} style={{ width: '50vw' }} onHide={() => setVisible(false)}>
            <div style={{ height: '400px' }}>
                <iframe 
                    src={pdfUrl} 
                    title="Terms of Use" 
                    width="100%" 
                    height="100%" 
                    style={{ border: 'none' }} 
                />
            </div>
            <div className="p-field-checkbox" style={{ marginTop: '1rem' }}>
                <Checkbox inputId="accept" checked={checked} onChange={(e) => setChecked(e.checked)} />
                <label htmlFor="accept">I agree to the Terms of Use</label>
            </div>
            <Button label="Confirm" icon="pi pi-check" onClick={handleConfirm} disabled={!checked} />
        </Dialog>
    );
};

export default TermsOfUseDialog;
