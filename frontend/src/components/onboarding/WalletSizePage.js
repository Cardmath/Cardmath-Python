import React, { useState } from 'react';
import { Button } from 'primereact/button';

const WalletSizeForm = ({ onSelect }) => {
  const [selectedSize, setSelectedSize] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

  const options = [
    { label: "0", value: 0 },
    { label: "1", value: 1 },
    { label: "2", value: 2 },
    { label: "3", value: 3 },
    { label: "4", value: 4 },
    { label: "5+", value: 5 }
  ];

  const handleSelect = (option) => {
    setSelectedSize(option);
    setShowSuccess(true);
  };

  if (showSuccess && selectedSize !== null) {
    return (
      <div className="transition-all duration-500 ease-in-out">
        <p className="text-lg mb-6">
          {selectedSize === 0 ? 
            "Perfect time to start your credit journey!" : 
            `Great! We'll help you optimize your ${selectedSize} card${selectedSize === 1 ? '' : 's'} and expand strategically.`}
        </p>
        <Button 
          label="Continue" 
          style={{ width: '100%' }}
          onClick={() => onSelect(selectedSize)}
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
              justifyContent: 'center',
              borderColor: selectedSize === option.value 
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

const WalletSizePage = {
  title: "How many credit cards do you currently own?",
  content: "This helps us understand your current credit profile",
  primaryColor: 'var(--onb-purple)',
  secondaryColor: 'var(--onb-blue)',
  additionalContent: WalletSizeForm
};

export default WalletSizePage;