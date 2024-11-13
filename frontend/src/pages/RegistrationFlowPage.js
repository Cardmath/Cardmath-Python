import React, { useState } from 'react';
import { Steps } from 'primereact/steps';
import VerifyEmailComponent from '../components/VerifyEmailComponent';
import UsagePlanComponent from '../components/UsagePlanComponent';
import { useNavigate } from 'react-router-dom';

const RegistrationFlowPage = () => {
    const [activeIndex, setActiveIndex] = useState(0);
    const navigate = useNavigate();

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
        // Add more steps here when extending to four stages
    ];

    const itemRenderer = (item, options, itemIndex) => {
        const isActiveItem = activeIndex === itemIndex;
        const isCompletedItem = activeIndex > itemIndex;
        const circleStyle = {
            backgroundColor: isActiveItem
                ? '#007ad9' // Active item color
                : isCompletedItem
                ? '#4CAF50' // Completed item color
                : '#333333', // Inactive item color
            color: '#FFFFFF', // Icon color for all states
            borderRadius: '50%',
            width: '2.5rem',
            height: '2.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '0.5rem',
        };
    
        const labelStyle = {
            fontWeight: isActiveItem ? 'bold' : 'normal',
            color: '#FFFFFF', // Explicit white text color for label
        };
    
        const descriptionStyle = {
            fontSize: '0.85rem',
            color: '#FFFFFF', // Explicit white text color for description
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
    
    // Function to proceed to the next step
    const nextStep = () => {
        setActiveIndex((prevIndex) => prevIndex + 1);
    };

    // Function to go back to the previous step
    const prevStep = () => {
        setActiveIndex((prevIndex) => prevIndex - 1);
    };

    return (
        <div className="bg-gray-800 min-h-screen text-white">
            <div
                className="px-4 py-6 md:px-6 lg:px-8 bg-no-repeat bg-cover"
                style={{ background: 'url("/demo/images/blocks/pricing/pricing-4.svg")' }}
            >
                <div className="flex flex-column align-items-start justify-content-start">
                    <img
                        src="/logos/svg/Color logo - no background.svg"
                        alt="Logo"
                        className="flex max-w-30rem"
                    />
                </div>

                <div className="card mt-5">
                    <Steps
                        model={steps}
                        activeIndex={activeIndex}
                        readOnly
                        className="custom-steps"
                    />

                    <div className="mt-4">
                        {activeIndex === 0 && <VerifyEmailComponent onSuccess={nextStep} />}
                        {activeIndex === 1 && (
                            <UsagePlanComponent onBack={prevStep} onSuccess={nextStep} />
                        )}
                        {/* Add more components for additional steps */}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RegistrationFlowPage;
