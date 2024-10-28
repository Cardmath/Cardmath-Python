import React, { useEffect, useState } from 'react';
import { Card } from 'primereact/card';
import { fetchWithAuth } from '../pages/AuthPage';
import { InputNumber } from 'primereact/inputnumber';
import { InputSwitch } from 'primereact/inputswitch';
import { Button } from 'primereact/button';
import { Carousel } from 'primereact/carousel';
import moment from 'moment';

import CreditCardItemTemplate from './CreditCardItemTemplate';

const OptimalAllocationSavingsCard = () => {
  // Existing state variables
  const [allTimeSavings, setAllTimeSavings] = useState(0);
  const [lastMonthSavings, setLastMonthSavings] = useState(0);

  const [toAdd, setToAdd] = useState(2);
  const [toUse, setToUse] = useState(4);

  const [useSignOnBonus, setUseSignOnBonus] = useState(false);

  const [cardsHeld, setCardsHeld] = useState([]);
  const [recommendedCards, setRecommendedCards] = useState([]);

  const [recommendedCardsBonusTotal, setRecommendedCardsBonusTotal] = useState(0);
  const [recommendedCardsLastMonthSavings, setRecommendedCardsLastMonthSavings] = useState(0);

  const [numRecommendedCards, setNumRecommendedCards] = useState(0);
  const [tolerance, setTolerance] = useState(5);

  // New state variables for the additional data
  const [summary, setSummary] = useState([]);
  const [spendingPlan, setSpendingPlan] = useState([]);
  const [actionableSteps, setActionableSteps] = useState([]);
  const [totalRegularRewards, setTotalRegularRewards] = useState(0);
  const [totalSignOnBonus, setTotalSignOnBonus] = useState(0);
  const [totalAnnualFees, setTotalAnnualFees] = useState(0);
  const [netRewards, setNetRewards] = useState(0);

  // New state variables for the current wallet data
  const [netRewardsCurrent, setNetRewardsCurrent] = useState(0);
  const [totalRegularRewardsCurrent, setTotalRegularRewardsCurrent] = useState(0);
  const [totalSignOnBonusCurrent, setTotalSignOnBonusCurrent] = useState(0);
  const [totalAnnualFeesCurrent, setTotalAnnualFeesCurrent] = useState(0);

  // Variable to store the difference in net rewards
  const netRewardsDifference = (netRewards - netRewardsCurrent).toFixed(2);

  // Fetch user's current card rewards (All-time)
  useEffect(() => {
    if (cardsHeld.length > 0) {
      fetchWithAuth('http://localhost:8000/compute_optimal_allocation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to_use: cardsHeld.length,
          to_add: 0,
          use_sign_on_bonus: useSignOnBonus, // Match the sign-on bonus setting
          save_to_db: false,
          timeframe: null,
          return_cards_used: true,
        })
      })
        .then(response => response.json())
        .then(data => {
          setAllTimeSavings(data.total_reward_usd);
          // Set current wallet data
          setNetRewardsCurrent(data.net_rewards_usd);
          setTotalRegularRewardsCurrent(data.total_regular_rewards_usd);
          setTotalSignOnBonusCurrent(data.total_sign_on_bonus_usd);
          setTotalAnnualFeesCurrent(data.total_annual_fees_usd);
        })
        .catch(error => console.log(error));
    }
  }, [cardsHeld, useSignOnBonus]); // Add useSignOnBonus to dependencies

  // Fetch user's current card rewards (Last month)
  useEffect(() => {
    if (cardsHeld.length > 0) {
      fetchWithAuth('http://localhost:8000/compute_optimal_allocation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to_use: cardsHeld.length,
          to_add: 0,
          timeframe: {
            start_month: moment().subtract(1, 'months').startOf('month').format('YYYY-MM-DD'),
            end_month: moment().startOf('month').format('YYYY-MM-DD')
          },
          save_to_db: false,
          return_cards_used: true,
        })
      })
        .then(response => response.json())
        .then(data => setLastMonthSavings(data.total_reward_usd))
        .catch(error => console.error('Error fetching savings data:', error));
    }
  }, [cardsHeld]);

  // Fetch recommended allocation
  const fetchOptimalAllocation = async (toUse, toAdd, useSignOnBonus) => {
    try {
      const response = await fetchWithAuth('http://localhost:8000/compute_optimal_allocation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to_use: toUse,
          to_add: toAdd,
          timeframe: null,
          use_sign_on_bonus: useSignOnBonus,
          return_cards_added: true,
          return_cards_used: true,
          save_to_db: false
        })
      });
      const data = await response.json();
      setRecommendedCards(data.cards_added);
      setRecommendedCardsBonusTotal(data.total_reward_usd);

      // Set new data from the API response
      setSummary(data.summary);
      setSpendingPlan(data.spending_plan);
      setActionableSteps(data.actionable_steps);
      setTotalRegularRewards(data.total_regular_rewards_usd);
      setTotalSignOnBonus(data.total_sign_on_bonus_usd);
      setTotalAnnualFees(data.total_annual_fees_usd);
      setNetRewards(data.net_rewards_usd);
    } catch (error) {
      console.error('Error fetching savings data:', error);
    }
  };

  useEffect(() => {
    fetchOptimalAllocation(toUse, toAdd, useSignOnBonus);
  }, []);

  // Fetch recommended cards last month's savings
  useEffect(() => {
    fetchWithAuth('http://localhost:8000/compute_optimal_allocation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        to_use: toUse,
        to_add: toAdd,
        timeframe: {
          start_month: moment().subtract(1, 'months').startOf('month').format('YYYY-MM-DD'),
          end_month: moment().startOf('month').format('YYYY-MM-DD')
        },
        save_to_db: false
      })
    })
      .then(response => response.json())
      .then(data => setRecommendedCardsLastMonthSavings(data.total_reward_usd))
      .catch(error => console.error('Error fetching savings data:', error));
  }, [cardsHeld]);

  // Fetch user's held cards
  useEffect(() => {
    fetchWithAuth('http://localhost:8000/read_user_held_cards', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => response.json())
      .then(data => {
        setCardsHeld(data.credit_card);
      })
      .catch(error => console.log(error));
  }, []);

  return (
    <Card className="w-full h-full justify-content-center align-items-stretch flex-wrap border-round shadow-2 mt-2">
      {/* Display net rewards difference */}
      <div className="flex gap-2 justify-content-center">
        <div className="col-10 border-round shadow-3">
          <div className="grid align-items-center justify-content-center py-2">
            Potential Increase in Net Rewards with Recommended Cards:
          </div>
          {cardsHeld.length === 0 ? (
            <div className='text-red-400 text-xl text-center p-2'>
              No cards detected. Unable to compute potential increase in net rewards.
            </div>
          ) : (
            <div className="font-bold text-3xl grid justify-content-center pb-1 text-green-600">
              ${netRewardsDifference}
            </div>
          )}
        </div>
      </div>

      {/* Display total rewards and net rewards */}
      <div className="flex pt-4 gap-2 justify-content-center">
        <div className="col-5 border-round shadow-3">
          <div className="grid align-items-center justify-content-center py-2">Current Wallet Net Rewards:</div>
          <div className="font-bold text-2xl grid justify-content-center pb-1">${netRewardsCurrent}</div>
        </div>
        <div className="col-5 border-round shadow-3">
          <div className="grid align-items-center justify-content-center py-2">Recommended Wallet Net Rewards:</div>
          <div className="font-bold text-2xl grid justify-content-center pb-1">${netRewards}</div>
        </div>
      </div>

      {/* Display total regular rewards and annual fees */}
      <div className="flex pt-2 gap-2 justify-content-center">
        {/* Current Wallet */}
        <div className="col-5 border-round shadow-3">
          <div className="grid justify-content-center py-2">Current Wallet Regular Rewards</div>
          <div className="font-bold text-2xl grid justify-content-center pb-1">${totalRegularRewardsCurrent}</div>
          <div className="grid justify-content-center py-2">Current Wallet Annual Fees</div>
          <div className="font-bold text-2xl grid justify-content-center pb-1">${totalAnnualFeesCurrent}</div>
        </div>
        {/* Recommended Wallet */}
        <div className="col-5 border-round shadow-3">
          <div className="grid justify-content-center py-2">Recommended Wallet Regular Rewards</div>
          <div className="font-bold text-2xl grid justify-content-center pb-1">${totalRegularRewards}</div>
          <div className="grid justify-content-center py-2">Recommended Wallet Annual Fees</div>
          <div className="font-bold text-2xl grid justify-content-center pb-1">${totalAnnualFees}</div>
        </div>
      </div>

      {/* Input controls and compute button */}
      <div className="flex pt-4 gap-2 h-full justify-content-center">
        <div className="col-3">
          {/* Existing controls */}
          <div className='bg-gray-200 mt-3 pt-1 pb-2 px-2 border-round shadow-2'>
            <p className='font-italic'>
              Select your desired total wallet size and the number of new cards you're considering. Based on these inputs, we'll recommend new cards while factoring in the possibility of canceling some of your current cards to optimize your rewards and benefits.
            </p>
            <div id="toUseInput" className="p-float-label">Desired Wallet Size</div>
            <InputNumber aria-labelledby='toUseInput' showButtons inputId="integeronly" className="w-full" value={toUse} onChange={e => setToUse(e.value)} min={1} max={5} />

            <div id="toAddInput" className="p-float-label mt-2">Number of Desired New Cards</div>
            <InputNumber aria-labelledby='toAddInput' showButtons inputId="integeronly" className="w-full" value={toAdd} onChange={e => setToAdd(e.value)} min={0} max={5} />
          </div>

          <div className='bg-gray-200 mt-3 pt-1 pb-2 px-2 border-round shadow-2'>
            <p className='font-italic'>
              Include sign-on bonuses to highlight cards with high short-term value. Disabling this will give a clearer picture of long-term rewards, helping you choose a card that's more beneficial over time.
            </p>
            <span id="switch1" className="p-float-label mt-2">Consider Sign on Bonus in Calculation</span>
            <InputSwitch className="align-self-center" aria-labelledby='switch1' checked={useSignOnBonus} onChange={e => setUseSignOnBonus(e.value)} />
          </div>

          <Button onClick={() => {
            fetchOptimalAllocation(toUse, toAdd, useSignOnBonus);
            // Re-fetch current wallet data to match sign-on bonus setting
            if (cardsHeld.length > 0) {
              fetchWithAuth('http://localhost:8000/compute_optimal_allocation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  to_use: cardsHeld.length,
                  to_add: 0,
                  use_sign_on_bonus: useSignOnBonus,
                  save_to_db: false,
                  timeframe: null,
                  return_cards_used: true,
                })
              })
                .then(response => response.json())
                .then(data => {
                  setNetRewardsCurrent(data.net_rewards_usd);
                  setTotalRegularRewardsCurrent(data.total_regular_rewards_usd);
                  setTotalSignOnBonusCurrent(data.total_sign_on_bonus_usd);
                  setTotalAnnualFeesCurrent(data.total_annual_fees_usd);
                })
                .catch(error => console.log(error));
            }
          }} className='w-full mt-5' label="Compute" />
        </div>

        {/* Display carousels and spending plan */}
        <div className="col-8 grid">
          {/* Carousels */}
          <div className="col-12 grid flex justify-content-center align-items-start">
    {/* Your Cards Carousel */}
    <div className="col-6">
      <div className="text-3xl pb-2 text-center">Your Cards</div>
      {cardsHeld.length === 0 ? (
        <Card title="No Credit Cards detected" className="w-9 py-3 bg-pink-200 border-3 shadow-2 surface-border border-round">
          <p className="m-0">We couldn't detect any credit cards associated with your account.</p>
        </Card>
      ) : (
        <Carousel
          value={cardsHeld}
          numVisible={1}
          numScroll={1}
          itemTemplate={(e) => <CreditCardItemTemplate sizingCss="w-full" cardData={e} />}
          className="w-full"
          contentClassName="w-full"
          containerClassName="w-full"
        />
      )}
    </div>

            {/* Recommended Cards Carousel */}
                  <div className="col-6">
            <div className="text-3xl pb-2 text-center">Recommended Cards</div>
            {recommendedCards.length === 0 ? (
              <Card title="No Recommended Cards" className="w-9 py-3 bg-yellow-200 border-3 shadow-2 surface-border border-round">
                <p className="m-0">No recommended cards based on your preferences.</p>
              </Card>
            ) : (
              <Carousel
                value={recommendedCards}
                numVisible={1}
                numScroll={1}
                itemTemplate={(e) => <CreditCardItemTemplate sizingCss="w-full" cardData={e} />}
                className="w-full"
                contentClassName="w-full"
                containerClassName="w-full"
              />
            )}
          </div>
          </div>

          {/* Sign-On Bonus Rewards Table */}
          <div className="col-12 mt-4 shadow-2 border-round bg-gray-200">
            <div className="text-3xl pb-2 text-center">Sign-On Bonus Rewards for New Cards</div>
            {summary && summary.length > 0 ? (
              <table className="w-full">
                <thead>
                  <tr>
                    <th>Card Name</th>
                    <th>Sign-On Bonus Estimated (USD)</th>
                  </tr>
                </thead>
                <tbody>
                  {summary
                    .filter(item => recommendedCards.some(card => card.name === item.name))
                    .map((item, index) => (
                      <tr key={index}>
                        <td className="text-center" >{item.name}</td>
                        <td className="text-center">${item.sign_on_bonus_estimated.toFixed(2)}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            ) : (
              <p>No sign-on bonus data available.</p>
            )}
          </div>

          {/* Spending Plan */}
          <div className="col-12 mt-4 shadow-2 border-round bg-gray-200">
            <div className="text-3xl pb-2 text-center">Spending Allocation Plan</div>
            {spendingPlan && spendingPlan.length > 0 ? (
              <table className="w-full">
                <thead>
                  <tr>
                    <th>Card Name</th>
                    <th>Category</th>
                    <th>Amount (USD)</th>
                  </tr>
                </thead>
                <tbody>
                  {spendingPlan.map((item, index) => (
                    <tr key={index}>
                      <td>{item.card_name}</td>
                      <td>{item.category}</td>
                      <td>${item.amount.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No spending plan available.</p>
            )}
          </div>
        </div>
      </div>
    </Card>
  );
};

export default OptimalAllocationSavingsCard;
