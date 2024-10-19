import React, { useState } from 'react';
import { Divider } from 'primereact/divider';
import { InputText } from 'primereact/inputtext';
import { Accordion, AccordionTab } from 'primereact/accordion';
import { Ripple } from 'primereact/ripple';
import { Checkbox } from 'primereact/checkbox';
import { Badge } from 'primereact/badge';
import { Slider } from 'primereact/slider';
import { InputNumber } from 'primereact/inputnumber';
import { Galleria } from 'primereact/galleria';
import classNames from 'classnames';
import CreditCardFaceouts from '../components/CreditCardFaceout';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';


const CreditCardDatabase = () => {
    const [selectedBrand_1, setSelectedBrand_1] = useState([]);
    const [rangeValues, setRangeValues] = useState([10, 10000]);
    const [selectedColors, setSelectedColors] = useState([]);
    const [selectedSizes1, setSelectedSizes1] = useState([]);

    const sizes = [
        { value: 'S' }, 
        { value: 'M' }, 
        { value: 'L' }, 
        { value: 'XL' }, 
        { value: 'XXL' }
    ];

    const responsiveOptions = [
        {
            breakpoint: '1024px',
            numVisible: 3
        },
        {
            breakpoint: '768px',
            numVisible: 2
        },
        {
            breakpoint: '560px',
            numVisible: 1
        }
    ];

    const onBrandChange = (e) => {
        let selectedBrands = [...selectedBrand_1];
        if (e.checked) {
            selectedBrands.push(e.value);
        } else {
            selectedBrands = selectedBrands.filter(brand => brand !== e.value);
        }
        setSelectedBrand_1(selectedBrands);
    };

    const onColorClick = (color) => {
        const colors = [...selectedColors];
        if (colors.indexOf(color) === -1) {
            colors.push(color);
        } else {
            colors.splice(colors.indexOf(color), 1);
        }
        setSelectedColors(colors);
    };

    const onSizeClick = (size) => {
        const sizes = [...selectedSizes1];
        if (sizes.indexOf(size.value) === -1) {
            sizes.push(size.value);
        } else {
            sizes.splice(sizes.indexOf(size.value), 1);
        }
        setSelectedSizes1(sizes);
    };

    return (
        <div> 
            <Navbar />
            <div className="bg-gray-900 px-4 py-8 md:px-6 lg:px-8">
                
                <div className="text-900 text-white font-bold text-3xl text-center">Open Source Credit Cards Database</div>
                <p className="text-600 text-white font-normal text-xl text-center">The world's first open-source credit card database. Welcome to the open finance revolution.</p>
                <Divider className="w-full" />
                <div className="flex flex-wrap lg:flex-nowrap">
                    <div className="col-fixed lg:col-2 mr-4 flex p-0 flex-column w-full lg:w-3">
                        <div className="bg-gray-700 p-3 flex flex-column p-0">
                            <a tabIndex="0" className="cursor-pointer text-900 font-medium mb-3 hover:text-white transition-duration-150">All Credit Cards</a>
                            <a tabIndex="0" className="cursor-pointer text-900 font-medium mb-3 hover:text-white transition-duration-150">Dining, Food, Grocery</a>
                            <a tabIndex="0" className="cursor-pointer text-900 font-medium mb-3 hover:text-white transition-duration-150">Travel</a>
                            <a tabIndex="0" className="cursor-pointer text-900 font-medium mb-3 hover:text-white transition-duration-150">Small Business</a>
                            <a tabIndex="0" className="cursor-pointer text-900 font-medium mb-3 hover:text-white transition-duration-150">Vendor-specific</a>
                            <a tabIndex="0" className="cursor-pointer text-900 font-medium mb-3 hover:text-white transition-duration-150">Students</a>
                        </div>
                        <Divider className="w-full m-0 p-0" />

                        <Accordion multiple className="mb-1 mt-3">
                            <AccordionTab selected header={`Issuer (${selectedBrand_1.length})`}>
                                <div className="transition-all transition-duration-400 transition-ease-in-out">
                                    <div className="mb-3">
                                        <span className="p-input-icon-right w-full">
                                            <i className="pi pi-search"></i>
                                            <InputText placeholder="Search" className="w-full" />
                                        </span>
                                    </div>
                                    <div className="flex w-full justify-content-between">
                                        <div className="field-checkbox">
                                            <Checkbox value="Alfred" inputId="alfred" onChange={onBrandChange} checked={selectedBrand_1.indexOf('Alfred') !== -1}></Checkbox>
                                            <label htmlFor="alfred" className="text-900">Alfred</label>
                                        </div>
                                        <Badge value={42} className="mr-2 bg-gray-200 text-gray-900 p-0 border-circle" />
                                    </div>
                                    <div className="flex w-full justify-content-between">
                                        <div className="field-checkbox">
                                            <Checkbox value="Hyper" inputId="hyper" onChange={onBrandChange} checked={selectedBrand_1.indexOf('Hyper') !== -1}></Checkbox>
                                            <label htmlFor="hyper" className="text-900">Hyper</label>
                                        </div>
                                        <Badge value={18} className="mr-2 bg-gray-200 text-gray-900 p-0 border-circle" />
                                    </div>
                                    <div className="flex w-full justify-content-between">
                                        <div className="field-checkbox">
                                            <Checkbox value="Bastion" inputId="bastion" onChange={onBrandChange} checked={selectedBrand_1.indexOf('Bastion') !== -1}></Checkbox>
                                            <label htmlFor="bastion" className="text-900">Bastion</label>
                                        </div>
                                        <Badge value={7} className="mr-2 bg-gray-200 text-gray-900 p-0 border-circle" />
                                    </div>
                                    <div className="flex w-full justify-content-between">
                                        <div className="field-checkbox">
                                            <Checkbox value="Peak" inputId="peak" onChange={onBrandChange} checked={selectedBrand_1.indexOf('Peak') !== -1}></Checkbox>
                                            <label htmlFor="peak" className="text-900">Peak</label>
                                        </div>
                                        <Badge value={36} className="mr-2 bg-gray-200 text-gray-900 p-0 border-circle" />
                                    </div>
                                    <a tabIndex="0" className="block cursor-pointer my-3 text-primary font-medium">Show all...</a>
                                </div>
                            </AccordionTab>
                            <AccordionTab selected header="Credit Score">
                                <div className="transition-all transition-duration-400 transition-ease-in-out">
                                    <Slider value={rangeValues} onChange={(e) => setRangeValues(e.value)} range className="mt-3 mx-auto" style={{ 'maxWidth': '93%' }} />
                                    <div className="flex my-4">
                                        <InputNumber placeholder="$10" value={rangeValues[0]} min={10} onChange={(e) => setRangeValues([e.value, rangeValues[1]])} inputClassName="w-full mr-3" />
                                        <InputNumber placeholder="$10000" value={rangeValues[1]} max={10000} onChange={(e) => setRangeValues([rangeValues[0], e.value])} inputClassName="w-full" />
                                    </div>
                                </div>
                            </AccordionTab>
                            <AccordionTab selected header={`Benefits (${selectedColors.length})`}>
                                <div className="transition-all transition-duration-400 transition-ease-in-out">
                                    <div className="grid mb-3">
                                        <div className="col-4 flex flex-column align-items-center">
                                            <div className="w-3rem h-3rem border-circle bg-gray-900 cursor-pointer border-none flex justify-content-center align-items-center" onClick={() => onColorClick('Black')}>
                                                {selectedColors.indexOf('Black') !== -1 && <i className="pi pi-check text-2xl text-white"></i>}
                                            </div>
                                            <p className="text-900 text-sm text-center mt-1">Black</p>
                                        </div>
                                        <div className="col-4 flex flex-column align-items-center">
                                            <div className="w-3rem h-3rem border-circle bg-orange-500 cursor-pointer border-none flex justify-content-center align-items-center" onClick={() => onColorClick('Orange')}>
                                                {selectedColors.indexOf('Orange') !== -1 && <i className="pi pi-check text-2xl text-white"></i>}
                                            </div>
                                            <p className="text-900 text-sm text-center mt-1">Orange</p>
                                        </div>
                                        <div className="col-4 flex flex-column align-items-center">
                                            <div className="w-3rem h-3rem border-circle bg-indigo-500 cursor-pointer border-none flex justify-content-center align-items-center" onClick={() => onColorClick('Indigo')}>
                                                {selectedColors.indexOf('Indigo') !== -1 && <i className="pi pi-check text-2xl text-white"></i>}
                                            </div>
                                            <p className="text-900 text-sm text-center mt-1">Indigo</p>
                                        </div>
                                        <div className="col-4 flex flex-column align-items-center">
                                            <div className="w-3rem h-3rem border-circle bg-gray-500 cursor-pointer border-none flex justify-content-center align-items-center" onClick={() => onColorClick('Gray')}>
                                                {selectedColors.indexOf('Gray') !== -1 && <i className="pi pi-check text-2xl text-white"></i>}
                                            </div>
                                            <p className="text-900 text-sm text-center mt-1">Gray</p>
                                        </div>
                                        <div className="col-4 flex flex-column align-items-center">
                                            <div className="w-3rem h-3rem border-circle bg-cyan-500 cursor-pointer border-none flex justify-content-center align-items-center" onClick={() => onColorClick('Cyan')}>
                                                {selectedColors.indexOf('Cyan') !== -1 && <i className="pi pi-check text-2xl text-white"></i>}
                                            </div>
                                            <p className="text-900 text-sm text-center mt-1">Cyan</p>
                                        </div>
                                        <div className="col-4 flex flex-column align-items-center">
                                            <div className="w-3rem h-3rem border-circle bg-pink-500 cursor-pointer border-none flex justify-content-center align-items-center" onClick={() => onColorClick('Pink')}>
                                                {selectedColors.indexOf('Pink') !== -1 && <i className="pi pi-check text-2xl text-white"></i>}
                                            </div>
                                            <p className="text-900 text-sm text-center mt-1">Pink</p>
                                        </div>
                                    </div>
                                </div>
                            </AccordionTab>
                        </Accordion>
                    </div>
                    <div className="flex w-full" style={{ minHeight: '25rem' }}>
                        <CreditCardFaceouts />
                    </div>
                </div>
            </div>
        <Footer/>
        </div>
    );
};

export default CreditCardDatabase;
