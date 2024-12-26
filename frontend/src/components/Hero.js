import React from 'react';
import SavingsComparisonChart from './calltoaction/SavingsComparisonChart';
import ResponsiveButton from './calltoaction/ResponsiveButton';
import { useNavigate } from 'react-router-dom';

const Hero = () => {
    const navigate = useNavigate();
    return (
        <div
            className="relative p-5 overflow-hidden flex flex-column md:flex-row align-items-center"
            style={{
                background: `linear-gradient(
                    135deg,
                    hsl(157deg 99% 48%) 0%,
                    hsl(159deg 100% 48%) 4%,
                    hsl(161deg 100% 47%) 8%,
                    hsl(162deg 100% 47%) 13%,
                    hsl(164deg 100% 46%) 17%,
                    hsl(166deg 100% 46%) 21%,
                    hsl(167deg 100% 45%) 25%,
                    hsl(169deg 100% 44%) 29%,
                    hsl(170deg 100% 44%) 33%,
                    hsl(172deg 100% 43%) 37%,
                    hsl(173deg 100% 43%) 42%,
                    hsl(175deg 100% 42%) 46%,
                    hsl(176deg 100% 41%) 50%,
                    hsl(178deg 100% 41%) 54%,
                    hsl(181deg 100% 41%) 58%,
                    hsl(184deg 100% 42%) 63%,
                    hsl(186deg 100% 44%) 67%,
                    hsl(188deg 100% 45%) 71%,
                    hsl(190deg 100% 46%) 75%,
                    hsl(192deg 100% 47%) 79%,
                    hsl(194deg 100% 47%) 83%,
                    hsl(196deg 100% 48%) 87%,
                    hsl(197deg 100% 48%) 92%,
                    hsl(198deg 100% 48%) 96%,
                    hsl(200deg 100% 48%) 100%
                )`,
                backgroundSize: '150% 150%',
                animation: 'bg-pan-diagonal-reverse 8s ease-in-out infinite',
                position: 'relative',
            }}
        >
            <style>
                {`
                /* Diagonal animation from bottom-right to top-left */
                @keyframes bg-pan-diagonal-reverse {
                    0% { background-position: 100% 100%; }
                    50% { background-position: 0% 0%; }
                    100% { background-position: 100% 100%; }
                }

                /* Text animation for Cardmath */
                @keyframes tracking-in-expand {
                    0% { letter-spacing: -0.5em; opacity: 0; }
                    40% { opacity: 0.6; }
                    100% { letter-spacing: normal; opacity: 1; }
                }
                `}
            </style>
            {/* Static dark gradient overlay for corner darkening */}
            <div
                style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: `
                        radial-gradient(circle at top right, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0) 50%),
                        radial-gradient(circle at bottom left, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0) 50%)
                    `,
                    zIndex: 1,
                }}
            />

            {/* Text content */}
            <div className="text-center lg:col-6 sm:col-12 my-4 relative" style={{ position: 'relative', zIndex: 2 }}>
                <div
                    className="text-4xl text-white mb-3"
                    style={{
                        textShadow: '1px 1px 5px rgba(0, 0, 0, 0.3)', // Subtle text shadow for readability
                        animation: 'tracking-in-expand 0.7s cubic-bezier(0.215, 0.61, 0.355, 1.000) both', // Animation for text
                    }}
                >
                    Maximum Rewards with the Best Credit Card Wallet
                </div>
                <p
                    className="mt-0 mb-3 line-height-3 text-center mx-auto text-white logo-secondary text-base text-2xl px-2 md:px-0"
                    style={{
                        maxWidth: '500px',
                        fontWeight: '600', // Slightly increased font weight for readability
                        textShadow: '1px 1px 3px rgba(0, 0, 0, 0.2)', // Lighter shadow for paragraph text
                        lineHeight: '1.5',
                    }}
                >
                    We calculate the perfect combination of credit cards tailored to your spending habits, maximizing cashback, points, and savings.
                </p>
                <ResponsiveButton onClick={() => navigate('/register')}>
                    Start Optimizing My Rewards
                </ResponsiveButton>
            </div>

            {/* Examples Section */}
            <div style={{ position: 'relative', zIndex: 2 }}>
                    <SavingsComparisonChart />
            </div>
        </div>
    );
};

export default Hero;
