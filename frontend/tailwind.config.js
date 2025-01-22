module.exports = {
  content: [
    "./app.vue",
    "./pages/**/*.{vue,js,ts}",
    "./components/**/*.{vue,js,ts}",
    "./node_modules/quasar/dist/**/*.js", // Quasar-Komponenten
  ],
  theme: {
    extend: {
      colors: {
        primary: "#4CAF50",
        secondary: "#FF9800",
      },
    },
  },
  plugins: [],
};
