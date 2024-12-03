import React, { useState, useEffect } from 'react';
import { Divider } from 'primereact/divider';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { Slider } from 'primereact/slider';
import CreditCardFaceouts from '../components/CreditCardFaceout';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { getBackendUrl } from '../utils/urlResolver';

const CreditCardDatabase = () => {
    const [selectedIssuer, setSelectedIssuer] = useState(null);
    const [nameFilter, setNameFilter] = useState('');
    const [annualFeeRange, setAnnualFeeRange] = useState([0, 500]);
    const [selectedRewardUnit, setSelectedRewardUnit] = useState(null);
    const [selectedKeyword, setSelectedKeyword] = useState(null);

    // State for dynamically loaded dropdown options
    const [issuers, setIssuers] = useState([]);
    const [rewardUnits, setRewardUnits] = useState([]);
    const [keywords, setKeywords] = useState([]);

    // Fetch enum values from backend API on component mount
    useEffect(() => {
        fetch(`${getBackendUrl()}/api/issuers`)
            .then(response => response.json())
            .then(data => setIssuers(data.map(item => ({ label: item, value: item }))))
            .catch(error => console.error("Error fetching issuers:", error));

        fetch(`${getBackendUrl()}/api/reward_units`)
            .then(response => response.json())
            .then(data => setRewardUnits(data.map(item => ({ label: item, value: item }))))
            .catch(error => console.error("Error fetching reward units:", error));

        fetch(`${getBackendUrl()}/api/keywords`)
            .then(response => response.json())
            .then(data => setKeywords(data.map(item => ({ label: item, value: item }))))
            .catch(error => console.error("Error fetching keywords:", error));
    }, []);

    const onIssuerChange = (e) => {
        setSelectedIssuer(e.value);
    };

    const onNameFilterChange = (e) => {
        setNameFilter(e.target.value);
    };

    const onAnnualFeeChange = (e) => {
        setAnnualFeeRange(e.value);
    };

    const onRewardUnitChange = (e) => {
        setSelectedRewardUnit(e.value);
    };

    const onKeywordChange = (e) => {
        setSelectedKeyword(e.value);
    };

    return (
        <div>
            <Navbar />
            <div className="bg-gray-900 px-4 py-8 md:px-6 lg:px-8">
                <div className="text-900 text-white font-bold text-3xl text-center">Open Source Credit Cards Database</div>
                <p className="text-600 text-white font-normal text-xl text-center">
                    The world's first open-source credit card database. Welcome to the open finance revolution.
                </p>
                <Divider className="w-full" />
                <div className="flex flex-wrap lg:flex-nowrap">
                    {/* Sidebar */}
                    <div className="col-fixed lg:col-2 mr-4 flex p-0 flex-column w-full lg:w-3">
                        <div className="bg-gray-700 p-3 flex flex-column p-0">
                            {/* Issuer Filter */}
                            <div className="p-field mb-4">
                                <h3 className="text-white mb-2">Issuer</h3>
                                <Dropdown
                                    value={selectedIssuer}
                                    options={issuers}
                                    onChange={onIssuerChange}
                                    placeholder="Select Issuer"
                                    className="w-full"
                                    showClear // Enable clear option
                                />
                            </div>

                            {/* Name Filter */}
                            <div className="p-field mb-4">
                                <h3 className="text-white mb-2">Name</h3>
                                <InputText
                                    value={nameFilter}
                                    onChange={onNameFilterChange}
                                    placeholder="Enter Card Name"
                                    className="w-full"
                                />
                            </div>

                            {/* Annual Fee Slider */}
                            <div className="p-field mb-4">
                                <h3 className="text-white mb-2">Annual Fee</h3>
                                <Slider
                                    value={annualFeeRange}
                                    onChange={onAnnualFeeChange}
                                    range
                                    min={0}
                                    max={500}
                                    className="w-full"
                                />
                                <div className="flex justify-content-between mt-2 text-white">
                                    <span>${annualFeeRange[0]}</span>
                                    <span>${annualFeeRange[1]}</span>
                                </div>
                            </div>

                            {/* Primary Reward Unit Filter */}
                            <div className="p-field mb-4">
                                <h3 className="text-white mb-2">Primary Reward Unit</h3>
                                <Dropdown
                                    value={selectedRewardUnit}
                                    options={rewardUnits}
                                    onChange={onRewardUnitChange}
                                    placeholder="Select Reward Unit"
                                    className="w-full"
                                    showClear // Enable clear option
                                />
                            </div>

                            {/* Keywords Filter */}
                            <div className="p-field mb-4">
                                <h3 className="text-white mb-2">Keywords</h3>
                                <Dropdown
                                    value={selectedKeyword}
                                    options={keywords}
                                    onChange={onKeywordChange}
                                    placeholder="Select Keyword"
                                    className="w-full"
                                    showClear // Enable clear option
                                />
                            </div>
                        </div>
                    </div>

                    {/* Main Content */}
                    <div className="flex w-full" style={{ minHeight: '25rem' }}>
                        <CreditCardFaceouts
                            issuer={selectedIssuer}
                            name={nameFilter}
                            annualFeeRange={annualFeeRange}
                            primaryRewardUnit={selectedRewardUnit}
                            keyword={selectedKeyword}
                        />
                    </div>
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default CreditCardDatabase;
