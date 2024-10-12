import React, { useState } from 'react';
import { Ripple } from 'primereact/ripple';
import { Button } from 'primereact/button';
import { Divider } from 'primereact/divider';
import { MultiSelect } from 'primereact/multiselect';
import { InputTextarea } from 'primereact/inputtextarea';
import { FloatLabel } from 'primereact/floatlabel';
import { fetchWithAuth } from '../pages/AuthPage';
import { Dropdown } from 'primereact/dropdown';

const PreferencesCard = ( {setAlert} ) => {
    function checkProperties(obj) {
        for (var key in obj) {
            if (obj[key] !== null && obj[key] != "")
                return false;
        }
        return true;
    }

    const [activeTab, setActiveTab] = useState('CreditProfile');

    const handleTabClick = (tab) => {
        setActiveTab(tab);
    };

    const [selectedHaveBanks, setSelectedHaveBanks] = useState(null);
    const [selectedBanks, setSelectedBanks] = useState(null);
    const [selectedAvoidBanks, setSelectedAvoidBanks] = useState(null);
    const banks = [
        'Chase',
        'Bank of America',
        'Wells Fargo',
        'Citi',
        'Capital One',
        'American Express',
        'Discover',
        'US Bank',
        'PNC Bank',
        'TD Bank',
        'HSBC'
    ];    
    const findBanksIntersection = () => {
        const intersection = selectedBanks?.filter(x => selectedAvoidBanks?.includes(x)) || [];
        if (intersection.length > 0) {
            return intersection;
        }
        return null;
    }

    const [selectedAirlines, setSelectedAirlines] = useState(null);
    const [selectedAvoidAirlines, setSelectedAvoidAirlines] = useState(null);
    const airlines = [
        'American Airlines',
        'Delta Airlines',
        'United Airlines',
        'Southwest Airlines',
        'Alaska Airlines',
        'JetBlue Airways',
        'Spirit Airlines',
        'Frontier Airlines',
        'Hawaiian Airlines',
    ];
    const findAirlinesIntersection = () => {
        const intersection = selectedAirlines?.filter(x => selectedAvoidAirlines?.includes(x)) || [];
        if (intersection.length > 0) {
            return intersection;
        }
        return null;
    }


    const [selectedRestaurants, setSelectedRestaurants] = useState(null);
    const restaurants = [
        'Starbucks',
        'McDonalds',
        'Panera Bread',
        'Chipotle',
        'Subway',
        'Pizza Hut',
        'Domino\'s Pizza',
        'Applebee\'s',
        'Olive Garden',
        'Red Lobster',
    ];

    const [selectedShopping, setSelectedShopping] = useState(null);
    const shopping = [
        'Amazon',
        'Target',
        'Walmart',
        'Best Buy',
        'Costco',
        'Home Depot',
        'Lowe\'s',
        'GameStop',
        'Bed Bath & Beyond',
        'TJX Companies',
    ];

    const [selectedLifestyle, setSelectedLifestyle] = useState(null);
    const lifestyle = [
        'Retired',
        'Student',
        'Early Career',
        'Mid-Career',
        'Late Career',
    ];

    const [creditScore, setCreditScore] = useState(null);
    const [salary, setSalary] = useState(null);

    const [selectedIndustries, setSelectedIndustries] = useState(null);
    const industries = [
        'Other',
        'Restaurant',
        'Hotel',
        'Hotel Rental',
        'Technology',
        'Healthcare',
        'Entertainment',
        'Consumer Goods',
        'Construction',
    ];

    const [selectedBusinessSize, setSelectedBusinessSize] = useState(null);
    const businessSizes = [
        'Micro (less than 10 employees)',
        'Small (10-49 employees)',
        'Medium (50-199 employees)',
        'Large (200-499 employees)',
        'Enterprise (500 or more employees)',
    ]

    const sendPreferences = () => {
        const credit_profile_out = { 
            credit_score: creditScore !== null ? creditScore : null,
            salary: salary !== null ? salary : null,
            lifestyle : selectedLifestyle !== null ? selectedLifestyle : null
        };

        const banks_preferences_out = {
            have_banks: selectedHaveBanks !== null ? [...selectedHaveBanks] : null,
            preferred_banks: selectedBanks !== null ? [...selectedBanks] : null,
            avoid_banks: selectedAvoidBanks !== null ? [...selectedAvoidBanks] : null
        }

        var intersection = findBanksIntersection();
        console.log(intersection);
        if (intersection !== null) {
            setAlert({
                visible: true,
                message: 'You cannot avoid and prefer the same bank. Violating Banks: ' + intersection.join(', '),
                heading: 'Preference Contradiction',
                type: 'error'
            })
            return;
        }

        const travel_preferences_out = {
            preferred_airlines : selectedAirlines !== null ? [...selectedAirlines] : null,
            avoid_airlines : selectedAvoidAirlines !== null ? [...selectedAvoidAirlines] : null,
            frequent_travel_destinations : null,
            desired_benefits : null
        }

        var intersection = findAirlinesIntersection();
        console.log(intersection);
        if (intersection !== null) {
            setAlert({
                visible: true,
                message: 'You cannot avoid and prefer the same airline. Violating airlines: ' + intersection.join(', '),
                heading: 'Preference Contradiction',
                type: 'error'
            })
            return;
        }
        
        const consumer_preferences_out = {
            favorite_restaurants: selectedRestaurants !== null ? [...selectedRestaurants] : null,
            favorite_stores: selectedShopping !== null ? [...selectedShopping] : null,
        };        

        const business_preferences_out = {
            business_type: selectedIndustries !== null ? [...selectedIndustries] : null,
            business_size: selectedBusinessSize !== null ? selectedBusinessSize : null
        }

        fetchWithAuth('http://localhost:8000/ingest_user_preferences', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                credit_profile: checkProperties(credit_profile_out) ? null : credit_profile_out, 
                banks_preferences: checkProperties(banks_preferences_out) ? null : banks_preferences_out,
                travel_preferences: checkProperties(travel_preferences_out) ? null : travel_preferences_out,
                consumer_preferences: checkProperties(consumer_preferences_out) ? null : consumer_preferences_out,
                business_preferences: checkProperties(business_preferences_out) ? null : business_preferences_out
            })
        }).then(() => {
            console.log("Preferences submitted!");
        }).then( () => {
            setAlert({
                visible: false,
                message: '',
                heading: '',
                type: 'error'
            })    
        }
        );
    }
        

    return (        
        <div className="surface-ground px-4 md:px-6 lg:px-8">
            <div className="p-fluid flex flex-column lg:flex-row">
                <ul className="w-3 flex-shrink-0 list-none m-0 p-0 flex flex-row lg:flex-column justify-content-evenly md:justify-content-between lg:justify-content-start mb-5 lg:pr-8 lg:mb-0">
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
                {activeTab == 'CreditProfile' && (<div className="sm:w-7 fadein animation-duration-100 surface-card flex sm:flex-column p-5 shadow-2 border-round">
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
                                    <InputTextarea onChange={(e) => setCreditScore(e.target.value)} className='p-2 w-6' autoResize id="email" type="text" keyfilter="int" placeholder="300-850" rows={1} cols={1} />
                                </FloatLabel>
                            </div>
                            <div className="mb-4 pt-5">
                                <FloatLabel>
                                    <label htmlFor="bio" className="block text-medium text-900 mb-2">
                                        Approximate Salary (USD)
                                    </label>
                                    <InputTextarea onChange={(e) => setSalary(e.target.value)} className='p-2 w-6' autoResize id="bio" type="text" keyfilter="int" placeholder="e.g. 65,000" rows={1} cols={1} />
                                </FloatLabel>                                                            
                            </div>
                            <div className="mb-4 mb-2">
                                <label className="block text-medium mb-2">
                                    Lifestyle
                                </label>
                                <Dropdown className="p-1 w-6" value={selectedLifestyle} onChange={(e) => setSelectedLifestyle(e.value)} options={lifestyle} 
                                    placeholder="Select your Lifestyle" />
                            </div>
                            
                            <div>
                                <Button onClick={() => {
                                    sendPreferences()
                                    setActiveTab('Banks')
                                }} label="Save and Continue" className="p-ripple w-auto"></Button>
                            </div>
                        </div>
                    </div>
                </div>)}
                {activeTab == 'Banks' && (<div className="sm:w-7 fadein animation-duration-100 surface-card p-5 shadow-2 border-round">
                    <div className="text-900 font-medium text-xl mt-3">Favorite Banks</div>
                    <Divider></Divider>
                    <div className="font-light text-lg text-500 mb-3">Tell us your preferred banks (and ones to avoid) for tailored credit card recommendations!  
                    </div>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    Banks you have Accounts with
                                </label>
                                
                                <MultiSelect value={selectedHaveBanks} onChange={(e) => setSelectedHaveBanks(e.value)} options={banks}
                                    placeholder="Select Your Banks" maxSelectedLabels={3} className="w-full md:w-20rem" />
                                
                            </div>
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    Preferred Banks
                                </label>
                                
                                <MultiSelect value={selectedBanks} onChange={(e) => setSelectedBanks(e.value)} options={banks}
                                    placeholder="Select Preferred Banks" maxSelectedLabels={3} className="w-full md:w-20rem" />
                                
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block text-medium mb-2">
                                    Banks to Avoid
                                </label>
                                <MultiSelect value={selectedAvoidBanks} onChange={(e) => setSelectedAvoidBanks(e.value)} options={banks}
                                    placeholder="Select Banks to Avoid" maxSelectedLabels={3} className="w-full md:w-20rem" /></div>
                            <div>
                                <Button onClick={() => {
                                    sendPreferences();
                                    setActiveTab('Travel'); 
                                    }} label="Save and Continue" className="p-ripple w-auto"></Button>
                            </div>
                        </div>
                    </div>
                </div>)}
                {activeTab == 'Travel' && (<div className="sm:w-7 fadein animation-duration-100 surface-card p-5 shadow-2 border-round">
                    <div className="text-900 font-medium text-xl mt-3">Travel Preferences</div>
                    <Divider></Divider>
                    <div className="font-light text-lg text-500 mb-3">Share your travel preferences, and we'll match you with the perfect card to get you there!</div>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    Preferred Airlines
                                </label>
                                
                                <MultiSelect value={selectedAirlines} onChange={(e) => setSelectedAirlines(e.value)} options={airlines}
                                    placeholder="Select Preferred Airlines" maxSelectedLabels={3} className="w-full md:w-20rem" />
                                
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block text-medium mb-2">
                                    Airlines to Avoid
                                </label>
                                <MultiSelect value={selectedAvoidAirlines} onChange={(e) => setSelectedAvoidAirlines(e.value)} options={airlines}
                                    placeholder="Select Airlines to Avoid" maxSelectedLabels={3} className="w-full md:w-20rem" /></div>
                            <div>
                                <Button onClick={() => {
                                    sendPreferences()
                                    setActiveTab('Shopping&Dining');     
                                }} label="Save and Continue" className="p-ripple w-auto"></Button>
                            </div>
                        </div>
                    </div>
                </div>)}
                {activeTab == 'Shopping&Dining' && (<div className="sm:w-7 fadein animation-duration-100 surface-card p-5 shadow-2 border-round">
                    <div className="text-900 font-medium text-xl mt-3">Shopping & Dining Preferences</div>
                    <Divider></Divider>
                    <div className="font-light text-lg text-500 mb-3">Share your dining and shopping preferences, and we’ll find the right card to match your taste!</div>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    Favorite Restaurants
                                </label>
                                <MultiSelect value={selectedRestaurants} onChange={(e) => setSelectedRestaurants(e.value)} options={restaurants}
                                    placeholder="Select you favorite restaurants" maxSelectedLabels={3} className="w-full md:w-20rem" />
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block text-medium mb-2">
                                    Favorite Stores
                                </label>
                                <MultiSelect value={selectedShopping} onChange={(e) => setSelectedShopping(e.value)} options={shopping}
                                    placeholder="Select your favorite stores" maxSelectedLabels={3} className="w-full md:w-20rem" /></div>
                            <div>
                                <Button onClick={() => {
                                    sendPreferences()
                                    setActiveTab('Business');
                                }} label="Save and Continue" className="p-ripple w-auto">
                                        <Ripple />
                                </Button>
                            </div>  
                        </div>
                    </div>
                </div>)}
                {activeTab == 'Business' && (<div className="sm:w-7 fadein animation-duration-100 surface-card p-5 shadow-2 border-round">
                    <div className="text-900 font-medium text-xl mt-3">Business Needs</div>
                    <Divider></Divider>
                    <div className="font-light text-lg text-500 mb-3">Tell us your business needs, and we’ll find the card that works as hard as you do!</div>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    How Big is Your Business
                                </label>
                                <Dropdown value={selectedBusinessSize} onChange={(e) => setSelectedBusinessSize(e.value)} options={businessSizes}
                                    placeholder="Select your business size" className="w-full md:w-20rem" />
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block text-medium mb-2">
                                    What Industries Does Your Business Operate In
                                </label>
                                <MultiSelect value={selectedIndustries} onChange={(e) => setSelectedIndustries(e.value)} options={industries}
                                    placeholder="Select all applicable industries" maxSelectedLabels={3} className="w-full md:w-20rem" /></div>
                            <div>
                                <Button onClick={() => sendPreferences()} label="Save and Continue" className="p-ripple w-auto"></Button>
                            </div>  
                        </div>
                    </div>
                </div>)}
            </div>
        </div>
    
    );
};

export default PreferencesCard;