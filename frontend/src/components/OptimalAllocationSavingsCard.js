import React, { useEffect, useState } from 'react';
import { Card } from 'primereact/card';
import { fetchWithAuth } from '../pages/AuthPage';
import { InputNumber } from 'primereact/inputnumber';
import { InputSwitch } from 'primereact/inputswitch';
import { Button } from 'primereact/button';
import { Carousel } from 'primereact/carousel';
import { FloatLabel } from 'primereact/floatlabel';
import { Calendar } from 'primereact/calendar';
import { Tooltip } from 'primereact/tooltip';
import moment from 'moment';

import CreditCardItemTemplate from './CreditCardItemTemplate';
import SpendingPlanTable from './SpendingPlanTable';

const OptimalAllocationSavingsCard = () => {
  const [timeframe, setTimeframe] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);

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

  // Method to fetch user's optimal allocation with just their current cards
  const fetchCurrentCardsOptimalAllocation = async () => {
    if (cardsHeld.length > 0) {
      try {
        const response = await fetchWithAuth('http://localhost:8000/compute_optimal_allocation', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            to_use: cardsHeld.length,
            to_add: 0,
            use_sign_on_bonus: false,
            save_to_db: false,
            timeframe: selectedDate !== null ? {
              start_month: moment(selectedDate[0]).startOf('month').format('YYYY-MM-DD'),
              end_month: moment(selectedDate[1]).startOf('month').format('YYYY-MM-DD')
            } : null,
            return_cards_used: true,
          })
        });
        const data = await response.json();
        setAllTimeSavings(data.total_reward_usd);
        // Set current wallet data
        setNetRewardsCurrent(data.net_rewards_usd);
        setTotalRegularRewardsCurrent(data.total_regular_rewards_usd);
      } catch (error) {
        console.error('Error fetching current cards optimal allocation:', error);
      }
    }
  };

  // Fetch user's current card rewards (All-time)
  useEffect(() => {
    fetchCurrentCardsOptimalAllocation();
  }, [cardsHeld]);

  // Fetch recommended allocation
  const fetchOptimalAllocation = async () => {
    try {
      const response = await fetchWithAuth('http://localhost:8000/compute_optimal_allocation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to_use: toUse,
          to_add: toAdd,
          use_sign_on_bonus: useSignOnBonus,
          timeframe: selectedDate !== null ? {
            start_month: moment(selectedDate[0]).startOf('month').format('YYYY-MM-DD'),
            end_month: moment(selectedDate[1]).startOf('month').format('YYYY-MM-DD')
          } : null,          
          return_cards_added: true,
          return_cards_used: true,
          save_to_db: false
        })
      });
      const data = await response.json();
      console.log(data);
      setRecommendedCards(data.cards_added);
      setRecommendedCardsBonusTotal(data.total_reward_usd);

      // Set new data from the API response
      setTimeframe(data.timeframe);
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

  // Fetch user's optimal allocation for the selected timeframe on component mount
  useEffect(() => {
    fetchOptimalAllocation();
  }, []);

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
        <Tooltip className='w-3' target=".potential-increase" position="bottom"/>
        <div className="potential-increase col-10 border-round shadow-3" data-pr-tooltip="Potential Increase in Net Rewards with Recommended Cards: Recommended Wallet Net Rewards - Current Wallet Net Rewards. The difference in net rewards after using only credit cards in the recommended wallet. This is how much you could potentially save by using your recommended wallet instead of your current wallet over the timeframe.">
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
        <Tooltip className='w-3' target=".current-wallet-net-rewards" position="bottom"/>
        <div className="current-wallet-net-rewards col-5 border-round shadow-3" data-pr-tooltip="Current Wallet Regular Rewards - Current Wallet Annual Fees. The estimated maximum potential value of rewards you could have earned in the timeframe after fees.">
          <div className="grid align-items-center justify-content-center py-2">Current Wallet Net Rewards:</div>
          <div className="font-bold text-2xl grid justify-content-center pb-1">${netRewardsCurrent}</div>
        </div>

        <Tooltip className='w-3' target=".recommended-wallet-net-rewards" position="bottom"/>
        <div className="recommended-wallet-net-rewards col-5 border-round shadow-3" data-pr-tooltip="Recommended Wallet Regular Rewards + Recommended Wallet Sign on Bonus - Recommended Wallet Annual Fees. How much you could earn in rewards if you used the credit cards in the recommended wallet, after fees.">
          <div className="grid align-items-center justify-content-center py-2">Recommended Wallet Net Rewards:</div>
          <div className="font-bold text-2xl grid justify-content-center pb-1">${netRewards}</div>
        </div>
      
      </div>

      {/* Display total regular rewards and annual fees */}
      <div className="flex pt-2 gap-2 justify-content-center">
        {/* Current Wallet */}
        <div className="col-5 border-round shadow-3">

          <Tooltip className='w-3' target=".current-wallet-regular-rewards" position="bottom"/>
          <div className='current-wallet-regular-rewards' data-pr-tooltip="Calculated over selected timeframe. Total dollar value of points or cash you'd earn from everyday purchases using your currently held credit cards optimally. These rewards accumulate as you use your card for daily spending."> 
            <div className="grid justify-content-center py-2">Current Wallet Regular Rewards</div>
            <div className="font-bold text-2xl grid justify-content-center pb-1">${totalRegularRewardsCurrent}</div>
            </div>
          
          <Tooltip className='w-3' target=".current-wallet-annual-fees" position="bottom"/>
          <div className='current-wallet-annual-fees' data-pr-tooltip="Annual fees amassed on the credit cards in the current wallet over the selected timeframe.">
            <div className="grid justify-content-center py-2">Current Wallet Annual Fees</div>
            <div className="font-bold text-2xl grid justify-content-center pb-1">${totalAnnualFeesCurrent}</div>
          </div>
          
          <Tooltip className='w-3' target=".timeframe-of-calculation" position="bottom"/>
          <div className='timeframe-of-calculation' data-pr-tooltip={"Timeframe of calculation for regular rewards and annual fees. All numbers displayed at the top of the page are calculated based on the selected timeframe."}>
            <div className="grid justify-content-center py-2">Timeframe of Calculation</div>
            {timeframe && <div className="font-bold text-2xl grid justify-content-center pb-1">{moment(timeframe.start_month).format('MMMM YYYY')} to {moment(timeframe.end_month).format('MMMM YYYY')}</div>}
          </div>
        </div>
        {/* Recommended Wallet */}
        <div className="col-5 border-round shadow-3">
          
          <Tooltip className='w-3' target=".recommended-wallet-regular-rewards" position="bottom"/>
          <div className='recommended-wallet-regular-rewards' data-pr-tooltip={"Calculated over selected timeframe. Total dollar value of points or cash you'd earn from everyday purchases using all the cards in the recommended wallet according to the spending plan. These rewards accumulate as you use your card for daily spending."}>
            <div className="grid justify-content-center py-2">Recommended Wallet Regular Rewards</div>
            <div className="font-bold text-2xl grid justify-content-center pb-1">${totalRegularRewards}</div>
          </div>

          <Tooltip className='w-3' target=".recommended-wallet-annual-fees" position="bottom"/>
          <div className='recommended-wallet-annual-fees' data-pr-tooltip={"Calculated over selected timeframe. The total annual fees you will be charged if you sign up for all recommended credit cards and cancel cards we recommend to cancel."}>
            <div className="grid justify-content-center py-2">Recommended Wallet Annual Fees</div>
            <div className="font-bold text-2xl grid justify-content-center pb-1">${totalAnnualFees}</div>
          </div>
            
          <Tooltip className='w-3' target=".expected-wallet-sign-on-bonus" position="bottom"/>
          <div className="expected-wallet-sign-on-bonus" data-pr-tooltip={"An estimated bonus you might earn when you sign up for a new credit card. This amount is based on the likelihood of meeting the bonus requirements, so it's not guaranteed"}> 
            <div className="grid justify-content-center py-2">Recommended Wallet Expected Sign on Bonus</div>
            <div className="font-bold text-2xl grid justify-content-center pb-1">${totalSignOnBonus}</div>
          </div>
        
        </div>
      </div>

      {/* Input controls and compute button */}
      <div className="flex pt-4 gap-2 h-full justify-content-center">
        <div className="col-3">

          <img src="/logos/png/Black logo - no background.png" alt="Optimal Savings" className="w-full" />

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

          <div className='bg-gray-200 mt-3 pt-1 pb-2 px-2 border-round shadow-2'>
            <p className='font-italic'>
              Select the date range to over which to calculate the optimal credit card wallet. You might do this when old transactions are not representative of your current spending habits.
            </p>
            <div className="flex justify-content-center mt-2">
              <FloatLabel htmlFor="dateRange" className="p-float-label mt-3">
                <Calendar  value={selectedDate} selectionMode="range" readOnlyInput hideOnRangeSelection onChange={(e) => setSelectedDate(e.value)} view="month" dateFormat="mm/yy" />
                <label htmlFor="dateRange">Date Range</label>
              </FloatLabel>
            </div>
          </div>

          <Button onClick={() => {
            fetchOptimalAllocation();
            fetchCurrentCardsOptimalAllocation();
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
                        <td>{item.name}</td>
                        <td className="text-center">${item.sign_on_bonus_estimated.toFixed(2)}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            ) : (
              <p>No sign-on bonus data available.</p>
            )}
          </div>

          <SpendingPlanTable spendingPlan={spendingPlan} />
        </div>
      </div>
    </Card>
  );
};

export default OptimalAllocationSavingsCard;
