import React from 'react';
import './CreditCard.css';
import './GlowingBorder.css'

const CreditCard = () => {
  return (
<div className="glow-card">
    <div className="glowing-body">
        <div className="card">
        <div className="flip">
            <div className="front">
            <div className="strip-top"></div>
            <div className="strip-bottom"></div>
            <img className="logo" src="logos/Favicons/logo.svg" alt="Logo" width="100" height="100" />
            <div className="investor">Investor</div>
            <div className="chip">
                <div className="chip-line"></div>
                <div className="chip-line"></div>
                <div className="chip-line"></div>
                <div className="chip-line"></div>
                <div className="chip-main"></div>
            </div>
            <svg className="wave" viewBox="0 3.71 26.959 38.787" width="26.959" height="38.787" fill="white">
                <path d="M19.709 3.719c..." />
                <path d="M13.74 7.563c..." />
                <path d="M7.584 11.438c..." />
            </svg>
            <div className="card-number">
                <div className="section">5453</div>
                <div className="section">2000</div>
                <div className="section">4242</div>
                <div className="section">5100</div>
            </div>
            <div className="end">
                <span className="end-text">exp. end:</span>
                <span className="end-date">11/22</span>
            </div>
            <div className="card-holder">mr Bill Dingcredit</div>
            <div className="master">
                <div className="circle master-red"></div>
                <div className="circle master-yellow"></div>
            </div>
            </div>

            <div className="back">
            <div className="strip-black"></div>
            <div className="ccv">
                <label>ccv</label>
                <div>123</div>
            </div>
            <div className="terms">
                <p>
                This is not a real credit card issued by a bank, and it is in no way affiliated with Mastercard Inc.
                </p>
                <p>This card is not real, why are you even reading this?</p>
            </div>
            </div>
        </div>
        </div>
    </div>
</div>  
  );
};

export default CreditCard;
