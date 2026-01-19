# Frontend (Vite + React) — Local preview

Quick steps to run the frontend locally:

1. cd frontend
2. npm install
3. npm run dev

By default the frontend expects the API under `/api` (development proxy). In `vite.config.js` the proxy is configured to **strip the `/api` prefix** so your client requests like `/api/auth/login` are forwarded to the backend path `/auth/login`:

```js
// vite.config.js
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        // rewrite removes the `/api` prefix when proxying to the backend
        rewrite: (path) => path.replace(/^\/api/, ''),
      }
    }
  }
});
```

The UI includes:
- `Login` — stores bearer token in `localStorage` (dev-only)
- `ReportForm` — submit a report payload to `/api/reports/submit`
- `ReportsList` — list reports (calls `/api/reports`)

Tip: If you're running the FastAPI backend locally on port 8000, either configure a proxy in `vite.config.js` or run:

    npm run dev -- --host 0.0.0.0 --port 5173

And access the UI at `http://localhost:5173`.
