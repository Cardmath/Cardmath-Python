import React from "react";
import LineChartWrapper from "./LineChartwrapper";
import SliderComponent from "../SliderComponent";

const ChartSlider = (props) => {
  const [xmin, setXmin] = React.useState("2013-04-28");
  const [xmax, setXmax] = React.useState("2014-06-28");

  const handleChart = (value) => {
    console.log("slidercalled");
    setXmin(res[value[0]].x);
    setXmax(res[value[1]].x);
  };
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
  return (
    <div>
      <LineChartWrapper xmin={xmin} xmax={xmax} />
      <SliderComponent data={res} handleChart={handleChart} />
    </div>
  );
};

export default ChartSlider;
