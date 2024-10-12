import React, { useEffect, useState } from 'react';
import { Ripple } from 'primereact/ripple';
import { InputText } from 'primereact/inputtext';
import { fetchWithAuth } from './AuthPage';
import HeavyHitterPieChart from '../components/HeavyHitterPieChart';
import ChartSlider from "../components/LineChart/LineChartWrapper";
import { StyleClass } from 'primereact/styleclass';
import ConnectBanks from '../components/calltoaction/ConnectBanks';


const DashboardPage = () => {
    const [dates, setDates] = useState([])
    const [categories, setCategories] = useState([])
    const [isMovingAveragesReady, setIsMovingAveragesReady] = useState(false) // isMovingAveragesReady 

    useEffect(() => {
        fetchWithAuth('http://localhost:8000/compute_categories_moving_averages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                account_ids: "all",
                date_range: null,
                window_size: 14,
                top_n: 10
            })
        }).then(response => {
            if (response.status === 200) {
                return response.json()        
            } 
            throw new Error(response.statusText);
        }).then(data => {
            setDates(data.dates);
            if (!Array.isArray(data.categories) || typeof data.categories[0] !== 'object') {
                throw new Error("Categories must be a list of lists");
            }
            setCategories(data.categories);
            setIsMovingAveragesReady(true);
        })
    }, []);

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
                    <div className="col-12 lg:col-6">
                        <div className="shadow-2 surface-card border-round p-3">
                            {heavyHittersCategories && heavyHittersCategories.length > 0 && <HeavyHitterPieChart heavyHitters={heavyHittersCategories} />}
                        </div>
                    </div>
                    <div className="col-12 lg:col-6">
                    <ChartSlider x={dates} y_list={categories} ready={isMovingAveragesReady} />
                    </div>
                    <div className="col-12">
                        <div className="surface-ground">                            
                            <ConnectBanks />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
};

export default DashboardPage;