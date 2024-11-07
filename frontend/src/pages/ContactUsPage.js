import React from 'react';
import { InputText } from 'primereact/inputtext';
import { InputTextarea } from 'primereact/inputtextarea';
import { Button } from 'primereact/button';
import Footer from '../components/Footer';

const ContactUsPage = () => {
    return (
        <div className="surface-section">
            <div className="grid grid-nogutter">
                {/* Left Section with Gradient */}
                <div
                    className="col-12 md:col-6 p-8"
                    style={{
                        background: 'linear-gradient(120deg, hsl(146deg 96% 28%) 0%, hsl(147deg 95% 27%) 12%, hsl(148deg 95% 26%) 18%, hsl(149deg 95% 26%) 22%, hsl(150deg 96% 25%) 26%, hsl(151deg 96% 24%) 29%, hsl(152deg 97% 23%) 33%, hsl(153deg 94% 20%) 36%, hsl(154deg 92% 18%) 39%, hsl(156deg 91% 15%) 42%, hsl(159deg 91% 13%) 44%, hsl(163deg 92% 10%) 47%, hsl(169deg 95% 8%) 50%, hsl(171deg 95% 10%) 53%, hsl(172deg 95% 12%) 56%, hsl(173deg 95% 15%) 58%, hsl(173deg 96% 18%) 61%, hsl(174deg 96% 20%) 64%, hsl(174deg 97% 23%) 67%, hsl(174deg 96% 25%) 71%, hsl(174deg 96% 28%) 74%, hsl(174deg 96% 30%) 78%, hsl(174deg 96% 33%) 82%, hsl(174deg 96% 36%) 88%, hsl(174deg 96% 38%) 100%)',
                        backgroundSize: 'cover',
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'flex-start',
                        color: 'white',
                    }}
                >
                    <div className="text-white text-2xl font-medium mb-6">Contact Us</div>
                    <div className="text-gray-300 line-height-3 mb-6">
                        We’d love to hear from you! Your feedback is invaluable in helping us improve our services and create the best possible experience for you. Whether you have questions, suggestions, or simply want to share your thoughts, don’t hesitate to reach out. We’re here to listen and respond to your needs!
                    </div>

                    <ul className="list-none p-0 m-0 mt-6 text-white">
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
                <div className="col-12 md:col-6 bg-gray-800">
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
                            <InputTextarea id="message" rows={3} autoResize className="py-3 px-2 text-lg" placeholder="Message" />
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
