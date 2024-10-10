import React, { useEffect, useState } from 'react';
import { Ripple } from 'primereact/ripple';
import { InputText } from 'primereact/inputtext';
import { fetchWithAuth } from './AuthPage';
import HeavyHitterPieChart from '../components/HeavyHitterPieChart';
import ChartSlider from "../components/LineChart/LineChartWrapper";
import { StyleClass } from 'primereact/styleclass';


const DashboardPage = () => {

    let res = [
        { x: "2013-04-28", y: 135.98 },
        { x: "2013-04-29", y: 147.49 },
        { x: "2013-04-30", y: 146.93 },
        { x: "2013-05-01", y: 139.89 },
        { x: "2013-05-02", y: 125.6 },
        { x: "2013-05-03", y: 108.13 },
        { x: "2013-05-04", y: 115 },
        { x: "2013-05-05", y: 118.8 },
        { x: "2013-05-06", y: 124.66 },
        { x: "2013-05-07", y: 113.44 },
        { x: "2013-05-08", y: 115.78 },
        { x: "2013-05-11", y: 118.68 },
        { x: "2013-05-12", y: 117.45 },
        { x: "2013-05-13", y: 118.7 },
        { x: "2013-05-14", y: 119.8 },
        { x: "2013-05-15", y: 115.81 },
        { x: "2013-05-16", y: 118.76 },
        { x: "2013-05-17", y: 125.3 },
        { x: "2013-05-18", y: 125.25 },
        { x: "2013-05-19", y: 124.5 },
        { x: "2014-05-09", y: 113.46 },
        { x: "2014-05-10", y: 122 },
        { x: "2014-05-11", y: 118.68 },
        { x: "2014-05-12", y: 117.45 },
        { x: "2014-05-13", y: 118.7 },
        { x: "2014-05-14", y: 119.8 },
        { x: "2014-05-15", y: 115.81 },
        { x: "2014-05-16", y: 118.76 },
        { x: "2014-05-17", y: 125.3 }
    ];

    const [heavyHittersCategories, setHeavyHittersCategories] = useState([]);

    useEffect(() => {
        fetchWithAuth('http://localhost:8000/read_heavy_hitters', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                account_ids: "all"
            })
        }).then(response => response.json())
        .then(data => setHeavyHittersCategories(data.categories))
        .catch(error => console.log(error));

    }, []);

    const btnRef10 = React.createRef();
    const btnRef11 = React.createRef();
    const btnRef12 = React.createRef();
    const btnRef13 = React.createRef();
    const Badge = React.forwardRef((props, ref) => {
        const { className, ...otherProps } = props;
        return <div ref={ref} className={className} {...otherProps} />;
    });      

    return <div className="min-h-screen flex relative lg:static surface-ground">
        <div id="app-sidebar-9" className="h-full lg:h-auto surface-section hidden lg:block flex-shrink-0 absolute lg:static left-0 top-0 z-1 border-right-1 surface-border w-18rem lg:w-7rem select-none">
            <div className="flex flex-column h-full">
                <div className="flex align-items-center justify-content-center flex-shrink-0" style={{ height: '60px' }}>
                    <img src="/demo/images/blocks/logos/hyper-cyan.svg" alt="Image" height="30" />
                </div>
                <div className="mt-3">
                    <ul className="list-none p-0 m-0">
                        <li>
                            <a className="p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center text-cyan-600 border-left-2 border-cyan-600 hover:border-300 transition-duration-150 transition-colors">
                                <i className="pi pi-home mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                <span className="font-medium inline text-base lg:text-xs lg:block">Home</span>
                                <Ripple />
                            </a>
                        </li>
                        <li>
                            <a className="p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center text-600 border-left-2 border-transparent hover:border-300 transition-duration-150 transition-colors">
                                <i className="pi pi-search mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                <span className="font-medium inline text-base lg:text-xs lg:block">Search</span>
                                <Ripple />
                            </a>
                        </li>
                        <li>
                            <a className="p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center text-600 border-left-2 border-transparent hover:border-300 transition-duration-150 transition-colors">
                                <i className="pi pi-users mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                <span className="font-medium inline text-base lg:text-xs lg:block">Team</span>
                                <Ripple />
                            </a>
                        </li>
                        <li className="relative">
                            <StyleClass nodeRef={btnRef10} selector="@next" enterClassName="hidden" leaveToClassName="hidden" hideOnOutsideClick>
                                <a ref={btnRef10} className="p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center text-600 border-left-2 border-transparent hover:border-300 transition-duration-150 transition-colors" >
                                    <i className="pi pi-chart-line mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl p-overlay-badge"><Badge severity="danger">3</Badge></i>
                                    <span className="font-medium inline text-base lg:text-xs lg:block">Reports</span>
                                    <i className="pi pi-chevron-down ml-auto lg:hidden"></i>
                                    <Ripple />
                                </a>
                            </StyleClass>
                            <ul className="list-none pl-3 pr-0 py-0 lg:p-3 m-0 hidden overflow-y-hidden transition-all transition-duration-400 transition-ease-in-out static border-round-right lg:absolute left-100 top-0 z-1 surface-overlay shadow-none lg:shadow-2 w-full lg:w-15rem">
                                <li>
                                    <StyleClass nodeRef={btnRef11} selector="@next" toggleClassName="hidden">
                                        <a ref={btnRef11} className="p-ripple flex align-items-center cursor-pointer p-3 hover:surface-100 hover:text-900 border-round text-600 hover:text-700 transition-duration-150 transition-colors">
                                            <i className="pi pi-chart-line mr-2"></i>
                                            <span className="font-medium">Revenue</span>
                                            <i className="pi pi-chevron-down ml-auto"></i>
                                    <Ripple />
                                        </a>
                                    </StyleClass>
                                    <ul className="list-none py-0 pl-3 pr-0 m-0 hidden overflow-y-hidden transition-all transition-duration-400 transition-ease-in-out">
                                        <li>
                                            <a className="p-ripple flex align-items-center cursor-pointer p-3 hover:surface-100 hover:text-900 border-round text-600 hover:text-700 transition-duration-150 transition-colors">
                                                <i className="pi pi-table mr-2"></i>
                                                <span className="font-medium">View</span>
                                    <Ripple />
                                            </a>
                                        </li>
                                        <li>
                                            <a className="p-ripple flex align-items-center cursor-pointer p-3 hover:surface-100 hover:text-900 border-round text-600 hover:text-700 transition-duration-150 transition-colors">
                                                <i className="pi pi-search mr-2"></i>
                                                <span className="font-medium">Search</span>
                                    <Ripple />
                                            </a>
                                        </li>
                                    </ul>
                                </li>
                                <li>
                                    <a className="p-ripple flex align-items-center cursor-pointer p-3 hover:surface-100 hover:text-900 border-round text-600 hover:text-700 transition-duration-150 transition-colors">
                                        <i className="pi pi-chart-line mr-2"></i>
                                        <span className="font-medium">Expenses</span>
                                    <Ripple />
                                    </a>
                                </li>
                            </ul>
                        </li>
                        <li>
                            <a className="p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center text-600 border-left-2 border-transparent hover:border-300 transition-duration-150 transition-colors">
                                <i className="pi pi-calendar mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                <span className="font-medium inline text-base lg:text-xs lg:block">Events</span>
                                <Ripple />
                            </a>
                        </li>
                        <li>
                            <a className="p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center text-600 border-left-2 border-transparent hover:border-300 transition-duration-150 transition-colors">
                                <i className="pi pi-cog mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                <span className="font-medium inline text-base lg:text-xs lg:block">Options</span>
                                <Ripple />
                            </a>
                        </li>
                    </ul>
                </div>
                <div className="mt-auto">
                    <hr className="mb-3 mx-3 border-top-1 border-none surface-border" />
                    <a className="p-ripple m-3 flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center hover:surface-200 border-round text-600 transition-duration-150 transition-colors">
                        <img src="/demo/images/blocks/avatars/circle/avatar-f-1.png" alt="avatar-f-1" className="mr-2 lg:mr-0" style={{ width: '32px', height: '32px' }} />
                        <span className="font-medium inline lg:hidden">Amy Elsner</span>
                        <Ripple />
                    </a>
                </div>
            </div>
        </div>
        <div className="min-h-screen flex flex-column relative flex-auto">
            <div className="flex justify-content-between align-items-center px-5 surface-section relative lg:static border-bottom-1 surface-border" style={{ height: '60px' }}>
                <div className="flex">
                    <StyleClass nodeRef={btnRef12} selector="#app-sidebar-9" enterClassName="hidden" enterActiveClassName="fadeinleft" leaveToClassName="hidden" leaveActiveClassName="fadeoutleft" hideOnOutsideClick>
                        <a ref={btnRef12} className="p-ripple cursor-pointer block lg:hidden text-700 mr-3">
                            <i className="pi pi-bars text-4xl"></i>
                            <Ripple />
                        </a>
                    </StyleClass>
                    <span className="p-input-icon-left">
                        <i className="pi pi-search"></i>
                        <InputText className="border-none w-10rem sm:w-20rem" placeholder="Search" />
                    </span>
                </div>
                <StyleClass nodeRef={btnRef13} selector="@next" enterClassName="hidden" enterActiveClassName="fadein" leaveToClassName="hidden" leaveActiveClassName="fadeout" hideOnOutsideClick>
                    <a ref={btnRef13} className="p-ripple cursor-pointer block lg:hidden text-700">
                        <i className="pi pi-ellipsis-v text-2xl"></i>
                        <Ripple />
                    </a>
                </StyleClass>
                <ul className="list-none p-0 m-0 hidden lg:flex lg:align-items-center select-none lg:flex-row
        surface-section border-1 lg:border-none surface-border right-0 top-100 z-1 shadow-2 lg:shadow-none absolute lg:static">
                    <li>
                        <a className="p-ripple flex p-3 lg:px-3 lg:py-2 align-items-center text-600 hover:text-900 hover:surface-100 font-medium border-round cursor-pointer
                transition-duration-150 transition-colors">
                            <i className="pi pi-inbox text-base lg:text-2xl mr-2 lg:mr-0"></i>
                            <span className="block lg:hidden font-medium">Inbox</span>
                            <Ripple />
                        </a>
                    </li>
                    <li>
                        <a className="p-ripple flex p-3 lg:px-3 lg:py-2 align-items-center text-600 hover:text-900 hover:surface-100 font-medium border-round cursor-pointer
                transition-duration-150 transition-colors">
                            <i className="pi pi-bell text-base lg:text-2xl mr-2 lg:mr-0 p-overlay-badge"><Badge severity="danger" /></i>
                            <span className="block lg:hidden font-medium">Notifications</span>
                            <Ripple />
                        </a>
                    </li>
                    <li className="border-top-1 surface-border lg:border-top-none">
                        <a className="p-ripple flex p-3 lg:px-3 lg:py-2 align-items-center hover:surface-100 font-medium border-round cursor-pointer
                transition-duration-150 transition-colors">
                            <img src="/demo/images/blocks/avatars/circle/avatar-f-1.png" alt="avatar-f-1" className="mr-3 lg:mr-0" style={{ width: '32px', height: '32px' }} />
                            <div className="block lg:hidden">
                                <div className="text-900 font-medium">Amy Elsner</div>
                                <span className="text-600 font-medium text-sm">Marketing Specialist</span>
                            </div>
                            <Ripple />
                        </a>
                    </li>
                </ul>
            </div>
            <div className="p-5 flex flex-column flex-auto">
                <div className="grid">
                    <div className="col-12">
                        <div className="grid">
                            <div className="col-12 md:col-6 lg:col-3 p-3">
                                <div className="p-3 text-center bg-blue-500 border-round">
                                    <span className="inline-flex justify-content-center align-items-center bg-blue-600 border-circle mb-3" style={{ width: '49px', height: '49px' }}>
                                        <i className="pi pi-inbox text-xl text-white"></i>
                                    </span>
                                    <div className="text-2xl font-medium text-white mb-2">123K</div>
                                    <span className="text-blue-100 font-medium">Messages</span>
                                </div>
                            </div>
                            <div className="col-12 md:col-6 lg:col-3 p-3">
                                <div className="p-3 text-center bg-purple-500 border-round">
                                    <span className="inline-flex justify-content-center align-items-center bg-purple-600 border-circle mb-3" style={{ width: '49px', height: '49px' }}>
                                        <i className="pi pi-map-marker text-xl text-white"></i>
                                    </span>
                                    <div className="text-2xl font-medium text-white mb-2">23K</div>
                                    <span className="text-purple-100 font-medium">Check-ins</span>
                                </div>
                            </div>
                            <div className="col-12 md:col-6 lg:col-3 p-3">
                                <div className="p-3 text-center bg-indigo-500 border-round">
                                    <span className="inline-flex justify-content-center align-items-center bg-indigo-600 border-circle mb-3" style={{ width: '49px', height: '49px' }}>
                                        <i className="pi pi-file text-xl text-white"></i>
                                    </span>
                                    <div className="text-2xl font-medium text-white mb-2">23K</div>
                                    <span className="text-indigo-100 font-medium">Files</span>
                                </div>
                            </div>
                            <div className="col-12 md:col-6 lg:col-3 p-3">
                                <div className="p-3 text-center bg-orange-500 border-round">
                                    <span className="inline-flex justify-content-center align-items-center bg-orange-600 border-circle mb-3" style={{ width: '49px', height: '49px' }}>
                                        <i className="pi pi-users text-xl text-white"></i>
                                    </span>
                                    <div className="text-2xl font-medium text-white mb-2">40K</div>
                                    <span className="text-orange-100 font-medium">Users</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-12 lg:col-6">
                        <div className="shadow-2 surface-card border-round p-3">
                            {heavyHittersCategories && heavyHittersCategories.length > 0 && <HeavyHitterPieChart heavyHitters={heavyHittersCategories} />}
                        </div>
                    </div>
                    <div className="col-12 lg:col-6">
                        <ChartSlider data={res} />
                    </div>
                    <div className="col-12">
                        <div className="surface-ground">
                            <div className="grid">
                                <div className="col-12 lg:col-4 p-2">
                                    <div className="shadow-2 surface-card border-round p-4 h-full">
                                        <div className="flex align-items-start mb-5">
                                            <img src="/demo/images/blocks/avatars/circle-big/avatar-m-1.png" alt="avatar-m-1" width="56" height="56" />
                                            <div className="ml-3">
                                                <span className="block text-900 mb-1 text-xl font-medium">Cameron Williamson</span>
                                                <p className="text-600 mt-0 mb-0">Marketing Coordinator</p>
                                            </div>
                                        </div>
                                        <ul className="list-none p-0 m-0">
                                            <li className="mb-5">
                                                <div className="flex justify-content-between align-items-center">
                                                    <span className="text-900 inline-flex justify-content-between align-items-center">
                                                        <i className="pi pi-twitter mr-2"></i>
                                                        <span className="font-medium text-900">Twitter</span>
                                                    </span>
                                                    <span className="text-cyan-500 font-medium">34.00%</span>
                                                </div>
                                                <div className="surface-300 w-full mt-2" style={{ height: '7px', borderRadius: '4px' }}>
                                                    <div className="bg-cyan-500 h-full" style={{ width: '34%', borderRadius: '4px' }}></div>
                                                </div>
                                            </li>
                                            <li className="mb-5">
                                                <div className="flex justify-content-between align-items-center">
                                                    <span className="text-900 inline-flex justify-content-between align-items-center">
                                                        <i className="pi pi-facebook mr-2"></i>
                                                        <span className="font-medium text-900">Facebook</span>
                                                    </span>
                                                    <span className="text-indigo-500 font-medium">45.86%</span>
                                                </div>
                                                <div className="surface-300 w-full mt-2" style={{ height: '7px', borderRadius: '4px' }}>
                                                    <div className="bg-indigo-500 h-full" style={{ width: '45%', borderRadius: '4px' }}></div>
                                                </div>
                                            </li>
                                            <li>
                                                <div className="flex justify-content-between align-items-center">
                                                    <span className="text-900 inline-flex justify-content-between align-items-center">
                                                        <i className="pi pi-google mr-2"></i>
                                                        <span className="font-medium text-900">Google</span>
                                                    </span>
                                                    <span className="text-orange-500 font-medium">79.00%</span>
                                                </div>
                                                <div className="surface-300 w-full mt-2" style={{ height: '7px', borderRadius: '4px' }}>
                                                    <div className="bg-orange-500 h-full" style={{ width: '79%', borderRadius: '4px' }}></div>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div className="col-12 lg:col-4 p-2">
                                    <div className="shadow-2 surface-card border-round p-4 h-full">
                                        <div className="flex align-items-start mb-5">
                                            <img src="/demo/images/blocks/avatars/circle-big/avatar-f-2.png" alt="avatar-f-2" width="56" height="56" />
                                            <div className="ml-3">
                                                <span className="block text-900 mb-1 text-xl font-medium">Kathryn Murphy</span>
                                                <p className="text-600 mt-0 mb-0">Sales Manager</p>
                                            </div>
                                        </div>
                                        <ul className="list-none p-0 m-0">
                                            <li className="mb-5">
                                                <div className="flex justify-content-between align-items-center">
                                                    <span className="text-900 inline-flex justify-content-between align-items-center">
                                                        <i className="pi pi-twitter mr-2"></i>
                                                        <span className="font-medium text-900">Twitter</span>
                                                    </span>
                                                    <span className="text-cyan-500 font-medium">64.47%</span>
                                                </div>
                                                <div className="surface-300 w-full mt-2" style={{ height: '7px', borderRadius: '4px' }}>
                                                    <div className="bg-cyan-500 h-full" style={{ width: '64%', borderRadius: '4px' }}></div>
                                                </div>
                                            </li>
                                            <li className="mb-5">
                                                <div className="flex justify-content-between align-items-center">
                                                    <span className="text-900 inline-flex justify-content-between align-items-center">
                                                        <i className="pi pi-facebook mr-2"></i>
                                                        <span className="font-medium text-900">Facebook</span>
                                                    </span>
                                                    <span className="text-indigo-500 font-medium">75.67%</span>
                                                </div>
                                                <div className="surface-300 w-full mt-2" style={{ height: '7px', borderRadius: '4px' }}>
                                                    <div className="bg-indigo-500 h-full" style={{ width: '75%', borderRadius: '4px' }}></div>
                                                </div>
                                            </li>
                                            <li>
                                                <div className="flex justify-content-between align-items-center">
                                                    <span className="text-900 inline-flex justify-content-between align-items-center">
                                                        <i className="pi pi-google mr-2"></i>
                                                        <span className="font-medium text-900">Google</span>
                                                    </span>
                                                    <span className="text-orange-500 font-medium">45.00%</span>
                                                </div>
                                                <div className="surface-300 w-full mt-2" style={{ height: '7px', borderRadius: '4px' }}>
                                                    <div className="bg-orange-500 h-full" style={{ width: '45%', borderRadius: '4px' }}></div>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div className="col-12 lg:col-4 p-2">
                                    <div className="shadow-2 surface-card border-round p-4 h-full">
                                        <div className="flex align-items-start mb-5">
                                            <img src="/demo/images/blocks/avatars/circle-big/avatar-m-3.png" alt="avatar-m-3" width="56" height="56" />
                                            <div className="ml-3">
                                                <span className="block text-900 mb-1 text-xl font-medium">Darrell Steward</span>
                                                <p className="text-600 mt-0 mb-0">Web Designer</p>
                                            </div>
                                        </div>
                                        <ul className="list-none p-0 m-0">
                                            <li className="mb-5">
                                                <div className="flex justify-content-between align-items-center">
                                                    <span className="text-900 inline-flex justify-content-between align-items-center">
                                                        <i className="pi pi-twitter mr-2"></i>
                                                        <span className="font-medium text-900">Twitter</span>
                                                    </span>
                                                    <span className="text-cyan-500 font-medium">23.55%</span>
                                                </div>
                                                <div className="surface-300 w-full mt-2" style={{ height: '7px', borderRadius: '4px' }}>
                                                    <div className="bg-cyan-500 h-full" style={{ width: '34%', borderRadius: '4px' }}></div>
                                                </div>
                                            </li>
                                            <li className="mb-5">
                                                <div className="flex justify-content-between align-items-center">
                                                    <span className="text-900 inline-flex justify-content-between align-items-center">
                                                        <i className="pi pi-facebook mr-2"></i>
                                                        <span className="font-medium text-900">Facebook</span>
                                                    </span>
                                                    <span className="text-indigo-500 font-medium">78.65%</span>
                                                </div>
                                                <div className="surface-300 w-full mt-2" style={{ height: '7px', borderRadius: '4px' }}>
                                                    <div className="bg-indigo-500 h-full" style={{ width: '45%', borderRadius: '4px' }}></div>
                                                </div>
                                            </li>
                                            <li>
                                                <div className="flex justify-content-between align-items-center">
                                                    <span className="text-900 inline-flex justify-content-between align-items-center">
                                                        <i className="pi pi-google mr-2"></i>
                                                        <span className="font-medium text-900">Google</span>
                                                    </span>
                                                    <span className="text-orange-500 font-medium">86.54%</span>
                                                </div>
                                                <div className="surface-300 w-full mt-2" style={{ height: '7px', borderRadius: '4px' }}>
                                                    <div className="bg-orange-500 h-full" style={{ width: '79%', borderRadius: '4px' }}></div>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
};

export default DashboardPage;