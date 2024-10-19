import React, { useState } from 'react';
import { Card } from 'primereact/card';
import { DataView } from 'primereact/dataview';
import { Chip } from 'primereact/chip';
import { ScrollPanel } from 'primereact/scrollpanel';

export default function CreditCardFaceouts() {

    const [creditCards, setCreditCards] = React.useState([]);
    React.useEffect(() => {
        fetch("http://localhost:8000/read_credit_cards_database", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                card_details: "all"
            })
        })
        .then(response => response.json())
        .then(data => setCreditCards(data.credit_card))
        .catch(error => console.log(error));
    }, []);

    const footer = (e) => {
        return (
            <div>
                <b> Credit Needed:</b> {e.credit_needed.join(', ')}
            </div>
        );
    }

    return (   
        <DataView
            value={creditCards}
            layout="grid"
            itemTemplate={(e) => (
                <div className='col-4 p-2'  key={e.id}> 
                    <Card title={e.name} subTitle={e.issuer} footer={footer(e)} className="bg-gray-300 border-3 shadow-2 surface-border surface-card border-round">
                        {e.benefits.length === 0 ? <Chip className="bg-yellow-100" key="no_benefits" label="No benefits found" /> : <p className="m-0"><b>Benefits:</b> {e.benefits.map(benefit => <Chip className="bg-green-100" key={benefit} label={benefit} />)} </p>}
                        <p className="m-0"><b>APR:</b> {e.apr} </p>
                        <b>Reward Summary:</b>
                        <ScrollPanel style={{ width: '100%', height: '200px' }}> 
                            <ul className="m-0">
                                {e.reward_category_map.map(reward => (
                                    <li key={reward.category}>{reward.category}: {reward.reward_unit} {reward.amount}</li>
                                ))}
                            </ul>
                        </ScrollPanel>
                    </Card>
                </div>
                )}
            paginator
            rows={9}
        />
    );
}

