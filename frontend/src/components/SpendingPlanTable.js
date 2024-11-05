import React from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Divider } from 'primereact/divider';

export default function SpendingPlanTable({ spendingPlan }) {
    // Calculate cumulative reward units and dollar value for each reward type
    const rewardSummary = spendingPlan.reduce((summary, item) => {
        const { reward_unit, reward_unit_amount, amount_value } = item;
        if (!summary[reward_unit]) {
            summary[reward_unit] = { totalUnits: 0, totalValue: 0 };
        }
        summary[reward_unit].totalUnits += reward_unit_amount;
        summary[reward_unit].totalValue += amount_value;
        return summary;
    }, {});

    // Convert rewardSummary object into an array for DataTable
    const rewardSummaryArray = Object.keys(rewardSummary).map(rewardType => ({
        reward_unit: rewardType,
        totalUnits: rewardSummary[rewardType].totalUnits,
        totalValue: rewardSummary[rewardType].totalValue,
    }));

    return (
        <div className="col-12 mt-4 shadow-2 border-round bg-gray-200">

            <div className="text-2xl pb-2 text-center">Reward Unit Summary</div>
                    
                    <DataTable value={rewardSummaryArray} showGridlines tableStyle={{ minWidth: '50rem' }}>
                        <Column field="reward_unit" header="Reward Unit Type" className="text-center"></Column>
                        <Column 
                            field="totalUnits" 
                            header="Total Units" 
                            body={(rowData) => rowData.totalUnits.toFixed(2)} 
                            className="text-center"
                        ></Column>
                        <Column 
                            field="totalValue" 
                            header="Total Dollar Value (USD)" 
                            body={(rowData) => `$${rowData.totalValue.toFixed(2)}`} 
                            className="text-center"
                        ></Column>
                    </DataTable>
                
            <Divider className="my-4" />            
            <div className="text-3xl pb-2 text-center">Spending Allocation Plan</div>
            {spendingPlan && spendingPlan.length > 0 ? (
                <>
                    <DataTable value={spendingPlan} showGridlines tableStyle={{ minWidth: '50rem' }}>
                        <Column field="card_name" header="Credit Card Name"></Column>
                        <Column field="category" header="Purchase Category"></Column>
                        <Column field="reward_unit" header="Reward Unit"></Column>
                        <Column 
                            field="reward_amount" 
                            header="Amount of Reward Unit" 
                            body={(rowData) => rowData.reward_unit_amount.toFixed(2)}
                        ></Column>
                        <Column 
                            field="amount_value" 
                            header="Total Dollar Value (USD)" 
                            body={(rowData) => `$${rowData.amount_value.toFixed(2)}`}
                            className="text-center"
                        ></Column>
                    </DataTable>
                </>
            ) : (
                <p>No spending plan available.</p>
            )}
        </div>
    );
}