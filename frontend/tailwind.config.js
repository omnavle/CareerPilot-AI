/** @type {import('tailwindcss').Config} */
export default {
  // Tells Tailwind which files to scan for class names, so it only
  // generates CSS for classes we actually use (keeps the CSS bundle small).
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
