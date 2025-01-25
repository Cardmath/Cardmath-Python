import React, { useState } from 'react';
import { Button } from 'primereact/button';

const CreditScoreForm = ({ onSelect }) => {
  const [selectedScore, setSelectedScore] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

  const options = [
    { label: "Less than 629", subLabel: "Poor", value: "Bad" },
    { label: "630 - 689", subLabel: "Fair", value: "Fair" },
    { label: "690 - 719", subLabel: "Good", value: "Good" },
    { label: "720 - 850", subLabel: "Excellent", value: "Excellent" }
  ];

  const handleSelect = (option) => {
    setSelectedScore(option);
    setShowSuccess(true);
  };

  if (showSuccess && selectedScore) {
    const messages = {
      poor: "Don't worry! We'll help you build your credit score with the right strategy.",
      fair: "Good start! We'll help you reach the next credit tier.",
      good: "Nice! You're in a great position to qualify for premium rewards.",
      excellent: "Excellent! You'll have access to the best cards available."
    };

    return (
      <div className="transition-all duration-500 ease-in-out">
        <p className="text-lg mb-6">
          {messages[selectedScore]}
        </p>
        <Button 
          label="Continue" 
          style={{ width: '100%' }}
          onClick={() => onSelect(selectedScore)}
        />
      </div>
    );
  }

  return (
    <div>
      {options.map((option) => (
        <div key={option.label} style={{ marginBottom: '0.5rem' }}>
          <Button
            label={
              <div className="flex flex-col items-start">
                <span>{option.label} - {option.subLabel}</span>
              </div>
            }
            variant="outlined"
            style={{
              width: '100%', 
              justifyContent: 'flex-start',
              borderColor: selectedScore === option.value 
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

const CreditScorePage = {
  title: "What's your approximate credit score?",
  content: "Don't worry if you're not sure - you can always update this later",
  primaryColor: 'var(--onb-pink)',
  secondaryColor: 'var(--onb-purple)',
  additionalContent: CreditScoreForm
};

export default CreditScorePage;