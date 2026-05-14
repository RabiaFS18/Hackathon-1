# Technical Book RAG Chatbot - Backend

FastAPI backend service providing RAG (Retrieval-Augmented Generation) capabilities for querying technical book content.

## Features

- **Full Book Query Mode**: Search across entire book content using vector similarity
- **Selected Text Mode**: Query specific text passages with strict context isolation
- **Vector Database Integration**: Qdrant Cloud for efficient semantic search
- **OpenAI Integration**: Embeddings and chat completion for intelligent answers
- **Robust Error Handling**: Retry logic, logging, and user-friendly error messages

## Prerequisites

- Python 3.10 or higher
- OpenAI API account and API key
- Qdrant Cloud account and cluster (free tier available)

## Setup Instructions

### 1. Clone and Navigate

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your credentials:
# - OPENAI_API_KEY: Get from https://platform.openai.com/api-keys
# - QDRANT_URL: Your Qdrant Cloud cluster URL
# - QDRANT_API_KEY: Your Qdrant Cloud API key
```

**Required Variables:**
- `OPENAI_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`

**Optional Variables** (have defaults):
- `OPENAI_EMBEDDING_MODEL` (default: text-embedding-3-small)
- `OPENAI_CHAT_MODEL` (default: gpt-3.5-turbo)
- `OPENAI_TEMPERATURE` (default: 0.7)
- `OPENAI_MAX_TOKENS` (default: 4096)
- `QDRANT_COLLECTION_NAME` (default: book_chunks)
- `CHUNK_SIZE` (default: 512)
- `CHUNK_OVERLAP` (default: 50)
- `TOP_K_RESULTS` (default: 5)
- `MAX_RETRIES` (default: 3)
- `RETRY_BACKOFF_FACTOR` (default: 2.0)
- `LOG_LEVEL` (default: INFO)

### 5. Initialize Vector Database

```bash
# Create the Qdrant collection
python scripts/init_db.py
```

### 6. Ingest Book Content

```bash
# Run the ingestion script to populate the vector database
python scripts/ingest.py --book-dir /path/to/book/content
```

### 7. Run the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /query/full

Query the entire book using vector search.

**Request:**
```json
{
  "question": "What is dependency injection?"
}
```

**Response:**
```json
{
  "answer": "Dependency injection is a design pattern...",
  "sources": [
    {
      "chapter": "Chapter 5",
      "section": "Design Patterns",
      "page": 42,
      "text_snippet": "Dependency injection allows..."
    }
  ],
  "mode": "full_book"
}
```

### POST /query/selected

Query specific selected text without vector search.

**Request:**
```json
{
  "question": "Explain this concept",
  "selected_text": "Dependency injection is a technique..."
}
```

**Response:**
```json
{
  "answer": "This concept refers to...",
  "mode": "selected_text"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "vector_db": "connected",
    "openai": "available"
  }
}
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── models/              # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── requests.py
│   │   └── responses.py
│   ├── services/            # Business logic services
│   │   ├── __init__.py
│   │   ├── rag_engine.py    # RAG orchestration
│   │   ├── vector_store.py  # Qdrant client wrapper
│   │   ├── embedding.py     # OpenAI embedding service
│   │   └── llm.py           # OpenAI LLM service
│   ├── api/                 # API routes and dependencies
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── dependencies.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── logging.py       # Logging configuration
│       ├── errors.py        # Custom exceptions
│       └── retry.py         # Retry logic
├── scripts/
│   ├── __init__.py
│   ├── init_db.py           # Database initialization
│   └── ingest.py            # Content ingestion
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_rag_engine.py
│   └── test_services.py
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── Dockerfile               # Container definition
└── README.md                # This file
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py

# Run property-based tests
pytest tests/ -k property
```

## Development

### Code Style

This project follows PEP 8 style guidelines. Format code with:

```bash
# Install development dependencies
pip install black isort flake8

# Format code
black app/ tests/
isort app/ tests/

# Check style
flake8 app/ tests/
```

### Adding New Features

1. Update data models in `app/models/`
2. Implement business logic in `app/services/`
3. Add API endpoints in `app/api/routes.py`
4. Write tests in `tests/`
5. Update this README

## Deployment

See the main project README for deployment instructions to:
- Render (recommended for backend)
- Railway
- Fly.io
- Docker container

## Troubleshooting

### "Missing required environment variable"

Ensure all required variables are set in your `.env` file:
- `OPENAI_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`

### "Vector database connection failed"

- Verify your Qdrant Cloud cluster is running
- Check that `QDRANT_URL` and `QDRANT_API_KEY` are correct
- Ensure your IP is not blocked by Qdrant Cloud firewall

### "OpenAI API rate limit exceeded"

- The system will automatically retry with exponential backoff
- Consider upgrading your OpenAI API tier
- Reduce `TOP_K_RESULTS` to minimize token usage

### "Ingestion script fails"

- Check that book content files are valid markdown
- Ensure sufficient Qdrant Cloud storage (free tier: 1GB)
- Review logs for specific error messages

## Cost Estimation

### OpenAI API Costs (approximate)

- **Embeddings**: $0.00002 per 1K tokens (text-embedding-3-small)
  - 100K tokens of book content ≈ $0.002
- **Chat Completion**: $0.0005 per 1K tokens (gpt-3.5-turbo input)
  - 100 queries with 5 chunks each ≈ $0.25

### Qdrant Cloud

- Free tier: 1GB storage (sufficient for ~500K embeddings)

### Total Monthly Cost

- Light usage (100 queries/month): < $1
- Medium usage (1000 queries/month): $5-10
- Heavy usage (10K queries/month): $50-100

## License

See the main project LICENSE file.

## Support

For issues and questions, please open an issue on the project repository.
