/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        cricket: {
          green: "#1a6b35",
          pitch: "#c8a96e",
          live: "#dc2626",
          accent: "#f59e0b",
        },
      },
    },
  },
  plugins: [],
};
