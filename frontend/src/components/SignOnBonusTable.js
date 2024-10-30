import React from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

export default function SignOnBonusTable({ summary, recommendedCards }) {
    // Filter summary based on recommendedCards to match your existing logic
    const filteredSummary = summary.filter(item => 
        recommendedCards.some(card => card.name === item.name)
    );

    return (
        <div className="col-12 mt-4 shadow-2 border-round bg-gray-200">
            <div className="text-3xl pb-2 text-center">Sign-On Bonus Rewards for New Cards</div>
            {filteredSummary && filteredSummary.length > 0 ? (
                <DataTable value={filteredSummary} showGridlines tableStyle={{ minWidth: '60rem' }}>
                    <Column field="name" header="Card Name"></Column>
                    <Column 
                        field="annual_fee_usd" 
                        header="Annual Fee (USD)" 
                        body={(rowData) => `$${rowData.annual_fee_usd.toFixed(2)}`}
                    ></Column>
                    <Column 
                        field="sign_on_bonus_total" 
                        header="Sign-On Bonus (USD)" 
                        body={(rowData) => `$${rowData.sign_on_bonus_total.toFixed(2)}`}
                    ></Column>
                    <Column 
                        field="sign_on_bonus_likelihood" 
                        header="Likelihood of Fulfilling Sign On Bonus Condition (%)" 
                        body={(rowData) => `${(rowData.sign_on_bonus_likelihood * 100).toFixed(2)}%`}
                    ></Column>
                    <Column 
                        field="sign_on_bonus_estimated" 
                        header="Sign-On Bonus Estimated (USD)" 
                        body={(rowData) => `$${rowData.sign_on_bonus_estimated.toFixed(2)}`}
                    ></Column>
                    <Column 
                        field="regular_rewards_usd" 
                        header="Regular Rewards Value (USD)" 
                        body={(rowData) => `$${rowData.regular_rewards_usd.toFixed(2)}`}
                    ></Column>
                                        <Column 
                        field="reward_unit" 
                        header="Reward Unit" 
                        body={(rowData) => `${rowData.sign_on_bonus_reward_unit}`}
                    ></Column>
                    <Column 
                        field="profit_usd" 
                        header="Profit (USD)" 
                        body={(rowData) => `$${rowData.profit_usd.toFixed(2)}`}
                    ></Column>
                </DataTable>
            ) : (
                <p>No sign-on bonus data available.</p>
            )}
        </div>
    );
}
