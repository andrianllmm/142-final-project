# Astra Web

React/FastAPI dashboard for Astra, a CMSC 142 Python code similarity detector.
The web UI accepts Python `.py` submissions and calls the FastAPI backend,
which uses AST normalization and Damerau–Levenshtein sequence alignment.

## Project Context

- Group members: Andrian Lloyd Maagma, Dejel Cyrus De Asis, John Romyr Lopez
- Subject: CMSC 142
- Project title: Astra
- Type: Web / CLI hybrid tool
- Supported submissions: Python `.py` files only

The dashboard is intended for instructors reviewing small to medium programming
lab batches. It reports ranked similarity pairs, threshold flags, and
chunk-level evidence for manual validation.

## API

Run the FastAPI backend from this package:

```bash
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The analysis endpoint is available at:

```text
POST http://127.0.0.1:8000/analyze
```

## Frontend

Run the React/Vite UI:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173/
```

By default the frontend calls `/api/analyze`, and Vite proxies `/api` to
`http://127.0.0.1:8000`. To point the UI at a different backend URL, create
`frontend/.env.local`:

```bash
VITE_ASTRA_API_BASE=https://your-backend-url.example
```

## ngrok

Start the backend first, then start the Vite server in ngrok-friendly mode:

```bash
cd frontend
npm run dev:ngrok
```

Expose the frontend:

```bash
ngrok http 5173
```

Use the HTTPS forwarding URL from ngrok. The browser will call
`/api/analyze` through the Vite proxy, so the FastAPI backend stays local on
port `8000`.
