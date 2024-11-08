import React, { useState , useEffect } from 'react';
import { Ripple } from 'primereact/ripple';
import { Button } from 'primereact/button';
import { Divider } from 'primereact/divider';
import { MultiSelect } from 'primereact/multiselect';
import { InputTextarea } from 'primereact/inputtextarea';
import { FloatLabel } from 'primereact/floatlabel';
import { fetchWithAuth } from '../pages/AuthPage';
import { Dropdown } from 'primereact/dropdown';

const PreferencesCard = ( {setAlert} ) => {

    useEffect(() => {
        const fetchUserPreferences = async () => {
            try {
                const response = await fetchWithAuth('https://backend-dot-cardmath-llc.uc.r.appspot.com/read_user_preferences', {
                    method: 'POST',  
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({}),
                });
                const data = await response.json();

                // Update state variables with fetched data
                if (data.banks_preferences) {
                    setSelectedHaveBanks(data.banks_preferences.have_banks || []);
                    setSelectedBanks(data.banks_preferences.preferred_banks || []);
                    setSelectedAvoidBanks(data.banks_preferences.avoid_banks || []);
                }
                if (data.rewards_programs_preferences) {
                    setSelectedPointsSystems(data.rewards_programs_preferences.preferred_rewards_programs || []);
                    setSelectedAvoidPointsSystems(data.rewards_programs_preferences.avoid_rewards_programs || []);
                }
                if (data.consumer_preferences) {
                    setSelectedGroceries(data.consumer_preferences.favorite_grocery_stores || []);
                    setSelectedShopping(data.consumer_preferences.favorite_general_goods_stores || []);
                }
                if (data.credit_profile) {
                    setCreditScore(data.credit_profile.credit_score || '');
                    setSalary(data.credit_profile.salary || '');
                    setSelectedLifestyle(data.credit_profile.lifestyle || null);
                }
                if (data.business_preferences) {
                    setSelectedIndustries(data.business_preferences.business_type || []);
                    setSelectedBusinessSize(data.business_preferences.business_size || null);
                }
            } catch (error) {
                console.error('Error fetching user preferences:', error);
            }
        };

        fetchUserPreferences();
    }, []);

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

    const [selectedPointsSystems, setSelectedPointsSystems] = useState(null);
    const [selectedAvoidPointsSystems, setSelectedAvoidPointsSystems] = useState(null);
    const pointsSystems = [
        'Chase Ultimate Rewards',
        'American Express Membership Rewards',
        'Citi ThankYou Points',
        'Capital One Miles',
        'Wells Fargo Go Far Rewards',
        'Bank of America Preferred Rewards',
        'Barclays Arrival Points',
        'Discover Cashback Bonus',
        'U.S. Bank Altitude Points',
        'PNC Points',
        'Hilton Honors Points',
        'Marriott Bonvoy Points',
        'World of Hyatt Points',
        'Delta SkyMiles',
        'United MileagePlus',
        'American Airlines AAdvantage Miles',
        'Southwest Rapid Rewards',
        'IHG One Rewards Points',
        'JetBlue TrueBlue Points',
        'Alaska Mileage Plan Miles',
        'Radisson Rewards Points',
        'Percent Cashback USD',
        'Statement Credit USD',
        'Avios',
        'Aeroplan Points',
        'Choice Privileges Points',
        'Unknown',
    ];
    const findAirlinesIntersection = () => {
        const intersection = selectedPointsSystems?.filter(x => selectedAvoidPointsSystems?.includes(x)) || [];
        if (intersection.length > 0) {
            return intersection;
        }
        return null;
    }


    const [selectedGroceries, setSelectedGroceries] = useState(null);
    const groceries = [
        'Walgreens',
        'Walmart',
        'Kroger',
        'Lowes',
        'Aldi',
        'Costco'
    ];

    const [selectedShopping, setSelectedShopping] = useState(null);
    const shopping = [
        'Amazon',
        'Target',
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
            credit_score: creditScore !== '' ? creditScore : null,
            salary: salary !== '' ? salary : null,
            lifestyle: selectedLifestyle !== null ? selectedLifestyle : null
        };
    
        const banks_preferences_out = {
            have_banks: selectedHaveBanks !== null ? [...selectedHaveBanks] : null,
            preferred_banks: selectedBanks !== null ? [...selectedBanks] : null,
            avoid_banks: selectedAvoidBanks !== null ? [...selectedAvoidBanks] : null
        };
    
        const rewards_programs_preferences_out = {
            preferred_rewards_programs: selectedPointsSystems !== null ? [...selectedPointsSystems] : null,
            avoid_rewards_programs: selectedAvoidPointsSystems !== null ? [...selectedAvoidPointsSystems] : null
        };
    
        const consumer_preferences_out = {
            favorite_grocery_stores: selectedGroceries !== null ? [...selectedGroceries] : null,
            favorite_general_goods_stores: selectedShopping !== null ? [...selectedShopping] : null,
        };
    
        const business_preferences_out = {
            business_type: selectedIndustries !== null ? [...selectedIndustries] : null,
            business_size: selectedBusinessSize !== null ? selectedBusinessSize : null
        };
    
        fetchWithAuth('https://backend-dot-cardmath-llc.uc.r.appspot.com', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                credit_profile: checkProperties(credit_profile_out) ? null : credit_profile_out, 
                banks_preferences: checkProperties(banks_preferences_out) ? null : banks_preferences_out,
                rewards_programs_preferences: checkProperties(rewards_programs_preferences_out) ? null : rewards_programs_preferences_out,
                consumer_preferences: checkProperties(consumer_preferences_out) ? null : consumer_preferences_out,
                business_preferences: checkProperties(business_preferences_out) ? null : business_preferences_out
            })
        }).then(() => {
            console.log("Preferences submitted!");
        }).then(() => {
            setAlert({
                visible: false,
                message: '',
                heading: '',
                type: 'error'
            });
        });
    };

    return (        
        <div className="px-4 md:px-6 lg:px-8 pb-8">
            <div className="grid align-items-start">
                <div className="col-2">
                    <ul className="border-round bg-gray-300 opacity-70 h-auto list-none p-0 text-lg">
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
                            <a onClick={() => handleTabClick('RewardsPrograms')} className="p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors">
                                <i className="pi pi-money-bill md:mr-2"></i>
                                <span className="font-medium hidden md:block">Rewards Programs</span>
                                <Ripple />
                            </a>
                        </li>
                        <li>
                            <a onClick={() => handleTabClick('Vendors')} className="p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors">
                                <i className="pi pi-shop md:mr-2"></i>
                                <span className="font-medium hidden md:block">Vendors</span>
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
                </div>
                {activeTab == 'CreditProfile' && (<div className="bg-gray-300 col-8 fadein animation-duration-100 flex sm:flex-column p-5 shadow-2 border-round">
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
                {activeTab == 'Banks' && (<div className="bg-gray-300 sm:w-7 fadein animation-duration-100 p-5 shadow-2 border-round">
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
                {activeTab == 'RewardsPrograms' && (<div className="bg-gray-300 sm:w-7 fadein animation-duration-100 p-5 shadow-2 border-round">
                    <div className="text-900 font-medium text-xl mt-3">Rewards Programs</div>
                    <Divider></Divider>
                    <div className="font-light text-lg text-500 mb-3">Pick your preferred points systems (and ones to avoid) for tailored credit card recommendations!</div>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    Preferred Rewards Programs
                                </label>
                                
                                <MultiSelect value={selectedPointsSystems} onChange={(e) => setSelectedPointsSystems(e.value)} options={pointsSystems}
                                    placeholder="Select Preferred Airlines" maxSelectedLabels={3} className="w-full md:w-20rem" />
                                
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block text-medium mb-2">
                                    Rewards Programs to Avoid
                                </label>
                                <MultiSelect value={selectedAvoidPointsSystems} onChange={(e) => setSelectedAvoidPointsSystems(e.value)} options={pointsSystems}
                                    placeholder="Select Airlines to Avoid" maxSelectedLabels={3} className="w-full md:w-20rem" /></div>
                            <div>
                                <Button onClick={() => {
                                    sendPreferences()
                                    setActiveTab('Vendors');     
                                }} label="Save and Continue" className="p-ripple w-auto"></Button>
                            </div>
                        </div>
                    </div>
                </div>)}
                {activeTab == 'Vendors' && (<div className="bg-gray-300 sm:w-7 fadein animation-duration-100 p-5 shadow-2 border-round">
                    <div className="text-900 font-medium text-xl mt-3">Shopping & Dining Preferences</div>
                    <Divider></Divider>
                    <div className="font-light text-lg text-500 mb-3">Share your dining and shopping preferences, and we’ll find the right card to match your taste!</div>
                    <div className="flex gap-5 flex-column-reverse md:flex-row">
                        <div className="flex-auto p-fluid">
                            <div className="mb-4">
                                <label className="block text-medium mb-2">
                                    Favorite Grocery Stores
                                </label>
                                <MultiSelect value={selectedGroceries} onChange={(e) => setSelectedGroceries(e.value)} options={groceries}
                                    placeholder="Select you favorite grocery stores" maxSelectedLabels={3} className="w-full md:w-20rem" />
                            </div>
                            <div className="mb-4">
                                <label htmlFor="bio" className="block text-medium mb-2">
                                    Favorite General Goods Stores
                                </label>
                                <MultiSelect value={selectedShopping} onChange={(e) => setSelectedShopping(e.value)} options={shopping}
                                    placeholder="Select your favorite general goods stores" maxSelectedLabels={3} className="w-full md:w-20rem" /></div>
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
                {activeTab == 'Business' && (<div className="bg-gray-300 sm:w-7 fadein animation-duration-100 p-5 shadow-2 border-round">
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