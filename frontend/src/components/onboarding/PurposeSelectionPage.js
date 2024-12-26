import React, { useState } from 'react';
import { Button } from 'primereact/button';

const PurposeSelectionForm = ({ onSelect }) => {
  const [selectedPurposes, setSelectedPurposes] = useState([]);
  const [showSuccess, setShowSuccess] = useState(false);

  const options = [
    { label: "Travel", icon: "pi pi-globe" },
    { label: "Cash-back", icon: "pi pi-dollar" },
    { label: "Business Expenses", icon: "pi pi-briefcase" },
    { label: "Building Credit", icon: "pi pi-chart-line" },
    { label: "Saving / Investing", icon: "pi pi-wallet" },
    { label: "I don't know yet", icon: "pi pi-question" }
  ];

  const messages = {
    "Travel": "traveling more with optimized rewards",
    "Cash-back": "maximizing your cash back rewards",
    "Business Expenses": "optimizing your business spending",
    "Building Credit": "building a stronger credit profile",
    "Saving / Investing": "growing your wealth through rewards",
    "I don't know yet": "finding the perfect cards for your needs"
  };

  const handleToggle = (option) => {
    setSelectedPurposes(prev => {
      if (prev.includes(option)) {
        return prev.filter(p => p !== option);
      }
      return [...prev, option];
    });
  };

  const handleSubmit = () => {
    setShowSuccess(true);
  };

  if (showSuccess && selectedPurposes.length > 0) {
    const primaryPurpose = selectedPurposes[0];
    return (
      <div className="transition-all duration-500 ease-in-out">
        <p className="text-lg mb-6">
          That's perfect! {messages[primaryPurpose]} - We're going to help you earn 4x more through optimizing your credit cards, and build a strong credit rating
        </p>
        <Button 
          label="Continue" 
          style={{ width: '100%' }}
          onClick={() => onSelect(selectedPurposes)}
        />
      </div>
    );
  }

  return (
    <div>
        {options.map((option) => (
            <div key={option.label}>
                <Button
                    label={option.label}
                    icon={option.icon}
                    className={`p-button ${selectedPurposes.includes(option.label) ? 'selected' : ''}`}
                    onClick={() => handleToggle(option.label)}
                />
            </div>
        ))}
      {selectedPurposes.length > 0 && (
        <div style={{ marginTop: '1.5rem' }}>
          <Button 
            label="Submit" 
            style={{ width: '100%' }}
            onClick={handleSubmit}
          />
        </div>
      )}
    </div>
  );
};

const PurposePage = {
  title: "What can we help you with?",
  content: "Select the option that best matches your goals",
  primaryColor: 'var(--onb-cyan)',
  secondaryColor: 'var(--onb-blue)',
  additionalContent: PurposeSelectionForm
};

export default PurposePage;