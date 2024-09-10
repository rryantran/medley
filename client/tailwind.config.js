/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    fontFamily: { sans: ["Trebuchet MS", "sans-serif"] },
    colors: {
      white: "#ffffff",
      black: "#000000",
      silver: "#c0c0c0",
      pink: "#ffc0cb",
      darkpink: "#ffaeb9",
    },
    extend: {},
  },
  plugins: [],
};
