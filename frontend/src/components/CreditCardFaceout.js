import React, { useState, useEffect } from 'react';
import { DataView } from 'primereact/dataview';
import CreditCardItemTemplate from './CreditCardItemTemplate';
import { getBackendUrl } from '../utils/urlResolver';

export default function CreditCardFaceouts({ issuer, name, annualFeeRange, primaryRewardUnit, keyword }) {
    const [creditCards, setCreditCards] = useState([]);

    useEffect(() => {
        fetch(`${getBackendUrl()}/read_credit_cards_database`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ card_details: "all", use_preferences: false })
        })
        .then(response => response.json())
        .then(data => {
            setCreditCards(data.credit_card); // Initial full data set
        })
        .catch(error => console.log(error));
    }, []);

    // Filter data each time filters or creditCards update
    const filteredCards = creditCards.filter(card => {
        const matchesIssuer = !issuer || card.issuer === issuer;
        const matchesName = !name || card.name.toLowerCase().includes(name.toLowerCase());
        const matchesAnnualFee = card.annual_fee && 
                                  card.annual_fee.fee_usd >= annualFeeRange[0] && 
                                  card.annual_fee.fee_usd <= annualFeeRange[1];
        const matchesRewardUnit = !primaryRewardUnit || card.primary_reward_unit === primaryRewardUnit;
        const matchesKeyword = !keyword || (card.keywords && card.keywords.includes(keyword));
        return matchesIssuer && matchesName && matchesAnnualFee && matchesRewardUnit && matchesKeyword;
    });

    return (
        <DataView
            value={filteredCards}
            layout="grid"
            itemTemplate={(e) => <CreditCardItemTemplate cardData={e} sizingCss="h-4 w-4" />}
            paginator
            rows={9}
        />
    );
}
