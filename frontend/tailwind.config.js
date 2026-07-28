/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        cricket: {
          green:  "#059669",
          dark:   "#064e3b",
          pitch:  "#c8a96e",
          live:   "#ef4444",
          accent: "#f59e0b",
          card:   "#0d1117",
          border: "#1f2937",
        },
      },
      backgroundImage: {
        "card-glow": "radial-gradient(ellipse at top left, rgba(5,150,105,0.08), transparent 60%)",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
    },
  },
  plugins: [],
};
