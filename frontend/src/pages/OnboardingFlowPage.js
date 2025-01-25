import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchWithAuth } from '../pages/AuthPage';
import { getBackendUrl } from '../utils/urlResolver';
import NameInputPage from '../components/onboarding/NameInputPage';
import PurposePage from '../components/onboarding/PurposePage';
import PurposeFollowUpPage from '../components/onboarding/PurposeFollowUpPage';
import IncomePage from '../components/onboarding/IncomePage';
import CreditScorePage from '../components/onboarding/CreditScorePage';
import BankConnectionPage from '../components/onboarding/BankConnectionPage';
import PaymentPage from '../components/onboarding/PaymentPage';
import "../components/onboarding/onboarding.css";
import WalletSizePage from '../components/onboarding/WalletSizePage';

const MobileWarning = () => {
  const navigate = useNavigate();
  const [countdown, setCountdown] = useState(5);

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          navigate('/');
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 text-center bg-gray-800">
      <div className="max-w-md space-y-4">
        <h1 className="text-2xl font-bold text-white">Mobile Experience Coming Soon</h1>
        <p className="text-gray-300">
          Cardmath is not yet optimized for mobile devices. Please check back in a few weeks. 
          We apologize for any inconvenience caused.
        </p>
        <p className="text-sm text-gray-500">
          Redirecting in {countdown} seconds...
        </p>
      </div>
    </div>
  );
};

const OnboardingFlow = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [formData, setFormData] = useState({
    name: '',
    archetype: '',
    wallet_size: -1,
    income: '',
    credit_score: '',
    user_bio: ''
  });
  const [isMobile, setIsMobile] = useState(false);
  const [contactInfo, setContactInfo] = useState(null);
  const [accounts, setAccounts] = useState(null);
  const [preferredAccount, setPreferredAccount] = useState({preferred: null, confirmed: false}); 
  const [solution, setSolution] = useState(null);
  const [dateRange, setDateRange] = useState(null);
  const [computationLoading, setComputationLoading] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    handleTransition(0);
    
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

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

  const handleCheckout = async (product) => {
    try {
      const response = await fetchWithAuth(
        `${getBackendUrl()}/create_checkout_session`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ product })
        }
      );
  
      if (!response.ok) {
        console.error('Checkout session creation failed');
        window.location.reload();
        return;
      }
  
      const data = await response.json();
      window.location.href = data.url;
      
    } catch (error) {
      console.error('Checkout error:', error);
      window.location.href = '/dashboard';
    }
  };

  const computeOptimalAllocation = async (use_mock) => {
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
              credit_score: 3,
              use_mock: use_mock,
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

  const handleBioSubmit = async (bio) => {
    const response = await fetchWithAuth(
      `${getBackendUrl()}/process-onboarding-enrollment`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          teller_connect_response: null,
          answers: {
            ...formData,
            use_mock: true,
            wallet_size: parseInt(formData.wallet_size, 10), // Ensure integer type
            user_bio: bio
          },  
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
    const solution = await computeOptimalAllocation(true);
    setSolution(solution.solutions[0]);
    setDateRange(solution.timeframe);
  }

  const handleTellerEnrollment = async (enrollment) => {
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
      
      if (!data.token) {
        throw new Error('No token found in response');
      }
      localStorage.setItem('cardmath_access_token', data.token);

      if (data.contact) {
        setContactInfo(data.contact);
      }

      if (data.accounts) {
        setAccounts(data.accounts);
      }

      // Compute the recommendation
      const solution = await computeOptimalAllocation(false);
      setSolution(solution.solutions[0]);
      setDateRange(solution.timeframe);
    } catch (error) {
      console.error('Error processing enrollment:', error);
      throw error;
    }
  };

  const handleFormSubmit = (field, value, nextIndex) => {
    if (field && value) {
      setFormData(prev => ({ ...prev, [field]: value }));
    }
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
      return response
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
      additionalContent: <PurposePage.additionalContent 
        onSelect={(purpose) => handleFormSubmit('purpose', purpose, 2)}
      />
    },
    {
      ...PurposeFollowUpPage,
      title: PurposeFollowUpPage.title({ purpose: formData.purpose }),
      additionalContent: <PurposeFollowUpPage.additionalContent 
        purpose={formData.purpose}
        onSelect={(archetype) => handleFormSubmit('archetype', archetype, 3)}
      />
    },
    {
      ...WalletSizePage,
      additionalContent: <WalletSizePage.additionalContent 
        onSelect={(size) => handleFormSubmit('wallet_size', size, 4)}
      />
    },
    {
      ...CreditScorePage,
      additionalContent: <CreditScorePage.additionalContent 
        onSelect={(score) => handleFormSubmit('credit_score', score, 5)}
      />
    },
    {
      ...IncomePage,
      additionalContent: <IncomePage.additionalContent 
        onSelect={(income) => handleFormSubmit('income', income, 6)}
      />
    },
    {
      ...BankConnectionPage,
      additionalContent: <BankConnectionPage.additionalContent 
        onSelect={(contactInfo) => handleFormSubmit('contactInfo', contactInfo, 7)}
        handleEnrollment={handleTellerEnrollment}
        handleBioSubmit={handleBioSubmit}
        handlePrimaryEmail={handlePrimaryEmail}
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
        preferredAccount={preferredAccount}
        handleCheckout={handleCheckout}
      />
    }
  ];

  if (isMobile) {
    return <MobileWarning />;
  }

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