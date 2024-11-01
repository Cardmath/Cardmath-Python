import React, { useState } from 'react';
import { Divider } from 'primereact/divider';
import { InputText } from 'primereact/inputtext';
import { Accordion, AccordionTab } from 'primereact/accordion';
import { Dropdown } from 'primereact/dropdown';
import { Slider } from 'primereact/slider';
import CreditCardFaceouts from '../components/CreditCardFaceout';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const CreditCardDatabase = () => {
    const [selectedIssuer, setSelectedIssuer] = useState(null);
    const [nameFilter, setNameFilter] = useState('');
    const [annualFeeRange, setAnnualFeeRange] = useState([0, 500]);
    const issuers = [
        { label: 'Capital One', value: "Capital One" },
        { label: 'Chase', value: "Chase" },
        { label: 'American Express', value: 'American Express' },
        { label: 'Citi', value: 'Citi' },
        { label: 'Discover', value: 'Discover' },
        { label: 'Bank of America', value: 'Bank of America' },
        { label: 'Wells Fargo', value: 'Wells Fargo' },
        { label: 'Barclays', value: 'Barclays' },
        { label: 'US Bank', value: 'US Bank' },
        { label: 'PNC', value: 'PNC' },
        { label: 'TD Bank', value: 'TD Bank' },
        { label: 'HSBC', value: 'HSBC' }
    ];

    const onIssuerChange = (e) => {
        setSelectedIssuer(e.value);
    };

    const onNameFilterChange = (e) => {
        setNameFilter(e.target.value);
    };

    const onAnnualFeeChange = (e) => {
        setAnnualFeeRange(e.value);
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
                        </div>
                    </div>

                    {/* Main Content */}
                    <div className="flex w-full" style={{ minHeight: '25rem' }}>
                        <CreditCardFaceouts
                            issuer={selectedIssuer}
                            name={nameFilter}
                            annualFeeRange={annualFeeRange}
                        />
                    </div>
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default CreditCardDatabase;
