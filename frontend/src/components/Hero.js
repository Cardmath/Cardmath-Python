import React from 'react';

const Hero = () => {
    return (
        <div
            className="relative p-4 md:p-8 overflow-hidden"
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
            <div className="text-center my-7 relative" style={{ position: 'relative', zIndex: 2 }}>
                <div
                    className="font-bold text-4xl md:text-6xl text-white mb-1"
                    style={{
                        textShadow: '1px 1px 5px rgba(0, 0, 0, 0.3)', // Subtle text shadow for readability
                        animation: 'tracking-in-expand 0.7s cubic-bezier(0.215, 0.61, 0.355, 1.000) both', // Animation for text
                    }}
                >
                    Cardmath
                </div>
                <div
                    className="font-bold text-4xl md:text-6xl text-blue-100 mb-4"
                    style={{
                        textShadow: '1px 1px 5px rgba(0, 0, 0, 0.3)', // Subtle text shadow for readability
                    }}
                >
                    Your Wallet's Best Friend
                </div>
                <p
                    className="mt-0 mb-4 line-height-3 text-center mx-auto text-white text-base md:text-lg px-2 md:px-0"
                    style={{
                        maxWidth: '500px',
                        fontWeight: '600', // Slightly increased font weight for readability
                        textShadow: '1px 1px 3px rgba(0, 0, 0, 0.2)', // Lighter shadow for paragraph text
                    }}
                >
                    Stop guessing and start saving. Cardmath helps you pick credit cards that maximize your rewards.
                </p>
            </div>
        </div>
    );
};

export default Hero;
