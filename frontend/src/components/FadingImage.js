import React from 'react';

function FadingImage({ src, alt, className }) {
    return (
        <div>
            <style>{`
                .fade-image-container {
                    width: 100%;
                    display: flex;
                    justify-content: center;
                    padding: 0;
                }

                .fade-image {
                    width: auto;
                    height: 100%;
                    max-height: 500px;
                    object-fit: cover;
                    mask-image: linear-gradient(to left, rgba(0, 0, 0, 1), rgba(0, 0, 0, 0));
                    -webkit-mask-image: linear-gradient(to left, rgba(0, 0, 0, 1), rgba(0, 0, 0, 0));
                    animation: fadeIn 2s ease-in-out;
                }

                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
            `}</style>
            <div className="fade-image-container">
                <img
                    className={`fade-image ${className}`}
                    src={src}
                    alt={alt}
                />
            </div>
        </div>
    );
}

export default FadingImage;
