import React, { useState } from 'react';

const ThresholdSlider = ({ onThresholdSelect, initialValue = 150 }) => {
  const [value, setValue] = useState(initialValue);

  const handleSliderChange = (event) => {
    const newValue = parseInt(event.target.value);
    setValue(newValue);
    onThresholdSelect(newValue);
  };

  return (
    <input
      type="range"
      min="0"
      max="255"
      value={value}
      onChange={handleSliderChange}
      className="slider"
    />
  );
};

export default ThresholdSlider;
