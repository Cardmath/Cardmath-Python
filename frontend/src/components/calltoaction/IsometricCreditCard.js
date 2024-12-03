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
    function updateGridSize() {
      const isMobile = window.matchMedia('(max-width: 768px)').matches;
      const gridSize = isMobile ? 2 : 5;
      document.documentElement.style.setProperty('--gridSize', gridSize.toString());
    }

    function scrollGrid() {
      const wrapperHeight = document.querySelector(".wrapper").offsetHeight;
      const cards = document.querySelector(".icc-cards");
      const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight));
      const transY = scrollPercent * -100 + 50;
      
      cards.style.setProperty("--scroll", `${transY}%`);
    }

    window.addEventListener("resize", () => {
      updateGridSize();
      scrollGrid();
    });
    window.addEventListener("scroll", scrollGrid);

    // Initial calls
    updateGridSize();
    scrollGrid();

    return () => {
      window.removeEventListener("resize", updateGridSize);
      window.removeEventListener("scroll", scrollGrid);
    };
  }, []);

  // Get current grid size for card count
  const gridSize = window.matchMedia('(max-width: 768px)').matches ? 2 : 5;
  const totalCards = gridSize * gridSize;

  return (
    <div className="wrapper">
      <div className="icc-main">
        <div className="icc-cards">
          {[...Array(totalCards)].map((_, index) => {
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
              </a>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default IsometricCreditCard;
