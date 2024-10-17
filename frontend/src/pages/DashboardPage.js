import React, { useEffect, useState } from 'react';
import { Ripple } from 'primereact/ripple';
import { InputText } from 'primereact/inputtext';
import { fetchWithAuth } from './AuthPage';
import HeavyHitterPieChart from '../components/HeavyHitterPieChart';
import ChartSlider from "../components/LineChart/LineChartWrapper";
import { StyleClass } from 'primereact/styleclass';
import ConnectBanks from '../components/calltoaction/ConnectBanks';
import OptimalAllocationSavingsCard from '../components/OptimalAllocationSavingsCard';


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
                window_size: 60,
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
                <div className="flex align-items-center justify-content-center" style={{ height: '60px' }}>
                    <img src="/logos/svg/Black logo - no background.svg" alt="Image" height="20" />
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
                                <span className="font-medium inline text-base lg:text-xs lg:block">Search Cards</span>
                                <Ripple />
                            </a>
                        </li>
                        <li>
                            <a className="p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center text-600 border-left-2 border-transparent hover:border-300 transition-duration-150 transition-colors">
                                <i className="pi pi-heart-fill mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                <span className="font-medium inline text-base lg:text-xs lg:block">Preferences</span>
                                <Ripple />
                            </a>
                        </li>
                        <li>
                            <a className="p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center text-600 border-left-2 border-transparent hover:border-300 transition-duration-150 transition-colors">
                                <i className="pi pi-cog mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                <span className="font-medium inline text-base lg:text-xs lg:block">Settings</span>
                                <Ripple />
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div className="min-h-screen flex flex-column relative flex-auto">
                <div className="flex align-content-end py-3">
                    <div className="flex-column flex-none shadow-2 surface-card border-round">
                        {heavyHittersCategories && heavyHittersCategories.length > 0 && <HeavyHitterPieChart className="w-full h-full" heavyHitters={heavyHittersCategories} />}
                    </div>
                    <div className="flex-column flex-grow-1 shadow-2 surface-card border-round p-4 h-full">
                        <ChartSlider x={dates} y_list={categories} ready={isMovingAveragesReady}/>
                    </div>
                </div>
                <div className="grid p-3 gap-3 surface-surface-ground">                                                 
                            <ConnectBanks className="col-6"/>
                            <OptimalAllocationSavingsCard className="col-2" />
                </div>
        </div>
    </div>
};

export default DashboardPage;