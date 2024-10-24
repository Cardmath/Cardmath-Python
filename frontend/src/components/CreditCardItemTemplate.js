import React from 'react';
import { Card } from 'primereact/card';
import { Chip } from 'primereact/chip';
import { ScrollPanel } from 'primereact/scrollpanel';

const CreditCardItemTemplate = ({ cardData }) => {

    // Correctly handle conditional rendering
    if (!cardData) {
        return (
            <div className='flex w-full h-full justify-center items-center'>
                <Card title="No Details Available" className="bg-gray-300 border-3 shadow-2 surface-border surface-card border-round">
                    <p className="m-0">We couldn't retrieve the details for this card.</p>
                </Card>
            </div>
        );
    }

    const footer = (e) => {
        return (
            <div>
                <b> Credit Needed:</b> {e.credit_needed.join(', ')}
            </div>
        );
    }

    return (
        <div className='p-2' key={cardData.id}>
            <Card title={cardData.name} subTitle={cardData.issuer} footer={footer(cardData)} className="flex-grow h-30rem bg-gray-300 border-3 shadow-2 surface-border surface-card border-round">
                {cardData.benefits.length === 0 ? (
                    <div> 
                        <b>Benefits:</b>
                        <Chip className="bg-yellow-100" key="no_benefits" label="No benefits found" />
                    </div>
                ) : (
                    <p className="m-0">
                        <b>Benefits:</b> {cardData.benefits.map(benefit => (
                            <Chip className="bg-green-100" key={benefit} label={benefit} />
                        ))}
                    </p>
                )}
                <b>APR:</b>
                <ul className="m-0">
                    {cardData.apr.map(apr => (
                        <li key={`${apr.type}_${apr.apr}`}>{apr.type}: {apr.apr}%</li>
                    ))}
                </ul>
                <b>Reward Summary:</b>
                <ScrollPanel style={{ width: '100%', height: '100px' }}>
                    <ul className="m-0">
                        {cardData.reward_category_map.map(reward => (
                            <li key={reward.category}>{reward.category}: {reward.reward_unit} {reward.amount}</li>
                        ))}
                    </ul>
                </ScrollPanel>
            </Card>
        </div>
    );
}

export default CreditCardItemTemplate;
