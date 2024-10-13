import React from 'react';
import { Card } from 'primereact/card';
        

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
        <div className="flex justify-content-center flex-wrap gap-3">   
             {creditCards ? creditCards.map(e => {
                console.log(JSON.stringify(e.reward_category_map))
                return (
                <Card className="md:w-20rem" 
                title={e.name}
                subtitle={e.issuer}>
                    <p className="m-0">Benefits: {e.benefits.join(', ')} </p>
                    <p className="m-0">Credit Needed: {e.credit_needed.join(', ')} </p>
                    <p className="m-0"><b>APR:</b> {e.apr} </p>
                    <p className="m-0"> 
                        <b>Reward Summary:</b>
                        <ul className="m-0">
                            {e.reward_category_map.map(reward => (
                                <li key={reward.category}>{reward.category}: {reward.reward.reward_unit} {reward.reward.amount}</li>
                            ))}
                        </ul>
                    </p>
                </Card>
                 )
             }) : null}
        </div>
    );
}

