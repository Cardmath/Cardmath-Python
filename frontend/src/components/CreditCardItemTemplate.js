import React from 'react';
import { Card } from 'primereact/card';
import { Chip } from 'primereact/chip';
import { ScrollPanel } from 'primereact/scrollpanel';

const CreditCardItemTemplate = ({ cardData, sizingCss = "h-4 w-4" }) => {
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

    return (
        <div className={`p-2 ${sizingCss}`} key={cardData.id} style={{ width: '300px', height: '700px' }}>
            <Card
                title={cardData.name}
                subTitle={cardData.issuer}
                className="flex flex-col h-full w-full bg-gray-300 border-3 shadow-2 surface-border surface-card border-round"
            >
                {cardData.benefits.length > 0 && (
                    <div className="mb-2">
                        <b>Benefits:</b>
                        <div className="flex flex-wrap">
                            {cardData.benefits.map(benefit => (
                                <Chip key={benefit} label={benefit} className="bg-green-100 mr-1 mb-1" />
                            ))}
                        </div>
                    </div>
                )}
                {cardData.sign_on_bonus && cardData.sign_on_bonus[0] && (
                    <div className="mb-2">
                        <b>Sign on Bonus:</b>
                        <div className='text-base'>
                            Spend ${cardData.sign_on_bonus[0].condition_amount} on {cardData.sign_on_bonus[0].purchase_type} within the first {cardData.sign_on_bonus[0].timeframe} months and get {cardData.sign_on_bonus[0].reward_amount} {cardData.sign_on_bonus[0].reward_type}
                        </div>
                    </div>
                )}
                
                {/* Reward Summary */}
                <div className="mb-2">
                    <b>Reward Summary:</b>
                    <ScrollPanel style={{ width: '100%', height: '125px' }}>
                        <ul className="m-0">
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

                {/* Primary Reward Unit */}
                <div className="mb-2">
                    <b>Primary Reward Unit:</b> {cardData.primary_reward_unit}
                </div>

                {/* Keywords */}
                <div className="mb-2">
                    <b>Keywords:</b>
                    <div className="flex flex-wrap">
                        {cardData.keywords.map(keyword => (
                            <Chip key={keyword} label={keyword} className="bg-blue-100 mr-1 mb-1" />
                        ))}
                    </div>
                </div>

                {cardData.apr.length > 0 && (
                    <div className="mb-1">
                        <b>APR:</b>
                        <ul className='m-0'>
                            {cardData.apr.map(apr => (
                                <li key={`${apr.type}_${apr.apr}`}>{apr.type}: {apr.apr}%</li>
                            ))}
                        </ul>
                    </div>
                )}
                {cardData.annual_fee && (
                    <div className="mb-1">
                        {cardData.annual_fee.fee_usd === 0 && cardData.annual_fee.waived_for === 0 ? (
                            <b>No Annual Fee!</b>
                        ) : (
                            <div>
                                <b>Annual Fee:</b> ${cardData.annual_fee.fee_usd}
                                {cardData.annual_fee.waived_for > 0 && (
                                    <div className='text-base'>Waived for {cardData.annual_fee.waived_for} years</div>
                                )}
                            </div>
                        )}
                    </div>
                )}

            <div className="flex flex-wrap">
                <b className="mr-1">Credit Needed:</b>
                {cardData.credit_needed.map(creditNeeded => (
                    <Chip key={creditNeeded} label={creditNeeded} className="mr-2 mb-2 bg-purple-100 text-black" />
                ))}
            </div>
            </Card>
        </div>
    );
}

export default CreditCardItemTemplate;
