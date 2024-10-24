import React, { useEffect, useState } from 'react';
import { Card } from 'primereact/card';
import { fetchWithAuth } from '../pages/AuthPage';
import { InputNumber } from 'primereact/inputnumber';
import { InputSwitch } from 'primereact/inputswitch';
import { Button } from 'primereact/button';
import { Carousel } from 'primereact/carousel';
import CreditCardItemTemplate from './CreditCardItemTemplate';
import moment from 'moment';
const OptimalAllocationSavingsCard = () => {
  const [allTimeSavings, setAllTimeSavings] = useState(0);
  const [lastMonthSavings, setLastMonthSavings] = useState(0);

  const [toAdd, setToAdd] = useState(2);
  const [toUse, setToUse] = useState(4);

  const [useSignOnBonus, setUseSignOnBonus] = useState(false);
  const [maxNumMonths, setMaxNumMonths] = useState(3);

  const [cardsHeld, setCardsHeld] = useState([]);
  const [recommendedCards, setRecommendedCards] = useState([]);

  const [recommendedCardsBonusTotal , setRecommendedCardsBonusTotal] = useState(0);
  const [recommendedCardsLastMonthSavings , setRecommendedCardsLastMonthSavings] = useState(0);

  useEffect(() => {
    fetchWithAuth('http://localhost:8000/compute_optimal_allocation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        to_use: cardsHeld.length,
        to_add: 0,
        save_to_db: false,
        timeframe: null
      })
    })
      .then(response => response.json())
      .then(data => setAllTimeSavings(data.total_reward_usd))
      .catch(error => console.log(error));
  }, [cardsHeld]);

  useEffect(() => {
    fetchWithAuth('http://localhost:8000/compute_optimal_allocation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        to_use: cardsHeld.length,
        to_add: 0,
        timeframe: {
          start_month: moment().subtract(1, 'months').startOf('month').format('YYYY-MM-DD'), // Previous month as start
          end_month: moment().startOf('month').format('YYYY-MM-DD') // Current month as end
        },
        save_to_db: false
      })
    })
      .then(response => response.json())
      .then(data => setLastMonthSavings(data.total_reward_usd))
      .catch(error => console.error('Error fetching savings data:', error));
  }, [cardsHeld]);

  useEffect(() => {
    fetchWithAuth('http://localhost:8000/compute_optimal_allocation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        to_use: toUse,
        to_add: toAdd,
        timeframe: null,
        return_cards_added: true,
        save_to_db: false
      })
    })
      .then(response => response.json())
      .then(data => {
        setRecommendedCards(data.cards_added);
        setRecommendedCardsBonusTotal(data.total_reward_usd);
      })
      .catch(error => console.error('Error fetching savings data:', error));
  }, []);

  useEffect(() => {
    fetchWithAuth('http://localhost:8000/compute_optimal_allocation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        to_use: toUse,
        to_add: toAdd,
        timeframe: {
          start_month: moment().subtract(1, 'months').startOf('month').format('YYYY-MM-DD'), // Previous month as start
          end_month: moment().startOf('month').format('YYYY-MM-DD') // Current month as end
        },
        save_to_db: false
      })
    })
      .then(response => response.json())
      .then(data => setRecommendedCardsLastMonthSavings(data.total_reward_usd))
      .catch(error => console.error('Error fetching savings data:', error));
  }, [cardsHeld]);
  
  
  useEffect(() => {
    fetchWithAuth('http://localhost:8000/read_user_held_cards', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => response.json())
      .then(data => {
        setCardsHeld(data.credit_card);
        setToUse(data.credit_card.length);
      })
      .catch(error => console.log(error));
  }, []);

  return (
    <Card className="w-full h-half justify-content-center align-items-stretch flex-wrap border-round shadow-2 mt-2" >
      <div className = "flex gap-2 justify-content-center"> 
        <div className="col-5 border-round shadow-3">
            <div className="grid align-items-center justify-content-center py-2"> All-time Rewards Value: </div>
            {cardsHeld.length === 0 ? (
              <div className='text-red-400 text-xl text-center p-2'>No cards detected. Unable to compute your all-time rewards value.</div>
            ) : (
              <div className="font-bold text-2xl grid justify-content-center pb-1">${allTimeSavings}</div>
            )}
          </div>
        <div className="col-5 border-round shadow-3">
          <div className="grid align-items-center justify-content-center py-2"> Last Month's Bonus Value:</div> 
          {cardsHeld.length === 0 ? (
            <div className='text-red-400 text-xl text-center p-2'>No cards detected. Unable to compute last month's bonus value.</div>
          ) : (
            <div className="font-bold text-2xl grid align-items-center justify-content-center pb-1">${lastMonthSavings}</div>
          )}
        </div>
      </div>
      <div className = "flex pt-2 gap-2 justify-content-center"> 
        <div className="col-5 border-round shadow-3">
          <div className=" grid justify-content-center py-2"> Recommended Wallet All-Time Savings </div> 
          <div className="font-bold text-2xl grid justify-content-center pb-1">${recommendedCardsBonusTotal}</div>
        </div>
        <div className="col-5 border-round shadow-3">
          <div className="grid align-items-center justify-content-center py-2"> Recommended Wallet Last Month's Bonus Value:</div> 
          <div className="font-bold text-2xl grid align-items-center justify-content-center pb-1">${recommendedCardsLastMonthSavings}</div>
        </div>
      </div>
      <div className="flex pt-4 gap-2 h-full justify-content-center"> 
        <div className="col-3">
          <div id="toUseInput" className="p-float-label">Desired Wallet Size</div>
          <InputNumber aria-labelledby='toUseInput' showButtons inputId="integeronly" className="w-full" value={toUse} onChange={e => setToUse(e.value)} min={0} max={5} />
          
          <div id="toAddInput" className="p-float-label mt-2">Number of Desired New Cards</div>
          <InputNumber aria-labelledby='toAddInput' showButtons inputId="integeronly" className="w-full" value={toAdd} onChange={e => setToAdd(e.value)} min={0} max={5} />
          
          <div className='bg-gray-200 mt-3 py-1 px-2 border-round'> 
            <p className='font-italic'>Include sign-on bonuses to highlight cards with high short-term value. Disabling this will give a clearer picture of long-term rewards, helping you choose a card that's more beneficial over time.</p>
            <span id="switch1" className="p-float-label mt-2">Consider Sign on Bonus in Calculation</span>
            <InputSwitch className="align-self-center" aria-labelledby='switch1' checked={useSignOnBonus} onChange={e => setUseSignOnBonus(e.value)} />  
          </div>


          <span id="monthsInput" className="p-float-label mt-2">Months to Consider for Sign On Bonus</span>
          <InputNumber aria-labelledby='monthsInput' showButtons inputId="integeronly" className="w-full" value={maxNumMonths} onChange={e => setMaxNumMonths(e.value)} min={0} max={5} />

          <Button className='w-full mt-5' label="Compute" />
        </div>
        <div className="col-8 grid">
          <div className="col-6 grid flex justify-content-center align-items-start">
            <div className="text-3xl pb-2">Your Cards</div>
            {cardsHeld.length === 0 ? (
              <Card title="No Credit Cards detected" className="w-9 py-3 bg-pink-200 border-3 shadow-2 surface-border border-round">
                <p className="m-0">We couldn't detect any credit cards associated with your account.</p>
              </Card>
            ) : (
              <Carousel className="w-full h-full" value={cardsHeld} numVisible={1} numScroll={1} itemTemplate={(e) => <CreditCardItemTemplate cardData={e} />}/>
            )}
          </div>
          <div className='col-6 grid flex justify-content-center align-items-start'>
            <div className="text-3xl pb-2">Recommended Cards</div>
            <Carousel className="w-full h-full" value={recommendedCards} numVisible={1} numScroll={1} itemTemplate={(e) => <CreditCardItemTemplate cardData={e} />}/>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default OptimalAllocationSavingsCard;

