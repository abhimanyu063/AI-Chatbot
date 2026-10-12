# RCIP React AI Assistant

Standalone React + TypeScript frontend preview. Uses mock responses by default. Does not integrate into Streamlit yet.

## Run

```bash
npm install
cp .env.example .env
npm run dev
```

## Connect FastAPI later

Set `VITE_USE_MOCK_API=false` in `.env` and implement `POST /api/v1/assistant/chat` returning `{ "answer": "...", "citations": [] }`. Request body includes `session_id`, `message`, `dashboard_context`. Configure backend CORS for the Vite origin.
