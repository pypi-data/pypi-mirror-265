import React, { useCallback, useRef, useState } from "react";
import Sidebar from "../components/Sidebar";
import { BiMinus } from "react-icons/bi";
import menuIcon from "../assets/Frame.svg";
import Drawer from "react-modern-drawer";
import close from "../assets/close.svg";
import Header from "../components/Header";
import DocumentSidebar from "../components/document/DocumentSidebar";
import portfolio from "../../src/images/portfolio.png";
import docprofile from "../../src/images/docprofile.png";
import { FiTable } from "react-icons/fi";
import { RiArrowLeftSLine, RiArrowRightSLine } from "react-icons/ri";
import docwave from '../images/docwave.png'
import { time } from 'ag-charts-community';
import { AgChartsReact } from 'ag-charts-react';

var lastTime = new Date('07 Jan 2020 13:25:00 GMT').getTime();
var data = [];
function getData() {
    data.shift();
    while (data.length < 20) {
        data.push({
            time: new Date((lastTime += 1000)),
            voltage: 1.1 + Math.random() / 2,
        });
    }
    return data;
}

function getData1() {
    return [
        { asset: "Stocks", amount: 60000 },
        { asset: "Bonds", amount: 40000 },
        { asset: "Cash", amount: 7000 },
        { asset: "Real Estate", amount: 5000 },
        { asset: "Commodities", amount: 3000 },
    ];
}

const Document = () => {
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);
    const chartRef = useRef(null);
    const [updating, setUpdating] = useState(false);
    const [options, setOptions] = useState({
        data: getData(),
        series: [
            {
                xKey: 'time',
                yKey: 'voltage',
            },
        ],
        axes: [
            {
                type: 'time',
                position: 'bottom',
                nice: false,
                tick: {
                    interval: time.second.every(5),
                },
                label: {
                    format: '%H:%M:%S',
                },
            },
            {
                type: 'number',
                position: 'left',
                label: {
                    format: '#{.2f}V',
                },
            },
        ],
        title: {
            text: 'Core Voltage',
        },
    });

    const [chartOptions, setChartOptions] = useState({
        data: getData1(),
        title: {
            text: "Portfolio Composition",
        },
        series: [
            {
                type: "pie",
                angleKey: "amount",
                calloutLabelKey: "asset",
                sectorLabelKey: "amount",
                sectorLabel: {
                    color: "white",
                    fontWeight: "bold",
                    formatter: ({ value }) => `$${(value / 1000).toFixed(0)}K`,
                },
            },
        ],
    });

    const update = useCallback(() => {
        const clone = { ...options };

        clone.data = getData();

        setOptions(clone);
    }, [getData, options]);

    const startUpdates = useCallback(() => {
        if (updating) {
            return;
        }
        setUpdating(true);
        update();
        setInterval(update, 500);
    }, [updating]);

    const toggleDrawer = () => {
        setIsDrawerOpen(!isDrawerOpen);
    };

    const [isDragging, setIsDragging] = useState(false);

    const handleDragStart = (event) => {
        event.dataTransfer.setData("text/plain", event.target.id);
        setIsDragging(true);
    };

    const handleDragEnd = () => {
        setIsDragging(false);
    };

    const handleDrop = (event) => {
        event.preventDefault();
        const draggableId = event.dataTransfer.getData("text/plain");
        const draggedElement = document.getElementById(draggableId);
        const dropTarget = event.currentTarget;

        if (dropTarget === event.target || dropTarget.contains(event.target)) {
            dropTarget.appendChild(draggedElement);
        }

        setIsDragging(false);
    };

    const handleDragOver = (event) => {
        event.preventDefault();
    };

    return (
        <>
            <div className="flex lg:block">
                <div className="z-[999]">
                    <img
                        src={menuIcon}
                        className={`hidden xl:flex xl:absolute w-[27px] h-[27px] mx-4 my-8 ${isDrawerOpen === true ? "xl:hidden" : ""
                            }`}
                        onClick={toggleDrawer}
                        alt=""
                    />
                </div>

                <div className="xl:hidden w-1/5 font-cerebri flex border-r-[0.5px] border-[#CDCDCD]">
                    <Sidebar />
                    <DocumentSidebar />
                </div>

                <Drawer
                    open={isDrawerOpen}
                    onClose={toggleDrawer}
                    direction="left"
                    className="chatDrawer"
                >
                    <Sidebar />
                    <div className="font-cerebri w-[-webkit-fill-available] flex flex-col justify-between">
                        <img
                            src={close}
                            className="w-[14px] h-[14px] absolute right-3 top-5"
                            onClick={toggleDrawer}
                            alt=""
                        />
                        <DocumentSidebar />
                    </div>
                </Drawer>

                <div className="w-full">
                    <Header />
                    <div className="flex lg:flex-col">
                        <div className="w-4/5 bg-[#f3f4f6] lg:w-full">
                            <div className="px-4 py-2">
                                {/* <div className="bg-customBg rounded-md px-12 py-2 flex items-center justify-between">
                                    <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">
                                        Agents
                                    </h1>
                                    <div className="flex items-center gap-2">
                                        <img src={docprofile} alt="docprofile" />
                                        <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">
                                            Risk Model Agent
                                        </h1>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <img src={docprofile} alt="docprofile" />
                                        <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">
                                            vs Benchmark Agent
                                        </h1>
                                    </div>
                                    <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">
                                        Agent 3
                                    </h1>
                                </div> */}
                                <div
                                    className="bg-[#fff] rounded-xl px-5 py-5 mt-4 h-[calc(100vh-205px)] overflow-auto scrollbar"
                                    id="drop-target"
                                    onDrop={handleDrop}
                                    onDragOver={handleDragOver}
                                >
                                    {/* <h1 className="text-[#3C3C3C] text-[18px] font-cerebri leading-[24px]">
                                        Canvas
                                    </h1> */}

                                    <div className="flex justify-between gap-7 xxl:flex-wrap">
                                        <div className="rounded-md shadow-dropCard px-5 pt-4 pb-2 w-full xxl:w-[200px] xs:w-full xs:text-center">
                                            <p className="text-[#808080] text-[16px] font-cerebrisemibold leading-[24px]">Your Portfolio Value</p>
                                            <h1 className="text-[#000000] text-[20px] font-cerebrisemibold leading-[40px]">$5,078,89</h1>
                                        </div>
                                        <div className="rounded-md shadow-dropCard px-5 pt-4 pb-2 w-full  xxl:w-[200px] xs:w-full xs:text-center">
                                            <p className="text-[#808080] text-[16px] font-cerebrisemibold leading-[24px]">Today’s Gain</p>
                                            <h1 className="text-[#000000] text-[20px] font-cerebrisemibold leading-[30px]">+85,87 (1,35%)</h1>
                                        </div>
                                        <div className="rounded-md shadow-dropCard px-5 pt-4 pb-2 w-full  xxl:w-[200px] xs:w-full xs:text-center">
                                            <p className="text-[#808080] text-[16px] font-cerebrisemibold leading-[24px]">Today’s Gain</p>
                                            <h1 className="text-[#000000] text-[20px] font-cerebrisemibold leading-[30px]">+843,70 (7,35%)</h1>
                                        </div>
                                        <div className="rounded-md shadow-dropCard px-5 pt-4 pb-2 w-full  xxl:w-[200px] xs:w-full xs:text-center">
                                            <p className="text-[#808080] text-[16px] font-cerebrisemibold leading-[24px]">Today’s Gain</p>
                                            <h1 className="text-[#000000] text-[20px] font-cerebrisemibold leading-[30px]">+843,70 (7,35%)</h1>
                                        </div>
                                    </div>

                                    <div className="my-4 flex xxl:flex-col">
                                        <div className="wrapper w-[50%] h-[384px] xxl:w-full">
                                            {/* <div class="toolPanel">
                                                <button onClick={startUpdates}>Start Updates</button>
                                            </div> */}
                                            <AgChartsReact ref={chartRef} options={options} />
                                        </div>
                                        {/* <div className="xxl:mt-4">
                                            <h1 className="text-[#000000] text-[20px] font-cerebri leading-[32px] mb-3">Portfolio Analysis</h1>
                                            <div className="flex justify-between items-center my-3">
                                                <div>
                                                    <h1 className="text-[#000000] text-[18px] font-cerebri leading-[28px]">Valuation</h1>
                                                    <p className="text-[#808080] text-[16px] font-cerebriregular leading-[24px]">3 of 5 stock are Near Fair Value in the midterm</p>
                                                </div>
                                                <RiArrowRightSLine className="text-[23px]" />
                                            </div>
                                            <hr />
                                            <div className="flex justify-between items-center my-3">
                                                <div>
                                                    <h1 className="text-[#000000] text-[18px] font-cerebri leading-[28px]">Diversification</h1>
                                                    <p className="text-[#808080] text-[16px] font-cerebriregular leading-[24px]">59% of the stocks are exposed to the Consumer Cyclical sector.</p>
                                                </div>
                                                <RiArrowRightSLine className="text-[23px]" />
                                            </div>
                                            <hr />
                                            <div className="flex justify-between items-center my-3">
                                                <div>
                                                    <h1 className="text-[#000000] text-[18px] font-cerebri leading-[28px]">Risk Level</h1>
                                                    <p className="text-[#808080] text-[16px] font-cerebriregular leading-[24px]">The risk profile is assessed as moderate.</p>
                                                </div>
                                                <RiArrowRightSLine className="text-[23px]" />
                                            </div>
                                        </div> */}
                                        <div className="xxl:mt-4 w-[50%] xxl:w-full">
                                            <AgChartsReact options={chartOptions} />
                                        </div>
                                    </div>

                                    <div className="flex gap-5 xxl:flex-wrap">
                                        <div className="w-full">
                                            <div className="flex items-center justify-between">
                                                <h1 className="text-[#000000] text-[20px] font-cerebri leading-[32px]">Your watchlist</h1>
                                                <div className="flex items-center gap-3">
                                                    <RiArrowLeftSLine className="text-[23px]" />
                                                    <RiArrowRightSLine className="text-[23px]" />
                                                </div>
                                            </div>
                                            <div className="cursor-pointer">
                                                <table className="bg-white w-full">
                                                    <thead>
                                                        <tr>
                                                            <th className="px-3 py-3 border-b-2 border-gray-300 text-left text-xs font-cerebriregular leading-[20px] text-[#808080] uppercase">
                                                                Company
                                                            </th>
                                                            <th className="px-3 py-3 border-b-2 border-gray-300 text-left text-xs font-cerebriregular leading-[20px] text-[#808080] uppercase">
                                                                Last Price
                                                            </th>
                                                            <th className="px-3 py-3 border-b-2 border-gray-300 text-left text-xs font-cerebriregular leading-[20px] text-[#808080] uppercase">
                                                                Change
                                                            </th>
                                                            <th className="px-3 py-3 border-b-2 border-gray-300 text-left text-xs font-cerebriregular leading-[20px] text-[#808080] uppercase">
                                                                7-Day Chart
                                                            </th>
                                                        </tr>
                                                    </thead>
                                                    <tbody className="bg-white">
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                Dow Jones
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                $19,626.34
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000] border-b border-gray-200">
                                                                <p className="font-cerebribold text-customColor">+547.34</p>
                                                                <p className="font-cerebriregular">+2.87%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                Apple
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                $4,626.34
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000] border-b border-gray-200">
                                                                <p className="font-cerebribold text-customColor">+79.34</p>
                                                                <p className="font-cerebriregular">+1.87%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                BTC/USD
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                $19,626.34
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000] border-b border-gray-200">
                                                                <p className="font-cerebribold text-customColor">+547.34</p>
                                                                <p className="font-cerebriregular">+2.87%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                ETH/USD
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                $0,7278
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000] border-b border-gray-200">
                                                                <p className="font-cerebribold text-customColor">+0.0034</p>
                                                                <p className="font-cerebriregular">+2.87%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                EUR/USD
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                $82.73
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000] border-b border-gray-200">
                                                                <p className="font-cerebribold text-customColor">+82.34</p>
                                                                <p className="font-cerebriregular">+0.27%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000]">
                                                                EUR/USD
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000]">
                                                                $82.73
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000]">
                                                                <p className="font-cerebribold text-customColor">+82.34</p>
                                                                <p className="font-cerebriregular">+0.27%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                        <div className="w-full">
                                            <div className="flex items-center justify-between">
                                                <h1 className="text-[#000000] text-[20px] font-cerebri leading-[32px]">Indices</h1>
                                                <div className="flex items-center gap-3">
                                                    <RiArrowLeftSLine className="text-[23px]" />
                                                    <RiArrowRightSLine className="text-[23px]" />
                                                </div>
                                            </div>
                                            <div className="cursor-pointer">
                                                <table className="bg-white w-full">
                                                    <thead>
                                                        <tr>
                                                            <th className="px-3 py-3 border-b-2 border-gray-300 text-left text-xs font-cerebriregular leading-[20px] text-[#808080] uppercase">
                                                                Company
                                                            </th>
                                                            <th className="px-3 py-3 border-b-2 border-gray-300 text-left text-xs font-cerebriregular leading-[20px] text-[#808080] uppercase">
                                                                Last Price
                                                            </th>
                                                            <th className="px-3 py-3 border-b-2 border-gray-300 text-left text-xs font-cerebriregular leading-[20px] text-[#808080] uppercase">
                                                                Change
                                                            </th>
                                                            <th className="px-3 py-3 border-b-2 border-gray-300 text-left text-xs font-cerebriregular leading-[20px] text-[#808080] uppercase">
                                                                7-Day Chart
                                                            </th>
                                                        </tr>
                                                    </thead>
                                                    <tbody className="bg-white">
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                S&P/TSX
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                $19,626.34
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000] border-b border-gray-200">
                                                                <p className="font-cerebribold text-customColor">+547.34</p>
                                                                <p className="font-cerebriregular">+2.87%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                S&P 500
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                $4,626.34
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000] border-b border-gray-200">
                                                                <p className="font-cerebribold text-customColor">+79.34</p>
                                                                <p className="font-cerebriregular">+1.87%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                DOW
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                $19,626.34
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000] border-b border-gray-200">
                                                                <p className="font-cerebribold text-customColor">+547.34</p>
                                                                <p className="font-cerebriregular">+2.87%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                CAD/USD
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                $0,7278
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000] border-b border-gray-200">
                                                                <p className="font-cerebribold text-customColor">+0.0034</p>
                                                                <p className="font-cerebriregular">+2.87%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                Bitcoin CAD
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000] border-b border-gray-200">
                                                                $82.73
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000] border-b border-gray-200">
                                                                <p className="font-cerebribold text-customColor">+82.34</p>
                                                                <p className="font-cerebriregular">+0.27%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000]">
                                                                NACDAQ
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] font-cerebribold text-[#000000]">
                                                                $82.73
                                                            </td>
                                                            <td className="p-2 text-[14px] leading-[20px] text-[#000000]">
                                                                <p className="font-cerebribold text-customColor">+82.34</p>
                                                                <p className="font-cerebriregular">+0.27%</p>
                                                            </td>
                                                            <td>
                                                                <img src={docwave} alt="docwave" />
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>

                                            </div>
                                        </div>
                                        {/* <div className="w-[370px]">
                                            <h1 className="text-[#000000] text-[20px] font-cerebri leading-[32px] mb-3">News</h1>
                                            <div>
                                                <p className="text-[#808080] text-[14px] font-cerebriregular leading-[20px] mb-2">5 minutes ago</p>
                                                <h1 className="text-[#000000] text-[16px] font-cerebribold leading-[24px] mb-2">Bitcoin rally driven by macroeconomic factors, not spot ETF speculation - QCP Capital</h1>
                                                <hr />
                                            </div>
                                            <div className="my-3">
                                                <p className="text-[#808080] text-[14px] font-cerebriregular leading-[20px] mb-2">17 minutes ago</p>
                                                <h1 className="text-[#000000] text-[16px] font-cerebribold leading-[24px] mb-2">Satoshi-Era Bitcoin (BTC) Whales Making Massive Transfers</h1>
                                                <hr />
                                            </div>
                                            <div className="my-3">
                                                <p className="text-[#808080] text-[14px] font-cerebriregular leading-[20px] mb-2">5 minutes ago</p>
                                                <h1 className="text-[#000000] text-[16px] font-cerebribold leading-[24px] mb-2">Bitcoin rally driven by macroeconomic factors, not spot ETF speculation - QCP Capital</h1>
                                                <hr />
                                            </div>
                                            <div className="my-3">
                                                <p className="text-[#808080] text-[14px] font-cerebriregular leading-[20px] mb-2">5 minutes ago</p>
                                                <h1 className="text-[#000000] text-[16px] font-cerebribold leading-[24px] mb-2">Bitcoin's Secret Catalyst: Not ETFs But Unexpected Macro Forces: QCP Research</h1>
                                            </div>
                                        </div> */}
                                    </div>

                                </div>
                                <div className="bg-customBg border rounded-md px-12 py-2 flex items-center justify-between mt-4">
                                    <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">
                                        Audience
                                    </h1>
                                    <div className="flex items-center gap-2">
                                        <img src={docprofile} alt="docprofile" />
                                        <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">
                                            Risk Model Agent
                                        </h1>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <img src={docprofile} alt="docprofile" />
                                        <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">
                                            vs Benchmark Agent
                                        </h1>
                                    </div>
                                    <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">
                                        Agent 3
                                    </h1>
                                </div>
                            </div>
                        </div>
                        <div className="w-1/5 h-[calc(100vh-93px)] overflow-auto scrollbar border-l-[0.5px] border-[#CDCDCD] px-5 py-6  lg:w-full lg:h-auto">
                            <h1 className="text-[#3C3C3C] text-[20px] font-cerebri leading-[24px]">
                                Outputs
                            </h1>

                            <div className="flex gap-3 mt-5 items-center"
                                id="drag-source3"
                                draggable
                                onDragStart={handleDragStart}
                                onDragEnd={handleDragEnd}>
                                <div className="bg-customBg p-3 rounded-xl border border-customBorder w-fit">
                                    <FiTable />
                                </div>
                                <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px]">
                                    Table
                                </p>
                            </div>

                            {/* <div className="cursor-pointer">
                                <table className="min-w-full bg-white">
                                    <thead>
                                        <tr>
                                            <th className="px-6 py-3 border-b-2 border-gray-300 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                                                Name
                                            </th>
                                            <th className="px-6 py-3 border-b-2 border-gray-300 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                                                Age
                                            </th>
                                            <th className="px-6 py-3 border-b-2 border-gray-300 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                                                Email
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody className="bg-white">
                                        <tr>
                                            <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                                                John Doe
                                            </td>
                                            <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                                                30
                                            </td>
                                            <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                                                john@example.com
                                            </td>
                                        </tr>
                                        <tr>
                                            <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                                                Jane Smith
                                            </td>
                                            <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                                                25
                                            </td>
                                            <td className="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                                                jane@example.com
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div> */}

                            <div
                                className="mt-8 cursor-pointer"
                                id="drag-source"
                                draggable
                                onDragStart={handleDragStart}
                                onDragEnd={handleDragEnd}
                            >
                                <div className="flex items-center gap-3">
                                    <img src={portfolio} alt="portfolio" />
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px]">
                                        Summary
                                    </p>
                                </div>
                                <div className="mt-3 ms-20 xxl:ms-14">
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit">
                                        Concise
                                    </p>
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit mt-2">
                                        Detailed
                                    </p>
                                </div>
                            </div>
                            <div
                                className="mt-8 cursor-pointer"
                                id="drag-source1"
                                draggable
                                onDragStart={handleDragStart}
                                onDragEnd={handleDragEnd}
                            >
                                <div className="flex items-center gap-3">
                                    <img src={portfolio} alt="portfolio" />
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px]">
                                        Charts
                                    </p>
                                </div>
                                <div className="mt-3 ms-20 xxl:ms-14">
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit">
                                        Most Relevant (Agent Chosen)
                                    </p>
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit mt-2">
                                        User-annotated
                                    </p>
                                </div>
                            </div>

                            <h1 className="text-[#3C3C3C] text-[20px] font-cerebri leading-[24px] mt-6">
                                Portfolio
                            </h1>
                            <div
                                className="mt-8 cursor-pointer"
                                id="drag-source2"
                                draggable
                                onDragStart={handleDragStart}
                                onDragEnd={handleDragEnd}
                            >
                                <div className="flex items-center gap-3">
                                    <img src={portfolio} alt="portfolio" />
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px]">
                                        Tables
                                    </p>
                                </div>
                                <div className="mt-3 ms-20 xxl:ms-14">
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit">
                                        Most Relevant (Agent Chosen)
                                    </p>
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit mt-2">
                                        User-annotated
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Document;
