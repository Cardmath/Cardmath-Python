import React, { useState, useEffect } from 'react';
import { DataView } from 'primereact/dataview';
import CreditCardItemTemplate from './CreditCardItemTemplate';

export default function CreditCardFaceouts() {

    const [creditCards, setCreditCards] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/read_credit_cards_database", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                card_details: "all"
            })
        })
        .then(response => response.json())
        .then(data => {
            setCreditCards(data.credit_card);
            console.log(data);
        })
        .catch(error => console.log(error));
    }, []);

    return (   
        <DataView
            value={creditCards}
            layout="grid"
            itemTemplate={(e) => <CreditCardItemTemplate cardData={e} />}
            paginator
            rows={9}
        />
    );
}
