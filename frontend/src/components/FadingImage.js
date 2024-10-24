import React from 'react';
import './FadingImage.css'; // Import the CSS file

function FadingImage({ src }) {
    return (
      <div>
        <img
          className="fade-image"
          src={src} // Dynamically set the image source
          alt="Fading Effect"
        />
      </div>
    );
  }
  
export default FadingImage;
  

