import React from 'react';
import { Card } from 'primereact/card';
import { Chip } from 'primereact/chip';
import { ScrollPanel } from 'primereact/scrollpanel';

const CreditCardItemTemplate = ({ cardData , sizingCss = "h-4 w-4"}) => {

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
            <div className="flex flex-wrap">
                <b className="mr-2">Credit Needed:</b>
                {e.credit_needed.map(creditNeeded => (
                    <Chip label={creditNeeded} className="mr-2 mb-2 bg-purple-100 text-black" />
                ))}
            </div>
        );
    }

    return (
        <div className={'p-2' + sizingCss} key={cardData.id}>
            <Card title={cardData.name} subTitle={cardData.issuer} footer={footer(cardData)} className="flex h-full bg-gray-300 border-3 shadow-2 surface-border surface-card border-round">
                {cardData.benefits.length > 0 && (
                    <p className="m-0 text-wrap">
                        <b>Benefits:</b> {cardData.benefits.map(benefit => (
                            <Chip className="bg-green-100" key={benefit} label={benefit} />
                        ))}
                    </p>
                )}
                {cardData.sign_on_bonus && cardData.sign_on_bonus[0] &&
                    <div>
                        <b>Sign on Bonus:</b> 
                        <div className='text-base'>
                            Spend {cardData.sign_on_bonus[0].condition_amount} dollars on {cardData.sign_on_bonus[0].purchase_type} within the first {cardData.sign_on_bonus[0].timeframe} months and get {cardData.sign_on_bonus[0].reward_amount} {cardData.sign_on_bonus[0].reward_type}
                        </div>
                    </div>
                }
                <b>Reward Summary:</b>
                <ScrollPanel style={{ width: '100%', height: '100px' }}>
                    <ul className="m-0">
                        {cardData.reward_category_map.map(reward => (
                            <li key={reward.category}>{reward.category}: {reward.reward_unit} {reward.amount}</li>
                        ))}
                    </ul>
                </ScrollPanel>
                <div className="m-0">
                    {cardData.apr.length > 0 && 
                        <div>
                            <b>APR:</b>
                            <ul>
                                {cardData.apr.map(apr => (
                                    <li key={`${apr.type}_${apr.apr}`}>{apr.type}: {apr.apr}%</li>
                                ))}
                            </ul>
                        </div>
                    }
                </div>
            </Card>
        </div>
    );
}

export default CreditCardItemTemplate;
