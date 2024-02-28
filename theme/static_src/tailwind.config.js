
//importamos los colores de la paleta de colores
const colors = require('tailwindcss/colors')
const flowbitePlugin = require('flowbite/plugin');
//mode: "jit",

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      './templates/**/*.html',
      './node_modules/flowbite/**/*.js',
      './src/**/*.{html,ts}',
      './pages/**/*.{html,js}',
      './components/**/*.{html,js}',
   
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    darkMode:'false',
    theme: {
        extend: {
            'dark-main': '#18191A',
            'dark-second': '#242526',
            'dark-third': '#3A3B3C',
            'dark-fourth': '#4b5563',
            'dark-text': '#88BBFF',
            sky: colors.sky,
            teal: colors.teal,
            rose: colors.rose,
            purple: colors.purple,
        },
    },
    variants: {
        extend: {
            display: ['group-hover'],
            transform: ['group-hover'],
            scale: ['group-hover'],
            textOpacity: ['dark'],
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        flowbitePlugin,
        require('flowbite/plugin'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('tailwind-scrollbar-hide'),
        require('@tailwind base'),
        require('@tailwind components'),
        require('@tailwind utilities'),
    ],
}
