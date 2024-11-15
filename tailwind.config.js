// tailwind.config.js

/** @type {import('tailwindcss').Config} */
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1E3A8A',    // Custom primary color
        secondary: '#F59E0B',  // Custom secondary color
        link: '#646cff',       // Link color
        linkHover: '#535bf2',  // Link hover color
        bodyBg: '#242424',     // Default dark background
        bodyText: 'rgba(255, 255, 255, 0.87)', // Default dark text
        lightBodyBg: '#ffffff', // Light mode background
        lightBodyText: '#213547', // Light mode text
        lightLinkHover: '#747bff', // Light mode link hover
        lightButtonBg: '#f9f9f9', // Light mode button background
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'Avenir', 'Helvetica', 'Arial', 'sans-serif'],
      },
      fontSize: {
        '3xl': '3.2em', // Custom h1 size
      },
      borderRadius: {
        'xl': '8px', // Custom border radius for buttons
      },
      spacing: {
        '0.6em': '0.6em',
        '1.2em': '1.2em',
      },
    },
  },
  plugins: [
    forms,      // Use import statements for plugins
    typography, // Use import statements for plugins
  ],
};
