import React, { useEffect, useState } from 'react';
import { Ripple } from 'primereact/ripple';
import { fetchWithAuth } from './AuthPage';
import { Tooltip } from 'primereact/tooltip';
import HeavyHitterPieChart from '../components/HeavyHitterPieChart';
import ChartSlider from "../components/LineChart/LineChartWrapper";
import ConnectBanks from '../components/calltoaction/ConnectBanks';
import OptimalAllocationSavingsCard from '../components/OptimalAllocationSavingsCard';
import WalletDisplay from '../components/WalletDisplay';
import CategorizationMeter from '../components/CategorizationMeter';
import PreferencesCard from '../components/PreferencesCard';
import Alert from '../components/Alert';
import SettingsPage from './SettingsPage';
import { getBackendUrl } from '../utils/urlResolver';

const DashboardPage = () => {
    const [pageView, setPageView] = useState('home');
    const [wallets, setWallets] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const [dates, setDates] = useState([]);
    const [categories, setCategories] = useState([]);
    const [isMovingAveragesReady, setIsMovingAveragesReady] = useState(false);
    const [heavyHittersCategories, setHeavyHittersCategories] = useState([]);
    const [hhTotal, setHHTotal] = useState(0);
    const [dateRange, setDateRange] = useState([null, null]);

    const [categorizationProgressSummary, setCategorizationProgressSummary] = useState({
        categorized_cc_eligible_count: 0,
        uncategorized_cc_eligible_count: 0,
        non_cc_eligible_count: 0
    });

    const [selectedWallet, setSelectedWallet] = useState(null);

    const [alert, setAlert] = useState({visible: false, message: '', heading : '', type: 'error'});

    // Fetch wallets function
    const fetchWallets = () => {
        setLoading(true);
        fetchWithAuth(`${getBackendUrl()}/read_user_wallets`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        })
        .then(response => response.json())
        .then(data => {
            setWallets(data);
            setLoading(false);
        })
        .catch(err => {
            console.error('Error fetching wallets:', err);
            setError('Failed to load wallets. Please try again later.');
            setLoading(false);
        });
    };

    // Fetch wallets when the component mounts or when pageView changes
    useEffect(() => {
        fetchWallets();
    }, [pageView]);

    const onWalletUpdate = () => {
        fetchWallets();
    };

    const handleComputeOptimalAllocation = (wallet) => {
        setSelectedWallet(wallet);
        setPageView('home');
    };

    const redirectToWallets = () => {
        setPageView('wallets')
    }

    useEffect(() => {
        fetchWithAuth(`${getBackendUrl()}/compute_categories_moving_averages`, {
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
                return response.json();
            }
            throw new Error(response.statusText);
        }).then(data => {
            if (data == null) {
                return
            }
            setDates(data.dates);
            if (!Array.isArray(data.categories) || typeof data.categories[0] !== 'object') {
                throw new Error("Categories must be a list of lists");
            }
            setCategories(data.categories);
            setIsMovingAveragesReady(true);
        });
    }, []);

    useEffect(() => {
        fetchWithAuth(`${getBackendUrl()}/read_heavy_hitters`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                account_ids: "all",
                date_range: dateRange
            })
        })
            .then(response => response.json())
            .then(data => {
                setHHTotal(data.total)
                setDates(data.timeframe)
                setHeavyHittersCategories(data.heavyhitters);
                if (data.categorization_progress_summary) {
                    setCategorizationProgressSummary(data.categorization_progress_summary);
                }
            })
            .catch(error => console.log(error));
    }, []);

    return (
        <div className="min-h-screen flex relative lg:static surface-ground">
            {/* Sidebar Navigation */}
            <div id="app-sidebar-9" className="h-full  lg:h-auto bg-gray-800  hidden lg:block flex-shrink-0 absolute lg:static left-0 top-0 z-1 border-right-1 w-18rem lg:w-7rem select-none">
                <div className="flex flex-column h-full">
                    <div className="mt-3">
                        <ul className="list-none p-0 m-0">
                            <li onClick={() => setPageView('home')}>
                                <a className={`p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center ${pageView === 'home' ? 'text-cyan-600 border-left-2 border-cyan-600' : 'text-600 border-transparent hover:border-300'} transition-duration-150 transition-colors`}>
                                    <i className="pi pi-home mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                    <span className="font-medium inline text-base lg:text-xs lg:block">Home</span>
                                    <Ripple />
                                </a>
                            </li>
                            <li onClick={() => setPageView('wallets')}>
                                <a className={`p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center ${pageView === 'wallets' ? 'text-cyan-600 border-left-2 border-cyan-600' : 'text-600 border-transparent hover:border-300'} transition-duration-150 transition-colors`}>
                                    <i className="pi pi-wallet mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                    <span className="font-medium inline text-base lg:text-xs lg:block">Your Wallets</span>
                                    <Ripple />
                                </a>
                            </li>
                            <li onClick={() => setPageView('travel')}>
                                <a className={`p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center ${pageView === 'travel' ? 'text-cyan-600 border-left-2 border-cyan-600' : 'text-600 border-transparent hover:border-300'} transition-duration-150 transition-colors`}>
                                    <i className="pi pi-compass mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                    <span className="font-medium inline text-base lg:text-xs lg:block">Travel</span>
                                    <Ripple />
                                </a>
                            </li>
                            {/* <li onClick={() => setPageView('preferences')}>
                                <a className={`p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center ${pageView === 'preferences' ? 'text-cyan-600 border-left-2 border-cyan-600' : 'text-600 border-transparent hover:border-300'} transition-duration-150 transition-colors`}>
                                    <i className="pi pi-heart-fill mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                    <span className="font-medium inline text-base lg:text-xs lg:block">Filters</span>
                                    <Ripple />
                                </a>
                            </li> */}
                            <li onClick={() => setPageView('settings')}>
                                <a className={`p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center ${pageView === 'settings' ? 'text-cyan-600 border-left-2 border-cyan-600' : 'text-600 border-transparent hover:border-300'} transition-duration-150 transition-colors`}>
                                    <i className="pi pi-cog mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                    <span className="font-medium inline text-base lg:text-xs lg:block">Settings</span>
                                    <Ripple />
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            {/* Page Content */}
            <div className="bg-gray-800 w-full">
                {pageView === 'home' && (
                    <div className="grid bg-gray-800">
                        <OptimalAllocationSavingsCard 
                            className="h-12rem w-full" 
                            selectedWallet={selectedWallet} 
                            wallets={wallets} 
                            redirectToWallets={redirectToWallets}
                        />
                        <Tooltip className='w-3' target=".categorization-meter" position="bottom"/>
                        <CategorizationMeter className="categorization-meter" data-pr-tooltip="  Non-Eligible transactions cannot be made with credit cards. Examples of Non-Eligible transactions are: ATM withdrawals, ACH transfers, etc. . You may have to wait for our systems categorize your transactions." progressSummary={categorizationProgressSummary} />                        
                        <div className="col-12 py-2">
                            <div className="col-5 shadow-2 border-round">
                                {heavyHittersCategories.length > 0 && <HeavyHitterPieChart total={hhTotal} heavyHitters={heavyHittersCategories} dateRange={dates} />}
                            </div>
                            {isMovingAveragesReady && (
                                <div className="col-7 shadow-2 border-round">
                                <ChartSlider x={dates} y_list={categories} ready={isMovingAveragesReady} onDateRangeChange={setDateRange} />
                            </div>
                            )}
                        </div>
                    </div>
                )}

                {pageView === 'wallets' && (
                    <div className="p-4 gap-4 bg-gray-800">
                        <div className='text-4xl font-bold text-white'>Your Wallets</div>
                        <WalletDisplay 
                            wallets={wallets} 
                            loading={loading} 
                            error={error} 
                            onWalletUpdate={onWalletUpdate}
                            onComputeOptimalAllocation={handleComputeOptimalAllocation}
                        />
                    </div>
                )}

                {pageView === 'travel' && (
                    <div className="flex flex-column align-items-center justify-content-center h-screen text-white">
                        <i className="pi pi-wrench text-4xl mb-3"></i>
                        <div className="text-3xl font-bold text-center mb-4">
                            Coming in Q3 2025 - Travel Optimally with Cash and Points
                        </div>
                        <p className="text-lg text-center">
                            Tell us your favorite destinations and when you want to go, and we'll calculate the cheapest, fastest, and most comfortable way to get you there!
                        </p>
                    </div>
                )}

                {pageView === 'preferences' && (
                    <div className="p-4 gap-4 bg-gray-800">
                        <Alert 
                            visible={alert.visible} 
                            message={alert.message} 
                            type={alert.type} 
                            heading={alert.heading} 
                            setVisible={(visible) => setAlert({ ...alert, visible })}
                        />
                        <PreferencesCard setAlert={setAlert}/>
                    </div>
                )}
                
                {pageView === 'settings' && <SettingsPage />}
            </div>
        </div>
    );
};

export default DashboardPage;
