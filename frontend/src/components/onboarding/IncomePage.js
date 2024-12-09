import React, { useState } from 'react';
import { Button } from 'primereact/button';

const IncomeSelectionForm = ({ onSelect }) => {
  const [selectedIncome, setSelectedIncome] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

  const options = [
    { label: "Less than $50,000", value: "under_50k" },
    { label: "$50,000 - $75,000", value: "50k_75k" },
    { label: "$75,000 - $100,000", value: "75k_100k" },
    { label: "$100,000+", value: "over_100k" }
  ];

  const handleSelect = (option) => {
    setSelectedIncome(option);
    setShowSuccess(true);
  };

  if (showSuccess && selectedIncome) {
    return (
      <div className="transition-all duration-500 ease-in-out">
        <p className="text-lg mb-6">
          Got it! We'll recommend cards that match your income level.
        </p>
        <Button 
          label="Continue" 
          style={{ width: '100%' }}
          onClick={() => onSelect(selectedIncome)}
        />
      </div>
    );
  }

  return (
    <div>
      {options.map((option) => (
        <div key={option.label} style={{ marginBottom: '0.5rem' }}>
          <Button
            label={option.label}
            variant="outlined"
            style={{
              width: '100%', 
              justifyContent: 'flex-start',
              borderColor: selectedIncome === option.value 
                ? 'rgba(255, 255, 255, 0.4)' 
                : 'rgba(255, 255, 255, 0.2)'
            }}
            onClick={() => handleSelect(option.value)}
          />
        </div>
      ))}
    </div>
  );
};

const IncomePage = {
  title: "What's your approximate annual income?",
  content: "This helps us recommend cards you're more likely to be approved for",
  primaryColor: 'var(--onb-orange)',
  secondaryColor: 'var(--onb-pink)',
  additionalContent: IncomeSelectionForm
};

export default IncomePage;