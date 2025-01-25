import React, { useState, useRef, useEffect } from 'react';
import { Button } from 'primereact/button';
import { confirmDialog, ConfirmDialog } from 'primereact/confirmdialog';
import { InputTextarea } from 'primereact/inputtextarea';
import { InputText } from 'primereact/inputtext';
import './LoadingQuestions.css';

const BankConnectionForm = ({ 
  handlePrimaryEmail, 
  onSelect, 
  handleEnrollment,
  handleBioSubmit, 
  solution, 
  dateRange, 
  contactInfo, 
  accounts, 
  preferredAccount, 
  setPreferredAccount,
  setUserBio // New prop for setting user bio
}) => {
  const [tellerConnectReady, setTellerConnectReady] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isEmailTaken, setIsEmailTaken] = useState(false);
  const [isEmailProcessed, setIsEmailProcessed] = useState(false);
  const [primaryEmail, setPrimaryEmail] = useState("");
  const [formsComplete, setFormsComplete] = useState(false);
  const [showBioInput, setShowBioInput] = useState(false);
  const [userBioText, setUserBioText] = useState('');
  const [charCount, setCharCount] = useState(0);
  const CHAR_MIN = 100;
  const [formData, setFormData] = useState({
    primaryEmail: "",
    paymentMethods: "",
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

  const submitPrimaryEmail = (primaryEmail) => {  
    handlePrimaryEmail(primaryEmail)
      .then((response) => {
        if (response.ok) {
          console.log('Primary email handled successfully');
          setIsEmailProcessed(true)
        } else {
          console.error('Email is taken');
          setIsEmailTaken(true);  
        }
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
    if (formData.paymentMethods.length > 0 && formData.creditKnowledge?.length > 0) {
      setFormsComplete(true);
    }
  }, [formData]);

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
          onExit: () => {}
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

  const handleGenerateMock = () => {
    setShowBioInput(true);
  };

  if (showBioInput) {
    return (
      <div className="flex flex-column gap-4">
        <div className="question-animate">
          <p className="text-lg mb-4">
            Please describe your typical monthly spending patterns and transactions
          </p>
          <div className="flex flex-column gap-2">
            <InputTextarea
              value={userBioText}
              onChange={(e) => {
                setUserBioText(e.target.value);
                setCharCount(e.target.value.length);
              }}
              rows={5}
              className={`w-full ${charCount < CHAR_MIN ? 'p-invalid' : ''}`}
              placeholder="Enter your transaction details here (minimum 100 characters)..."
            />
            <div className="flex justify-content-between mt-2 text-sm">
              <span className={charCount < CHAR_MIN ? 'text-red-500' : ''}>
                {charCount} / {CHAR_MIN} characters
              </span>
              {charCount < CHAR_MIN && (
                <span>
                  Please enter at least {CHAR_MIN} characters
                </span>
              )}
            </div>
            <div className="flex gap-2 mt-2">
              <Button
                label="Cancel"
                icon="pi pi-times"
                onClick={() => {
                  setShowBioInput(false);
                  setUserBioText('');
                  setCharCount(0);
                }}
                className="w-6"
                severity="secondary"
              />
              <Button
                label="Submit"
                icon="pi pi-check"
                onClick={() => {
                  handleBioSubmit(userBioText);
                  setShowBioInput(false);
                  setIsProcessing(true);
                }}
                className="w-6"
                disabled={userBioText.trim().length < CHAR_MIN}
              />
            </div>
          </div>
        </div>
        <ConfirmDialog />
      </div>
    );
  }

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
        <Button 
          label="Generate mock transactions"
          icon="pi pi-lightbulb"
          onClick={handleGenerateMock}
          className="w-full"
        />
        <ConfirmDialog />
      </div>
    );
  }
  {/* Only showing the relevant solutions display section for brevity */}
  if (solution && dateRange && formsComplete) {
    return (
      <div className="flex flex-column gap-4">
        <div className="continue-animate">
          <div className="text-2xl font-medium mb-3 text-white">
            Here's your optimal card allocation from {dateRange.start_month} to {dateRange.start_month}
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
            onClick={() => onSelect()}
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
            {!solution ? (
              <i className="pi pi-sync pi-spin text-xl text-blue-500" />
            ) : (
              <i className="pi pi-check text-xl " />
            )}
            <span className="ml-2">
              {solution ? 'Analysis Complete!' : 'Analyzing your transactions...'}
            </span>
        </div>

        {!isEmailProcessed && (
          <div className="mb-4">
            <p className="text-lg">
              <span className="underline">A detailed breakdown of your transactions we've analyzed will be available at the bottom of your dashboard</span>.
            </p>
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
                onClick={() => submitPrimaryEmail(primaryEmail)}
                className='mt-3'
              />
              {isEmailTaken && 
              <small className="text-red-800">
                This email is taken.
              </small>}
            </div>
          </div>
        )}

        {isEmailProcessed && (!preferredAccount.confirmed) && (
          <div className="mb-4">
            <p className="text-lg mb-2">
              Please select a primary payment account
            </p>
            <div className="flex flex-column gap-2">
              <Button
                key={-1}
                label={'Pay with Credit Card'}
                className={`p-button ${preferredAccount.preferred === -1 ? 'selected' : ''}`}
                onClick={() => setPreferredAccount(prev => ({...prev, preferred: -1}))}
              />
              {accounts && 
                Object.entries(accounts).map(([id, name]) => (
                  <Button
                    key={id}
                    label={name}
                    className={`p-button ${preferredAccount.preferred === id ? 'selected' : ''}`}
                    onClick={() => setPreferredAccount(prev => ({...prev, preferred: id}))}
                  />
                ))
              }
              <Button
                label="Submit Preferred Payment Method"
                onClick={() => setPreferredAccount(prev => ({...prev, confirmed: true}))}
                className="mt-3"
                disabled={!preferredAccount.preferred}
              />
            </div>
          </div>
        )}

        {isEmailProcessed && preferredAccount.confirmed && !formData.paymentMethods.length && (
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
  title: "Let's analyze your transactions!",
  primaryColor: 'var(--onb-green)',
  secondaryColor: 'var(--onb-cyan)',
  additionalContent: BankConnectionForm
};

export default BankConnectionPage;