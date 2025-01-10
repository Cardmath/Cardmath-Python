import React, { useEffect, useState, useRef } from 'react';

const FadeInSection = ({ children }) => {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef();

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      {
        threshold: 0.1, // Trigger when 10% of the element is visible
      }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, []);

  // Inline styles for the fade-in effect
  const styles = {
    base: {
      opacity: 0,
      transform: 'translateY(40px)',
      transition: 'opacity 1.5s ease-out, transform 1.5s ease-out',
    },
    visible: {
      opacity: 1,
      transform: 'translateY(0)',
    },
  };

  return (
    <div
      ref={ref}
      style={{
        ...styles.base,
        ...(isVisible ? styles.visible : {}),
      }}
    >
      {children}
    </div>
  );
};

export default FadeInSection;
