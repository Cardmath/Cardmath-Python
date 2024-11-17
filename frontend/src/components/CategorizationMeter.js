import React, { useState, useEffect } from 'react';
import { MeterGroup } from 'primereact/metergroup';

const CategorizationMeter = ({ progressSummary }) => {
    const [percentages, setPercentages] = useState([]);

    useEffect(() => {
        const total =
            progressSummary.categorized_cc_eligible_count +
            progressSummary.uncategorized_cc_eligible_count +
            progressSummary.non_cc_eligible_count;

        if (total > 0) {
            setPercentages([
                {
                    label: 'Categorized',
                    color: '#34d399',
                    value: Math.round(
                        (progressSummary.categorized_cc_eligible_count / total) * 100
                    ),
                },
                {
                    label: 'Uncategorized',
                    color: '#fbbf24',
                    value: Math.round(
                        (progressSummary.uncategorized_cc_eligible_count / total) * 100
                    ),
                },
                {
                    label: 'Non-Eligible',
                    color: '#ef4444',
                    value: Math.round(
                        (progressSummary.non_cc_eligible_count / total) * 100
                    ),
                },
            ]);
        } else {
            // Default to 0% if total is zero to avoid division errors
            setPercentages([
                { label: 'Categorized', color: '#34d399', value: 0 },
                { label: 'Uncategorized', color: '#fbbf24', value: 0 },
                { label: 'Non-Eligible', color: '#ef4444', value: 0 },
            ]);
        }
    }, [progressSummary]);

    return (
        <div className="w-full h-auto m-2 p-3 border-round shadow-2">
            <MeterGroup values={percentages} />
        </div>
    );
};

export default CategorizationMeter;
