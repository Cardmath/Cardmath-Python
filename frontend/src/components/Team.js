import React from 'react';
import './Team.css';

const Team = () => {
    return (
        <div className="surface-section px-4 py-8 md:px-6 lg:px-8">
            <div className="grid">
                <div className="col-12 lg:col-4 pr-0 lg:pr-4">
                    <div className="text-900 text-5xl font-bold mb-3">Meet our team</div>
                    <p className="text-700 text-lg line-height-3">Our founding team, composed of Columbia University undergraduates, brings a dynamic interdisciplinary focus on engineering and finance. With a strong foundation in both fields, we combine technical expertise with a deep understanding of financial systems to tackle complex challenges. The integration of cutting-edge engineering solutions with strategic financial insight allows us to approach problems from multiple angles, ensuring that our innovations are not only technically sound but also economically viable. Columbia’s collaborative environment has enabled us to bridge the gap between these two critical disciplines, positioning our team to develop solutions that are both technologically advanced and financially sustainable.</p>
                </div>
                <div className="col-12 lg:col-8">
                    <div className="grid">
                        <div className="col-12 lg:col-6 p-3">
                            <img src="/people/johannes.jpg" className="image-class mb-4 w-full" alt="team-1"/>
                            <div className="font-medium text-xl mb-1 text-900">Johannes Losert</div>
                            <span className="text-600 font-medium">Founder</span>
                            <p className="line-height-3 mt-3 mb-3">Undergraduate Senior at Columbia University who has done AI Security research at NIST and Software Engineering at Google, Amazon.</p>
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