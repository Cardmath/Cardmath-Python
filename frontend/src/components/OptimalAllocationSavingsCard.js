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
import { Dropdown } from 'primereact/dropdown';
import moment from 'moment';

import CreditCardItemTemplate from './CreditCardItemTemplate';
import SpendingPlanTable from './SpendingPlanTable';
import SignOnBonusTable from './SignOnBonusTable';
import PreferencesDisplay from './PreferencesDisplay';

const OptimalAllocationSavingsCard = ({ selectedWallet, wallets }) => {
  const [solutions, setSolutions] = useState([]);
  const [solutionIndex, setSolutionIndex] = useState(0);

  const [preferences, setPreferences] = useState(null);
  const [computationLoading, setComputationLoading] = useState(false);

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

  const [summary, setSummary] = useState([]);
  const [spendingPlan, setSpendingPlan] = useState([]);
  const [actionableSteps, setActionableSteps] = useState([]);
  const [totalRegularRewards, setTotalRegularRewards] = useState(0);
  const [totalSignOnBonus, setTotalSignOnBonus] = useState(0);
  const [totalAnnualFees, setTotalAnnualFees] = useState(0);
  const [netRewards, setNetRewards] = useState(0);

  const [netRewardsCurrent, setNetRewardsCurrent] = useState(0);
  const [totalRegularRewardsCurrent, setTotalRegularRewardsCurrent] = useState(0);
  const [totalSignOnBonusCurrent, setTotalSignOnBonusCurrent] = useState(0);
  const [totalAnnualFeesCurrent, setTotalAnnualFeesCurrent] = useState(0);

  const netRewardsDifference = (netRewards - netRewardsCurrent).toFixed(2);

  const [selectedWalletState, setSelectedWalletState] = useState(selectedWallet);
  const [cardBonusToggles, setCardBonusToggles] = useState({});

  const handleBonusToggleChange = (cardName, isEnabled) => {
    setCardBonusToggles((prev) => ({
      ...prev,
      [cardName]: isEnabled,
    }));
  };

  useEffect(() => {
    if (selectedWallet) {
      setSelectedWalletState(selectedWallet);
    }
  }, [selectedWallet]);

  const fetchUserPreferences = async () => {
    try {
      const response = await fetchWithAuth('https://backend-dot-cardmath-llc.uc.r.appspot.com/read_user_preferences', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await response.json();
      setPreferences(data);
    } catch (error) {
      console.error('Error fetching user preferences:', error);
    }
  };

  // Fetch current cards optimal allocation
  const fetchCurrentCardsOptimalAllocation = async () => {
      try {
        const body = {
          to_use: 4,
          to_add: 0,
          use_sign_on_bonus: false,
          save_to_db: false,
          timeframe: selectedDate !== null ? {
            start_month: moment(selectedDate[0]).startOf('month').format('YYYY-MM-DD'),
            end_month: moment(selectedDate[1]).startOf('month').format('YYYY-MM-DD')
          } : null,
          return_cards_used: true,
        };

        if (selectedWalletState) {
          body.wallet_override = {
            name: selectedWalletState.name,
            cards: selectedWalletState.cards.map(cc => ({
              is_new: cc.is_held ? false : (cardBonusToggles[cc.card.name] || false),
              card: {
                name: cc.card.name,
                issuer: cc.card.issuer
              }
            }))
          };
        }

        const response = await fetchWithAuth('https://backend-dot-cardmath-llc.uc.r.appspot.com/compute_optimal_allocation', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body)
        });
        console.log(JSON.stringify(body));
        let data = await response.json();
        data = data.solutions[0];
        console.log(data)
        setAllTimeSavings(data.total_reward_usd);
        setNetRewardsCurrent(data.net_rewards_usd);
        setTotalRegularRewardsCurrent(data.total_regular_rewards_usd);
      } catch (error) {
        console.error('Error fetching current cards optimal allocation:', error);
      }
  };

  // Fetch recommended allocation
  const fetchOptimalAllocation = async () => {
    setComputationLoading(true);
    try {
      const body = {
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
      };

      if (selectedWalletState) {
        body.wallet_override = {
          name: selectedWalletState.name,
          cards: selectedWalletState.cards.map(cc => ({
            is_new: cc.is_held ? false : (cardBonusToggles[cc.card.name] || false),
            card: {
              name: cc.card.name,
              issuer: cc.card.issuer
            }
          }))
        };
      }

      const response = await fetchWithAuth('https://backend-dot-cardmath-llc.uc.r.appspot.com/compute_optimal_allocation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await response.json();
      setSolutions(data);
    } catch (error) {
      console.error('Error fetching savings data:', error);
    }
    setComputationLoading(false);
  };

  useEffect(() => {
    if (!solutions || !solutions.solutions || solutions.solutions.length === 0) {
      console.log('Solutions array is empty');
      return;
    }
    
    let data = solutions.solutions[solutionIndex % solutions.solutions.length];
    let timeframe = solutions.timeframe;

    setCardsHeld(data.cards_used);
    setRecommendedCards(data.cards_added);
    setRecommendedCardsBonusTotal(data.total_reward_usd);

    setTimeframe(timeframe);
    setSummary(data.summary);
    setSpendingPlan(data.spending_plan);
    setActionableSteps(data.actionable_steps);
    setTotalRegularRewards(data.total_regular_rewards_usd);
    setTotalSignOnBonus(data.total_sign_on_bonus_usd);
    setTotalAnnualFees(data.total_annual_fees_usd);
    setNetRewards(data.net_rewards_usd);
  }, [solutionIndex, solutions]);

  // Fetch user's optimal allocation on component mount
  useEffect(() => {
    fetchOptimalAllocation();
    fetchUserPreferences();
    fetchCurrentCardsOptimalAllocation();
  }, []);

  useEffect(() => {
    fetchCurrentCardsOptimalAllocation();
  }, [selectedWalletState]);

  return (
    <Card className="w-full h-full justify-content-center align-items-stretch flex-wrap border-round shadow-2 mt-2">
      {/* Display net rewards difference */}
      <div className="flex gap-2 justify-content-center">
        <Tooltip className='w-3' target=".potential-increase" position="bottom"/>
        <div className="potential-increase col-10 border-round shadow-3" data-pr-tooltip="Potential Increase in Net Rewards with Recommended Cards: Recommended Wallet Net Rewards - Current Wallet Net Rewards. The difference in net rewards after using only credit cards in the recommended wallet. This is how much you could potentially save by using your recommended wallet instead of your current wallet over the timeframe.">
          <div className="grid align-items-center justify-content-center py-2">
            Potential Increase in Net Rewards with Recommended Cards:
          </div>
          {netRewardsDifference ? (
            <div className="font-bold text-3xl grid justify-content-center pb-1 text-green-600">
              ${netRewardsDifference}
            </div> 
          ) : (
            <div className='text-red-400 text-xl text-center p-2'>
              No cards detected. Unable to compute potential increase in net rewards.
            </div>
          )}
        </div>
      </div>

      <Tooltip className='w-3' target=".solutions-iterator" position="bottom"/>
      <div className='pt-4 border-round flex justify-content-center'>
        <div className='solutions-iterator w-3 p-3 shadow-2 flex justify-content-center' data-pr-tooltip="We find at most 5 of the best (but often fewer) credit card wallets, including the optimal one. Click on the left and right arrows to cycle through solutions."> 
          <Button icon="pi pi-arrow-left" onClick={() => solutions.solutions && setSolutionIndex((solutionIndex - 1 + solutions.solutions.length) % solutions.solutions.length)} />
          <div className='text-center text-2xl px-3 pt-1'>Current Solution: {solutionIndex + 1} / {solutions.solutions?.length || 0}</div>
          <Button icon="pi pi-arrow-right" onClick={() => solutions.solutions && setSolutionIndex((solutionIndex + 1) % solutions.solutions.length)} />
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

          {/* Wallet selector */}
          <div className='bg-gray-200 mt-3 pt-1 pb-2 px-2 border-round shadow-2'>
            <p className='font-italic'>
              Use a different wallet to change the cards that appear in 'Your Held Cards'. The custom wallet option is great for experimenting with different combinations of cards.
            </p>
            
            <div className='flex justify-content-center'> 
              <Dropdown 
                value={selectedWalletState} 
                options={wallets} 
                onChange={(e) => setSelectedWalletState(e.value)} 
                optionLabel="name" 
                placeholder="Select a Wallet" 
                className="w-6 flex"
              />
            </div>
          </div>

          {/* Individual Card Sign-On Bonus Toggles */}
          <div className='bg-gray-200 mt-3 pt-1 pb-2 px-2 border-round shadow-2'>
            <p className='font-italic'>
              Toggle sign-on bonus for each card to decide if it should be included in the calculation.
            </p>
            {selectedWalletState && selectedWalletState.cards.map((cc, index) => (
              <div key={index} className="flex p-2 align-items-center border-round border-dotted border-blue-200 my-2">
                <div className="mr-2">{cc.card.name} (Issuer: {cc.card.issuer})
                <InputSwitch
                  className='ml-2'
                  checked={cardBonusToggles[cc.card.name] || false}
                  onChange={(e) => handleBonusToggleChange(cc.card.name, e.value)}
                />
                </div>
              </div>
            ))}
          </div>

          <div className='bg-gray-200 mt-3 pt-1 pb-2 px-2 border-round shadow-2'>
            <p className='font-italic'>
              Include sign-on bonuses to highlight cards with high short-term value. Disabling this will give a clearer picture of long-term rewards, helping you choose a card that's more beneficial over time.
            </p>
            <span id="switch1" className="p-float-label mt-2">Consider Sign on Bonus in Calculation</span>
            <InputSwitch className="align-self-center" aria-labelledby='switch1' checked={useSignOnBonus} onChange={e => setUseSignOnBonus(e.value)} />
          </div>
  
          {/* Existing controls */}
          <div className='bg-gray-200 mt-3 pt-1 pb-2 px-2 border-round shadow-2'>
            <p className='font-italic'>
              Select your desired total wallet size and the number of new cards you're considering. Based on these inputs, we'll recommend new cards while factoring in the possibility of canceling some of your current cards to optimize your rewards and benefits.
            </p>
            <div id="toUseInput" className="p-float-label">Desired Wallet Size</div>
            <InputNumber aria-labelledby='toUseInput' showButtons inputId="integeronly" className="w-full" value={toUse} onChange={e => setToUse(e.value)} min={1} max={5} />

            <div id="toAddInput" className="p-float-label mt-2">Number of Desired New Cards</div>
            <InputNumber aria-labelledby='toAddInput' showButtons inputId="integeronly" className="w-full" value={toAdd} onChange={e => setToAdd(e.value)} min={0} max={5} />
            <p className='font-italic'>
              Since you have <span className='font-bold'>{cardsHeld.length}</span> credit cards in this wallet, and you want to add up to <span className='font-bold'>{toAdd}</span> new credit cards from the recommendation algorithm, we'll recommend you to cancel up to <span className='font-bold'>{Math.max(cardsHeld.length, cardsHeld.length - toAdd)}</span> of your <span className='font-bold'>{cardsHeld.length}</span> cards. Cancelling up to  <span className='font-bold'>{Math.max(cardsHeld.length, cardsHeld.length - toAdd)}</span> of your cards will make room for up to <span className='font-bold'>{toAdd}</span> new ones so that you have a final wallet of <span className='font-bold'>{toUse}</span> credit cards. 
            </p>
          </div>

          <div className='bg-gray-200 mt-3 pt-1 pb-2 px-2 border-round shadow-2'>
            <p className='font-italic'>
              Select the date range to over which to calculate the optimal credit card wallet. You might do this when old transactions are not representative of your current spending habits. If no date range is selected, we'll use the last 48 months of your entire available history.
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
          }} className='w-full mt-5' label="Compute" loading={computationLoading} />


          <div className='bg-gray-200 mt-3 pt-1 pb-2 px-2 border-round shadow-2'>
            <p className='font-italic'>
              Your preferences inform which credit cards we input to our recommendation algorithm. If you haven't set your preferences yet, you can do so by clicking the button below.
            </p>
            {preferences && <PreferencesDisplay preferences={preferences} />}
            <Button onClick={() => window.location.href="https://cardmath.ai/preferences"} className='w-full mt-5' label="Set Preferences" />
          </div>

          
        </div>

        {/* Display carousels and spending plan */}
        <div className="col-8 grid">
          {/* Carousels */}
          <div className="col-12 grid flex justify-content-center align-items-start">
            {/* Your Cards Carousel */}
            <div className="col-6">
              <div className="text-3xl pb-2 text-center">Your Held Cards</div>
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
              <div className="text-3xl pb-2 text-center">Recommended New Cards</div>
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

          {/* Replaced Sign-On Bonus Table */}
          <SignOnBonusTable summary={summary} heldCards={cardsHeld} cardBonusToggles={cardBonusToggles} recommendedCards={recommendedCards} useSignOnBonus={useSignOnBonus}/>

          {/* Spending Plan Table */}
          <SpendingPlanTable spendingPlan={spendingPlan} />
        </div>
      </div>
    </Card>
  );
};

export default OptimalAllocationSavingsCard;
