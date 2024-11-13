import React from 'react';
import './Team.css';

const Team = () => {
    return (
        <div className="surface-section px-4 py-8 md:px-6 lg:px-8">
            <div className="grid">
                <div className="col-12 lg:col-3 pr-0 lg:pr-4">
                    <div className="text-900 text-5xl font-bold mb-3">Meet the Founder</div>
                    <p className="text-700 text-lg line-height-3">
                        Cardmath was founded by Johannes Losert, a senior at Columbia University with experience at Amazon and Google. Johannes has led all aspects of Cardmath's development, from backend and frontend architecture to advanced algorithms, creating a platform that helps users maximize their credit card rewards.
                        As a solo founder, Johannes has brought Cardmath to life, but we're seeking talented cofounders with engineering and design skills to help us progress. If you're passionate about simplifying personal finance, let's connect!
                    </p>
                </div>
                <div className="col-12 lg:col-8">
                    <div className="grid">
                        <div className="col-12 lg:col-6 p-3">
                            <img src="/people/johannes.jpg" className="image-class w-full mb-3" alt="team-1"/>
                            <div className="font-medium text-xl mb-1 text-900">Johannes Losert</div>
                            <span className="text-600 font-medium">Founder & CEO</span>
                            <p className="line-height-3 mt-3 mb-3">Senior at Columbia University. Ex Google, Amazon, National Institute of Standards & Technology Intern. Passionate about algorithms and software engineering. </p>
                            <div className="mb-2">
                                <a onClick={() => window.open('https://github.com/johannes-losert/')} tabIndex="0" className="cursor-pointer"><i className="pi pi-github text-600 text-xl mr-3"></i></a>
                                <a onClick={() => window.open('https://www.linkedin.com/in/johannes-losert/')} tabIndex="0" className="cursor-pointer"><i className="pi pi-linkedin text-600 text-xl"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    );
};

export default Team;