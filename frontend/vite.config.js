import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite's config file. Sets up the React plugin so JSX files work,
// and runs the dev server on port 5173 (the default that our backend's
// CORS setting in main.py already allows).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
})
