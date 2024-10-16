import React, { useEffect, useState } from 'react';
import { Card } from 'primereact/card';
import { fetchWithAuth } from '../pages/AuthPage';

const OptimalAllocationSavingsCard = () => {
  const [savings, setSavings] = useState(0);

  useEffect(() => {
    fetchWithAuth('http://localhost:8000/compute_optimal_held_cards_allocation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        held_cards_only: false,
        all_cards: true,
        save_to_db: false
      })
    })
      .then(response => response.json())
      .then(data => setSavings(data.total_reward_usd))
      .catch(error => console.log(error));
  }, []);

  return (
    <Card className="p-text-center">
      <h2 className="font-bold">Here's how much you could have saved</h2>
      <p className="text-lg text-secondary">Amount Saved: <span className="font-bold">${savings}</span></p>
    </Card>
  );
};

export default OptimalAllocationSavingsCard;

