import React, { useState } from 'react';
import { Button } from 'primereact/button';

const getFollowUpContent = (purpose) => {
  const followUps = {
    'BUILD_CREDIT': {
      question: "What's your primary goal with a credit card?",
      options: [
        { label: "Build or improve my credit", value: "Student Starter" },
        { label: "Earn cashback on everyday purchases", value: "Everyday Essentialist" },
        { label: "Start earning points for travel", value: "Beginner Points Traveler" }
      ]
    },
    'MAXIMIZE_REWARDS': {
      question: "What do you value most in a credit card?",
      options: [
        { label: "Earn travel rewards (flights, hotels)", value: "Points Traveler" },
        { label: "Earn cashback on essentials", value: "Cashback Connoisseur" },
        { label: "A mix of rewards and perks", value: "Hybrid User" }
      ]
    },
    'MANAGE_DEBT': {
      question: "Do you currently carry a balance on any cards?",
      options: [
        { label: "Yes", value: "Balance Buster" },
        { label: "No", value: "Balance Buster" }
      ]
    },
    'PREMIUM_PERKS': {
      question: "What's your primary goal with a credit card?",
      options: [
        { label: "Access premium perks (lounges, concierge)", value: "Luxury Seeker" },
        { label: "Maximize points for travel", value: "Travel Hacker" },
        { label: "Optimize rewards for business expenses", value: "Business Boss" }
      ]
    }
  };

  return followUps[purpose] || null;
};

const PurposeFollowUpForm = ({ purpose, onSelect }) => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

  const content = getFollowUpContent(purpose);
  
  if (!content) {
    return <div>Invalid purpose selected</div>;
  }

  const handleToggle = (option) => {
    setSelectedOption(option);
    setShowSuccess(false);
  };

  const handleSubmit = () => {
    setShowSuccess(true);
  };

  if (showSuccess && selectedOption) {
    return (
      <div className="transition-all duration-500 ease-in-out">
        <div className="archetype-display mb-4 text-center">
          <h3 className="text-xl font-semibold">
            Your Archetype:
          </h3>
          <h3 className="text-3xl font-semibold">
            {selectedOption.value}
          </h3>
        </div>
        <Button 
          label="Continue" 
          className="w-full"
          onClick={() => onSelect(selectedOption.value)}
        />
      </div>
    );
  }
  return (
    <div>
      {content.options.map((option) => (
        <div key={option.value} className="mb-3">
          <Button
            label={option.label}
            className={`p-button w-full justify-start ${selectedOption?.label === option.label ? 'selected' : ''}`}
            onClick={() => handleToggle(option)}
          />
        </div>
      ))}
      {selectedOption && (
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

const PurposeFollowUpPage = {
  title: ({ purpose }) => {
    const content = getFollowUpContent(purpose);
    return content?.question || "Let's learn more about your goals";
  },
  content: "Based on your last two answers, we deduce a credit card user archetype for you.",
  primaryColor: 'var(--onb-purple)',
  secondaryColor: 'var(--onb-blue)',
  additionalContent: PurposeFollowUpForm
};

export default PurposeFollowUpPage