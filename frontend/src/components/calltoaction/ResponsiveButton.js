import React from 'react';

const ResponsiveButton = ({ onClick, children, className = '' }) => {
    const buttonStyle = {
        fontSize: '30px',
        padding: '10px 30px',
        margin: '30px',
        border: '0',
        cursor: 'pointer',
        color: 'white',  // Changed to white for better contrast on dark background
        borderRadius: '10px',
        display: 'inline-block',
        overflow: 'hidden',
        transition: 'all 0.4s cubic-bezier(.86, .01, .15, .99)',
        backgroundColor: '#2A2A2A',  // Dark grey background
        transform: 'translateY(0)',
        fontFamily: 'Playfair Display, sans-serif',
        position: 'relative'
    };

    const beforeElementStyle = {
        content: '""',
        position: 'absolute',
        zIndex: '-1',
        top: '0px',
        left: '0px',
        right: '0px',
        bottom: '0',
        background: 'linear-gradient(to right, #00E5B0, #00E5FF)',  // Light teal gradient
        transform: 'scaleX(0)',
        transformOrigin: '100% 0%',
        transition: '0.4s cubic-bezier(.86, .01, .15, .99)'
    };

    const hoverStyles = {
        color: '#333',  // Dark text on hover for contrast with teal
        boxShadow: '0 5px 35px rgba(0, 0, 0, 0.6)',
        transform: 'translateY(-5px)'
    };

    const beforeHoverStyles = {
        transform: 'scaleX(1.1) scaleY(1.1)'
    };

    const [isHovered, setIsHovered] = React.useState(false);

    return (
        <button 
            onClick={onClick}
            className={className}
            style={{
                ...buttonStyle,
                ...(isHovered ? hoverStyles : {})
            }}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            <div
                style={{
                    ...beforeElementStyle,
                    ...(isHovered ? beforeHoverStyles : {})
                }}
            />
            {children}
        </button>
    );
};

export default ResponsiveButton;