import React from 'react';
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
    <div className="bg-gray-800 p-2">
      <div className="text-2xl font-bold">Current Preferences</div>

      {/* Credit Profile */}
      <div className="flex flex-column">
        <Tooltip target=".credit-profile" position="bottom" />
        <div
          className="credit-profile font-bold p-2 bg-gray-600 border-round"
          data-pr-tooltip="Your credit profile informs the types of cards recommended."
        >
          Credit Profile
        </div>
        {credit_profile ? (
          <div className="ml-3">
            <p>Credit Score: {credit_profile.credit_score ?? 'Not specified'}</p>
            <p>Salary: {credit_profile.salary ?? 'Not specified'}</p>
            <p>Lifestyle: {credit_profile.lifestyle ?? 'Not specified'}</p>
          </div>
        ) : (
          <p>No credit profile specified.</p>
        )}
      </div>

      {/* Banks Preferences */}
      {banks_preferences && (
        <div className="flex flex-column">
          <Tooltip target=".banks-preferences" position="bottom" />
          <div
            className="banks-preferences font-bold p-2 bg-gray-600 border-round"
            data-pr-tooltip="These are your bank preferences used in recommendations."
          >
            Banks Preferences
          </div>
          {/* Have Banks */}
          <div className="p-2">
            <div className="text-lg font-bold mb-1">Have Banks</div>
            {banks_preferences.have_banks?.length > 0 ? (
              <ul className="ml-3">
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
            <div className="text-lg font-bold mb-1">Preferred Banks</div>
            {banks_preferences.preferred_banks?.length > 0 ? (
              <ul className="ml-3">
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
              <div className="text-lg font-bold mb-1">Avoid Banks</div>
              <ul className="ml-3">
                {banks_preferences.avoid_banks.map((bank, index) => (
                  <li key={index}>{bank}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Rewards Programs Preferences */}
      {rewards_programs_preferences ? (
        <div className="flex flex-column">
          <Tooltip target=".rewards-preferences" position="bottom" />
          <div
            className="rewards-preferences font-bold p-2 bg-gray-600 border-round"
            data-pr-tooltip="Specifies your preferences for rewards programs."
          >
            Rewards Programs Preferences
          </div>

          {/* Preferred Rewards Programs */}
          {rewards_programs_preferences.preferred_rewards_programs && rewards_programs_preferences.preferred_rewards_programs.length > 0 ? (
            <div className="p-2">
              <div className="text-lg font-bold mb-1">Preferred Rewards Programs</div>
              <ul className="ml-3">
                {rewards_programs_preferences.preferred_rewards_programs.map((program, index) => (
                  <li key={index}>{program}</li>
                ))}
              </ul>
            </div>
          ) : (
            <p>No preferred rewards programs specified.</p>
          )}

          {/* Avoid Rewards Programs */}
          {rewards_programs_preferences.avoid_rewards_programs && rewards_programs_preferences.avoid_rewards_programs.length > 0 ? (
            <div className="p-2">
              <div className="text-lg font-bold mb-1">Avoid Rewards Programs</div>
              <ul className="ml-3">
                {rewards_programs_preferences.avoid_rewards_programs.map((program, index) => (
                  <li key={index}>{program}</li>
                ))}
              </ul>
            </div>
          ) : (
            <p>No rewards programs to avoid specified.</p>
          )}

          {/* If both lists are empty */}
          {(!rewards_programs_preferences.preferred_rewards_programs || rewards_programs_preferences.preferred_rewards_programs.length === 0) &&
           (!rewards_programs_preferences.avoid_rewards_programs || rewards_programs_preferences.avoid_rewards_programs.length === 0) && (
            <p>No rewards programs preferences specified.</p>
          )}
        </div>
      ) : (
        <div className="flex flex-column">
          <Tooltip target=".rewards-preferences" position="bottom" />
          <div
            className="rewards-preferences font-bold p-2 bg-gray-600 border-round"
            data-pr-tooltip="Specifies your preferences for rewards programs."
          >
            Rewards Programs Preferences
          </div>
          <p>No rewards programs preferences specified.</p>
        </div>
      )}

      {/* Consumer Preferences */}
      <div className="flex flex-column">
        <Tooltip target=".consumer-preferences" position="bottom" />
        <div
          className="consumer-preferences font-bold p-2 bg-gray-600 border-round"
          data-pr-tooltip="Your consumer-specific card preferences."
        >
          Consumer Preferences
        </div>
        <p>{consumer_preferences ? JSON.stringify(consumer_preferences) : "No consumer preferences specified."}</p>
      </div>

      {/* Business Preferences */}
      <div className="flex flex-column">
        <Tooltip target=".business-preferences" position="bottom" />
        <div
          className="business-preferences font-bold p-2 bg-gray-600 border-round"
          data-pr-tooltip="Business-specific preferences that guide recommendations."
        >
          Business Preferences
        </div>
        <p>{business_preferences ? JSON.stringify(business_preferences) : "No business preferences specified."}</p>
      </div>
    </div>
  );
};

export default PreferencesDisplay;
