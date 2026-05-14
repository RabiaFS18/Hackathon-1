# Implementation Plan: Technical Book RAG Chatbot

## Overview

This implementation plan breaks down the Technical Book RAG Chatbot into discrete, implementable tasks. The system consists of a FastAPI backend with RAG capabilities and a Docusaurus frontend with chat integration. Tasks are organized to build incrementally, with early validation through testing and checkpoints.

The implementation uses Python/FastAPI for the backend and TypeScript/React for the Docusaurus frontend. All tasks reference specific requirements for traceability.

## Tasks

- [ ] 1. Backend project structure and configuration
  - [x] 1.1 Create backend folder structure and core files
    - Create `backend/` directory with subdirectories: `app/`, `scripts/`, `tests/`
    - Create `app/` subdirectories: `models/`, `services/`, `api/`, `utils/`
    - Create `__init__.py` files in all Python packages
    - Create `requirements.txt` with pinned versions: fastapi, uvicorn, pydantic, openai, qdrant-client, python-dotenv, tiktoken
    - Create `.env.example` with all required environment variables
    - Create `backend/README.md` with setup instructions
    - _Requirements: 10.2, 10.4, 14.1, 14.2, 14.3_

  - [-] 1.2 Implement configuration management
    - Create `app/config.py` with Pydantic Settings class
    - Define all configuration fields: OpenAI (API key, models, temperature, max tokens), Qdrant (URL, API key, collection name), RAG (chunk size, overlap, top-k), retry (max retries, backoff factor), logging (log level)
    - Implement validation for required environment variables
    - Implement default values for optional parameters
    - Add startup validation that fails with clear error messages for missing required variables
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

  - [ ]* 1.3 Write property test for configuration validation
    - **Property 21: Required Configuration Validation**
    - **Validates: Requirements 14.4**
    - Test that missing OPENAI_API_KEY, QDRANT_URL, or QDRANT_API_KEY causes startup failure with specific error message

  - [ ]* 1.4 Write property test for optional configuration defaults
    - **Property 22: Optional Configuration Defaults**
    - **Validates: Requirements 14.5**
    - Test that optional parameters use predefined defaults when environment variables are not set

- [ ] 2. Logging and error handling infrastructure
  - [ ] 2.1 Implement logging configuration
    - Create `app/utils/logging.py` with structured JSON logging setup
    - Configure log levels: DEBUG, INFO, WARNING, ERROR
    - Implement log formatters with timestamp, level, service, message, context fields
    - Add request/response logging middleware
    - _Requirements: 12.1, 12.2, 12.3, 12.4_

  - [ ] 2.2 Implement custom exception classes
    - Create `app/utils/errors.py` with custom exceptions: VectorDBError, EmbeddingServiceError, LLMServiceError, ValidationError
    - Each exception should include user-friendly messages without internal details
    - _Requirements: 12.5_

  - [ ] 2.3 Implement retry logic with exponential backoff
    - Create `app/utils/retry.py` with retry decorator
    - Implement exponential backoff: initial delay 1s, backoff factor 2.0, max retries 3
    - Add logging for retry attempts
    - Handle rate limit errors specifically
    - _Requirements: 6.5, 7.5_

  - [ ]* 2.4 Write unit tests for retry logic
    - Test successful retry after transient failure
    - Test max retries exhaustion
    - Test exponential backoff timing
    - _Requirements: 6.5, 7.5_

  - [ ]* 2.5 Write property test for error logging completeness
    - **Property 17: Error Logging Completeness**
    - **Validates: Requirements 12.1**
    - Test that any error creates log entry with timestamp, severity, and stack trace

  - [ ]* 2.6 Write property test for request logging
    - **Property 19: Request Logging**
    - **Validates: Requirements 12.3**
    - Test that any HTTP request creates log entry with method, path, and status code

- [ ] 3. Data models and validation
  - [ ] 3.1 Implement request models
    - Create `app/models/requests.py` with Pydantic models
    - Implement FullQueryRequest: question field (1-1000 chars, required, non-empty)
    - Implement SelectedQueryRequest: question field (1-1000 chars) and selected_text field (1-10000 chars)
    - Add validators to strip whitespace and reject empty strings
    - _Requirements: 3.2, 4.2, 13.1, 13.2, 13.3, 13.4_

  - [ ] 3.2 Implement response models
    - Create `app/models/responses.py` with Pydantic models
    - Implement Source model: chapter, section, page, text_snippet fields
    - Implement FullQueryResponse: answer, sources list, mode="full_book"
    - Implement SelectedQueryResponse: answer, mode="selected_text"
    - Implement ErrorResponse: error, optional detail
    - Implement HealthResponse: status, services dict
    - _Requirements: 2.3, 3.5, 4.6_

  - [ ]* 3.3 Write property test for length validation
    - **Property 3: Length Validation**
    - **Validates: Requirements 13.3, 13.4**
    - Test that questions > 1000 chars or selected_text > 10000 chars return HTTP 400

  - [ ]* 3.4 Write property test for invalid request rejection
    - **Property 2: Invalid Request Rejection**
    - **Validates: Requirements 2.4, 13.1, 13.2, 13.5**
    - Test that missing fields, empty values, or invalid formats return HTTP 400 with error details

- [ ] 4. Vector database service
  - [ ] 4.1 Implement Qdrant client wrapper
    - Create `app/services/vector_store.py` with VectorStore class
    - Implement connection to Qdrant Cloud using URL and API key from config
    - Implement collection creation with cosine similarity, dimension 1536, HNSW index (M=16, ef_construct=100)
    - Implement health check method
    - Add connection error handling with custom VectorDBError
    - _Requirements: 5.1, 5.5_

  - [ ] 4.2 Implement vector search method
    - Add search method: accepts query vector, returns top-k results with scores
    - Results should include payload metadata: chunk_id, text, chapter, section, page, token_count, book_title, created_at
    - Implement ranking by cosine similarity in descending order
    - Add performance logging for searches > 3 seconds
    - _Requirements: 5.3, 5.4, 15.3_

  - [ ] 4.3 Implement vector storage method
    - Add upsert method: accepts vectors with payload metadata
    - Support batch uploads for efficiency
    - Validate metadata completeness before storage
    - Add error handling for storage failures
    - _Requirements: 5.2, 6.4_

  - [ ]* 4.4 Write unit tests for vector store
    - Test connection establishment
    - Test collection creation
    - Test search with mock results
    - Test storage with metadata
    - Test error handling for unreachable database

  - [ ]* 4.5 Write property test for vector search ranking
    - **Property 10: Vector Search Ranking**
    - **Validates: Requirements 5.3**
    - Test that returned chunks are ordered by cosine similarity descending

  - [ ]* 4.6 Write property test for embedding storage with metadata
    - **Property 9: Embedding Storage with Metadata**
    - **Validates: Requirements 5.2, 6.4**
    - Test that stored embeddings are retrievable with complete metadata

- [ ] 5. Checkpoint - Verify configuration and infrastructure
  - Ensure all tests pass, verify configuration loads correctly, check logging works
  - Ask the user if questions arise

- [ ] 6. OpenAI embedding service
  - [ ] 6.1 Implement embedding generation service
    - Create `app/services/embedding.py` with EmbeddingService class
    - Implement generate_embedding method using OpenAI text-embedding-3-small
    - Add retry logic with exponential backoff for rate limits
    - Implement batch embedding generation (up to 100 texts per batch)
    - Add error handling with custom EmbeddingServiceError
    - Log service failures with service name and reason
    - _Requirements: 6.1, 6.3, 6.5, 12.2_

  - [ ] 6.2 Implement token counting utility
    - Add token counting using tiktoken library
    - Support counting for text-embedding-3-small model
    - _Requirements: 6.2, 7.6_

  - [ ]* 6.3 Write unit tests for embedding service
    - Test single embedding generation
    - Test batch embedding generation
    - Test retry on rate limit
    - Test error handling for API failures

  - [ ]* 6.4 Write property test for embedding generation completeness
    - **Property 12: Embedding Generation Completeness**
    - **Validates: Requirements 6.3**
    - Test that any chunk creates a vector embedding that gets stored

- [ ] 7. OpenAI LLM service
  - [ ] 7.1 Implement LLM answer generation service
    - Create `app/services/llm.py` with LLMService class
    - Implement generate_answer method using OpenAI gpt-3.5-turbo
    - Accept context and question as parameters
    - Implement prompt templates for full book mode and selected text mode
    - Add retry logic with exponential backoff for rate limits
    - Add performance logging for calls > 8 seconds
    - Add error handling with custom LLMServiceError
    - Log service failures with service name and reason
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 12.2, 15.4_

  - [ ] 7.2 Implement context truncation
    - Add method to truncate context to fit within 4096 token limit
    - Preserve chunk boundaries (don't split mid-chunk)
    - Truncate from end if context exceeds limit
    - _Requirements: 7.6_

  - [ ]* 7.3 Write unit tests for LLM service
    - Test answer generation with mock API
    - Test prompt construction for both modes
    - Test context truncation
    - Test retry on rate limit
    - Test error handling for API failures

  - [ ]* 7.4 Write property test for prompt context inclusion
    - **Property 13: Prompt Context Inclusion**
    - **Validates: Requirements 7.2, 7.3**
    - Test that prompts include both retrieved chunks and user question

  - [ ]* 7.5 Write property test for context token limit
    - **Property 14: Context Token Limit**
    - **Validates: Requirements 7.6**
    - Test that context provided to LLM never exceeds 4096 tokens

- [ ] 8. RAG engine orchestration
  - [ ] 8.1 Implement RAG engine core class
    - Create `app/services/rag_engine.py` with RAGEngine class
    - Initialize with dependencies: VectorStore, EmbeddingService, LLMService, Config
    - Create separate methods for full book mode and selected text mode
    - Ensure no shared state between modes
    - _Requirements: 8.4_

  - [ ] 8.2 Implement full book query processing
    - Add process_full_query method: accepts question string
    - Generate query embedding using EmbeddingService
    - Search VectorStore for top-k similar chunks
    - Extract and format retrieved chunks with metadata
    - Build context window from retrieved chunks
    - Generate answer using LLMService with context and question
    - Return answer with source references (chapter, section, page, text_snippet)
    - _Requirements: 3.3, 3.4, 3.5_

  - [ ] 8.3 Implement selected text query processing
    - Add process_selected_query method: accepts question and selected_text
    - Do NOT access VectorStore or generate embeddings
    - Use only selected_text as context
    - Generate answer using LLMService with selected_text and question
    - Return answer without source references
    - _Requirements: 4.3, 4.4, 4.5, 8.1, 8.2_

  - [ ]* 8.4 Write unit tests for RAG engine
    - Test full query flow with mocked services
    - Test selected query flow with mocked services
    - Test mode isolation (no vector search in selected mode)
    - Test error propagation from services

  - [ ]* 8.5 Write property test for full query vector search
    - **Property 4: Full Query Vector Search**
    - **Validates: Requirements 3.3, 3.4**
    - Test that any valid /query/full request performs vector search before generating answer

  - [ ]* 8.6 Write property test for selected text mode isolation
    - **Property 6: Selected Text Mode Isolation**
    - **Validates: Requirements 4.3, 4.4, 8.1, 8.2**
    - Test that /query/selected uses only provided text and never accesses vector database

  - [ ]* 8.7 Write property test for full mode isolation
    - **Property 8: Full Mode Isolation**
    - **Validates: Requirements 8.3**
    - Test that /query/full never uses user-provided selected text

- [ ] 9. Checkpoint - Verify core services
  - Ensure all service tests pass, verify RAG engine orchestration works correctly
  - Ask the user if questions arise

- [ ] 10. API endpoints implementation
  - [ ] 10.1 Implement FastAPI application setup
    - Create `app/main.py` with FastAPI app instance
    - Add CORS middleware for frontend domain
    - Add request/response logging middleware
    - Add startup event to validate configuration and initialize services
    - Add shutdown event for cleanup
    - _Requirements: 2.1_

  - [ ] 10.2 Implement dependency injection
    - Create `app/api/dependencies.py` with dependency functions
    - Implement get_rag_engine dependency that returns initialized RAGEngine
    - Implement get_config dependency
    - _Requirements: 2.1_

  - [ ] 10.3 Implement POST /query/full endpoint
    - Create `app/api/routes.py` with router
    - Implement POST /query/full endpoint accepting FullQueryRequest
    - Call RAGEngine.process_full_query
    - Return FullQueryResponse with answer and sources
    - Handle errors and return appropriate HTTP status codes (400, 500, 503)
    - _Requirements: 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.5_

  - [ ] 10.4 Implement POST /query/selected endpoint
    - Implement POST /query/selected endpoint accepting SelectedQueryRequest
    - Call RAGEngine.process_selected_query
    - Return SelectedQueryResponse with answer
    - Handle errors and return appropriate HTTP status codes (400, 500)
    - _Requirements: 2.2, 2.3, 2.4, 2.5, 4.1, 4.2, 4.6_

  - [ ] 10.5 Implement GET /health endpoint
    - Implement GET /health endpoint
    - Check VectorStore connection status
    - Check OpenAI API availability (lightweight check)
    - Return HealthResponse with status and service states
    - _Requirements: 2.1_

  - [ ]* 10.6 Write integration tests for API endpoints
    - Test /query/full with valid request
    - Test /query/selected with valid request
    - Test /health endpoint
    - Test error responses for invalid requests
    - Test error responses for service failures

  - [ ]* 10.7 Write property test for JSON response format
    - **Property 1: JSON Response Format**
    - **Validates: Requirements 2.3**
    - Test that any valid API request returns parseable JSON

  - [ ]* 10.8 Write property test for full query response structure
    - **Property 5: Full Query Response Structure**
    - **Validates: Requirements 3.5**
    - Test that successful /query/full returns answer and sources array with required fields

  - [ ]* 10.9 Write property test for selected query response structure
    - **Property 7: Selected Query Response Structure**
    - **Validates: Requirements 4.6**
    - Test that successful /query/selected returns answer and mode="selected_text"

  - [ ]* 10.10 Write property test for user-friendly error messages
    - **Property 20: User-Friendly Error Messages**
    - **Validates: Requirements 12.5**
    - Test that error responses contain user-friendly messages without internal details

- [ ] 11. Content ingestion script
  - [ ] 11.1 Implement content parsing
    - Create `scripts/ingest.py` with ingestion script
    - Implement markdown file parsing preserving structure
    - Extract chapter, section, page metadata from file structure and frontmatter
    - _Requirements: 11.1, 11.2_

  - [ ] 11.2 Implement chunking strategy
    - Implement text splitting: split on section boundaries first, then paragraphs, then sentences
    - Enforce maximum chunk size of 512 tokens
    - Implement 50-token overlap between chunks
    - Attach metadata (chapter, section, page, book_title, created_at) to each chunk
    - _Requirements: 6.2, 11.2_

  - [ ] 11.3 Implement batch embedding and storage
    - Generate embeddings for chunks in batches of 100
    - Store embeddings with metadata in VectorStore
    - Implement error resilience: log errors and continue processing remaining chunks
    - Add progress logging
    - Support incremental ingestion (skip already processed chunks)
    - _Requirements: 11.3, 11.4, 11.5, 11.6_

  - [ ] 11.4 Add CLI interface for ingestion script
    - Add command-line arguments: --book-dir, --collection, --incremental
    - Add help text and usage examples
    - _Requirements: 10.1, 10.5_

  - [ ]* 11.5 Write unit tests for ingestion
    - Test markdown parsing
    - Test chunking with various content sizes
    - Test metadata extraction
    - Test error resilience

  - [ ]* 11.6 Write property test for chunk size limit
    - **Property 11: Chunk Size Limit**
    - **Validates: Requirements 6.2**
    - Test that all generated chunks have token count ≤ 512

  - [ ]* 11.7 Write property test for ingestion parsing
    - **Property 15: Ingestion Parsing**
    - **Validates: Requirements 11.2**
    - Test that any book source file is parsed into structured chunks with valid metadata

  - [ ]* 11.8 Write property test for ingestion error resilience
    - **Property 16: Ingestion Error Resilience**
    - **Validates: Requirements 11.5**
    - Test that chunk failures are logged and processing continues

- [ ] 12. Checkpoint - Verify backend completeness
  - Ensure all backend tests pass, verify ingestion script works with sample content
  - Test API endpoints manually with curl or Postman
  - Ask the user if questions arise

- [ ] 13. Frontend project structure and configuration
  - [ ] 13.1 Create Docusaurus project
    - Create `frontend/` directory
    - Initialize Docusaurus project with TypeScript template
    - Create `package.json` with pinned versions: @docusaurus/core, @docusaurus/preset-classic, react, react-dom, typescript
    - Create `tsconfig.json` with strict TypeScript configuration
    - Create `frontend/README.md` with setup instructions
    - _Requirements: 1.1, 10.3_

  - [ ] 13.2 Configure Docusaurus
    - Create `docusaurus.config.js` with site metadata, theme configuration, navbar, footer
    - Create `sidebars.js` for book navigation structure
    - Configure code block syntax highlighting
    - Add custom CSS in `src/theme/custom.css`
    - _Requirements: 1.2, 1.3_

  - [ ] 13.3 Create TypeScript type definitions
    - Create `src/types/index.ts` with types for API requests/responses
    - Define FullQueryRequest, SelectedQueryRequest, FullQueryResponse, SelectedQueryResponse, ErrorResponse types
    - _Requirements: 2.2, 2.3_

- [ ] 14. Frontend API client
  - [ ] 14.1 Implement API service
    - Create `src/services/api.ts` with API client functions
    - Implement queryFull function: POST to /query/full
    - Implement querySelected function: POST to /query/selected
    - Implement checkHealth function: GET /health
    - Add error handling and response parsing
    - Use environment variable for backend API URL
    - _Requirements: 2.1, 2.2, 3.1, 4.1_

  - [ ]* 14.2 Write unit tests for API client
    - Test API calls with mocked fetch
    - Test error handling
    - Test request/response parsing

- [ ] 15. Chat widget component
  - [ ] 15.1 Implement chat state management hook
    - Create `src/hooks/useChat.ts` with custom hook
    - Manage chat state: messages array, loading state, error state
    - Implement sendMessage function that calls API service
    - Handle both full book and selected text modes
    - _Requirements: 3.1, 4.1_

  - [ ] 15.2 Implement chat message component
    - Create `src/components/ChatWidget/ChatMessage.tsx`
    - Display user questions and assistant answers
    - Display source references for full book mode
    - Add styling with CSS modules
    - _Requirements: 3.5_

  - [ ] 15.3 Implement chat input component
    - Create `src/components/ChatWidget/ChatInput.tsx`
    - Text input field for questions
    - Submit button
    - Loading indicator
    - Character count display (max 1000)
    - _Requirements: 13.3_

  - [ ] 15.4 Implement main chat widget component
    - Create `src/components/ChatWidget/index.tsx`
    - Compose ChatMessage and ChatInput components
    - Integrate useChat hook
    - Add mode toggle (full book vs selected text)
    - Add collapsible/expandable UI
    - Add styling with CSS modules
    - _Requirements: 1.1, 3.1, 4.1_

  - [ ]* 15.5 Write unit tests for chat components
    - Test message rendering
    - Test input handling
    - Test mode switching
    - Test error display

- [ ] 16. Text selection component
  - [ ] 16.1 Implement text selection hook
    - Create `src/hooks/useTextSelection.ts` with custom hook
    - Detect text selection on page
    - Extract selected text
    - Validate selection length (max 10000 chars)
    - _Requirements: 4.2, 13.4_

  - [ ] 16.2 Implement text selector component
    - Create `src/components/TextSelector/index.tsx`
    - Show floating button when text is selected
    - Open chat widget in selected text mode when clicked
    - Pass selected text to chat widget
    - Add styling with CSS modules
    - _Requirements: 4.1, 4.2_

  - [ ]* 16.3 Write unit tests for text selection
    - Test selection detection
    - Test text extraction
    - Test length validation
    - Test component interaction

- [ ] 17. Integrate components into Docusaurus
  - [ ] 17.1 Create Docusaurus plugin for chat widget
    - Add chat widget to all documentation pages
    - Ensure widget doesn't interfere with page content
    - Add text selector to all documentation pages
    - _Requirements: 1.1, 1.4_

  - [ ] 17.2 Add sample book content
    - Create `docs/` structure with sample chapters
    - Add intro.md with book introduction
    - Add chapter-01/ with sample sections
    - Test navigation and rendering
    - _Requirements: 1.1, 1.2_

  - [ ]* 17.3 Write end-to-end tests
    - Test full book query flow in browser
    - Test selected text query flow in browser
    - Test navigation between chapters
    - Test chat widget interaction

- [ ] 18. Checkpoint - Verify frontend completeness
  - Ensure all frontend tests pass, verify chat widget works in browser
  - Test text selection and query flows manually
  - Ask the user if questions arise

- [ ] 19. Deployment configuration
  - [ ] 19.1 Create backend Dockerfile
    - Create `backend/Dockerfile` with Python base image
    - Install dependencies from requirements.txt
    - Set up uvicorn command
    - Expose port
    - _Requirements: 9.2_

  - [ ] 19.2 Create deployment documentation
    - Document Vercel deployment for frontend
    - Document Render deployment for backend
    - Document Qdrant Cloud setup
    - Document OpenAI API setup
    - Document environment variable configuration
    - Add troubleshooting section
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 10.1, 10.4, 10.6_

  - [ ] 19.3 Create CI/CD pipeline
    - Create `.github/workflows/test.yml` for running tests on push
    - Create `.github/workflows/deploy.yml` for automated deployment
    - Add test job for backend (pytest)
    - Add test job for frontend (npm test)
    - Add deploy job for frontend (Vercel)
    - Add deploy job for backend (Render)
    - _Requirements: 10.6_

  - [ ] 19.4 Create database initialization script
    - Create `scripts/init_db.py` to create Qdrant collection
    - Add CLI arguments for collection configuration
    - Add verification step
    - _Requirements: 10.5_

- [ ] 20. Documentation and final integration
  - [ ] 20.1 Create comprehensive README
    - Add project overview and architecture diagram
    - Add prerequisites and dependencies
    - Add step-by-step setup instructions for local development
    - Add deployment instructions
    - Add usage examples
    - Add troubleshooting guide
    - Add cost estimation for OpenAI usage
    - _Requirements: 10.1, 10.6_

  - [ ] 20.2 Create environment variable templates
    - Ensure `.env.example` files are complete for both backend and frontend
    - Add comments explaining each variable
    - Add example values
    - _Requirements: 10.4_

  - [ ] 20.3 Add performance monitoring
    - Implement performance logging for vector searches > 3s
    - Implement performance logging for LLM calls > 8s
    - Add request timing middleware
    - _Requirements: 15.1, 15.2, 15.3, 15.4_

  - [ ]* 20.4 Write property test for performance warning logging
    - **Property 23: Performance Warning Logging**
    - **Validates: Requirements 15.3, 15.4**
    - Test that slow operations log performance warnings with operation type and duration

  - [ ]* 20.5 Write property test for service failure logging
    - **Property 18: Service Failure Logging**
    - **Validates: Requirements 12.2**
    - Test that external service failures log service name and failure reason

- [ ] 21. Final checkpoint and validation
  - Run complete test suite (unit tests and property tests)
  - Deploy to staging environment
  - Test end-to-end flows: full book query, selected text query, content ingestion
  - Verify all requirements are met
  - Verify deployment on free-tier infrastructure
  - Ask the user if questions arise or if ready for production deployment

## Notes

- Tasks marked with `*` are optional testing tasks and can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation and provide opportunities for user feedback
- Property tests validate universal correctness properties across all inputs
- Unit tests validate specific examples, edge cases, and integration points
- The implementation follows a bottom-up approach: infrastructure → services → orchestration → API → frontend
- All code should be production-ready with proper error handling, logging, and documentation
- Follow the design document specifications for all implementation details
