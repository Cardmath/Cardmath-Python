import React from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

export default function SpendingPlanTable({ spendingPlan }) {
    return (
        <div className="col-12 mt-4 shadow-2 border-round bg-gray-200">
            <div className="text-3xl pb-2 text-center">Spending Allocation Plan</div>
            {spendingPlan && spendingPlan.length > 0 ? (
                <DataTable value={spendingPlan} showGridlines tableStyle={{ minWidth: '50rem' }}>
                    <Column field="card_name" header="Credit Card Name"></Column>
                    <Column field="category" header="Purchase Category"></Column>
                    <Column field="reward_unit" header="Reward Unit"></Column>
                    <Column 
                        field="reward_amount" 
                        header="Amount of Reward Unit" 
                        body={(rowData) => rowData.reward_amount.toFixed(2)}
                    ></Column>
                    <Column 
                        field="amount_value" 
                        header="Dollar Value (USD)" 
                        body={(rowData) => `$${rowData.amount_value.toFixed(2)}`}
                        className="text-center"
                    ></Column>
                </DataTable>
            ) : (
                <p>No spending plan available.</p>
            )}
        </div>
    );
}