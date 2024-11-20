import React, { useState } from 'react';
import { Button } from 'primereact/button';
import { confirmDialog } from 'primereact/confirmdialog';
import { fetchWithAuth } from '../pages/AuthPage';

const UsagePlanComponent = ({ onBack }) => {
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
                console.error(
                    'Error creating checkout session. Please confirm that you are logged in and try again.'
                );
                confirmDialog({
                    message: `The server could not create a checkout session. Please confirm that you are logged in and try again.`,
                    header: 'Error Starting Checkout',
                    icon: 'pi pi-exclamation-triangle',
                    accept: () => {
                        setProcessingError(false);
                    },
                    reject: () => {
                        setProcessingError(false);
                    },
                });
                setProcessingError(true);
                return;
            }

            const data = await response.json();
            window.location.href = data.url;
        } catch (error) {
            console.error('Error creating checkout session:', error);
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
                },
            });
            setProcessingError(true);
        }
    };

    return (
        <div>
            <div className="flex pt-6 pb-2 text-white font-bold text-6xl">Pricing</div>
            <div className="text-gray-400 text-xl line-height-3 mb-4 lg:mb-0">
                Unlock Cardmath's full power with two flexible options. Both the Flex and Unlimited
                plans give you unlimited access to our platform's advanced credit card optimization
                features. Maximize your savings and travel rewards every day, worry-free. Start with
                Flex to try it out, or go Unlimited to get the best value and start optimizing your
                spending today.
            </div>
            <div className="flex flex-wrap mt-5 -mx-3">
                {/* Monthly Plan */}
                <div className="w-full lg:w-6 p-3">
                    <div
                        className="shadow-2 p-3 h-full bg-gray-700 text-white"
                        style={{ borderRadius: '6px' }}
                    >
                        <div className="font-medium text-xl mb-5 text-white">Monthly - Flex</div>
                        <div className="flex align-items-center mb-5">
                            <span className="text-white font-bold text-5xl">$10</span>
                            <span className="font-medium text-gray-400 ml-2">per month</span>
                        </div>
                        <Button
                            label="Proceed Monthly"
                            onClick={() => handleCheckout('monthly')}
                            icon="pi pi-arrow-right"
                            iconPos="right"
                            className="lg:w-full font-medium p-2 text-white"
                            style={{ backgroundColor: '#007ad9', borderRadius: '6px' }}
                        />
                        <p className="text-sm text-gray-300 line-height-3 mb-0 mt-5">
                            Perfect for exploring the platform's benefits, with no long-term
                            commitment. Enjoy all the features for just $10 per month.
                        </p>
                    </div>
                </div>

                {/* Yearly Plan */}
                <div className="w-full lg:w-6 p-3">
                    <div
                        className="shadow-2 p-3 h-full flex flex-column bg-gray-700 text-white"
                        style={{ borderRadius: '6px' }}
                    >
                        <div className="flex flex-row justify-content-between mb-5 align-items-center">
                            <div className="text-white text-xl font-medium">Yearly - Unlimited</div>
                            <span className="bg-orange-500 text-white font-semibold px-2 py-1 border-round">
                                🎉 Save 50% Annually Compared to Flex
                            </span>
                        </div>
                        <div className="flex align-items-center mb-5">
                            <span className="text-white font-bold text-5xl">$60</span>
                            <span className="font-medium text-gray-400 ml-2">per year</span>
                        </div>
                        <Button
                            label="Proceed Yearly"
                            onClick={() => handleCheckout('annual')}
                            icon="pi pi-arrow-right"
                            iconPos="right"
                            className="lg:w-full font-medium p-2 text-white"
                            style={{ backgroundColor: '#007ad9', borderRadius: '6px' }}
                        />
                        <p className="text-sm text-gray-300 line-height-3 mb-0 mt-5">
                            Designed for committed users who want ongoing access to every tool and
                            feature, all at a reduced rate of $60 per year.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UsagePlanComponent;
