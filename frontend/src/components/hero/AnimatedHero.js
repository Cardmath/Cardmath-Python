import React, { useEffect, useState } from 'react';
import  ResponsiveButton  from '../calltoaction/ResponsiveButton'
import { useNavigate } from 'react-router-dom';

const AnimatedHero = () => {
  const [showFirstMessage, setShowFirstMessage] = useState(false);
  const [showSecondMessage, setShowSecondMessage] = useState(false);
  const [showThirdMessage, setShowThirdMessage] = useState(false);
  const [showBackground, setShowBackground] = useState(false);
  const navigate = useNavigate();
  const [count, setCount] = useState(0);
  const [savingsCount, setSavingsCount] = useState(0);
  const targetAmount = 1000000;
  const targetSavings = 40000;
  const duration = 2000;
  const steps = 60;

  const gradientText = `
    linear-gradient(
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
    )
  `;

  const styles = {
    overlay: {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: '#212121',
      opacity: showBackground ? 1 : 1,
      transition: 'opacity 1.5s ease-out',
      zIndex: 2
    },
    container: {
      position: 'relative', 
      fontFamily: 'Source Sans Pro, sans-serif',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center', 
      width: '50%',
      height: '400px',    
      zIndex: 3
    },    
    textLine: {
      position: 'absolute',
      textAlign: 'center',
      fontSize: window.innerWidth < 768 ? '32px' : '78px',
      lineHeight: 1.2,
      gap: '12px',
      opacity: 0,
      top: -100,
      transform: 'translateY(40px)',
      transition: 'all 1s ease-out, color 1.5s ease-out',
      background: showBackground ? 'none' : gradientText,
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: showBackground ? 'white' : 'transparent',
      backgroundSize: '150% 150%',
      animation: 'bg-pan-diagonal-reverse 8s ease-in-out infinite'
    },
    buttonContainer: {
      position: 'absolute',
      textAlign: 'center',
      marginLeft: 'auto',
      marginRight: 'auto',
      transform: `translate(0%, ${showBackground ? '-100px' : '0'})`,
      opacity: showBackground ? 1 : 0,
      transition: 'all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)',
      transitionDelay: '0.3s',
      zIndex: 10
    },
    firstMessage: {
      opacity: showFirstMessage && !showSecondMessage ? 1 : 0,
      transform: showFirstMessage ? 'translateY(0)' : 'translateY(40px)',
    },
    secondMessage: {
      opacity: showSecondMessage && !showThirdMessage ? 1 : 0,
      transform: showSecondMessage ? 'translateY(0)' : 'translateY(40px)',
    },
    thirdMessage: {
      opacity: showThirdMessage ? 1 : 0,
      transform: showThirdMessage ? 'translateY(0)' : 'translateY(40px)',
    },
    amount: {
      fontSize: window.innerWidth < 768 ? '36px' : '85px',
      fontWeight: 'bold',
      background: showBackground ? 'none' : gradientText,
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: showBackground ? 'white' : 'transparent',
      backgroundSize: '150% 150%',
      animation: 'bg-pan-diagonal-reverse 8s ease-in-out infinite'
    },
    finalText: {
      opacity: showBackground ? 0 : 1,
      transition: 'opacity 0.5s ease-out',
    },
    logo: {
      fontSize: '85px',
      fontFamily: 'DM Sans',
      fontWeight: 700,
      display: 'inline-block',
      transform: showBackground ? 'translateY(-190px) scale(1.8)' : 'translateY(0) scale(1)',
      transition: 'all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)',
      animation: showBackground ? 'aura 15s linear infinite' : 'none',
      backgroundImage: showBackground ? `
        radial-gradient(transparent 0, transparent 5%),
        radial-gradient(at 9% 50%, rgb(0, 248, 170) 0px, transparent 30%),
        radial-gradient(at 10% 89%, rgb(41, 238, 195) 0px, transparent 30%),
        radial-gradient(at 30% 12%, rgb(0, 243, 166) 0px, transparent 30%),
        radial-gradient(at 78% 50%, rgb(0, 204, 255) 0px, transparent 60%),
        radial-gradient(at 20% 60%, rgb(80, 220, 255) 0px, transparent 60%),
        radial-gradient(at 75% 25%, rgb(3, 203, 253) 0px, transparent 55%)
      ` : 'none',
      WebkitBackgroundClip: showBackground ? 'text' : 'unset',
      WebkitTextFillColor: 'transparent',
      textShadow: showBackground ? 
        '0 0 2ch rgba(0, 255, 163, 1), 0 0 3ch rgba(0, 194, 255, 1), 0 0 4ch rgba(255, 255, 255, 0.5)' : 
        'none'
    },
    period: {
      opacity: showFirstMessage ? 1 : 0,
      transition: 'opacity 1s ease-out',
      transitionDelay: '2.5s'
    }
  };
  useEffect(() => {
    const firstMessageTimer = setTimeout(() => {
      setShowFirstMessage(true);
    }, 250);

    const secondMessageTimer = setTimeout(() => {
      setShowSecondMessage(true);
    }, 3500);

    const thirdMessageTimer = setTimeout(() => {
      setShowThirdMessage(true);
    }, 7000)

    const backgroundTimer = setTimeout(() => {
      setShowBackground(true);
    }, 9000);

    return () => {
      clearTimeout(firstMessageTimer);
      clearTimeout(secondMessageTimer);
      clearTimeout(thirdMessageTimer);
      clearTimeout(backgroundTimer);
    };
  }, []);

  useEffect(() => {
    if (showFirstMessage) {
      const interval = targetAmount / steps;
      let current = 0;
      
      const timer = setInterval(() => {
        current += 1;
        setCount(Math.floor((current / steps) * targetAmount));
        
        if (current >= steps) {
          clearInterval(timer);
        }
      }, duration / steps);

      return () => clearInterval(timer);
    }
  }, [showFirstMessage]);

  useEffect(() => {
    if (showSecondMessage) {
      const interval = targetSavings / steps;
      let current = 0;
      
      const timer = setInterval(() => {
        current += 1;
        setSavingsCount(Math.floor((current / steps) * targetSavings));
        
        if (current >= steps) {
          clearInterval(timer);
        }
      }, duration / steps);

      return () => clearInterval(timer);
    }
  }, [showSecondMessage]);

  return (
    <div className="relative p-5 overflow-hidden h-screen flex align-items-center justify-content-center z-1">
      <div style={styles.overlay}/>
      <div style={styles.container}>
            <span style={{...styles.textLine, ...styles.firstMessage}}>
              You'll probably exceed <span style={styles.amount}>${count.toLocaleString()}</span> spend with credit cards in your lifetime.
            </span>
            <span style={{...styles.textLine, ...styles.secondMessage}}>
              Spending with the right cards could save you <span style={styles.amount}>${savingsCount.toLocaleString()}</span> or more.
            </span>
            <span style={{...styles.textLine, ...styles.secondMessage}}>
              Spending with the right cards could save you <span style={styles.amount}>${savingsCount.toLocaleString()}</span> or more.
            </span>
            <span style={{...styles.textLine, ...styles.thirdMessage}}>
              <span style={styles.finalText}>Realize these savings on autopilot with </span>
              <span style={styles.logo}>cardmath</span>
              <div style={styles.buttonContainer}>
                <ResponsiveButton onClick={() => navigate('register')}>
                  <span>Calculate your savings</span>              
                </ResponsiveButton>
              </div>
            </span>
            <div className='text-500' style={{fontFamily: 'Inter', opacity: showBackground ? '90%' : '0%', position: 'absolute', top: '20vh', fontFamily: 'Source Sans Pro, sans-serif'}}> 
              <p className='text-xl flex flex-row text-italic'> Our founders previously worked at: </p>
              <div className='text-4xl pi flex flex-row justify-content-center gap-5'>
                <span className='pi-amazon'/>
                <span className='pi-google'/>
                <span className='pi-microsoft'/>
              </div>
            </div>
            <div className='text-500' style={{fontFamily: 'Inter', opacity: showBackground ? '90%' : '0%' , position: 'absolute', top: '52vh', fontFamily: 'Source Sans Pro, sans-serif'}}> 
              <p className='m-0'> Read more </p>
              <div className='text-5xl -m-1 pi flex justify-content-center'>
                <span className='pi-chevron-down fadeoutdown animation-duration-2000 animation-iteration-infinite ' style={styles.chevron}/>
              </div>
            </div>
      </div>
    </div>);
};

export default AnimatedHero;