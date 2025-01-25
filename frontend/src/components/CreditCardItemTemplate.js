import React from 'react';
import { Card } from 'primereact/card';
import { Chip } from 'primereact/chip';
import { ScrollPanel } from 'primereact/scrollpanel';

const CreditCardItemTemplate = ({ cardData, sizingCss = "h-4 w-4" }) => {
    if (!cardData) {
        return (
            <div className='flex w-full h-full justify-center items-center'>
                <Card title="No Details Available" className="bg-gray-300 border-3 shadow-2 surface-border surface-card border-round">
                    <p className="m-0">We couldn't retrieve the details for this card.</p>
                </Card>
            </div>
        );
    }

    // Define status messages and colors
    const statusStyles = {
        "Keep this card": "text-green-600",
        "Leave at home": "text-red-600",
        "Add this card": "text-blue-600",
    };

    // Safely handle the status field
    const status = cardData.status || null;

    return (
        <>
            <style>
            {`
                @layer primereact {
                    .p-card .p-card-content {
                        padding: 0 !important; /* Override padding to zero */
                    }
                }
            `}
            </style>
            <div className={`${sizingCss}`} key={cardData.id} style={{ width: '300px', height: '700px' }}>
                <Card
                    title={
                        <>
                            {/* Display status message if it exists */}
                            {status && (
                                <div className={`text-lg font-bold ${statusStyles[status] || ''}`}>
                                    {status}
                                </div>
                            )}
                            <div className="text-lg font-bold">{cardData.name}</div>
                        </>
                    }
                    subTitle={<div className="text-sm text-gray-600">{cardData.issuer}</div>}
                    className="h-full w-full bg-gray-300 border-3 shadow-2 surface-border surface-card border-round mt-0 pt-0"
                >
                    {cardData.benefits.length > 0 && (
                        <div className="mb-2">
                            <div className="text-base font-bold">Benefits:</div>
                            <div className="flex flex-wrap">
                                {cardData.benefits.map(benefit => (
                                    <Chip key={benefit} label={benefit} className="bg-green-100 text-sm" />
                                ))}
                            </div>
                        </div>
                    )}
                    {cardData.sign_on_bonus && cardData.sign_on_bonus[0] && (
                        <div className="mb-2">
                            <div className="text-base font-bold">Sign on Bonus:</div>
                            <div className='text-sm'>
                                Spend ${cardData.sign_on_bonus[0].condition_amount} on {cardData.sign_on_bonus[0].purchase_type} within the first {cardData.sign_on_bonus[0].timeframe} months and get {cardData.sign_on_bonus[0].reward_amount} {cardData.sign_on_bonus[0].reward_type}
                            </div>
                        </div>
                    )}
                    
                    {/* Reward Summary */}
                    <div>
                        <div className="text-base font-bold">Reward Summary:</div>
                        <ScrollPanel style={{ width: '100%', height: '100px' }}>
                            <ul className="text-sm mt-0 pl-3">
                                {cardData.reward_category_map.map(reward => (
                                    <li key={reward.category}>
                                        Spend $1 on {reward.category} and get {reward.reward_amount}
                                        {reward.reward_unit === 'Cashback USD' && '%'} {reward.reward_unit}
                                        {reward.reward_threshold !== null && ` on up to $${reward.reward_threshold.on_up_to_purchase_amount_usd}`}
                                    </li>
                                ))}
                            </ul>
                        </ScrollPanel>
                    </div>
                    {/* Keywords */}
                    <div>
                        <div className="text-base font-bold">Keywords:</div>
                        <ScrollPanel style={{ width: '100%', height: '70px' }}>
                            <div className="flex flex-wrap">
                                {cardData.keywords.map(keyword => (
                                    <Chip key={keyword} label={keyword} className="bg-blue-100 text-sm mr-1" />
                                ))}
                            </div>
                        </ScrollPanel>
                    </div>

                    {/* Statement Credit */}
                    {cardData.statement_credit.length > 0 && 
                        <ScrollPanel style={{ width: '100%', height: '100px' }}>
                            <div className="flex flex-wrap">
                                <div className="text-base font-bold">Statement Credit:</div>
                                <div className='flex flex-wrap'>
                                    {cardData.statement_credit.map(statementCredit => (
                                        <div className='text-sm'>
                                            {statementCredit.description}
                                        </div>
                                    ))}
                                </div>
                            </div> 
                        </ScrollPanel>
                    }

                    {/* Annual Fee */}
                    {cardData.annual_fee && (
                        <div>
                            {cardData.annual_fee.fee_usd === 0 && cardData.annual_fee.waived_for === 0 ? (
                                <div className="text-base font-bold">No Annual Fee!</div>
                            ) : (
                                <div>
                                    <div className="text-base font-bold">Annual Fee: ${cardData.annual_fee.fee_usd} </div> 
                                    {cardData.annual_fee.waived_for > 0 && (
                                        <div className='text-base'>Waived for {cardData.annual_fee.waived_for} years</div>
                                    )}
                                </div>
                            )}
                        </div>
                    )}

                <div className="flex flex-wrap">
                    <div className="text-base font-bold">Credit Needed:</div>
                    {cardData.credit_needed.map(creditNeeded => (
                        <Chip key={creditNeeded} label={creditNeeded} className="mr-2 mb-2 bg-purple-100 text-black text-sm" />
                    ))}
                </div>
                </Card>
            </div>
        </>
    );
}

export default CreditCardItemTemplate;
