import React, { useState, useRef, useEffect } from 'react';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { ConfirmDialog, confirmDialog } from 'primereact/confirmdialog';
import { fetchWithAuth } from '../../pages/AuthPage';
import { getBackendUrl } from '../../utils/urlResolver';
import { useNavigate } from 'react-router-dom';


const PaymentForm = ({ preferredAccount }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [amount] = useState("0.00"); // Fixed amount for the service
  const [paymentError, setPaymentError] = useState(null);
  const [tellerConnectToken, setTellerConnectToken] = useState('');
  const [tellerConnectReady, setTellerConnectReady] = useState(false);
  const tellerConnectRef = useRef(null);
  const navigate = useNavigate();

  const handleError = (message) => {
    setPaymentError(message);
    setIsProcessing(false);
    confirmDialog({
      header: 'Payment Error',
      message,
      icon: 'pi pi-exclamation-triangle',
      accept: () => setIsProcessing(false)
    });
  };

  const openTellerConnect = () => {
    if (tellerConnectRef.current) tellerConnectRef.current.open();
  };

  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdn.teller.io/connect/connect.js';
    script.onload = () => {
      if (window.TellerConnect) {
        const tellerConnect = window.TellerConnect.setup({
          applicationId: 'app_p79ra9mqcims8r8gqa000', // Replace with your app ID
          connectToken: tellerConnectToken,
          selectAccount: 'disabled',
          environment: 'development',
          products: ['payments'],  // Note: changed from 'transactions' to 'payments'
          onInit: () => setTellerConnectReady(true),
          onSuccess: handleSuccess,
          onExit: () => {
            confirmDialog({
              header: 'Payment Verification Cancelled',
              message: 'You have closed the verification window. Would you like to try again?',
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


  const handleStripeCheckout = async (product) => {
    await refreshAccessToken();
    const response = await fetchWithAuth(
        `${getBackendUrl()}/create_checkout_session`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ product: product }),
        }
    );

    const data = await response.json();
    window.location.href = data.url;
  }; 

  const handleZellePayment = async () => {
    setIsProcessing(true);
    setPaymentError(null);
    await refreshAccessToken();
    try {
      const paymentResponse = await fetchWithAuth(
        `${getBackendUrl()}/initiate-zelle-payment`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            acc_id: preferredAccount.preferred
          })
        }
      );

      if (!paymentResponse.ok) {
        throw new Error('Failed to initiate payment');
      }

      const paymentData = await paymentResponse.json();

      // If MFA is required, open Teller Connect
      if (!paymentData.verified && paymentData.teller_connect_token) {
        setTellerConnectToken(paymentData.teller_connect_token)
        console.log("Attempting to open teller connect")
        openTellerConnect()
      } else if (paymentData.verified){
        refreshAccessToken();
        setIsProcessing(false);
      }
    } catch (error) {
      console.error('Payment error:', error);
      handleError(error.message || 'Failed to process payment');
    }
    navigate("/dashboard")
  };

  const handleSuccess = async (tellerResponse) => {
    if (!tellerResponse.id) {
      throw new Error('Failed to verify payment - please contact support@cardmath.ai')
    }  
    const paymentVerificationResponse = await fetchWithAuth(
      `${getBackendUrl()}/verify-zelle-payment`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          acc_id: preferredAccount.preferred,
          pid: tellerResponse.id
        })
      }
    );
    if (!paymentVerificationResponse.ok) {
      throw new Error('Zelle payment unable to be verified');
    }
    console.log("Zelle payment verified successfully");
  };

  const refreshAccessToken = async () => {
    setIsProcessing(false);
    const getUserToken = await fetchWithAuth(
      `${getBackendUrl()}/get-onboarding-user-token`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      }
    );

    if (!getUserToken.ok) {
      throw new Error('Couldn not retrieve a user token')
    }

    const response = await getUserToken.json();
    const token = response.access_token;
    
    console.log("New token is", token)
    localStorage.setItem('cardmath_access_token', token);
  }

  if (isProcessing) {
    return (
      <div className="flex flex-column gap-4">
        <div className="question-animate">
          <div className="flex align-items-center gap-3 mb-4">
            <i className="pi pi-sync pi-spin text-xl text-blue-500"></i>
            <div>
              <div className="font-medium">Processing Payment</div>
              <div className="text-sm text-gray-300">Please wait while we process your payment</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-column gap-4">
      <div className="bg-black-alpha-70 p-4 border-round mb-3">
        <div className="flex align-items-center gap-3 mb-3">
          <i className="pi pi-dollar text-primary text-2xl"></i>
          <div>
            <div className="text-white-alpha-70 mb-1">Service Fee</div>
            <div className="text-3xl font-medium text-white">{amount}</div>
          </div>
        </div>
        
        <div className="border-top-1 surface-border pt-3">
          <div className="text-white-alpha-70 mb-3">
            Pay securely using {preferredAccount.preferred == -1 ? 'Credit Card' : 'Zelle'}
          </div>
          
          <Button
            label={`Pay with ${preferredAccount.preferred === -1 ? 'Credit Card' : 'Zelle'}`}
            onClick={preferredAccount.preferred == -1 ? () => handleStripeCheckout('beta') : handleZellePayment}
            className="w-full"
            disabled={!tellerConnectReady}
          />
        </div>
      </div>

      {paymentError && (
        <div className="text-red-500 text-sm mt-2">
          {paymentError}
        </div>
      )}
      
      <ConfirmDialog />
    </div>
  );
};

const PaymentPage = {
  title: "Complete Your Registration",
  content: "Please complete the payment to activate your personalized card recommendations",
  primaryColor: 'var(--onb-purple)',
  secondaryColor: 'var(--onb-blue)',
  additionalContent: PaymentForm
};

export default PaymentPage;