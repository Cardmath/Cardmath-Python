import React, { useState } from 'react';
import { Ripple } from 'primereact/ripple';
import { Button } from 'primereact/button';
import { Divider } from 'primereact/divider';
import { MultiSelect } from 'primereact/multiselect';
import { InputTextarea } from 'primereact/inputtextarea';
import { FloatLabel } from 'primereact/floatlabel';

const PreferencesCard = () => {

    const [activeTab, setActiveTab] = useState('CreditProfile');

    const handleTabClick = (tab) => {
        setActiveTab(tab);
    };

    const [selectedHaveBanks, setSelectedHaveBanks] = useState(null);
    const [selectedBanks, setSelectedBanks] = useState(null);
    const [selectedAvoidBanks, setSelectedAvoidBanks] = useState(null);
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
    
    const [selectedAirlines, setSelectedAirlines] = useState(null);
    const [selectedAvoidAirlines, setSelectedAvoidAirlines] = useState(null);
    const airlines = [
        { name: 'American Airlines', code: 'AA' },
        { name: 'Delta Airlines', code: 'DL' },
        { name: 'United Airlines', code: 'UA' },
        { name: 'Southwest Airlines', code: 'SW' },
        { name: 'Alaska Airlines', code: 'AK' },
        { name: 'JetBlue Airways', code: 'JB' },
        { name: 'Spirit Airlines', code: 'SP' },
        { name: 'Frontier Airlines', code: 'FR' },
        { name: 'Hawaiian Airlines', code: 'HA' },
    ];

    const [selectedRestaurants, setSelectedRestaurants] = useState(null);
    const restaurants = [
        { name: 'Starbucks', code: 'STARBUCKS' },
        { name: 'McDonalds', code: 'MCDONALDS' },
        { name: 'Panera Bread', code: 'PANERA' },
        { name: 'Chipotle', code: 'CHIPOTLE' },
        { name: 'Subway', code: 'SUBWAY' },
        { name: 'Pizza Hut', code: 'PIZZAHUT' },
        { name: 'Domino\'s Pizza', code: 'DOMINOS' },
        { name: 'Applebee\'s', code: 'APPLEBEES' },
        { name: 'Olive Garden', code: 'OLIVEGARDEN' },
        { name: 'Red Lobster', code: 'REDLOBSTER' },
    ];

    const [selectedShopping, setSelectedShopping] = useState(null);
    const shopping = [
        { name: 'Amazon', code: 'AMAZON' },
        { name: 'Target', code: 'TARGET' },
        { name: 'Walmart', code: 'WALMART' },
        { name: 'Best Buy', code: 'BESTBUY' },
        { name: 'Costco', code: 'COSTCO' },
        { name: 'Home Depot', code: 'HOMEDEPOT' },
        { name: 'Lowe\'s', code: 'LOWES' },
        { name: 'GameStop', code: 'GAMESTOP' },
        { name: 'Bed Bath & Beyond', code: 'BEDBATHANDBEYOND' },
        { name: 'TJX Companies', code: 'TJX' },
    ];

    const [selectedLifestyle, setSelectedLifestyle] = useState(null);
    const lifestyle = [
        { name: 'Retired', code: 'RETIRED' },
        { name: 'Student', code: 'STUDENT' },
        { name: 'Early Career', code: 'EARLYCAREER' },
        { name: 'Mid Career', code: 'MIDCAREER' },
        { name: 'Late Career', code: 'LATECAREER' },
    ];
        

    return (        
        <div className="surface-ground px-4 md:px-6 lg:px-8">
            <div className="flex w-full p-fluid flex-column lg:flex-row">
                <ul className="w-3 flex-shrink-0 list-none m-0 p-0 flex flex-row lg:flex-column justify-content-evenly md:justify-content-between lg:justify-content-start mb-5 lg:pr-8 lg:mb-0">
                    <li>
                        <a onClick={() => handleTabClick('CreditProfile')} className="p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors">
                            <Ripple />
                            <i className="pi pi-credit-card md:mr-2"></i>
                            <span className="font-medium hidden md:block">Credit Profile</span>
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
                        <a onClick={() => handleTabClick('Travel')} className="p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors">
                            <i className="pi pi-map md:mr-2"></i>
                            <span className="font-medium hidden md:block">Travel</span>
                            <Ripple />
                        </a>
                    </li>
                    <li>
                        <a onClick={() => handleTabClick('Shopping&Dining')} className="p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors">
                            <i className="pi pi-shop md:mr-2"></i>
                            <span className="font-medium hidden md:block">Shopping & Dining</span>
                            <Ripple />
                        </a>
                    </li>
                    <li>
                        <a onClick={() => handleTabClick('Business')} className="p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors">
                            <i className="pi pi-briefcase  md:mr-2"></i>
                            <span className="font-medium hidden md:block">Business Needs</span>
                            <Ripple />
                        </a>
                    </li>
                </ul>
                {activeTab == 'CreditProfile' && (<div className="sm:w-7 surface-card flex sm:flex-column p-5 shadow-2 border-round">
                    <div className="text-900 font-medium text-xl mt-3">Credit Profile</div>
                    <Divider></Divider>
                    <div className="flex-auto block gap-5 flex-column-reverse font-light text-lg text-500 md:flex-row">
                        Our service doesn’t require a credit check, so your credit score won’t be affected. 
                        Explore our offerings with confidence, knowing your credit remains untouched. 
                        Don’t know your credit score? We recommend checking it through sites like:  
                        <div className="flex-auto">
                            <a className="text-blue-500" href="https://www.creditkarma.com" target="_blank">Credit Karma</a>,&ensp; 
                            <a className="text-blue-500" href="https://www.experian.com" target="_blank">Experian</a>,&ensp;
                            <a className="text-blue-500" href="https://www.creditsesame.com" target="_blank">Credit Sesame</a>.
                        </div>
                    </div>
                    <div className="flex gap-5 flex-column-reverse text-lg text-500 sm:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="pt-5">
                                <FloatLabel>
                                    <label htmlFor="email" className="block text-medium text-900 mb-2">
                                        Approximate Credit Score
                                    </label>
                                    <InputTextarea className='p-2 w-6' autoResize id="email" type="text" keyfilter="int" placeholder="300-850" rows={1} cols={1} />
                                </FloatLabel>
                            </div>
                            <div className="mb-4 pt-5">
                                <FloatLabel>
                                    <label htmlFor="bio" className="block text-medium text-900 mb-2">
                                        Approximate Salary (USD)
                                    </label>
                                    <InputTextarea className='p-2 w-6' autoResize id="bio" type="text" keyfilter="int" placeholder="e.g. 65,000" rows={1} cols={1} />
                                </FloatLabel>                                                            
                            </div>
                            <div className="mb-4 mb-2">
                                <label className="block text-medium mb-2">
                                    Lifestyle
                                </label>
                                <MultiSelect className="p-1 w-6" value={selectedLifestyle} onChange={(e) => setSelectedLifestyle(e.value)} options={lifestyle} optionLabel="name" 
                                    placeholder="Select your Lifestyle" maxSelectedLabels={2} />
                            </div>
                            
                            <div>
                                <Button label="Save" className="p-ripple w-auto"></Button>
                            </div>
                        </div>
                    </div>
                </div>)}
                {activeTab == 'Banks' && (<div className="sm:w-7 surface-card p-5 shadow-2 border-round">
                    <div className="text-900 font-medium text-xl mt-3">Favorite Banks</div>
                    <Divider></Divider>
                    <div className="font-light text-lg text-500 mb-3">Tell us your preferred banks (and ones to avoid) for tailored credit card recommendations!  
                    </div>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    Banks you are already a part of
                                </label>
                                
                                <MultiSelect value={selectedHaveBanks} onChange={(e) => setSelectedHaveBanks(e.value)} options={banks} optionLabel="name" 
                                    placeholder="Select Preferred Banks" maxSelectedLabels={3} className="w-full md:w-20rem" />
                                
                            </div>
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    Preferred Banks
                                </label>
                                
                                <MultiSelect value={selectedBanks} onChange={(e) => setSelectedBanks(e.value)} options={banks} optionLabel="name" 
                                    placeholder="Select Preferred Banks" maxSelectedLabels={3} className="w-full md:w-20rem" />
                                
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block text-medium mb-2">
                                    Banks to Avoid
                                </label>
                                <MultiSelect value={selectedAvoidBanks} onChange={(e) => setSelectedAvoidBanks(e.value)} options={banks} optionLabel="name" 
                                    placeholder="Select Banks to Avoid" maxSelectedLabels={3} className="w-full md:w-20rem" /></div>
                            <div>
                                <Button label="Update Profile" className="p-ripple w-auto"></Button>
                            </div>
                        </div>
                    </div>
                </div>)}
                {activeTab == 'Travel' && (<div className="sm:w-7 surface-card p-5 shadow-2 border-round">
                    <div className="text-900 font-medium text-xl mt-3">Travel Preferences</div>
                    <Divider></Divider>
                    <div className="font-light text-lg text-500 mb-3">Share your travel preferences, and we'll match you with the perfect card to get you there!</div>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    Preferred Airlines
                                </label>
                                
                                <MultiSelect value={selectedAirlines} onChange={(e) => setSelectedAirlines(e.value)} options={airlines} optionLabel="name" 
                                    placeholder="Select Preferred Airlines" maxSelectedLabels={3} className="w-full md:w-20rem" />
                                
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block text-medium mb-2">
                                    Airlines to Avoid
                                </label>
                                <MultiSelect value={selectedAvoidAirlines} onChange={(e) => setSelectedAvoidAirlines(e.value)} options={airlines} optionLabel="name" 
                                    placeholder="Select Airlines to Avoid" maxSelectedLabels={3} className="w-full md:w-20rem" /></div>
                            <div>
                                <Button label="Update Profile" className="p-ripple w-auto"></Button>
                            </div>
                        </div>
                    </div>
                </div>)}
                {activeTab == 'Shopping&Dining' && (<div className="sm:w-7 surface-card p-5 shadow-2 border-round">
                    <div className="text-900 font-medium text-xl mt-3">Shopping & Dining Preferences</div>
                    <Divider></Divider>
                    <div className="font-light text-lg text-500 mb-3">Share your dining and shopping preferences, and we’ll find the right card to match your taste!</div>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    Favorite Restaurants
                                </label>
                                <MultiSelect value={selectedRestaurants} onChange={(e) => setSelectedRestaurants(e.value)} options={restaurants} optionLabel="name" 
                                    placeholder="Select you favorite restaurants" maxSelectedLabels={3} className="w-full md:w-20rem" />
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block text-medium mb-2">
                                    Favorite Stores
                                </label>
                                <MultiSelect value={selectedShopping} onChange={(e) => setSelectedShopping(e.value)} options={shopping} optionLabel="name" 
                                    placeholder="Select your favorite stores" maxSelectedLabels={3} className="w-full md:w-20rem" /></div>
                            <div>
                                <Button label="Update Profile" className="p-ripple w-auto"></Button>
                            </div>  
                        </div>
                    </div>
                </div>)}
                {activeTab == 'Business' && (<div className="sm:w-7 surface-card p-5 shadow-2 border-round">
                    <div className="text-900 font-medium text-xl mt-3">Business Needs</div>
                    <Divider></Divider>
                    <div className="font-light text-lg text-500 mb-3">Tell us your business needs, and we’ll find the card that works as hard as you do!</div>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    Favorite Restaurants
                                </label>
                                <MultiSelect value={selectedRestaurants} onChange={(e) => setSelectedRestaurants(e.value)} options={restaurants} optionLabel="name" 
                                    placeholder="Select you favorite restaurants" maxSelectedLabels={3} className="w-full md:w-20rem" />
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block text-medium mb-2">
                                    Preferred Stores
                                </label>
                                <MultiSelect value={selectedShopping} onChange={(e) => setSelectedShopping(e.value)} options={shopping} optionLabel="name" 
                                    placeholder="Select your favorite stores" maxSelectedLabels={3} className="w-full md:w-20rem" /></div>
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