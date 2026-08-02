# MultiDocChat

MultiDocChat is a lightweight document Q&A application built with FastAPI and LangChain. Users can upload one or more documents, index them with a FAISS vector store, and then ask questions about the uploaded content in natural language.

The app is designed for local experimentation and small internal deployments, with conversational retrieval built on top of an LLM and semantic document search.

## Features

- Upload multiple documents in supported formats
  - PDF
  - DOCX
  - TXT
- Automatic document parsing and chunking
- Embedding-based semantic search using FAISS
- MMR retriever configuration for diverse search results
- Conversation-aware question answering with chat history
- Simple web UI for document upload and chat
- REST API endpoints for integration
- Docker support for containerized deployment

## Tech Stack

- Python 3.12+
- FastAPI
- LangChain / LangChain Core / LangChain Community
- FAISS
- Google Generative AI / Groq / OpenAI models
- Jinja2 + static HTML frontend
- Docker

## Project Structure

```text
.
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project metadata / packaging config
├── Dockerfile                  # Container build instructions
├── data/                       # Temporary uploaded documents
├── faiss_index/                # Session-specific FAISS indexes
├── static/                     # Static frontend assets
├── templates/
│   └── index.html              # Web UI
├── multi_doc_chat/
│   ├── config/
│   │   └── congif.yaml         # Model and retrieval config
│   ├── exception/
│   ├── logger/
│   ├── model/
│   ├── prompts/
│   ├── src/
│   │   ├── document_chat/
│   │   └── document_ingestion/
│   └── utils/
├── notebook/
│   ├── data_ingestion.ipynb
│   ├── experiments.ipynb
│   └── rag.ipynb
└── README.md
```

## How It Works

1. A user uploads one or more documents through the web UI or API.
2. Files are saved to a session-specific folder under `data/`.
3. Documents are loaded and split into chunks.
4. Chunks are embedded and stored in a FAISS vector database.
5. A user prompt is used to retrieve relevant chunks from the index.
6. The LLM answers using the retrieved context along with prior chat history.

## Prerequisites

- Python 3.12 or newer
- A working virtual environment
- At least one supported LLM provider API key:
  - `GOOGLE_API_KEY`
  - `OPENAI_API_KEY`
  - `GROQ_API_KEY`
- Optional: Docker if you want containerized deployment

## Environment Setup

Create a `.env` file in the project root with the required keys:

```env
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
LLM_PROVIDER=google
ENV=local
```

The app also loads configuration from `multi_doc_chat/config/congif.yaml` by default. If you are using the repo as-is, check that this file exists and has the correct structure. The project currently includes a file named `congif.yaml`, which is a misspelling of `config.yaml`; if your environment expects `config.yaml`, rename it accordingly.

## Configuration

The main model and retrieval settings live in the config file.

Example:

```yaml
embedding_model:
  provider: "google"
  model_name: "models/text-embedding-004"

retriever:
  top_k: 10
  search_type: "mmr"
  fetch_k: 20
  lambda_mult: 0.5

llm:
  google:
    provider: "google"
    model_name: "gemini-2.0-flash"
    temperature: 0
    max_output_tokens: 2048
```

You can switch providers using the `LLM_PROVIDER` environment variable.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

Start the FastAPI app:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

```text
http://localhost:8000
```

The homepage serves a simple web interface where you can:

- upload documents
- wait for indexing to complete
- ask questions in the chat box

## API Endpoints

### Health check

```http
GET /health
```

Returns:

```json
{"status": "ok"}
```

### Upload documents

```http
POST /upload
```

- Form field: `files`
- Accepts multiple uploaded files
- Returns a `session_id` and indexing status

### Chat with uploaded documents

```http
POST /chat
```

Request body:

```json
{
  "session_id": "session_20260802_abc12345",
  "message": "Summarize the main points in these documents."
}
```

Response:

```json
{
  "answer": "Here is a summary ..."
}
```

## Docker

Build the image:

```bash
docker build -t multidoctchat .
```

Run the container:

```bash
docker run -p 8080:8080 --env-file .env multidoctchat
```

The Dockerfile exposes port `8080` and launches the FastAPI app via uvicorn.

## Notes

- Uploaded documents are indexed per session and kept in local directories.
- FAISS indexes are stored under `faiss_index/`.
- The app uses in-memory chat history for the active session.
- This project is a good base for internal document assistants, research copilots, and retrieval-augmented QA prototypes.

## License

This project does not currently include a license file. If you are distributing or deploying it publicly, add an appropriate open-source license before release.

## Next Ideas

- Add authentication and user management
- Support more file types and OCR for scanned PDFs
- Persist chat history in a database
- Add evaluation and testing for retrieval quality
- Containerize with a production WSGI setup and secure secret management
