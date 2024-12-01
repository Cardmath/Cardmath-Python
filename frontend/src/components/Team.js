import React from 'react';
import './Team.css';

const Team = () => {
    return (
        <div className="surface-section px-4 py-8 md:px-6 lg:px-8">
            <div className="grid">
                <div className="col-12 lg:col-3 pr-0 lg:pr-4">
                    <div className="text-900 text-5xl font-bold mb-3">Meet the Founder</div>
                    <p className="text-700 text-lg line-height-3">
                        Founders Nick Eliacin and Johannes Losert met during the Google STEP program in the summer of 2023. Their shared passion for technology and finance led them to create Cardmath—a user-friendly conversational assistant that provides personalized credit card recommendations and spending insights to simplify your credit journey.                    
                    </p>
                </div>
                <div className="col-6 lg:col-6">
                    <div className="grid">
                        <div className="col-12 lg:col-6 p-3">
                            <img src="/people/johannes.jpg" className="image-class w-full mb-3" alt="team-1"/>
                            <div className="font-medium text-xl mb-1 text-900">Johannes Losert</div>
                            <span className="text-600 font-medium">Co-Founder</span>
                            <p className="line-height-3 mt-3 mb-3">Senior at Columbia University. Ex Google, Amazon, National Institute of Standards & Technology Intern. Passionate about algorithms and software engineering. </p>
                            <div className="mb-2">
                                <a onClick={() => window.open('https://github.com/johannes-losert/')} tabIndex="0" className="cursor-pointer"><i className="pi pi-github text-600 text-xl mr-3"></i></a>
                                <a onClick={() => window.open('https://www.linkedin.com/in/johannes-losert/')} tabIndex="0" className="cursor-pointer"><i className="pi pi-linkedin text-600 text-xl"></i></a>
                            </div>
                        </div>
                        <div className="col-6 lg:col-6">
                            <img src="people/Eliacin_Nicholas_GeorgiaInstituteOfTechnology.jpg" className="image-class w-full mb-3" alt="team-1"/>
                            <div className="font-medium text-xl mb-1 text-900">Nick Eliacin</div>
                            <span className="text-600 font-medium">Co-Founder</span>
                            <p className="line-height-3 mt-3 mb-3">
                                Senior at Georgia Institute of Technology. Ex Microsoft, Google, and Equifax Intern. Passionate about data analysis in finance.                             </p>
                            <div className="mb-2">
                                <a onClick={() => window.open('https://github.com/gtnick19')} tabIndex="0" className="cursor-pointer"><i className="pi pi-github text-600 text-xl mr-3"></i></a>
                                <a onClick={() => window.open('https://www.linkedin.com/in/neliacin3/')} tabIndex="0" className="cursor-pointer"><i className="pi pi-linkedin text-600 text-xl"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    );
};

export default Team;