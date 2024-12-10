import React, { useEffect, useRef } from 'react';
import { Chart } from 'primereact/chart';

const SavingsComparisonChart = () => {
    const chartRef = useRef(null);

    useEffect(() => {
        const chartElement = document.querySelector('.p-chart');
        if (chartElement) {
            const canvas = chartElement.querySelector('canvas');
            if (canvas) {
                let width, height;
                
                // Get viewport width
                const vw = window.innerWidth;
                
                // Set dimensions based on viewport
                if (vw < 480) { // Mobile
                    width = Math.min(vw - 40, 320); // 40px for padding
                    height = width * 1; // 4:3 ratio
                } else if (vw < 768) { // Tablet
                    width = Math.min(vw - 60, 480);
                    height = width * 0.6;
                } else if (vw < 1024) { // Small laptop
                    width = Math.min(vw - 80, 640);
                    height = width * 0.5;
                } else { // Desktop
                    width = 787;
                    height = 390;
                }
                
                // Set the canvas attributes for render size
                canvas.setAttribute('width', width.toString());
                canvas.setAttribute('height', height.toString());
                
                // Set the display size through styles
                canvas.style.width = `${width}px`;
                canvas.style.height = `${height}px`;
                
                // Set the parent container size
                chartElement.style.width = `${width}px`;
                chartElement.style.height = `${height}px`;
            }
        }    
    }, []);

    const P = 30000;
    const r = 0.05;
    const years = Array.from({length: 11}, (_, i) => i);

    const calculateUserBSavings = (year) => P * 0.01 * year;
    const calculateUserCSavings = (year) => {
        const annualReward = P * 0.042;
        return r > 0 ? annualReward * (Math.pow(1 + r, year) - 1) / r : annualReward * year;
    };
  
    const data = {
        labels: years.map(year => `Year ${year}`),
        datasets: [
            {
                label: 'Average Cardmath Wallet',
                data: years.map(year => Math.round(calculateUserCSavings(year))),
                fill: false,
                borderColor: '#00E5FF',
                tension: 0.4
            },
            {
                label: 'Average American Wallet',
                data: years.map(year => Math.round(calculateUserBSavings(year))),
                fill: false,
                borderColor: 'rgba(255, 255, 255, 0.5)',
                tension: 0.4
            }
        ]
    };
  
    const options = {
        responsive: false, // Turn off ChartJS's built-in responsiveness
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: 'See How Much You Could Save Over 10 Years!',
                color: '#FFFFFF',
                font: {
                    size: 20,
                    weight: 'bold'
                }
            },
            legend: {
                position: 'bottom',
                labels: {
                    color: '#FFFFFF'
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return `${context.dataset.label}: ${new Intl.NumberFormat('en-US', { 
                            style: 'currency', 
                            currency: 'USD' 
                        }).format(context.parsed.y)}`;
                    }
                }
            }
        },
        scales: {
            x: {
                ticks: { color: '#FFFFFF' }
            },
            y: {
                ticks: {
                    color: '#FFFFFF',
                    callback: value => new Intl.NumberFormat('en-US', { 
                        style: 'currency', 
                        currency: 'USD',
                        maximumFractionDigits: 0
                    }).format(value)
                }
            }
        }
    };

    return (
        <div style={{
            padding: '20px',
            background: 'rgba(0, 0, 0, 0.2)',
            backdropFilter: 'blur(10px)',
            borderRadius: '12px',
            display: 'flex',
            justifyContent: 'center'
        }}>
            <Chart 
                ref={chartRef}
                type="line" 
                data={data} 
                options={options} 
            />
        </div>
    );
};

export default SavingsComparisonChart;