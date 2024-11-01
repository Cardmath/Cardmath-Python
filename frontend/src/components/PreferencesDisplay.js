import React from 'react';
import { Card } from 'primereact/card';
import { Tooltip } from 'primereact/tooltip';
import 'primeflex/primeflex.css';

const PreferencesDisplay = ({ preferences }) => {
  const {
    credit_profile,
    banks_preferences,
    rewards_programs_preferences,
    consumer_preferences,
    business_preferences,
  } = preferences;

  return (
    <div className="bg-gray-200 p-2">
      <div className="text-2xl font-bold">Current Preferences</div>

      {/* Credit Profile */}
      <div className="flex flex-column">
        <Tooltip target=".credit-profile" position="bottom"/>
        <h3 className="credit-profile p-2 bg-blue-100 border-round" data-pr-tooltip="Your credit profile informs the types of cards recommended.">
          Credit Profile
        </h3>
        <p>{credit_profile || "No credit profile specified."}</p>
      </div>

      {/* Banks Preferences */}
      {banks_preferences && (
        <div className="flex flex-column">
          <Tooltip target=".banks-preferences" position="bottom"/>
          <h3 className="banks-preferences p-2 bg-blue-100 border-round" data-pr-tooltip="These are your bank preferences used in recommendations.">
            Banks Preferences
          </h3>
          
          {/* Have Banks */}
          <div className="p-2">
            <h4 className="mb-1">Have Banks</h4>
            {banks_preferences.have_banks?.length ? (
              <ul>
                {banks_preferences.have_banks.map((bank, index) => (
                  <li key={index}>{bank}</li>
                ))}
              </ul>
            ) : (
              <p>No specific banks listed under 'Have Banks'.</p>
            )}
          </div>

          {/* Preferred Banks */}
          <div className="p-2">
            <h4 className="mb-1">Preferred Banks</h4>
            {banks_preferences.preferred_banks ? (
              <ul>
                {banks_preferences.preferred_banks.map((bank, index) => (
                  <li key={index}>{bank}</li>
                ))}
              </ul>
            ) : (
              <p>No preferred banks specified.</p>
            )}
          </div>

          {/* Avoid Banks */}
          {banks_preferences.avoid_banks?.length > 0 && (
            <div className="p-2">
              <h4 className="mb-1">Avoid Banks</h4>
              <ul>
                {banks_preferences.avoid_banks.map((bank, index) => (
                  <li key={index}>{bank}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Rewards Programs Preferences */}
      <div className="flex flex-column mb-3">
        <Tooltip target=".rewards-preferences" position="bottom"/>
        <h3 className="rewards-preferences p-2 bg-blue-100 border-round" data-pr-tooltip="Specifies your preferences for rewards programs.">
          Rewards Programs Preferences
        </h3>
        <p>{rewards_programs_preferences ? JSON.stringify(rewards_programs_preferences) : "No rewards programs preferences specified."}</p>
      </div>

      {/* Consumer Preferences */}
      <div className="flex flex-column mb-3">
        <Tooltip target=".consumer-preferences" position="bottom"/>
        <h3 className="consumer-preferences p-2 bg-blue-100 border-round" data-pr-tooltip="Your consumer-specific card preferences.">
          Consumer Preferences
        </h3>
        <p>{consumer_preferences ? JSON.stringify(consumer_preferences) : "No consumer preferences specified."}</p>
      </div>

      {/* Business Preferences */}
      <div className="flex flex-column mb-3">
        <Tooltip target=".business-preferences" position="bottom"/>
        <h3 className="business-preferences p-2 bg-blue-100 border-round" data-pr-tooltip="Business-specific preferences that guide recommendations.">
          Business Preferences
        </h3>
        <p>{business_preferences ? JSON.stringify(business_preferences) : "No business preferences specified."}</p>
      </div>
    </div>
  );
};

export default PreferencesDisplay;
