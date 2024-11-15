import React, { useState } from 'react';
import { SketchPicker } from 'react-color';

const ColorPicker = ({ onColorSelect }) => {
  const [color, setColor] = useState('#0000ff'); // Default color

  const handleColorChange = (newColor) => {
    setColor(newColor.hex);
    onColorSelect(newColor.hex);
  };

  return <SketchPicker color={color} onChangeComplete={handleColorChange} />;
};

export default ColorPicker;
