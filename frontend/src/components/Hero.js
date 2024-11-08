import React from 'react';

const Hero = () => {
    return (
        <div
            className="relative p-8 overflow-hidden"
            style={{
                backgroundImage: `linear-gradient(
                    90deg,
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
                position: 'relative',
            }}
        >
            {/* Dark gradient overlay with a frosted blur effect */}
            <div
                style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    backgroundImage: `linear-gradient(
                        90deg,
                        rgba(0, 0, 0, 0.4) 0%,
                        rgba(0, 0, 0, 0.2) 100%
                    )`,
                    backdropFilter: 'blur(5px)', // Subtle blur for frosted effect
                    zIndex: 1,
                }}
            />

            {/* Text content */}
            <div className="text-center my-6 relative" style={{ position: 'relative', zIndex: 2 }}>
                <div
                    className="text-6xl text-white font-bold mb-1"
                    style={{
                        textShadow: '1px 1px 5px rgba(0, 0, 0, 0.3)', // Subtle text shadow for readability
                    }}
                >
                    Cardmath
                </div>
                <div
                    className="text-6xl text-blue-100 font-bold mb-4"
                    style={{
                        textShadow: '1px 1px 5px rgba(0, 0, 0, 0.3)', // Subtle text shadow for readability
                    }}
                >
                    We crunch the numbers.
                </div>
                <p
                    className="mt-0 mb-4 line-height-3 text-center mx-auto text-white"
                    style={{
                        maxWidth: '500px',
                        fontWeight: '600', // Slightly increased font weight for readability
                        textShadow: '1px 1px 3px rgba(0, 0, 0, 0.2)', // Lighter shadow for paragraph text
                    }}
                >
                    We provide independent, data-driven credit-card recommendations—just sign into your bank accounts for personalized insights, and rest assured your data is securely protected and only used as needed.
                </p>
                <p
                    className="text-sm mt-4 mb-4 line-height-3 text-white"
                    style={{
                        fontWeight: '600', // Increased font weight for small text
                        textShadow: '1px 1px 3px rgba(0, 0, 0, 0.2)',
                    }}
                >
                    Available for users in the United States Only
                </p>
            </div>
        </div>
    );
};

export default Hero;
