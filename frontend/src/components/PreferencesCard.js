import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Ripple } from 'primereact/ripple';
import { Button } from 'primereact/button';
import { Divider } from 'primereact/divider';
import { MultiSelect } from 'primereact/multiselect';
import { InputTextarea } from 'primereact/inputtextarea';
import { FloatLabel } from 'primereact/floatlabel';
import { fetchWithAuth } from '../pages/AuthPage';
import { Dropdown } from 'primereact/dropdown';
import { getBackendUrl } from '../utils/urlResolver';

const PreferencesCard = ({ onBack, onSuccess }) => {
    const navigate = useNavigate();

    // Debugging: Track state changes
    const debugLog = (message, data = null) => {
        console.log(`[DEBUG] ${message}`, data);
    };

    // Tab state and order
    const [activeTab, setActiveTab] = useState('CreditProfile');
    const tabOrder = ['CreditProfile', 'Banks', 'RewardsPrograms', 'Vendors', 'Business'];

    const handleTabClick = (tab) => {
        debugLog('Switching to tab:', tab);
        setActiveTab(tab);
    };

    const saveCurrentTabPreferences = async () => {
        const payload = {};
        
        switch (activeTab) {
            case 'CreditProfile':
                payload.credit_profile = { 
                    credit_score: creditScore, 
                    salary, 
                    lifestyle: selectedLifestyle 
                };
                break;
            case 'Banks':
                payload.banks_preferences = {
                    have_banks: selectedHaveBanks,
                    preferred_banks: selectedBanks,
                    avoid_banks: selectedAvoidBanks
                };
                break;
            case 'RewardsPrograms':
                payload.rewards_programs_preferences = {
                    preferred_rewards_programs: selectedPointsSystems,
                    avoid_rewards_programs: selectedAvoidPointsSystems
                };
                break;
            case 'Vendors':
                payload.consumer_preferences = {
                    favorite_grocery_stores: selectedGroceries,
                    favorite_general_goods_stores: selectedShopping
                };
                break;
            case 'Business':
                payload.business_preferences = {
                    business_type: selectedIndustries,
                    business_size: selectedBusinessSize
                };
                break;
        }

        try {
            const response = await fetchWithAuth(`${getBackendUrl()}/save_user_preferences`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error('Failed to save preferences');
            }

            // Only navigate to dashboard if saving business preferences
            if (activeTab === 'Business') {
                onSuccess();
                navigate('/dashboard');
            }
        } catch (error) {
            console.error('Error saving preferences:', error);
        }
    };

    // State and preference management
    const [selectedHaveBanks, setSelectedHaveBanks] = useState([]);
    const [selectedBanks, setSelectedBanks] = useState([]);
    const [selectedAvoidBanks, setSelectedAvoidBanks] = useState([]);
    const [banks, setBanks] = useState([]);

    const [selectedPointsSystems, setSelectedPointsSystems] = useState([]);
    const [selectedAvoidPointsSystems, setSelectedAvoidPointsSystems] = useState([]);
    const [pointsSystems, setPointsSystems] = useState([]);

    const [selectedGroceries, setSelectedGroceries] = useState([]);
    const [groceries, setGroceries] = useState([]);

    const [selectedShopping, setSelectedShopping] = useState([]);
    const [shopping, setShopping] = useState([]);

    const [selectedLifestyle, setSelectedLifestyle] = useState(null);
    const [lifestyle, setLifestyle] = useState([]);

    const [creditScore, setCreditScore] = useState('');
    const [salary, setSalary] = useState('');

    const [selectedIndustries, setSelectedIndustries] = useState([]);
    const [industries, setIndustries] = useState([]);

    const [selectedBusinessSize, setSelectedBusinessSize] = useState(null);
    const [businessSizes, setBusinessSizes] = useState([]);

    useEffect(() => {
        const fetchEnumsAndPreferences = async () => {
            try {
                debugLog('Fetching enums and user preferences');
                const [banksData, pointsSystemsData, groceriesData, shoppingData, lifestyleData, industriesData, businessSizesData] = await Promise.all([
                    fetch(`${getBackendUrl()}/api/issuers`).then(res => res.json()),
                    fetch(`${getBackendUrl()}/api/reward_units`).then(res => res.json()),
                    fetch(`${getBackendUrl()}/api/grocery_stores`).then(res => res.json()),
                    fetch(`${getBackendUrl()}/api/general_goods_stores`).then(res => res.json()),
                    fetch(`${getBackendUrl()}/api/lifestyles`).then(res => res.json()),
                    fetch(`${getBackendUrl()}/api/industries`).then(res => res.json()),
                    fetch(`${getBackendUrl()}/api/business_sizes`).then(res => res.json()),
                ]);

                // Populate dropdowns
                setBanks(banksData.map(item => ({ label: item, value: item })));
                setPointsSystems(pointsSystemsData.map(item => ({ label: item, value: item })));
                setGroceries(groceriesData.map(item => ({ label: item, value: item })));
                setShopping(shoppingData.map(item => ({ label: item, value: item })));
                setLifestyle(lifestyleData.map(item => ({ label: item, value: item })));
                setIndustries(industriesData.map(item => ({ label: item, value: item })));
                setBusinessSizes(businessSizesData.map(item => ({ label: item, value: item })));

                // Fetch preferences
                const response = await fetchWithAuth(
                    `${getBackendUrl()}/read_user_preferences`,
                    { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) }
                );
                const data = await response.json();
                debugLog('Fetched user preferences:', data);

                // Apply fetched preferences to state
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
                console.error('Error fetching data:', error);
            }
        };

        fetchEnumsAndPreferences();
    }, []);
        
    const findBanksIntersection = () => {
        const intersection = selectedBanks.filter((x) => selectedAvoidBanks.includes(x));
        if (intersection.length > 0) {
            return intersection;
        }
        return null;
    };

    const findAirlinesIntersection = () => {
        const intersection = selectedPointsSystems.filter((x) =>
            selectedAvoidPointsSystems.includes(x)
        );
        if (intersection.length > 0) {
            return intersection;
        }
        return null;
    };

    // Handle conflicting selections
    useEffect(() => {
        const conflictingBanks = findBanksIntersection();
        if (conflictingBanks && conflictingBanks.length > 0) {
            alert(
                `You have selected the same bank in both preferred and avoid lists: ${conflictingBanks.join(
                    ', '
                )}`
            );
        }
    }, [selectedBanks, selectedAvoidBanks]);

    useEffect(() => {
        const conflictingRewards = findAirlinesIntersection();
        if (conflictingRewards && conflictingRewards.length > 0) {
            alert(
                `You have selected the same rewards program in both preferred and avoid lists: ${conflictingRewards.join(
                    ', '
                )}`
            );
        }
    }, [selectedPointsSystems, selectedAvoidPointsSystems]);

    const renderSaveButton = () => {
        return (
            <Button
                label="Save Preferences In This Tab"
                icon="pi pi-save"
                onClick={saveCurrentTabPreferences}
            />
        );
    };

    // [Previous tab content rendering remains the same, but replace Button groups with:]
    const renderButtonGroup = () => (
        <div className="flex justify-content-end mt-4">
            {renderSaveButton()}
        </div>
    );

    return (
        <div className="px-4 md:px-6 lg:px-8 pb-8 bg-gray-800">
            <div className="grid align-items-start">
                <div className="col-2">
                    <ul className="border-round bg-gray-300 opacity-70 h-auto list-none p-0 text-lg">
                        {tabOrder.map((tab) => (
                            <li key={tab}>
                                <a
                                    onClick={() => handleTabClick(tab)}
                                    className={`p-ripple flex align-items-center cursor-pointer p-3 border-round text-800 hover:surface-hover transition-duration-150 transition-colors ${
                                        activeTab === tab ? 'bg-gray-400' : ''
                                    }`}
                                >
                                    <i
                                        className={`pi ${
                                            tab === 'CreditProfile'
                                                ? 'pi-credit-card'
                                                : tab === 'Banks'
                                                ? 'pi-building-columns'
                                                : tab === 'RewardsPrograms'
                                                ? 'pi-money-bill'
                                                : tab === 'Vendors'
                                                ? 'pi-shop'
                                                : 'pi-briefcase'
                                        } md:mr-2`}
                                    ></i>
                                    <span className="font-medium hidden md:block">
                                        {tab === 'CreditProfile'
                                            ? 'Credit Profile'
                                            : tab === 'Banks'
                                            ? 'Banks'
                                            : tab === 'RewardsPrograms'
                                            ? 'Rewards Programs'
                                            : tab === 'Vendors'
                                            ? 'Vendors'
                                            : 'Business Needs'}
                                    </span>
                                    <Ripple />
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>
                {/* Render the active tab */}
                {activeTab === 'CreditProfile' && (
                    <div className="bg-gray-300 col-8 fadein animation-duration-100 p-5 shadow-2 border-round">
                        <div className="text-900 font-medium text-xl mt-3">Credit Profile</div>
                        <Divider></Divider>
                        <div className="flex-auto block gap-5 flex-column-reverse font-light text-lg text-gray-900 md:flex-row">
                            Our service doesn’t require a credit check, so your credit score won’t be affected.
                            Explore our offerings with confidence, knowing your credit remains untouched.
                            Don’t know your credit score? We recommend checking it through sites like:
                            <div className="flex-auto">
                                <a
                                    className="text-blue-500"
                                    href="https://www.creditkarma.com"
                                    target="_blank"
                                    rel="noreferrer"
                                >
                                    Credit Karma
                                </a>
                                ,&ensp;
                                <a
                                    className="text-blue-500"
                                    href="https://www.experian.com"
                                    target="_blank"
                                    rel="noreferrer"
                                >
                                    Experian
                                </a>
                                ,&ensp;
                                <a
                                    className="text-blue-500"
                                    href="https://www.creditsesame.com"
                                    target="_blank"
                                    rel="noreferrer"
                                >
                                    Credit Sesame
                                </a>
                                .
                            </div>
                        </div>
                        <div className="flex gap-5 flex-column-reverse text-lg text-gray-900 sm:flex-row">
                            <div className="flex-auto p-fluid">
                                <div className="pt-5">
                                    <FloatLabel>
                                        <label
                                            htmlFor="creditScore"
                                            className="block text-lg text-gray-900 text-900 mb-2"
                                        >
                                            Approximate Credit Score
                                        </label>
                                        <InputTextarea
                                            onChange={(e) => setCreditScore(e.target.value)}
                                            value={creditScore}
                                            className="p-2 w-6"
                                            autoResize
                                            id="creditScore"
                                            type="text"
                                            keyfilter="int"
                                            placeholder="300-850"
                                            rows={1}
                                            cols={1}
                                        />
                                    </FloatLabel>
                                </div>
                                <div className="mb-4 pt-5">
                                    <FloatLabel>
                                        <label
                                            htmlFor="salary"
                                            className="block text-lg text-gray-900 text-900 mb-2"
                                        >
                                            Approximate Salary (USD)
                                        </label>
                                        <InputTextarea
                                            onChange={(e) => setSalary(e.target.value)}
                                            value={salary}
                                            className="p-2 w-6"
                                            autoResize
                                            id="salary"
                                            type="text"
                                            keyfilter="int"
                                            placeholder="e.g. 65,000"
                                            rows={1}
                                            cols={1}
                                        />
                                    </FloatLabel>
                                </div>
                                <div className="mb-4 mb-2">
                                    <label className="block text-lg text-gray-900 mb-2">Lifestyle</label>
                                    <Dropdown
                                        className="p-1 w-6"
                                        value={selectedLifestyle}
                                        onChange={(e) => setSelectedLifestyle(e.value)}
                                        options={lifestyle}
                                        optionLabel="label"
                                        placeholder="Select your Lifestyle"
                                    />
                                </div>
                                {renderButtonGroup()}
                            </div>
                        </div>
                    </div>
                )}
                {/* Banks Tab */}
                {activeTab === 'Banks' && (
                    <div className="bg-gray-300 col-8 fadein animation-duration-100 p-5 shadow-2 border-round">
                        <div className="text-900 font-medium text-xl mt-3">Favorite Banks</div>
                        <Divider></Divider>
                        <div className="font-light text-lg text-gray-900 mb-3">
                            Tell us your preferred banks (and ones to avoid) for tailored credit card
                            recommendations!
                        </div>
                        <div className="flex gap-5 flex-column-reverse md:flex-row">
                            <div className="flex-auto p-fluid">
                                <div className="mb-4">
                                    <label className="block text-lg text-gray-900 mb-2">
                                        Banks Inclusion Filter
                                    </label>
                                    <MultiSelect
                                        value={selectedHaveBanks}
                                        onChange={(e) => setSelectedHaveBanks(e.value)}
                                        options={banks}
                                        optionLabel="label"
                                        optionValue="value"
                                        placeholder="Select Your Banks"
                                        maxSelectedLabels={3}
                                        className="w-full md:w-20rem"
                                    />
                                </div>
                                <div className="mb-4">
                                    <label htmlFor="avoidBanks" className="block text-lg text-gray-900 mb-2">
                                        Banks Exclusion Filter
                                    </label>
                                    <MultiSelect
                                        value={selectedAvoidBanks}
                                        onChange={(e) => setSelectedAvoidBanks(e.value)}
                                        options={banks}
                                        optionLabel="label"
                                        optionValue="value"
                                        placeholder="Select Banks to Avoid"
                                        maxSelectedLabels={3}
                                        className="w-full md:w-20rem"
                                    />
                                </div>
                                {renderButtonGroup()}
                            </div>
                        </div>
                    </div>
                )}
                {/* RewardsPrograms Tab */}
                {activeTab === 'RewardsPrograms' && (
                    <div className="bg-gray-300 col-8 fadein animation-duration-100 p-5 shadow-2 border-round">
                        <div className="text-900 font-medium text-xl mt-3">Rewards Programs</div>
                        <Divider></Divider>
                        <div className="font-light text-lg text-gray-900 mb-3">
                            Pick your preferred points systems (and ones to avoid) for tailored credit
                            card recommendations!
                        </div>
                        <div className="flex gap-5 flex-column-reverse md:flex-row">
                            <div className="flex-auto p-fluid">
                                <div className="mb-4">
                                    <label className="block text-base text-gray-900 mb-2">
                                        Preferred Rewards Programs
                                    </label>
                                    <MultiSelect
                                        value={selectedPointsSystems}
                                        onChange={(e) => setSelectedPointsSystems(e.value)}
                                        options={pointsSystems}
                                        optionLabel="label"
                                        optionValue="value"
                                        placeholder="Select Preferred Programs"
                                        maxSelectedLabels={3}
                                        className="w-full md:w-20rem"
                                    />
                                </div>
                                <div className="mb-4">
                                    <label htmlFor="avoidRewards" className="block text-lg text-gray-900 mb-2">
                                        Rewards Programs to Avoid
                                    </label>
                                    <MultiSelect
                                        value={selectedAvoidPointsSystems}
                                        onChange={(e) => setSelectedAvoidPointsSystems(e.value)}
                                        options={pointsSystems}
                                        optionLabel="label"
                                        optionValue="value"
                                        placeholder="Select Programs to Avoid"
                                        maxSelectedLabels={3}
                                        className="w-full md:w-20rem"
                                    />
                                </div>
                                {renderButtonGroup()}
                            </div>
                        </div>
                    </div>
                )}
                {/* Vendors Tab */}
                {activeTab === 'Vendors' && (
                    <div className="bg-gray-300 col-8 fadein animation-duration-100 p-5 shadow-2 border-round">
                        <div className="text-900 font-medium text-xl mt-3">
                            Shopping & Dining Preferences
                        </div>
                        <Divider></Divider>
                        <div className="font-light text-lg text-gray-900 mb-3">
                            Share your dining and shopping preferences, and we’ll find the right card to
                            match your taste!
                        </div>
                        <div className="flex gap-5 flex-column-reverse md:flex-row">
                            <div className="flex-auto p-fluid">
                                <div className="mb-4">
                                    <label className="block text-lg text-gray-900 mb-2">
                                        Favorite Grocery Stores
                                    </label>
                                    <MultiSelect
                                        value={selectedGroceries}
                                        onChange={(e) => setSelectedGroceries(e.value)}
                                        options={groceries}
                                        optionLabel="label"
                                        optionValue="value"
                                        placeholder="Select your favorite grocery stores"
                                        maxSelectedLabels={3}
                                        className="w-full md:w-20rem"
                                    />
                                </div>
                                <div className="mb-4">
                                    <label htmlFor="shopping" className="block text-lg text-gray-900 mb-2">
                                        Favorite General Goods Stores
                                    </label>
                                    <MultiSelect
                                        value={selectedShopping}
                                        onChange={(e) => setSelectedShopping(e.value)}
                                        options={shopping}
                                        optionLabel="label"
                                        optionValue="value"
                                        placeholder="Select your favorite general goods stores"
                                        maxSelectedLabels={3}
                                        className="w-full md:w-20rem"
                                    />
                                </div>
                                {renderButtonGroup()}
                            </div>
                        </div>
                    </div>
                )}
                {/* Business Tab */}
                {activeTab === 'Business' && (
                    <div className="bg-gray-300 col-8 fadein animation-duration-100 p-5 shadow-2 border-round">
                        <div className="text-900 font-medium text-xl mt-3">Business Needs</div>
                        <Divider></Divider>
                        <div className="font-light text-lg text-gray-900 mb-3">
                            Tell us your business needs, and we’ll find the card that works as hard as you
                            do!
                        </div>
                        <div className="flex gap-5 flex-column-reverse md:flex-row">
                            <div className="flex-auto p-fluid">
                                <div className="mb-4">
                                    <label className="block text-lg text-gray-900 mb-2 ">
                                        How Big is Your Business
                                    </label>
                                    <Dropdown
                                        value={selectedBusinessSize}
                                        onChange={(e) => setSelectedBusinessSize(e.value)}
                                        options={businessSizes}
                                        optionLabel="label"
                                        optionValue="value"
                                        placeholder="Select your business size"
                                        className="w-full md:w-20rem"
                                    />
                                </div>
                                <div className="mb-4">
                                    <label htmlFor="industries" className="block text-lg text-gray-900 mb-2">
                                        What Industries Does Your Business Operate In
                                    </label>
                                    <MultiSelect
                                        value={selectedIndustries}
                                        onChange={(e) => setSelectedIndustries(e.value)}
                                        options={industries}
                                        optionLabel="label"
                                        optionValue="value"
                                        placeholder="Select all applicable industries"
                                        maxSelectedLabels={3}
                                        className="w-full md:w-20rem"
                                    />
                                </div>
                                {renderButtonGroup()}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PreferencesCard;
