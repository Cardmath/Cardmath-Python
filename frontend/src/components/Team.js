import React from 'react';
import './Team.css';

const Team = () => {
    return (
        <div className="surface-section px-4 py-8 md:px-6 lg:px-8">
            <div className="grid">
                <div className="col-12 lg:col-3 pr-0 lg:pr-4">
                    <div className="text-900 text-5xl font-bold mb-3">Meet our team</div>
                    <p className="text-700 text-lg line-height-3">
                    Our team includes Cornell, Columbia, and Ohio State Honors students, a 2x founder, and interns from Google and Amazon, with expertise in business, algorithms, and software engineering.
                    </p>
                </div>
                <div className="col-12 lg:col-8">
                    <div className="grid">
                        <div className="col-12 lg:col-6 p-3">
                            <img src="/people/johannes.jpeg" className="image-class mb-4 w-full" alt="team-1"/>
                            <div className="font-medium text-xl mb-1 text-900">Johannes Losert</div>
                            <span className="text-600 font-medium">Founder, Engineering & Business</span>
                            <p className="line-height-3 mt-3 mb-3">Senior @ Columbia - Google, Amazon Intern. Has done AI Security research at NIST and Software Engineering at Google, Amazon.</p>
                            <div className="mb-2">
                                <a tabIndex="0" className="cursor-pointer"><i className="pi pi-twitter text-600 text-xl mr-3"></i></a>
                                <a tabIndex="0" className="cursor-pointer"><i className="pi pi-github text-600 text-xl mr-3"></i></a>
                                <a tabIndex="0" className="cursor-pointer"><i className="pi pi-facebook text-600 text-xl"></i></a>
                            </div>
                        </div>
                        <div className="col-12 lg:col-6 p-3">
                            <img src="/people/trey.jpeg" className="image-class mb-4 w-full" alt="team-2" />
                            <div className="font-medium text-xl mb-1 text-900">Maitreya Dixit</div>
                            <span className="text-600 font-medium">Co-Founder, Engineering</span>
                            <p className="line-height-3 mt-3 mb-3">Senior @ tOSU Honors, 3x Google Intern. Aspiring software engineer with ambitions in the fields of high performance computing and machine learning.</p>
                            <div className="mb-2">
                                <a tabIndex="0" className="cursor-pointer"><i className="pi pi-twitter text-600 text-xl mr-3"></i></a>
                                <a tabIndex="0" className="cursor-pointer"><i className="pi pi-github text-600 text-xl mr-3"></i></a>
                                <a tabIndex="0" className="cursor-pointer"><i className="pi pi-facebook text-600 text-xl"></i></a>
                            </div>
                        </div>
                        <div className="col-12 lg:col-6 p-3">
                            <img src="/people/jackson.webp" className="image-class mb-4 w-full" alt="team-2" />
                            <div className="font-medium text-xl mb-1 text-900">Jackson McBride</div>
                            <span className="text-600 font-medium">Lead Data Scientist</span>
                            <p className="line-height-3 mt-3 mb-3">Passionate data science student at Columbia University with a keen interest in machine learning and its applications in social sciences, particularly economics. As a rising senior, I'm dedicated to expanding my knowledge and skills in the field, with aspirations to pursue advanced studies, potentially including a PhD.</p>
                            <div className="mb-2">
                                <a tabIndex="0" className="cursor-pointer"><i className="pi pi-twitter text-600 text-xl mr-3"></i></a>
                                <a tabIndex="0" className="cursor-pointer"><i className="pi pi-github text-600 text-xl mr-3"></i></a>
                                <a tabIndex="0" className="cursor-pointer"><i className="pi pi-facebook text-600 text-xl"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    );
};

export default Team;