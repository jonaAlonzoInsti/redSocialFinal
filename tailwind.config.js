

/** @type {import('tailwindcss').Config} */
const color = require('tailwindcss/colors')
module.exports = {
  content: [
    './src/**/*.{html,ts}',
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'false',
  theme: {

    extend: {
      colors: {
        'light-blue': color.lightBlue,
        'cyan': color.cyan,
        'teal': color.teal,
        'emerald': color.emerald,
        'lime': color.lime,
        'amber': color.amber,
        'orange': color.orange,
        'red': color.red,
        'pink': color.pink,
        'purple': color.purple,
        'indigo': color.indigo,
        'blue': color.blue,
        'green': color.green,
        'yellow': color.yellow,
        'gray': color.gray,
        'true-gray': color.trueGray,
        'warm-gray': color.warmGray,
        'cool-gray': color.coolGray,
        'blue-gray': color.blueGray,
        dark: {
          100: '#1a1a1a',
          200: '#333333',
          300: '#4d4d4d',
          400: '#666666',
          500: '#808080',
          600: '#999999',
          700: '#b3b3b3',
          800: '#cccccc',
          900: '#e6e6e6',
        },
      },
    },

  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/line-clamp'),
    require('@tailwind base'),
    require('@tailwind components'),
    require('@tailwind utilities'),
    require('tailwind-scrollbar-hide'),


  ],
}

