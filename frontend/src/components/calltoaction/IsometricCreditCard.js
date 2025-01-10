import React, { useEffect } from 'react';
import './IsometricCreditCard.css';

const cardText = [
  { name: "Ava Banks", date: "12/25", number: "5555-6666-7777-8888" },
  { name: "Eli Manning", date: "01/30", number: "1234-5678-9012-3456" },
  { name: "Liam Harper", date: "05/14", number: "9876-5432-1098-7654" },
  { name: "Sophia Lane", date: "09/08", number: "1111-2222-3333-4444" },
  { name: "Max Ryder", date: "02/14", number: "9999-8888-7777-6666" },
];

const CardText = ({ number, date, name}) => (
  <div className="icc-contents">
    <h1>{number}</h1>
    <h2>{date}</h2>
    <h2>{name}</h2>
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
      const gridSize = isMobile ? 2 : 4;
      document.documentElement.style.setProperty('--gridSize', gridSize.toString());
    }

    function scrollGrid() {
      const wrapperHeight = document.querySelector(".wrapper").offsetHeight;
      const cards = document.querySelector(".icc-cards");
      const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight));
      const transY = scrollPercent * 100 - 90;
      
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
  const gridSize = window.matchMedia('(max-width: 768px)').matches ? 2 : 4;
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
