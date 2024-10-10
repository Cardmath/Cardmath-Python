import React from "react";
import { Slider } from 'primereact/slider';
    
const SliderComponent = (props) => {
  const [value, setValue] = React.useState([0,props.data.length - 1]);
  const [min, setMin] = React.useState(0);
  const [max, setMax] = React.useState(props.data.length - 1);
  const [mark, setMark] = React.useState([]);

  const calculateValue = (value) => {
    if (!value) return "";
    return props.data[value].x;
  };

  const valueLabelFormat = (value) => {
    return value;
  };

  const minDistance = 4;

  const handleChange = (newValue) => {
    let [left, right] = newValue.value;
    left = isNaN(left) ? value[0] : left;
    right = isNaN(right) ? value[1] : right; 
    const activeThumb = left == value[0];
    
    if (right - left < minDistance) {
      if (activeThumb === 0) {
        const clamped = Math.min(left, right-minDistance);
        setValue([clamped, clamped + minDistance]);
        props.handleChart([clamped, clamped + minDistance]);
      } else {
        const clamped = Math.max(right, minDistance);
        setValue([clamped - minDistance, clamped]);
        props.handleChart([clamped - minDistance, clamped]);
      }
    } else if (right - left === minDistance) {
      const clamped = Math.max(left, minDistance);
      setValue([left, left + minDistance]);
      props.handleChart([left, left + minDistance]);
    } else {
      setValue([left, right]);
      props.handleChart([left, right]);
    }
  };

  React.useEffect(() => {
    let val = [];
    let markObj = [];
    let objLength = props.data.length;
    props.data.map((e, i) => {
      val.push(i);
      if (i % 4 === 0) {
        markObj.push({
          label: e.x,
          value: i
        });
      }
    });
    setValue([val[0], val[val.length - 1]]);
    setMark(markObj);
    setMin(val[0]);
    setMax(val[val.length - 1]);
  }, [props.data]);

  return (
    <div>
      {/* <Typography id="range-slider" gutterBottom>
        Chart range
      </Typography> */}
      <Slider
        value={value}
        min={min}
        max={max}
        onChange={handleChange}
        range
        // getAriaValueText={valueLabelFormat}
        // valueLabelFormat={valueLabelFormat}
        // ValueLabelComponent={ValueLabelComponent}
        // marks={mark}
        // valueLabelDisplay="auto"
        aria-labelledby="range-slider"
      />
    </div>
  );
};

export default SliderComponent;
