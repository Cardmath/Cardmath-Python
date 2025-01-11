import React from 'react';
import { useEffect } from 'react';

const ResponsiveButton = ({ onClick, children, className = '' }) => {
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      @property --gradient-angle {
        syntax: "<angle>";
        initial-value: 0deg;
        inherits: false;
      }

      @property --gradient-angle-offset {
        syntax: "<angle>";
        initial-value: 0deg;
        inherits: false;
      }

      @property --gradient-percent {
        syntax: "<percentage>";
        initial-value: 5%;
        inherits: false;
      }

      @property --gradient-shine {
        syntax: "<color>";
        initial-value: white;
        inherits: false;
      }

      .shiny-cta {
        --animation: gradient-angle linear infinite;
        --duration: 3s;
        --shadow-size: 2px;
        isolation: isolate;
        display: table;
        position: relative;
        overflow: hidden;
        cursor: pointer;
        padding: 1.25rem 4rem;
        outline-offset: 4px;
        font-family: 'Inter';
        padding: 0.5em 0.7em;
        font-size: 0.6em;
        line-height: 1.2;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: 1px solid transparent;
        border-radius: 360px;
        color: #ffffff;
        background: linear-gradient(#000000, #000000) padding-box,
          conic-gradient(
            from calc(var(--gradient-angle) - var(--gradient-angle-offset)),
            transparent,
            #00FFA3 var(--gradient-percent),
            var(--gradient-shine) calc(var(--gradient-percent) * 2),
            #00C2FF calc(var(--gradient-percent) * 3),
            transparent calc(var(--gradient-percent) * 4)
          ) border-box;
        box-shadow: inset 0 0 0 1px #1a1818;
      }

      .shiny-cta::before,
      .shiny-cta::after,
      .shiny-cta span::before {
        content: "";
        pointer-events: none;
        position: absolute;
        inset-inline-start: 50%;
        inset-block-start: 50%;
        translate: -50% -50%;
        z-index: -1;
      }

      .shiny-cta:active {
        translate: 0 1px;
      }

      .shiny-cta::before {
        --size: calc(100% - var(--shadow-size) * 3);
        --position: 2px;
        --space: calc(var(--position) * 2);
        width: var(--size);
        height: var(--size);
        background: radial-gradient(
          circle at var(--position) var(--position),
          white calc(var(--position) / 4),
          transparent 0
        ) padding-box;
        background-size: var(--space) var(--space);
        background-repeat: space;
        mask-image: conic-gradient(
          from calc(var(--gradient-angle) + 45deg),
          black,
          transparent 10% 90%,
          black
        );
        border-radius: inherit;
        opacity: 0.4;
        z-index: -1;
      }

      .shiny-cta::after {
        --animation: shimmer linear infinite;
        width: 100%;
        aspect-ratio: 1/1;
        background: linear-gradient(
          -50deg,
          transparent,
          #00FFA3,
          transparent
        );
        mask-image: radial-gradient(circle at bottom, transparent 40%, black);
        opacity: 0.6;
      }

      .shiny-cta span {
        z-index: 1;
      }

      .shiny-cta span::before {
        --size: calc(100% + 1rem);
        width: var(--size);
        height: var(--size);
        box-shadow: inset 0 -1ex 2rem 4px #00C2FF;
        opacity: 0;
      }

      .shiny-cta {
        --transition: 800ms cubic-bezier(0.25, 1, 0.5, 1);
        transition: var(--transition);
        transition-property: --gradient-angle-offset, --gradient-percent,
          --gradient-shine;
      }

      .shiny-cta,
      .shiny-cta::before,
      .shiny-cta::after {
        animation: var(--animation) var(--duration),
          var(--animation) calc(var(--duration) / 0.4) reverse paused;
        animation-composition: add;
      }

      .shiny-cta span::before {
        transition: opacity var(--transition);
        animation: calc(var(--duration) * 1.5) breathe linear infinite;
      }

      .shiny-cta:is(:hover, :focus-visible) {
        --gradient-percent: 20%;
        --gradient-angle-offset: 95deg;
        --gradient-shine: #00C2FF;
      }

      .shiny-cta:is(:hover, :focus-visible),
      .shiny-cta:is(:hover, :focus-visible)::before,
      .shiny-cta:is(:hover, :focus-visible)::after {
        animation-play-state: running;
      }

      .shiny-cta:is(:hover, :focus-visible) span::before {
        opacity: 1;
      }

      @keyframes gradient-angle {
        to {
          --gradient-angle: 360deg;
        }
      }

      @keyframes shimmer {
        to {
          rotate: 360deg;
        }
      }

      @keyframes breathe {
        from,
        to {
          scale: 1;
        }
        50% {
          scale: 1.2;
        }
      }
    `;
    document.head.appendChild(style);
    return () => document.head.removeChild(style);
  }, []);

  return (
    <button 
      onClick={onClick}
      className={`shiny-cta ${className}`}
    >
      <span>{children}</span>
    </button>
  );
};

export default ResponsiveButton;