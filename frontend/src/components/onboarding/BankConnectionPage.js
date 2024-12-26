import React, { useState, useRef, useEffect } from 'react';
import { Button } from 'primereact/button';
import { confirmDialog, ConfirmDialog } from 'primereact/confirmdialog';
import './LoadingQuestions.css';
import { InputText } from 'primereact/inputtext';

const BankConnectionForm = ({ handlePrimaryEmail, emailProcessed, handleEnrollment, solution, contactInfo }) => {
  const [tellerConnectReady, setTellerConnectReady] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [primaryEmail, setPrimaryEmail] = useState("");
  const [formsComplete, setFormsComplete] = useState(false);
  const [formData, setFormData] = useState({
    primaryEmail: "", 
    paymentMethods: "", // Either Google Pay or Apple Pay
    creditKnowledge: ""
  });
  const tellerConnectRef = useRef(null);

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

  const handleSuccess = async (enrollment) => {
    setIsProcessing(true);
    try {
      await handleEnrollment(enrollment);
    } catch (error) {
      console.error('Error in handleSuccess:', error);
      handleError('Failed to process enrollment');
    }
  };

  useEffect(() => {
    if (formData.paymentMethods.length > 0) {
      setFormsComplete(true)
    }
  }, [formData])

  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdn.teller.io/connect/connect.js';
    script.onload = () => {
      if (window.TellerConnect) {
        const tellerConnect = window.TellerConnect.setup({
          applicationId: 'app_p79ra9mqcims8r8gqa000',
          selectAccount: 'disabled',
          environment: 'sandbox',
          products: ['transactions'],
          onInit: () => setTellerConnectReady(true),
          onSuccess: handleSuccess,
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
    
    return () => {
      const scriptElement = document.querySelector('script[src="https://cdn.teller.io/connect/connect.js"]');
      if (scriptElement) {
        scriptElement.remove();
      }
    };
  }, []);

  if (!isProcessing) {
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
          className="w-full"
        />
        <ConfirmDialog />
      </div>
    );
    }
  {/* Only showing the relevant solutions display section for brevity */}
  if (solution && formsComplete) {
    return (
      <div className="flex flex-column gap-4">
        <div className="continue-animate">
          <div className="text-2xl font-medium mb-3 text-white">
            Here's your optimal card allocation
          </div>
          <div className="text-base mb-4 text-white-alpha-70">
            {`Analysis period: TODO`}
          </div>
          
          <div className="bg-black-alpha-70 p-4 border-round mb-3">
            <div className="flex align-items-center gap-3 mb-3">
              <i className="pi pi-dollar text-primary text-2xl"></i>
              <div>
                <div className="text-white-alpha-70 mb-1">Total Rewards</div>
                <div className="text-3xl font-medium text-white">
                  ${solution.total_reward_usd.toLocaleString('en-US', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                  })}
                </div>
              </div>
            </div>
            <div className="border-top-1 surface-border pt-3">
              {[
                { label: 'Regular Rewards', value: solution.total_regular_rewards_usd },
                { label: 'Sign-up Bonuses', value: solution.total_sign_on_bonus_usd },
                { label: 'Statement Credits', value: solution.total_statement_credits_usd }
              ].map((detail, index) => (
                <div key={index} className="flex justify-content-between align-items-center py-2">
                  <span className="text-white-alpha-70">{detail.label}</span>
                  <span className="text-white font-medium">
                    ${detail.value.toLocaleString('en-US', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2
                    })}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <Button 
            label="See Full Analysis" 
            className="w-full p-button-outlined"
            style={{ borderColor: 'rgba(255,255,255,0.2)', color: 'white' }}
          />
        </div>
        <ConfirmDialog />
      </div>
    );
  }

  return (
    <div className="flex flex-column gap-4">
      <div className="question-animate">
        <div className="flex align-items-center gap-3 mb-4">
          <i className="pi pi-sync pi-spin text-xl text-blue-500"></i>
          <div>
            <div className="font-medium">Analyzing your transactions</div>
            <div className="text-sm text-gray-300">Processing your spending patterns</div>
          </div>
        </div>
            {!emailProcessed && (
        <div className="mb-4">
            <p className="text-lg mb-2">
                Please select a primary email to associate with your Cardmath account
            </p>
            <div className="flex flex-column gap-2">
                {contactInfo &&
                    contactInfo.emails.map((email) => (
                        <Button
                            label={email}
                            className={`p-button ${primaryEmail === email ? 'selected' : ''}`}
                            onClick={() => setPrimaryEmail(email)}
                        />
                    ))}
                <InputText id="email" onChange={(e) => setPrimaryEmail(e.target.value)} aria-describedby="email-help" />
                <small id="email-help">
                    Preferred email not in the list? Pick a custom email.
                </small>
                <Button
                    label="Submit Chosen Email"
                    onClick={()=>handlePrimaryEmail(primaryEmail)}
                    className='mt-3'
                />
            </div>
        </div>
    )}

        {emailProcessed && !formData.paymentMethods.length && (
          <div className="mb-4">
            <p className="text-lg mb-2">While we analyze your transactions, do you use any of these?</p>
            <div className="flex flex-column gap-2">
              <Button
                label="Apple Pay"
                outlined
                onClick={() => setFormData(prev => ({
                  ...prev,
                  paymentMethods: [...prev.paymentMethods, 'apple']
                }))}
              />
              <Button
                label="Google Pay"
                outlined
                onClick={() => setFormData(prev => ({
                  ...prev,
                  paymentMethods: [...prev.paymentMethods, 'google']
                }))}
              />
            </div>
          </div>
        )}

        {formData.paymentMethods.length > 0 && !formData.creditKnowledge && (
          <div className="question-animate">
            <p className="text-lg mb-2">How much do you know about credit cards?</p>
            <div className="flex flex-column gap-2">
              <Button
                label="A little"
                outlined
                onClick={() => setFormData(prev => ({ ...prev, creditKnowledge: 'little' }))}
              />
              <Button
                label="A lot"
                outlined
                onClick={() => setFormData(prev => ({ ...prev, creditKnowledge: 'lot' }))}
              />
            </div>
          </div>
        )}
      </div>
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