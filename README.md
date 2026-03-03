# Dr. Silvério — Assistente de Fisiologia e Saúde

Assistente educativo virtual de fisiologia humana, baseado no livro Tortora (Principles of Anatomy and Physiology).

## Stack

- **Frontend**: Next.js 15 + Tailwind CSS
- **Backend**: Python FastAPI + Groq API (Llama 3.3 70B)
- **RAG**: Tortora PDF indexado com sentence-transformers

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # Editar com a tua GROQ_API_KEY
uvicorn app.main:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Abrir http://localhost:3000

### 3. RAG (opcional)

Para processar o PDF do Tortora:

```bash
cd backend
python scripts/index_tortora.py /caminho/para/tortora.pdf
```

## Endpoints

- `GET /api/health` — Health check
- `POST /api/chat` — Chat (non-streaming)
- `POST /api/chat/stream` — Chat (SSE streaming)

## Deploy

- **Frontend**: Vercel (auto-deploy)
- **Backend**: Railway (Dockerfile)

## Disclaimer

O Dr. Silvério é um assistente educativo. As informações fornecidas são de carácter educativo e informativo. Não substituem diagnóstico, tratamento ou aconselhamento médico profissional.
