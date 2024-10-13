import React, { useState } from 'react';
import { Card } from 'primereact/card';
import { DataView } from 'primereact/dataview';
import { Dropdown } from 'primereact/dropdown';
        

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

    return (
        <div className="w-full">   
            <DataView className='gap-2'  
                value={creditCards}
                layout="grid"
                itemTemplate={(e) => (
                    <Card title={e.name} subTitle={e.issuer} footer={() => <div> <b> Credit Needed:</b> {e.credit_needed.join(', ')} </div>} className="col-12 sm:col-6 lg:col-12 xl:col-4 p-2" key={e.id}>
                        <div className="p-4 border-3 surface-border surface-card border-round">
                            <p className="m-0"><b>Benefits:</b> {e.benefits.join(', ')} </p>
                            <p className="m-0"><b>APR:</b> {e.apr} </p>
                            <p className="m-0"> 
                                <b>Reward Summary:</b>
                                <ul className="m-0">
                                    {e.reward_category_map.map(reward => (
                                        <li key={reward.category}>{reward.category}: {reward.reward.reward_unit} {reward.reward.amount}</li>
                                    ))}
                                </ul>
                            </p>
                        </div>
                    </Card>
                    )}
                paginator
                rows={8}
            />
        </div>
    );
}

