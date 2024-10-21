import React, { useEffect, useState } from "react";
import { Slider } from 'primereact/slider';

const SliderComponent = ({ data = [], handleChart }) => {
  const [value, setValue] = useState([0, data.length - 1]);
  const [mark, setMark] = useState([]);

  const minDistance = 4;

  const handleChange = (newValue) => {
    let [left, right] = newValue.value;
    left = isNaN(left) ? (isNaN(value[0]) ? 0 : value[0]) : left;
    right = isNaN(right) ? (isNaN(value[1]) ? data.length - 1 : value[1]) : right;

    if (right - left < minDistance) {
      if (left === value[0]) {
        const clamped = Math.min(left, right - minDistance);
        setValue([clamped, clamped + minDistance]);
        handleChart([clamped, clamped + minDistance]);
      } else {
        const clamped = Math.max(right, left + minDistance);
        setValue([clamped - minDistance, clamped]);
        handleChart([clamped - minDistance, clamped]);
      }
    } else {
      setValue([left, right]);
      handleChart([left, right]);
    }
  };

  useEffect(() => {
    if (data.length === 0) return;

    let markObj = [];
    data.forEach((e, i) => {
      if (i % 4 === 0) {
        markObj.push({
          label: e.x,
          value: i
        });
      }
    });

    setValue([0, data.length - 1]);
    setMark(markObj);
  }, [data]);

  if (data.length === 0) {
    return <div>No data available</div>;
  }

  return (
    <div>
      <Slider className="mr-7"
        value={value}
        min={0}
        max={data.length - 1}
        onChange={handleChange}
        range
        aria-labelledby="range-slider"
      />
    </div>
  );
};

export default SliderComponent;
