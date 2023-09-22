/** @type {import('tailwindcss').Config} */

const colors = require('tailwindcss/colors');
module.exports = {
  content: [
    './templates/**/*.html',
  './static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        violet: colors.violet
      },
      fontFamily: {
        'lato': ['Lato', 'san-serif']
      }
    },
  },
  plugins: [],
}
