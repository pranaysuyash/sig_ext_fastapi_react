// src/components/Common/Button.jsx
import React from 'react';

const Button = ({ type = 'button', children, className = '', ...props }) => {
  return (
    <button
      type={type}
      className={`bg-primary text-white px-4 py-2 rounded hover:bg-secondary transition-colors ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
