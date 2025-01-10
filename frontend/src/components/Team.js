import React from 'react';

const Team = () => {
    return (
        <div className="px-4 py-8 md:px-6 lg:px-8 sm:px-6">
            <div className="grid">
                <div className="lg:col-3 sm:col-12 pr-4">
                    <div className="text-white text-5xl font-bold mb-3">Contact Us</div>
                    <p className="text-200 text-lg line-height-3">
                        We'd love to hear from you! Nick and Johannes are always eager to receive your feedback and insights. Nick and Johannes met during the Google STEP program in the summer of 2023. Their shared passion for technology and finance led them to build Cardmath.                    
                    </p>
                </div>
                    <div className='lg:col-4 sm:col-12'>
                        <div className="bg-no-repeat bg-center border-round h-20rem w-full" style={{ backgroundImage: "url('people/Eliacin_Nicholas_GeorgiaInstituteOfTechnology.jpg')", backgroundSize: '300px auto' }} ></div>
                        <div className="font-medium text-xl mb-1 text-0">
                            Nick Eliacin    
                        </div>
                        <div className="text-md mb-1 text-300" style={{fontFamily: 'Consolas, Monaco, "Courier New", monospace', fontStyle: 'italic'}}>
                            nick@cardmath.ai    
                        </div>
                        <span className="text-300 font-medium">Co-Founder, CEO</span>
                        <p className="line-height-3 mt-3 mb-3 mr-3 text-200">Senior at Georgia Institute of Technology. Ex Microsoft, Google, and Equifax Intern. Passionate about data analysis in finance.</p>
                        <div className="mb-2">
                            <a onClick={() => window.open('https://github.com/gtnick19')} tabIndex="0" className="cursor-pointer"><i className="pi pi-github text-600 text-xl mr-3"></i></a>
                            <a onClick={() => window.open('https://www.linkedin.com/in/neliacin3/')} tabIndex="0" className="cursor-pointer"><i className="pi pi-linkedin text-600 text-xl"></i></a>
                        </div>
                    </div>
                    <div className="lg:col-4 sm:col-12">
                        <div className="bg-no-repeat bg-center border-round h-20rem w-full" style={{ backgroundImage: "url('people/johannes.jpg')", backgroundSize: '300px auto' }} ></div>
                        <div className="font-medium text-xl mb-1 text-0">Johannes Losert</div>
                        <div className="text-md mb-1 text-300" style={{fontFamily: 'Consolas, Monaco, "Courier New", monospace', fontStyle: 'italic'}}>
                            johannes@cardmath.ai    
                        </div>
                        <span className="text-300 font-medium">Co-Founder, CTO</span>
                        <p className="line-height-3 mt-3 mb-3 mr-3 text-200">Senior at Columbia University. Ex Amazon, Google,  National Institute of Standards & Technology Intern. Passionate about algorithms and software engineering. </p>
                        <div className="mb-2">
                            <a onClick={() => window.open('https://github.com/johannes-losert/')} tabIndex="0" className="cursor-pointer"><i className="pi pi-github text-600 text-xl mr-3"></i></a>
                            <a onClick={() => window.open('https://www.linkedin.com/in/johannes-losert/')} tabIndex="0" className="cursor-pointer"><i className="pi pi-linkedin text-600 text-xl"></i></a>
                        </div>
                    </div>
            </div>
        </div>

    );
};

export default Team;