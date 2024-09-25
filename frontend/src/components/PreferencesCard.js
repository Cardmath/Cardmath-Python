import React, { useState } from 'react';
import { Ripple } from 'primereact/ripple';
import { Button } from 'primereact/button';
import { Divider } from 'primereact/divider';
import { MultiSelect } from 'primereact/multiselect';
import { InputTextarea } from 'primereact/inputtextarea';

const PreferencesCard = () => {

    const [activeTab, setActiveTab] = useState('CreditProfile');

    const handleTabClick = (tab) => {
        setActiveTab(tab);
    };

    const [selectedBanks, setSelectedBanks] = useState(null);
    const banks = [
        { name: 'Chase', code: 'CHASE' },
        { name: 'Bank of America', code: 'BOA' },
        { name: 'Wells Fargo', code: 'WF' },
        { name: 'Citi', code: 'CITI' },
        { name: 'Capital One', code: 'CAPONE' },
        { name: 'American Express', code: 'AMEX' },
        { name: 'Discover', code: 'DISCOVER' },
        { name: 'US Bank', code: 'USBANK' },
        { name: 'PNC Bank', code: 'PNC' },
        { name: 'TD Bank', code: 'TD' },
        { name: 'HSBC', code: 'HSBC' }
    ];
            
        

    return (        
        <div className="surface-ground px-4 md:px-6 lg:px-8">
            <div className="p-fluid flex flex-column lg:flex-row">
                <ul className="list-none m-0 p-0 flex flex-row lg:flex-column justify-content-evenly md:justify-content-between lg:justify-content-start mb-5 lg:pr-8 lg:mb-0">
                    <li>
                        <a onClick={() => handleTabClick('CreditProfile')} className="p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors">
                            <i className="pi pi-credit-card md:mr-2"></i>
                            <span className="font-medium hidden md:block">Credit Profile</span>
                            <Ripple />
                        </a>
                    </li>
                    <li>
                        <a onClick={() => handleTabClick('Banks')} className="p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors">
                            <i className="pi pi-building-columns md:mr-2"></i>
                            <span className="font-medium hidden md:block">Banks</span>
                            <Ripple />
                        </a>
                    </li>
                    <li>
                        <a className="p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors">
                            <i className="pi pi-map md:mr-2"></i>
                            <span className="font-medium hidden md:block">Travel</span>
                            <Ripple />
                        </a>
                    </li>
                    <li>
                        <a className="p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors">
                            <i className="pi pi-shop md:mr-2"></i>
                            <span className="font-medium hidden md:block">Shopping & Dining</span>
                            <Ripple />
                        </a>
                    </li>
                    <li>
                        <a className="p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors">
                            <i className="pi pi-briefcase  md:mr-2"></i>
                            <span className="font-medium hidden md:block">Business Needs</span>
                            <Ripple />
                        </a>
                    </li>
                </ul>
                {activeTab == 'CreditProfile' && (<div className="surface-card p-5 shadow-2 border-round flex-auto">
                    <div className="text-900 font-semibold text-lg mt-3">Credit Profile</div>
                    <Divider></Divider>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label htmlFor="email" className="block font-medium text-900 mb-2">
                                    Credit Score
                                </label>
                                <InputTextarea autoResize id="email" type="text" keyfilter="int" placeholder="300-850" rows={1} cols={1} />
                                
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block font-medium text-900 mb-2">
                                    Estimated Salary
                                </label>
                                <InputTextarea autoResize id="bio" type="text" keyfilter="int" placeholder="Enter your salary here" rows={1} cols={1} />
                            </div>
                            <div>
                                <Button label="Update Profile" className="p-ripple w-auto"></Button>
                            </div>
                        </div>
                    </div>
                </div>)}
                {activeTab == 'Banks' && (<div className="surface-card p-5 shadow-2 border-round flex-auto">
                    <div className="text-900 font-semibold text-lg mt-3">Favorite Banks</div>
                    <Divider></Divider>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label htmlFor="email" className="block font-medium text-900 mb-2">
                                    Preferred Banks
                                </label>
                                <MultiSelect value={selectedBanks} onChange={(e) => setSelectedBanks(e.value)} options={banks} optionLabel="name" 
                                    placeholder="Select Preferred Banks" maxSelectedLabels={3} className="w-full md:w-20rem" />
                                
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block font-medium text-900 mb-2">
                                    Banks to Avoid
                                </label>
                                <MultiSelect value={selectedBanks} onChange={(e) => setSelectedBanks(e.value)} options={banks} optionLabel="name" 
                                    placeholder="Select Banks to Avoid" maxSelectedLabels={3} className="w-full md:w-20rem" /></div>
                            <div>
                                <Button label="Update Profile" className="p-ripple w-auto"></Button>
                            </div>
                        </div>
                    </div>
                </div>)}
            </div>
        </div>
    
    );
};

export default PreferencesCard;