import React, { useState, useRef, useEffect } from 'react';
import { Button } from 'primereact/button';
import { confirmDialog, ConfirmDialog } from 'primereact/confirmdialog';
import { fetchWithAuth } from '../../pages/AuthPage';
import { getBackendUrl } from '../../utils/urlResolver';
import './LoadingQuestions.css';

const BankConnectionForm = ({ onSelect }) => {
  const [tellerConnectReady, setTellerConnectReady] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isEnrollmentComplete, setIsEnrollmentComplete] = useState(false);
  const [contactInfo, setContactInfo] = useState(null);
  const [formData, setFormData] = useState({
    paymentMethods: [],
    creditKnowledge: ''
  });
  const tellerConnectRef = useRef(null);

  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdn.teller.io/connect/connect.js';
    script.onload = () => {
      if (window.TellerConnect) {
        const tellerConnect = window.TellerConnect.setup({
          applicationId: 'app_p3oodma27qfrj3hs8a000',
          selectAccount: 'disabled',
          environment: 'sandbox',
          products: ['transactions'],
          onInit: () => setTellerConnectReady(true),
          onSuccess: async (enrollment) => {
            setIsProcessing(true);
            try {
              await onSelect(enrollment);
              setIsEnrollmentComplete(true);
            } catch (error) {
              handleError('Failed to process enrollment');
            }
          },
          onExit: () => {
            confirmDialog({
              header: 'Connection Cancelled',
              message: 'You have closed the bank connection window. Would you like to try again?',
              icon: 'pi pi-exclamation-triangle',
              accept: () => openTellerConnect(),
              reject: () => null
            });
          }
        });
        tellerConnectRef.current = tellerConnect;
      }
    };
    document.body.appendChild(script);
  }, []);

  const handleError = (message) => {
    confirmDialog({
      header: 'Error',
      message,
      icon: 'pi pi-exclamation-triangle',
      accept: () => setIsProcessing(false)
    });
  };

  const openTellerConnect = () => {
    if (tellerConnectRef.current) tellerConnectRef.current.open();
  };

  const handleContinue = () => {
    // Pass both form data and contact info to parent
    onSelect({
      ...formData,
      contactInfo
    });
  };

  if (isProcessing) {
    const showPaymentMethods = !formData.paymentMethods.length > 0;
    const showCreditKnowledge = !!(formData.paymentMethods.length && !formData.creditKnowledge);
    const showContinue = !!(isEnrollmentComplete && formData.paymentMethods.length && formData.creditKnowledge);
    
    return (
      <div className="flex flex-col gap-4">
        <div className="loading-questions">
          <div className="text-lg mb-4">While we process your bank connection, please answer two quick questions:</div>
          
          {showPaymentMethods && (
            <div className="question-animate">
              <p className="mb-2">Do you use any of these?</p>
              <div className="flex flex-col gap-2">
                <Button
                  label="Apple Pay"
                  variant="outlined"
                  onClick={() => setFormData(prev => ({
                    ...prev,
                    paymentMethods: [...prev.paymentMethods, 'apple']
                  }))}
                />
                <Button
                  label="Google Pay"
                  variant="outlined"
                  onClick={() => setFormData(prev => ({
                    ...prev,
                    paymentMethods: [...prev.paymentMethods, 'google']
                  }))}
                />
              </div>
            </div>
          )}

          {showCreditKnowledge && (
            <div className="question-animate">
              <p className="mb-2">How much do you know about credit cards?</p>
              <div className="flex flex-col gap-2">
                <Button
                  label="A little"
                  variant="outlined"
                  onClick={() => setFormData(prev => ({ ...prev, creditKnowledge: 'little' }))}
                />
                <Button
                  label="A lot"
                  variant="outlined"
                  onClick={() => setFormData(prev => ({ ...prev, creditKnowledge: 'lot' }))}
                />
              </div>
            </div>
          )}

          {showContinue && (
            <div className="continue-animate">
              <Button
                label="Continue"
                onClick={handleContinue}
                style={{ width: '100%' }}
              />
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-column gap-4">
      <p className="text-lg">
        Cardmath uses Teller Connect to securely link your bank account. We only access transaction data 
        and never store your banking credentials.
      </p>
      <Button 
        label="Connect Bank Account"
        icon="pi pi-link"
        onClick={openTellerConnect}
        disabled={!tellerConnectReady}
        style={{ width: '100%' }}
      />
      <ConfirmDialog />
    </div>
  );
};

const BankConnectionPage = {
  title: "Let's connect your bank account",
  content: "This helps us analyze your spending and recommend the best cards",
  primaryColor: 'var(--onb-green)',
  secondaryColor: 'var(--onb-cyan)',
  additionalContent: BankConnectionForm
};

export default BankConnectionPage;