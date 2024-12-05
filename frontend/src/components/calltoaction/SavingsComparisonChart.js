import React from 'react';
import { Chart } from 'primereact/chart';

const SavingsComparisonChart = () => {
    // Parameters
    const P = 30000; // Annual purchases
    const r = 0.05;  // Growth rate
    const years = Array.from({length: 11}, (_, i) => i);

    // Calculate savings for User A (3% + $100, with reinvestment)
    const calculateUserASavings = (year) => {
        const annualReward = P * 0.03 + 100;
        let savings = 0;
        for (let t = 1; t <= year; t++) {
            savings += annualReward * Math.pow(1 + r, year - t);
        }
        return savings;
    };

    // Calculate savings for User B with reinvestment (1%)
    const calculateUserBSavingsReinvested = (year) => {
        const annualReward = P * 0.01;
        return r > 0 ? 
            annualReward * (Math.pow(1 + r, year) - 1) / r :
            annualReward * year;
    };

    // Calculate savings for User B without reinvestment (1%)
    const calculateUserBSavings = (year) => {
        return P * 0.01 * year;
    };

    // Calculate savings for User C (4.2% with reinvestment)
    const calculateUserCSavings = (year) => {
        const annualReward = P * 0.042;
        return r > 0 ?
            annualReward * (Math.pow(1 + r, year) - 1) / r :
            annualReward * year;
    };
  
    const data = {
      labels: years.map(year => `Year ${year}`),
      datasets: [
          {
              label: '3% Cashback + $100 Credit (Reinvested)',
              data: years.map(year => Math.round(calculateUserASavings(year))),
              fill: false,
              borderColor: '#00FF94',  // Bright green
              tension: 0.4
          },
          {
            label: '4.2% Cashback (Reinvested)',
            data: years.map(year => Math.round(calculateUserCSavings(year))),
            fill: false,
            borderColor: '#00E5FF',  // Bright light blue
            tension: 0.4
          },
          {
              label: '1% Cashback (Reinvested)',
              data: years.map(year => Math.round(calculateUserBSavingsReinvested(year))),
              fill: false,
              borderColor: '#FFFFFF',  // White
              tension: 0.4
          },
          {
              label: '1% Cashback (No Reinvestment)',
              data: years.map(year => Math.round(calculateUserBSavings(year))),
              fill: false,
              borderColor: 'rgba(255, 255, 255, 0.5)',  // Semi-transparent white
              tension: 0.4
          }
      ]
  };
  
      const options = {
          maintainAspectRatio: false,
          aspectRatio: 0.9,
          plugins: {
              title: {
                  display: true,
                  text: 'The Sooner You Start, The More You Save',
                  color: '#FFFFFF',
                  font: {
                      size: 20,
                      weight: 'bold'
                  },
                  padding: {
                      bottom: 10
                  }
              },
              legend: {
                  position: 'bottom',
                  labels: {
                      padding: 15,
                      boxWidth: 10,
                      usePointStyle: true,
                      color: '#FFFFFF'  // White text for legend
                  },
              },
              tooltip: {
                  callbacks: {
                      label: function(context) {
                          let label = context.dataset.label || '';
                          if (label) {
                              label += ': ';
                          }
                          if (context.parsed.y !== null) {
                              label += new Intl.NumberFormat('en-US', { 
                                  style: 'currency', 
                                  currency: 'USD' 
                              }).format(context.parsed.y);
                          }
                          return label;
                      }
                  },
                  backgroundColor: 'rgba(0, 0, 0, 0.8)',
                  titleColor: '#FFFFFF',
                  bodyColor: '#FFFFFF',
                  borderColor: '#333333'
              }
          },
          scales: {
              x: {
                  grid: {
                      color: 'rgba(255, 255, 255, 0.1)',  // Subtle grid lines
                      drawBorder: true
                  },
                  ticks: {
                      color: '#FFFFFF'  // White text for x-axis
                  }
              },
              y: {
                  title: {
                      display: true,
                      text: 'Total Savings ($)',
                      color: '#FFFFFF'  // White text for y-axis title
                  },
                  grid: {
                      color: 'rgba(255, 255, 255, 0.1)',  // Subtle grid lines
                      drawBorder: true
                  },
                  ticks: {
                      color: '#FFFFFF',  // White text for y-axis
                      callback: function(value) {
                          return new Intl.NumberFormat('en-US', { 
                              style: 'currency', 
                              currency: 'USD',
                              maximumFractionDigits: 0
                          }).format(value);
                      }
                  }
              }
          }
      };
  
      return (
          <div className="bg-gray-900 border-round-xl p-3" style={{
              background: 'rgba(0, 0, 0, 0.2)',  // Semi-transparent dark background
              backdropFilter: 'blur(10px)'  // Glassmorphism effect
          }}>
              <div style={{ height: '330px', width: '700px' }}>
                  <Chart type="line" data={data} options={options} />
              </div>
          </div>
      );
  };
  
  export default SavingsComparisonChart;