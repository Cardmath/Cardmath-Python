import React, { useState, useEffect } from 'react';
import { Steps } from 'primereact/steps';
import VerifyEmailComponent from '../components/VerifyEmailComponent';
import UsagePlanComponent from '../components/UsagePlanComponent';
import TellerConnectComponent from './TellerConnect';
import PreferencesCard from '../components/PreferencesCard';
import { useNavigate, useLocation } from 'react-router-dom';
import { fetchWithAuth } from '../pages/AuthPage';
import { ProgressSpinner } from 'primereact/progressspinner';
import Alert from '../components/Alert'; // Import the Alert component

const RegistrationFlowPage = () => {
    const [activeIndex, setActiveIndex] = useState(0);
    const [paymentError, setPaymentError] = useState(null);
    const [isLoading, setIsLoading] = useState(false); // Loading state for payment verification
    const navigate = useNavigate();
    const location = useLocation();

    // Added alert state
    const [alert, setAlert] = useState({
        visible: false,
        message: '',
        heading: '',
        type: 'error',
    });

    // Steps configuration with labels, icons, descriptions, and custom renderer
    const steps = [
        {
            label: 'Verify Email',
            icon: 'pi pi-envelope',
            description: 'Confirm your email address',
            template: (item, options) => itemRenderer(item, options, 0),
        },
        {
            label: 'Choose Plan',
            icon: 'pi pi-shopping-cart',
            description: 'Select your subscription plan',
            template: (item, options) => itemRenderer(item, options, 1),
        },
        {
            label: 'Connect Bank',
            icon: 'pi pi-credit-card',
            description: 'Link your bank account',
            template: (item, options) => itemRenderer(item, options, 2),
        },
        {
            label: 'Preferences',
            icon: 'pi pi-cog',
            description: 'Set your preferences',
            template: (item, options) => itemRenderer(item, options, 3),
        },
    ];

    // Custom renderer for each step item
    const itemRenderer = (item, options, itemIndex) => {
        const isActiveItem = activeIndex === itemIndex;
        const isCompletedItem = activeIndex > itemIndex;
        const circleStyle = {
            backgroundColor: isActiveItem ? '#007ad9' : isCompletedItem ? '#4CAF50' : '#333333',
            color: '#FFFFFF',
            borderRadius: '50%',
            width: '2.5rem',
            height: '2.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '0.5rem',
        };
        const labelStyle = { fontWeight: isActiveItem ? 'bold' : 'normal', color: '#FFFFFF' };
        const descriptionStyle = {
            fontSize: '0.85rem',
            color: '#FFFFFF',
            textAlign: 'center',
            maxWidth: '6rem',
        };

        return (
            <div className="flex flex-column align-items-center bg-gray-900 p-3 border-round z-1">
                <div style={circleStyle}>
                    <i className={`${item.icon} text-xl`} />
                </div>
                <span style={labelStyle}>{item.label}</span>
                <span style={descriptionStyle}>{item.description}</span>
            </div>
        );
    };

    // Check query params for payment status on mount
    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const sessionId = params.get('session_id');
        const paymentStatus = params.get('payment_status');

        if (sessionId) {
            setIsLoading(true); // Set loading to true while fetching session data
            fetchWithAuth(`https://backend-dot-cardmath-llc.uc.r.appspot.com/get_checkout_session`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (
                        data.payment_status === 'paid' ||
                        data.payment_status === 'no_payment_required'
                    ) {
                        setActiveIndex(2); // Move to the next step on success
                    } else {
                        setPaymentError(
                            'Payment failed. Please try again or use a different payment method.'
                        );
                        setActiveIndex(1); // Stay on 'Choose Plan' step on failure
                    }
                })
                .catch((error) => {
                    console.error('Error fetching checkout session:', error);
                    setPaymentError(
                        'An error occurred while verifying your payment. Please contact support.'
                    );
                })
                .finally(() => setIsLoading(false)); // Set loading to false after fetching completes
        } else if (paymentStatus === 'cancelled') {
            setPaymentError('Payment was cancelled. Please select a plan to continue.');
            setActiveIndex(1); // Stay on 'Choose Plan' step on cancellation
        }
    }, [location.search]);

    // Navigation helper functions with bounds checks
    const nextStep = () =>
        setActiveIndex((prevIndex) => Math.min(prevIndex + 1, steps.length - 1));
    const prevStep = () => setActiveIndex((prevIndex) => Math.max(prevIndex - 1, 0));
    const completeRegistration = () => navigate('/dashboard');

    return (
        <div className="bg-gray-800 w-full h-screen flex justify-content-center text-white">
            <div className="w-full px-4 py-6 md:px-6 lg:px-8">
                <div className="flex flex-column align-items-start justify-content-start">
                    <img
                        src="/logos/svg/Color logo - no background.svg"
                        alt="Logo"
                        className="flex max-w-30rem"
                    />
                </div>

                <div className="mt-5">
                    <Steps model={steps} activeIndex={activeIndex} readOnly className="custom-steps" />

                    {/* Added Alert component */}
                    <Alert
                        visible={alert.visible}
                        message={alert.message}
                        type={alert.type}
                        heading={alert.heading}
                        setVisible={(visible) => setAlert({ ...alert, visible })}
                    />

                    <div className="mt-5">
                        {isLoading && <ProgressSpinner />} {/* Loading spinner while verifying payment */}

                        {paymentError && (
                            <div className="alert alert-danger">{paymentError}</div>
                        )}

                        {/* Step Content Rendering */}
                        {activeIndex === 0 && <VerifyEmailComponent onSuccess={nextStep} />}
                        {activeIndex === 1 && (
                            <UsagePlanComponent onBack={prevStep} onSuccess={nextStep} />
                        )}
                        {activeIndex === 2 && (
                            <TellerConnectComponent onBack={prevStep} onSuccess={nextStep} />
                        )}
                        {activeIndex === 3 && (
                            <PreferencesCard
                                onBack={prevStep}
                                onSuccess={completeRegistration}
                                setAlert={setAlert} // Passed setAlert prop
                            />
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RegistrationFlowPage;
