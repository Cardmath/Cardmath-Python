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

const PreferencesCard = ({ onBack, onSuccess }) => {
    const navigate = useNavigate(); // Initialize useNavigate
    useEffect(() => {
        const fetchEnumsAndPreferences = async () => {
            try {
                // Fetch Enums
                const [banksData, pointsSystemsData, groceriesData, shoppingData, lifestyleData, industriesData, businessSizesData] = await Promise.all([
                    fetch('https://backend-dot-cardmath-llc.uc.r.appspot.com/api/issuers').then(res => res.json()),
                    fetch('https://backend-dot-cardmath-llc.uc.r.appspot.com/api/reward_units').then(res => res.json()),
                    fetch('https://backend-dot-cardmath-llc.uc.r.appspot.com/api/grocery_stores').then(res => res.json()),
                    fetch('https://backend-dot-cardmath-llc.uc.r.appspot.com/api/general_goods_stores').then(res => res.json()),
                    fetch('https://backend-dot-cardmath-llc.uc.r.appspot.com/api/lifestyles').then(res => res.json()),
                    fetch('https://backend-dot-cardmath-llc.uc.r.appspot.com/api/industries').then(res => res.json()),
                    fetch('https://backend-dot-cardmath-llc.uc.r.appspot.com/api/business_sizes').then(res => res.json()),
                ]);

                // Set Enums
                setBanks(banksData.map(item => ({ label: item, value: item })));
                setPointsSystems(pointsSystemsData.map(item => ({ label: item, value: item })));
                setGroceries(groceriesData.map(item => ({ label: item, value: item })));
                setShopping(shoppingData.map(item => ({ label: item, value: item })));
                setLifestyle(lifestyleData.map(item => ({ label: item, value: item })));
                setIndustries(industriesData.map(item => ({ label: item, value: item })));
                setBusinessSizes(businessSizesData.map(item => ({ label: item, value: item })));

                // Fetch User Preferences
                const response = await fetchWithAuth(
                    'https://backend-dot-cardmath-llc.uc.r.appspot.com/read_user_preferences',
                    {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({}),
                    }
                );
                const data = await response.json();

                // Update state variables with fetched data
                if (data.banks_preferences) {
                    setSelectedHaveBanks(data.banks_preferences.have_banks || []);
                    setSelectedBanks(data.banks_preferences.preferred_banks || []);
                    setSelectedAvoidBanks(data.banks_preferences.avoid_banks || []);
                }
                if (data.rewards_programs_preferences) {
                    setSelectedPointsSystems(
                        data.rewards_programs_preferences.preferred_rewards_programs || []
                    );
                    setSelectedAvoidPointsSystems(
                        data.rewards_programs_preferences.avoid_rewards_programs || []
                    );
                }
                if (data.consumer_preferences) {
                    setSelectedGroceries(data.consumer_preferences.favorite_grocery_stores || []);
                    setSelectedShopping(
                        data.consumer_preferences.favorite_general_goods_stores || []
                    );
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
                console.error('Error fetching enums or user preferences:', error);
            }
        };

        fetchEnumsAndPreferences();
    }, []);

    function checkProperties(obj) {
        for (var key in obj) {
            if (obj[key] !== null && obj[key] !== '') return false;
        }
        return true;
    }

    const [activeTab, setActiveTab] = useState('CreditProfile');

    const tabOrder = ['CreditProfile', 'Banks', 'RewardsPrograms', 'Vendors', 'Business'];

    const handleTabClick = (tab) => {
        setActiveTab(tab);
    };

    const moveToNextTab = () => {
        const currentIndex = tabOrder.indexOf(activeTab);
        if (currentIndex < tabOrder.length - 1) {
            sendPreferences();
            setActiveTab(tabOrder[currentIndex + 1]);
        }
    };

    const moveToPreviousTab = () => {
        const currentIndex = tabOrder.indexOf(activeTab);
        if (currentIndex > 0) {
            sendPreferences();
            setActiveTab(tabOrder[currentIndex - 1]);
        } else {
            // If on the first tab, call onBack to go to the previous step
            onBack();
        }
    };

    // State variables for preferences
    const [selectedHaveBanks, setSelectedHaveBanks] = useState([]);
    const [selectedBanks, setSelectedBanks] = useState([]);
    const [selectedAvoidBanks, setSelectedAvoidBanks] = useState([]);
    const [banks, setBanks] = useState([]);

    const findBanksIntersection = () => {
        const intersection = selectedBanks.filter((x) => selectedAvoidBanks.includes(x));
        if (intersection.length > 0) {
            return intersection;
        }
        return null;
    };

    const [selectedPointsSystems, setSelectedPointsSystems] = useState([]);
    const [selectedAvoidPointsSystems, setSelectedAvoidPointsSystems] = useState([]);
    const [pointsSystems, setPointsSystems] = useState([]);

    const findAirlinesIntersection = () => {
        const intersection = selectedPointsSystems.filter((x) =>
            selectedAvoidPointsSystems.includes(x)
        );
        if (intersection.length > 0) {
            return intersection;
        }
        return null;
    };

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

    const sendPreferences = () => {
        const credit_profile_out = {
            credit_score: creditScore !== '' ? creditScore : null,
            salary: salary !== '' ? salary : null,
            lifestyle: selectedLifestyle !== null ? selectedLifestyle : null,
        };

        const banks_preferences_out = {
            have_banks: selectedHaveBanks.length > 0 ? selectedHaveBanks : null,
            preferred_banks: selectedBanks.length > 0 ? selectedBanks : null,
            avoid_banks: selectedAvoidBanks.length > 0 ? selectedAvoidBanks : null,
        };

        const rewards_programs_preferences_out = {
            preferred_rewards_programs:
                selectedPointsSystems.length > 0 ? selectedPointsSystems : null,
            avoid_rewards_programs:
                selectedAvoidPointsSystems.length > 0 ? selectedAvoidPointsSystems : null,
        };

        const consumer_preferences_out = {
            favorite_grocery_stores: selectedGroceries.length > 0 ? selectedGroceries : null,
            favorite_general_goods_stores:
                selectedShopping.length > 0 ? selectedShopping : null,
        };

        const business_preferences_out = {
            business_type: selectedIndustries.length > 0 ? selectedIndustries : null,
            business_size: selectedBusinessSize !== null ? selectedBusinessSize : null,
        };

        fetchWithAuth('https://backend-dot-cardmath-llc.uc.r.appspot.com/save_user_preferences', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                credit_profile: checkProperties(credit_profile_out) ? null : credit_profile_out,
                banks_preferences: checkProperties(banks_preferences_out)
                    ? null
                    : banks_preferences_out,
                rewards_programs_preferences: checkProperties(rewards_programs_preferences_out)
                    ? null
                    : rewards_programs_preferences_out,
                consumer_preferences: checkProperties(consumer_preferences_out)
                    ? null
                    : consumer_preferences_out,
                business_preferences: checkProperties(business_preferences_out)
                    ? null
                    : business_preferences_out,
            }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Failed to save preferences.');
                }
                console.log('Preferences submitted!');
                // Move to next tab or complete registration
                if (activeTab === 'Business') {
                    onSuccess(); // Complete registration
                } else {
                    moveToNextTab();
                }
            })
            .catch((error) => {
                console.error('Error saving preferences:', error);
                // Handle error (e.g., display a message to the user)
            });
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

    return (
        <div className="px-4 md:px-6 lg:px-8 pb-8">
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
                                <div className="flex justify-content-between mt-4">
                                    <Button
                                        label="Back"
                                        icon="pi pi-arrow-left"
                                        className="p-button-secondary"
                                        onClick={moveToPreviousTab}
                                    />
                                    <Button
                                        label="Save and Continue"
                                        icon="pi pi-arrow-right"
                                        iconPos="right"
                                        onClick={moveToNextTab}
                                    />
                                </div>
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
                                        Banks you have Accounts with
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
                                    <label className="block text-lg text-gray-900 mb-2">Preferred Banks</label>
                                    <MultiSelect
                                        value={selectedBanks}
                                        onChange={(e) => setSelectedBanks(e.value)}
                                        options={banks}
                                        optionLabel="label"
                                        optionValue="value"
                                        placeholder="Select Preferred Banks"
                                        maxSelectedLabels={3}
                                        className="w-full md:w-20rem"
                                    />
                                </div>
                                <div className="mb-4">
                                    <label htmlFor="avoidBanks" className="block text-lg text-gray-900 mb-2">
                                        Banks to Avoid
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
                                <div className="flex justify-content-between mt-4">
                                    <Button
                                        label="Back"
                                        icon="pi pi-arrow-left"
                                        className="p-button-secondary"
                                        onClick={moveToPreviousTab}
                                    />
                                    <Button
                                        label="Save and Continue"
                                        icon="pi pi-arrow-right"
                                        iconPos="right"
                                        onClick={moveToNextTab}
                                    />
                                </div>
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
                                <div className="flex justify-content-between mt-4">
                                    <Button
                                        label="Back"
                                        icon="pi pi-arrow-left"
                                        className="p-button-secondary"
                                        onClick={moveToPreviousTab}
                                    />
                                    <Button
                                        label="Save and Continue"
                                        icon="pi pi-arrow-right"
                                        iconPos="right"
                                        onClick={moveToNextTab}
                                    />
                                </div>
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
                                <div className="flex justify-content-between mt-4">
                                    <Button
                                        label="Back"
                                        icon="pi pi-arrow-left"
                                        className="p-button-secondary"
                                        onClick={moveToPreviousTab}
                                    />
                                    <Button
                                        label="Save and Continue"
                                        icon="pi pi-arrow-right"
                                        iconPos="right"
                                        onClick={moveToNextTab}
                                    />
                                </div>
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
                                <div className="flex justify-content-between mt-4">
                                    <Button
                                        label="Back"
                                        icon="pi pi-arrow-left"
                                        className="p-button-secondary"
                                        onClick={moveToPreviousTab}
                                    />
                                    <Button
                                        label="Save and Complete Registration"
                                        icon="pi pi-check"
                                        iconPos="right"
                                        onClick={() => {
                                            sendPreferences();
                                            navigate('/dashboard');
                                        }}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PreferencesCard;
