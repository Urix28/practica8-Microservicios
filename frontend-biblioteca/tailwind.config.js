/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'ipn-guinda': '#6E1C32',
        'ipn-blanco': '#FFFFFF',
      }
    },
  },
  plugins: [],
}