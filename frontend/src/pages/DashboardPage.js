import React, { useEffect, useState } from 'react';
import { Ripple } from 'primereact/ripple';
import { fetchWithAuth } from './AuthPage';
import HeavyHitterPieChart from '../components/HeavyHitterPieChart';
import ChartSlider from "../components/LineChart/LineChartWrapper";
import ConnectBanks from '../components/calltoaction/ConnectBanks';
import OptimalAllocationSavingsCard from '../components/OptimalAllocationSavingsCard';
import WalletDisplay from '../components/WalletDisplay';

const DashboardPage = () => {
    const [pageView, setPageView] = useState('home');
    const [wallets, setWallets] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const [dates, setDates] = useState([]);
    const [categories, setCategories] = useState([]);
    const [isMovingAveragesReady, setIsMovingAveragesReady] = useState(false);
    const [heavyHittersCategories, setHeavyHittersCategories] = useState([]);
    const [dateRange, setDateRange] = useState([null, null]);

    const [selectedWallet, setSelectedWallet] = useState(null);

    // Function to fetch wallets
    const fetchWallets = () => {
        setLoading(true);
        fetchWithAuth('http://localhost:8000/read_user_wallets', {
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

    // Function to handle wallet updates
    const onWalletUpdate = () => {
        fetchWallets();
    };

    // Function to handle computing optimal allocation with a selected wallet
    const handleComputeOptimalAllocation = (wallet) => {
        setSelectedWallet(wallet);
        setPageView('home'); // Switch back to the 'home' view
    };

    // Fetch data for charts
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
        });
    }, []);

    // Fetch heavy hitters for the chart
    useEffect(() => {
        fetchWithAuth('http://localhost:8000/read_heavy_hitters', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                account_ids: "all",
                date_range: dateRange
            })
        }).then(response => response.json())
            .then(data => setHeavyHittersCategories(data.heavyhitters))
            .catch(error => console.log(error));
    }, [dateRange]);

    return (
        <div className="min-h-screen flex relative lg:static surface-ground">
            {/* Sidebar Navigation */}
            <div id="app-sidebar-9" className="h-full lg:h-auto surface-section hidden lg:block flex-shrink-0 absolute lg:static left-0 top-0 z-1 border-right-1 surface-border w-18rem lg:w-7rem select-none">
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
                            <li onClick={() => setPageView('preferences')}>
                                <a className={`p-ripple flex flex-row lg:flex-column align-items-center cursor-pointer p-3 lg:justify-content-center ${pageView === 'preferences' ? 'text-cyan-600 border-left-2 border-cyan-600' : 'text-600 border-transparent hover:border-300'} transition-duration-150 transition-colors`}>
                                    <i className="pi pi-heart-fill mr-2 lg:mr-0 mb-0 lg:mb-2 text-base lg:text-2xl"></i>
                                    <span className="font-medium inline text-base lg:text-xs lg:block">Preferences</span>
                                    <Ripple />
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            {/* Page Content */}
            <div className="grid surface-ground">
                {pageView === 'home' && (
                    <div className="grid surface-surface-ground">
                        <OptimalAllocationSavingsCard 
                            className="h-12rem w-full" 
                            selectedWallet={selectedWallet} 
                            wallets={wallets} 
                        />
                        <div className="grid align-content-end py-2">
                            <div className="col-5 shadow-2 surface-card border-round">
                                {heavyHittersCategories.length > 0 && <HeavyHitterPieChart heavyHitters={heavyHittersCategories} dateRange={dateRange} />}
                            </div>
                            <div className="col-7 shadow-2 surface-card border-round">
                                <ChartSlider x={dates} y_list={categories} ready={isMovingAveragesReady} onDateRangeChange={setDateRange} />
                            </div>
                        </div>
                        <div className="grid p-3 gap-3 surface-surface-ground">
                            <ConnectBanks className="col-6" />
                        </div>
                    </div>
                )}

                {pageView === 'wallets' && (
                    <div className="p-4 gap-4 surface-ground">
                        <div className='text-4xl font-bold'>Your Wallets</div>
                        <WalletDisplay 
                            wallets={wallets} 
                            loading={loading} 
                            error={error} 
                            onWalletUpdate={onWalletUpdate}
                            onComputeOptimalAllocation={handleComputeOptimalAllocation}
                        />
                    </div>
                )}

                {pageView === 'preferences' && (
                    <div className="grid p-4 gap-4 surface-ground">
                        <h2>Your Preferences</h2>
                        {/* Preferences display component or content goes here */}
                    </div>
                )}
            </div>
        </div>
    );
};

export default DashboardPage;
