import React, { useState } from 'react';
import { Ripple } from 'primereact/ripple';
import { Button } from 'primereact/button';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { confirmDialog } from 'primereact/confirmdialog';
import { fetchWithAuth } from './AuthPage';

export default function PricingPage() {
    const [processingError, setProcessingError] = useState(false);
    const handleCheckout = async (product) => {
        try {
            const response = await fetchWithAuth(
                'https://backend-dot-cardmath-llc.uc.r.appspot.com/create_checkout_session', 
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ product: product }),
                }
            );
    
            if (!response.ok) {
                console.error("Error creating checkout session. Please confirm that you are logged in and try again.");
                confirmDialog({
                    message: `The server could not create a checkout session. Please confirm that you are logged in and try again.`,
                    header: 'Error Starting Checkout',
                    icon: 'pi pi-exclamation-triangle',
                    accept: () => {
                        setProcessingError(false);
                        window.location.href = 'https://cardmath.ai/dashboard';
                    },
                    reject: () => {
                        window.location.reload();
                        setProcessingError(false);
                    }
                });
                setProcessingError(true);
                return;
            }
    
            const data = await response.json();
            window.location.href = data.url;
        } catch (error) {
            console.error("Error creating checkout session:", error);
            confirmDialog({
                message: `Error creating checkout session. Please try again.`,
                header: 'Checkout Error',
                icon: 'pi pi-exclamation-triangle',
                accept: () => {
                    setProcessingError(false);
                    window.location.href = 'https://cardmath.ai/dashboard';
                },
                reject: () => {
                    window.location.reload();
                    setProcessingError(false);
                }
            });
            setProcessingError(true);
        }
    };
    

    return (
        <div className="bg-gray-800 min-h-screen text-white">
            <Navbar />
            <div className="px-4 py-8 md:px-6 lg:px-8 bg-no-repeat bg-cover" style={{ background: 'url("/demo/images/blocks/pricing/pricing-4.svg")' }}>
                <div className="flex flex-wrap">
                    <div className="w-full lg:w-6 lg:pr-8">
                        <div className="text-white font-bold text-6xl mb-4">Pricing</div>
                        <div className="text-gray-400 text-xl line-height-3 mb-4 lg:mb-0">Choose the plan that fits your needs and enjoy access to advanced features.</div>
                    </div>
                </div>

                <div className="flex flex-wrap mt-5 -mx-3">
                    {/* Free Plan */}
                    <div className="w-full lg:w-4 p-3">
                        <div className="shadow-2 p-3 h-full bg-gray-700 text-white" style={{ borderRadius: '6px' }}>
                            <div className="font-medium text-xl mb-5">Free Forever</div>
                            <div className="font-bold text-5xl mb-5">Free</div>
                            <button type="button" onClick={() => window.location.href = 'https://cardmath.ai/register'} className="p-ripple font-medium appearance-none border-none p-2 text-white bg-primary hover:bg-primary-dark p-component lg:w-full border-rounded cursor-pointer transition-colors transition-duration-150" style={{ borderRadius: '6px' }}>
                                <span>Create Account</span>
                                <Ripple />
                            </button>
                            <p className="text-sm text-gray-300 line-height-3 mb-0 mt-5">3 computations per month. No consideration of sign on bonus.</p>
                        </div>
                    </div>

                    {/* Monthly Plan */}
                    <div className="w-full lg:w-4 p-3">
                        <div className="shadow-2 p-3 h-full bg-gray-700 text-white" style={{ borderRadius: '6px' }}>
                            <div className="font-medium text-xl mb-5 text-white">Monthly - Flex</div>
                            <div className="flex align-items-center mb-5">
                                <span className="text-white font-bold text-5xl">$10</span>
                                <span className="font-medium text-gray-400 ml-2">per month</span>
                            </div>
                            <Button label="Proceed Monthly" onClick={() => handleCheckout("limited")} icon="pi pi-arrow-right" iconPos="right" className="lg:w-full font-medium p-2 text-white" style={{ backgroundColor: '#007ad9', borderRadius: '6px' }} />
                            <p className="text-sm text-gray-300 line-height-3 mb-0 mt-5">10 computations per month. Consider the sign on bonus of each card. Access to our advanced travel features.</p>
                        </div>
                    </div>

                    {/* Yearly Plan */}
                    <div className="w-full lg:w-4 p-3">
                        <div className="shadow-2 p-3 h-full flex flex-column bg-gray-700 text-white" style={{ borderRadius: '6px' }}>
                            <div className="flex flex-row justify-content-between mb-5 align-items-center">
                                <div className="text-white text-xl font-medium">Yearly - Unlimited</div>
                                <span className="bg-orange-500 text-white font-semibold px-2 py-1 border-round">🎉 Save 50%</span>
                            </div>
                            <div className="flex align-items-center mb-5">
                                <span className="text-white font-bold text-5xl">$60</span>
                                <span className="font-medium text-gray-400 ml-2">per year</span>
                            </div>
                            <Button label="Proceed Yearly" onClick={() => handleCheckout("unlimited")} icon="pi pi-arrow-right" iconPos="right" className="lg:w-full font-medium p-2 text-white" style={{ backgroundColor: '#007ad9', borderRadius: '6px' }} />
                            <p className="text-sm text-gray-300 line-height-3 mb-0 mt-5">Unlimited computations. Consider the sign on bonus of each card. Access to our advanced travel features.</p>
                        </div>
                    </div>
                </div>
            </div>
            <Footer />
        </div>
    );
}
