import React, { useState } from 'react';
import { Button } from 'primereact/button';

const PurposeSelectionForm = ({ onSelect }) => {
  const [selectedPurpose, setSelectedPurpose] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

  const options = [
    { 
      label: "Build credit or get started", 
      icon: "pi pi-graduation-cap",
      value: "BUILD_CREDIT"
    },
    { 
      label: "Maximize rewards", 
      icon: "pi pi-money-bill",
      value: "MAXIMIZE_REWARDS"
    },
    { 
      label: "Manage debt", 
      icon: "pi pi-money-bill",
      value: "MANAGE_DEBT"
    },
    { 
      label: "Access Premium perks", 
      icon: "pi pi-star",
      value: "PREMIUM_PERKS"
    }
  ];

  const messages = {
    "BUILD_CREDIT": "build or improve your credit profile",
    "MAXIMIZE_REWARDS": "earn the most rewards possible on your spending",
    "MANAGE_DEBT": "eliminate your debt with smart credit card choices",
    "PREMIUM_PERKS": "access the best luxury travel and premium card benefits",
  };

  const handleToggle = (option) => {
    setSelectedPurpose(option);
    setShowSuccess(false);
  };

  const handleSubmit = () => {
    setShowSuccess(true);
  };

  if (showSuccess && selectedPurpose) {
    return (
      <div className="transition-all duration-500 ease-in-out">
        <p className="text-lg mb-6">
          That's perfect! We'll help you {messages[selectedPurpose.value]}.
        </p>
        <Button 
          label="Continue" 
          className="w-full"
          onClick={() => onSelect(selectedPurpose.value)}
        />
      </div>
    );
  }

  return (
    <div>
      {options.map((option) => (
        <div key={option.label} className="mb-3">
          <Button
            label={option.label}
            icon={option.icon}
            className={`p-button w-full justify-start ${selectedPurpose?.label === option.label ? 'selected' : ''}`}
            onClick={() => handleToggle(option)}
          />
        </div>
      ))}
      {selectedPurpose && (
        <div className="mt-6">
          <Button 
            label="Submit" 
            className="w-full"
            onClick={handleSubmit}
          />
        </div>
      )}
    </div>
  );
};

const PurposePage = {
  title: "What do you want to get out of your credit cards?",
  primaryColor: 'var(--onb-cyan)',
  secondaryColor: 'var(--onb-blue)',
  additionalContent: PurposeSelectionForm
};

export default PurposePage;
