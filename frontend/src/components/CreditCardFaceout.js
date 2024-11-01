import React, { useState, useEffect } from 'react';
import { DataView } from 'primereact/dataview';
import CreditCardItemTemplate from './CreditCardItemTemplate';

export default function CreditCardFaceouts({ issuer, name, annualFeeRange }) {
    const [creditCards, setCreditCards] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/read_credit_cards_database", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ card_details: "all", use_preferences: false })
        })
        .then(response => response.json())
        .then(data => {
            const filteredData = filterData(data.credit_card);
            setCreditCards(filteredData);
        })
        .catch(error => console.log(error));
    }, [issuer, name, annualFeeRange]);

    const filterData = (data) => {
        return data.filter(card => {
            const matchesIssuer = !issuer || card.issuer === issuer;
            const matchesName = !name || card.name.toLowerCase().includes(name.toLowerCase());
            const matchesAnnualFee = card.annual_fee && 
                                      card.annual_fee.fee_usd >= annualFeeRange[0] && 
                                      card.annual_fee.fee_usd <= annualFeeRange[1];
            return matchesIssuer && matchesName && matchesAnnualFee;
        });
    };

    return (
        <DataView
            value={creditCards}
            layout="grid"
            itemTemplate={(e) => <CreditCardItemTemplate cardData={e} sizingCss="h-4 w-4" />}
            paginator
            rows={9}
        />
    );
}
