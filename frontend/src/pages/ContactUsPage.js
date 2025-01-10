// This component is being archived
import React from 'react';
import { InputText } from 'primereact/inputtext';
import { InputTextarea } from 'primereact/inputtextarea';
import { Button } from 'primereact/button';
import Footer from '../components/Footer';
import Navbar from '../components/Navbar';

const ContactUsPage = () => {
    return (
        <div className="h-screen">
            <Navbar />
            <div className="flex grid grid-nogutter">
                {/* Left Section with Gradient */}
                <div
                    className="col-6 p-8"
                    style={{
                        background: `linear-gradient(
                            135deg,
                            hsl(157deg 99% 48%) 0%,
                            hsl(159deg 100% 48%) 4%,
                            hsl(161deg 100% 47%) 8%,
                            hsl(162deg 100% 47%) 13%,
                            hsl(164deg 100% 46%) 17%,
                            hsl(166deg 100% 46%) 21%,
                            hsl(167deg 100% 45%) 25%,
                            hsl(169deg 100% 44%) 29%,
                            hsl(170deg 100% 44%) 33%,
                            hsl(172deg 100% 43%) 37%,
                            hsl(173deg 100% 43%) 42%,
                            hsl(175deg 100% 42%) 46%,
                            hsl(176deg 100% 41%) 50%,
                            hsl(178deg 100% 41%) 54%,
                            hsl(181deg 100% 41%) 58%,
                            hsl(184deg 100% 42%) 63%,
                            hsl(186deg 100% 44%) 67%,
                            hsl(188deg 100% 45%) 71%,
                            hsl(190deg 100% 46%) 75%,
                            hsl(192deg 100% 47%) 79%,
                            hsl(194deg 100% 47%) 83%,
                            hsl(196deg 100% 48%) 87%,
                            hsl(197deg 100% 48%) 92%,
                            hsl(198deg 100% 48%) 96%,
                            hsl(200deg 100% 48%) 100%
                        )`,
                        backgroundSize: '150% 150%',
                        animation: 'bg-pan-diagonal-reverse 8s ease-in-out infinite',
                        position: 'relative',
                    }}
                >
                    <style>
                        {`
                        /* Diagonal animation from bottom-right to top-left */
                        @keyframes bg-pan-diagonal-reverse {
                            0% { background-position: 100% 100%; }
                            50% { background-position: 0% 0%; }
                            100% { background-position: 100% 100%; }
                        }
        
                        /* Text animation for Cardmath */
                        @keyframes tracking-in-expand {
                            0% { letter-spacing: -0.5em; opacity: 0; }
                            40% { opacity: 0.6; }
                            100% { letter-spacing: normal; opacity: 1; }
                        }
                        `}
                    </style>
                    {/* Static dark gradient overlay for corner darkening */}
                    <div
                        style={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            zIndex: 1,
                        }}
                    />
                    <div className="text-gray-800 text-5xl font-bold mb-6"
                        style={{
                            textShadow: '1px 1px 5px rgba(0, 0, 0, 0.3)', // Subtle text shadow for readability
                        }}
                    >Contact Us</div>
                    <div className="text-gray-800 text-2xl mb-6 z-2"
                        style={{
                            textShadow: '1px 1px 5px rgba(0, 0, 0, 0.3)', // Subtle text shadow for readability
                        }}
                    >
                        We’d love to hear from you! Your feedback is invaluable in helping us improve our services and create the best possible experience for you. Whether you have questions, suggestions, or simply want to share your thoughts, don’t hesitate to reach out. We’re here to listen and respond to your needs!
                    </div>

                    <ul className="text-gray-800 list-none p-0 m-0 mt-6">
                        <li className="flex align-items-center mb-3">
                            <i className="pi pi-twitter mr-2"></i>
                            <span>@cardmath</span>
                        </li>
                        <li className="flex align-items-center">
                            <i className="pi pi-inbox mr-2"></i>
                            <span>contact@cardmath.ai</span>
                        </li>
                    </ul>
                </div>

                {/* Right Section with Form */}
                <div className="col-6 bg-gray-800">
                    <div className="p-fluid formgrid grid px-4 py-8 md:px-6 lg:px-8">
                        <div className="field col-12 lg:col-6 mb-4">
                            <InputText id="firstname" type="text" className="py-3 px-2 text-lg" placeholder="First Name" />
                        </div>
                        <div className="field col-12 lg:col-6 mb-4">
                            <InputText id="lastname" type="text" className="py-3 px-2 text-lg" placeholder="Last Name" />
                        </div>
                        <div className="field col-12 mb-4">
                            <InputText id="email2" type="text" className="py-3 px-2 text-lg" placeholder="Email" />
                        </div>
                        <div className="field col-12 mb-4">
                            <InputText id="phone" type="text" className="py-3 px-2 text-lg" placeholder="Phone" />
                        </div>
                        <div className="field col-12 mb-4">
                            <InputTextarea id="message" rows={5} autoResize className="py-3 px-2 text-lg" placeholder="Message" />
                        </div>
                        <div className="col-12 text-right">
                            <Button type="button" label="Submit" icon="pi pi-envelope" className="px-5 py-3 w-auto" />
                        </div>
                    </div>
                </div>
            </div>
        <Footer />
        </div>
    );
};

export default ContactUsPage;
