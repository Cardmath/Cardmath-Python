import React, { useState, useEffect } from 'react';
import { fetchWithAuth } from '../pages/AuthPage';
import { getBackendUrl } from '../utils/urlResolver';
import NameInputPage from '../components/onboarding/NameInputPage';
import PurposePage from '../components/onboarding/PurposeSelectionPage';
import WalletSizePage from '../components/onboarding/WalletSizePage';
import IncomePage from '../components/onboarding/IncomePage';
import CreditScorePage from '../components/onboarding/CreditScorePage';
import BankConnectionPage from '../components/onboarding/BankConnectionPage';
import PaymentPage from '../components/onboarding/PaymentPage';
import "../components/onboarding/onboarding.css";

const OnboardingFlow = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [formData, setFormData] = useState({
    name: '',
    purpose: '',
    walletSize: '',
    income: '',
    creditScore: ''
  });
  const [contactInfo, setContactInfo] = useState(null);
  const [accounts, setAccounts] = useState(null);
  const [preferredAccount, setPreferredAccount] = useState({preferred: null, confirmed: false}); 
  const [emailProcessed, setEmailProcessed] = useState(false);
  const [solution, setSolution] = useState(null);
  const [dateRange, setDateRange] = useState(null);
  const [computationLoading, setComputationLoading] = useState(false);

  useEffect(() => {
    handleTransition(0);
  }, []);

  const handleTransition = (nextIndex) => {
    const container = document.querySelector('.onboarding-container');
    container.querySelectorAll('[data-active]').forEach(el => {
      el.removeAttribute('data-active');
    });

    const articles = container.querySelectorAll('.content article');
    const backgrounds = container.querySelectorAll('.background');
    articles[nextIndex].setAttribute('data-active', true);
    backgrounds[nextIndex].setAttribute('data-active', true);
    
    setActiveIndex(nextIndex);
  };

  const computeOptimalAllocation = async () => {
    setComputationLoading(true);
    try {
      const response = await fetchWithAuth(
        `${getBackendUrl()}/compute-onboarding-savings`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            answers: {
              num_cards: 4,
              credit_score: 3
            },
          })
        }
      );

      if (!response.ok) {
        throw new Error('Failed to compute optimal allocation');
      }

      const data = await response.json();
      console.log('Optimal allocation computed:', data);
      setSolution(data);
      return data;
    } catch (error) {
      console.error('Error computing optimal allocation:', error);
      throw error;
    } finally {
      setComputationLoading(false);
    }
  };

  const handleEnrollment = async (enrollment) => {
    try {
      console.log('Processing enrollment:', enrollment);
      const response = await fetchWithAuth(
        `${getBackendUrl()}/process-onboarding-enrollment`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            teller_connect_response: enrollment,
            answers: formData,
          }),
        }
      );
      
      if (!response.ok) throw new Error('Failed to process enrollment');
      
      const data = await response.json();
      
      // onboarding token necessary to authenticate the session
      if (!data.token) {
        throw new Error('No token found in response');
      }
      localStorage.setItem('cardmath_access_token', data.token);

      // to give the user primary email options
      if (data.contact) {
        setContactInfo(data.contact);
      }

      // To give the user payment account options
      if (data.accounts) {
        setAccounts(data.accounts);
      }

      // Compute the recommendation
      const solution = await computeOptimalAllocation(data.token);
      setSolution(solution.solutions[0]);
      setDateRange(solution.timeframe);
    } catch (error) {
      console.error('Error processing enrollment:', error);
      throw error;
    }
  };

  const handleFormSubmit = (field, value, nextIndex) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (nextIndex !== undefined) {
      handleTransition(nextIndex);
    }
  };

  const handlePrimaryEmail = async (primary_email) => {
    const response = await fetchWithAuth(
    `${getBackendUrl()}/ingest-onboarding-primary-email`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            first_name: formData.name,
            primary_email: primary_email
          }),
        }
      )
    if (response.ok) {
      setEmailProcessed(true)
    }
  }

  const pages = [
    {
      ...NameInputPage,
      additionalContent: <NameInputPage.additionalContent 
        onSubmit={(name) => handleFormSubmit('name', name, 1)} 
      />
    },
    {
      ...PurposePage,
      title: `Nice to meet you, ${formData.name}! What can we help you with?`,
      additionalContent: <PurposePage.additionalContent 
        onSelect={(purpose) => handleFormSubmit('purpose', purpose, 2)}
      />
    },
    {
      ...WalletSizePage,
      additionalContent: <WalletSizePage.additionalContent 
        onSelect={(size) => handleFormSubmit('walletSize', size, 3)}
      />
    },
    {
      ...IncomePage,
      additionalContent: <IncomePage.additionalContent 
        onSelect={(income) => handleFormSubmit('income', income, 4)}
      />
    },
    {
      ...CreditScorePage,
      additionalContent: <CreditScorePage.additionalContent 
        onSelect={(score) => handleFormSubmit('creditScore', score, 5)}
      />
    },
    {
      ...BankConnectionPage,
      additionalContent: <BankConnectionPage.additionalContent 
        onSelect={(score) => handleFormSubmit('contactInfo', contactInfo, 6)}
        handleEnrollment={handleEnrollment}
        handlePrimaryEmail={handlePrimaryEmail}
        emailProcessed={emailProcessed}
        solution={solution}
        dateRange={dateRange}
        contactInfo={contactInfo}
        accounts={accounts}
        preferredAccount={preferredAccount}
        setPreferredAccount={setPreferredAccount}
      />
    },
    {
      ...PaymentPage,
      additionalContent: <PaymentPage.additionalContent 
      onPaymentComplete={(score) => handleFormSubmit('creditScore', score, 5)}
      preferredAccount={preferredAccount}
      />
    }
  ];

  return (
    <div className="onboarding-container">
      <svg className="goo-filter" viewBox="0 0 1 1">
        <filter id="goo">
          <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
          <feColorMatrix 
            in="blur" 
            mode="matrix" 
            values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 50 -20" 
            result="goo" 
          />
        </filter>
      </svg>

      <div className="app-container">
        <section className="backgrounds">
          {pages.map((page, index) => (
            <div
              key={`bg-${index}`}
              className="background"
              style={{
                '--primary': page.primaryColor,
                '--secondary': page.secondaryColor
              }}
            />
          ))}
        </section>

        <section className="content">
          {pages.map((page, index) => (
            <article
              key={`content-${index}`}
            >
              <header>
                <h1>{page.title}</h1>
              </header>
              <p>{typeof page.content === 'function' ? page.content(formData) : page.content}</p>
              {page.additionalContent}
            </article>
          ))}
        </section>
      </div>
    </div>
  );
};

export default OnboardingFlow;