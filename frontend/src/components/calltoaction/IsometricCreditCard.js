import React, { useEffect } from 'react';
import './IsometricCreditCard.css';

const cardText = [
  {issuer: "Visa", name:"Don Joel",position:"Web Developer",email:"donjoel@example.com",phone:"216-362-0665",address:"2699 Glenwood Avenue",city:"Brook Park, OH 44142"},
  {issuer: "Mastercard",name:"Joe Schmoe",position:"Graphic Designer",email:"joeschmoe@example.com",phone:"407-712-8549",address:"469 Grand Avenue",city:"Winter Park, FL 32789"},
  {issuer: "Citi" ,name:"Clint Westwood",position:"Customer Support",email:"clintwestwood@example.com",phone:"865-217-3165",address:"2212 Brown Avenue",city:"Hartford, TN 37753"},
  {issuer: "Bank of America", name:"Ann Thrax",position:"Project Manager",email:"annthrax@example.com",phone:"808-293-4613",address:"3801 Stratford Drive",city:"Laie, HI 96762"}
];

const CardText = ({ issuer, name, position, email, phone, address, city }) => (
  <div className="icc-contents">
    <h2>{issuer}</h2>
    <h3>{name}</h3>
    {position}
    <br />
    {email}
    <br />
    {phone}
    <br />
    {address}
    <br />
    {city}
  </div>
);

const CityOnly = ({ city }) => (
  <div className="icc-contents">
    <div className="icc-city">{city}</div>
  </div>
);

const IsometricCreditCard = () => {
  useEffect(() => {
    function scrollGrid() {
      const wrapperHeight = document.querySelector(".wrapper").offsetHeight;
      const cards = document.querySelector(".icc-cards");
      const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight));
      const transY = scrollPercent * -100 + 50 ;
      
      cards.style.setProperty("--scroll", `${transY}%`);
    }

    {// // Log positions
    // const main = document.querySelector('.icc-main');
    // const wrapper = document.querySelector('.wrapper');
    // const cardsEl = document.querySelector('.icc-cards');
    
    // [main, wrapper, cardsEl].forEach(el => {
    //   const rect = el.getBoundingClientRect();
    //   console.log(`${el.className}:`, {
    //     top: rect.top,
    //     left: rect.left, 
    //     bottom: rect.bottom,
    //     right: rect.right,
    //     width: rect.width,
    //     height: rect.height
    //   });
    // });}
    }

    window.addEventListener("resize", scrollGrid);
    window.addEventListener("scroll", scrollGrid);

    scrollGrid(); // Initial call

    return () => {
      window.removeEventListener("resize", scrollGrid);
      window.removeEventListener("scroll", scrollGrid);
    };
  }, []);

  return (
    <div class="wrapper">
    <div className="icc-main">
      <div className="icc-cards">
        {[...Array(64)].map((_, index) => {
          const c = index % cardText.length;
          return (
            <a className="icc-stack" key={index}>
              <div className="icc-card top">
                <CardText {...cardText[c]} />
              </div>
              <div className="icc-card mid">
                <CityOnly city={cardText[c].city} />
              </div>
              <div className="icc-card bottom">
                <CityOnly city={cardText[c].city} />
              </div>
              <div className="icc-card shadow"></div>
            </a>
          );
        })}
      </div>
    </div>
    </div>
  );
};

export default IsometricCreditCard;
