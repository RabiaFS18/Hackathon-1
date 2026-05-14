# Requirements Document

## Introduction

The Technical Book RAG Chatbot is a platform that hosts technical books as static content and provides an intelligent chatbot interface for querying book content. The system combines Docusaurus for content presentation with a FastAPI backend that uses RAG (Retrieval-Augmented Generation) to answer user questions. The platform supports two distinct query modes: full book retrieval using vector search, and selected text mode with strict context isolation.

## Glossary

- **Platform**: The complete Technical Book RAG Chatbot system including frontend and backend
- **Docusaurus_Frontend**: The static site generator hosting the technical book content
- **FastAPI_Backend**: The REST API server handling query processing and RAG operations
- **RAG_Engine**: The retrieval-augmented generation component combining vector search and LLM
- **Vector_Database**: The Qdrant Cloud instance storing document embeddings
- **Embedding_Service**: The OpenAI service generating vector embeddings from text
- **LLM_Service**: The OpenAI service generating natural language answers
- **Full_Book_Mode**: Query mode that searches across the entire book using vector similarity
- **Selected_Text_Mode**: Query mode that uses only user-provided text without vector search
- **Query_Endpoint**: REST API endpoint accepting user queries
- **Chunk**: A segmented portion of book content prepared for embedding
- **Context_Window**: The text provided to the LLM for answer generation
- **Deployment_Environment**: The infrastructure hosting the Platform components

## Requirements

### Requirement 1: Static Book Hosting

**User Story:** As a reader, I want to access technical book content through a web interface, so that I can read and navigate the material easily.

#### Acceptance Criteria

1. THE Docusaurus_Frontend SHALL serve technical book content as static HTML pages
2. THE Docusaurus_Frontend SHALL provide navigation between book chapters and sections
3. THE Docusaurus_Frontend SHALL render code examples with syntax highlighting
4. THE Docusaurus_Frontend SHALL be accessible via standard web browsers

### Requirement 2: Backend API Infrastructure

**User Story:** As a system integrator, I want a REST API backend, so that the frontend can communicate with the RAG system.

#### Acceptance Criteria

1. THE FastAPI_Backend SHALL expose REST API endpoints over HTTP
2. THE FastAPI_Backend SHALL accept JSON-formatted request payloads
3. THE FastAPI_Backend SHALL return JSON-formatted response payloads
4. WHEN an invalid request is received, THE FastAPI_Backend SHALL return an HTTP 400 status code with error details
5. WHEN an internal error occurs, THE FastAPI_Backend SHALL return an HTTP 500 status code with error details

### Requirement 3: Full Book Query Endpoint

**User Story:** As a reader, I want to ask questions about the entire book, so that I can find relevant information without manual searching.

#### Acceptance Criteria

1. THE FastAPI_Backend SHALL expose a POST endpoint at /query/full
2. WHEN a query is submitted to /query/full, THE FastAPI_Backend SHALL accept a JSON payload containing a question field
3. WHEN a query is submitted to /query/full, THE RAG_Engine SHALL retrieve relevant chunks from the Vector_Database
4. WHEN relevant chunks are retrieved, THE RAG_Engine SHALL generate an answer using the LLM_Service
5. THE FastAPI_Backend SHALL return a JSON response containing the generated answer and source references

### Requirement 4: Selected Text Query Endpoint

**User Story:** As a reader, I want to ask questions about specific text I select, so that I can get focused answers without interference from other book content.

#### Acceptance Criteria

1. THE FastAPI_Backend SHALL expose a POST endpoint at /query/selected
2. WHEN a query is submitted to /query/selected, THE FastAPI_Backend SHALL accept a JSON payload containing a question field and a selected_text field
3. WHEN a query is submitted to /query/selected, THE RAG_Engine SHALL use only the selected_text as context
4. WHEN processing /query/selected requests, THE RAG_Engine SHALL NOT perform vector database searches
5. WHEN processing /query/selected requests, THE RAG_Engine SHALL generate an answer using only the provided selected_text
6. THE FastAPI_Backend SHALL return a JSON response containing the generated answer

### Requirement 5: Vector Database Integration

**User Story:** As a system administrator, I want the system to use Qdrant Cloud for vector storage, so that embeddings are persisted and searchable.

#### Acceptance Criteria

1. THE FastAPI_Backend SHALL connect to a Qdrant Cloud instance using provided credentials
2. THE Vector_Database SHALL store document embeddings with associated metadata
3. WHEN the RAG_Engine performs a search, THE Vector_Database SHALL return the top-k most similar chunks based on cosine similarity
4. THE Vector_Database SHALL support filtering by metadata fields
5. WHEN the Vector_Database is unreachable, THE FastAPI_Backend SHALL return an HTTP 503 status code with error details

### Requirement 6: Embedding Generation

**User Story:** As a content processor, I want to generate embeddings for book content, so that semantic search can be performed.

#### Acceptance Criteria

1. THE Embedding_Service SHALL use OpenAI's embedding API to generate vector embeddings
2. WHEN book content is processed, THE Platform SHALL split content into chunks of maximum 512 tokens
3. WHEN a chunk is created, THE Embedding_Service SHALL generate a vector embedding for that chunk
4. THE Platform SHALL store each embedding in the Vector_Database with metadata including chapter, section, and page references
5. WHEN the Embedding_Service rate limit is exceeded, THE Platform SHALL retry with exponential backoff up to 3 attempts

### Requirement 7: Answer Generation

**User Story:** As a reader, I want to receive natural language answers to my questions, so that I can understand the book content more easily.

#### Acceptance Criteria

1. THE LLM_Service SHALL use OpenAI's chat completion API to generate answers
2. WHEN generating an answer, THE RAG_Engine SHALL provide retrieved chunks as context to the LLM_Service
3. WHEN generating an answer, THE RAG_Engine SHALL include the user's question in the prompt
4. THE LLM_Service SHALL generate answers that reference the provided context
5. WHEN the LLM_Service rate limit is exceeded, THE FastAPI_Backend SHALL retry with exponential backoff up to 3 attempts
6. WHEN the context exceeds the LLM token limit, THE RAG_Engine SHALL truncate context to fit within 4096 tokens

### Requirement 8: Mode Isolation

**User Story:** As a reader using Selected Text Mode, I want strict isolation from the full book content, so that answers are based only on my selected text.

#### Acceptance Criteria

1. WHEN processing a /query/selected request, THE RAG_Engine SHALL NOT access the Vector_Database
2. WHEN processing a /query/selected request, THE RAG_Engine SHALL NOT use any book content beyond the provided selected_text
3. WHEN processing a /query/full request, THE RAG_Engine SHALL NOT use any user-provided selected text
4. THE Platform SHALL maintain separate code paths for Full_Book_Mode and Selected_Text_Mode

### Requirement 9: Free-Tier Deployment

**User Story:** As a developer, I want to deploy the system on free-tier infrastructure, so that I can minimize operational costs.

#### Acceptance Criteria

1. THE Docusaurus_Frontend SHALL be deployable on platforms offering free static hosting
2. THE FastAPI_Backend SHALL be deployable on platforms offering free compute instances
3. THE Platform SHALL use Qdrant Cloud's free tier with a maximum of 1GB storage
4. THE Platform SHALL use OpenAI API with configurable rate limits to control costs
5. THE Deployment_Environment SHALL support deployment without requiring paid services

### Requirement 10: Setup Reproducibility

**User Story:** As a developer, I want reproducible setup instructions, so that I can deploy the system consistently across environments.

#### Acceptance Criteria

1. THE Platform SHALL include a README file with step-by-step setup instructions
2. THE Platform SHALL include a requirements.txt file listing all Python dependencies with pinned versions
3. THE Platform SHALL include a package.json file listing all Node.js dependencies with pinned versions
4. THE Platform SHALL include environment variable templates for configuration
5. THE Platform SHALL include scripts for initializing the Vector_Database with book content
6. WHEN following the setup instructions, a developer SHALL be able to deploy a working instance within 30 minutes

### Requirement 11: Content Ingestion

**User Story:** As a content administrator, I want to ingest book content into the vector database, so that the RAG system can retrieve relevant information.

#### Acceptance Criteria

1. THE Platform SHALL provide a content ingestion script that processes book source files
2. WHEN the ingestion script runs, THE Platform SHALL parse book content into structured chunks
3. WHEN the ingestion script runs, THE Platform SHALL generate embeddings for each chunk using the Embedding_Service
4. WHEN the ingestion script runs, THE Platform SHALL upload embeddings and metadata to the Vector_Database
5. WHEN ingestion fails for a chunk, THE Platform SHALL log the error and continue processing remaining chunks
6. THE Platform SHALL support incremental ingestion to update only modified content

### Requirement 12: Error Handling and Logging

**User Story:** As a system administrator, I want comprehensive error handling and logging, so that I can diagnose and resolve issues quickly.

#### Acceptance Criteria

1. WHEN an error occurs, THE FastAPI_Backend SHALL log the error with timestamp, severity level, and stack trace
2. WHEN an external service fails, THE FastAPI_Backend SHALL log the service name and failure reason
3. THE FastAPI_Backend SHALL log all incoming requests with method, path, and response status
4. THE Platform SHALL support configurable log levels (DEBUG, INFO, WARNING, ERROR)
5. WHEN a query fails, THE FastAPI_Backend SHALL return a user-friendly error message without exposing internal details

### Requirement 13: API Request Validation

**User Story:** As a backend developer, I want to validate API requests, so that invalid inputs are rejected before processing.

#### Acceptance Criteria

1. WHEN a request to /query/full is received, THE FastAPI_Backend SHALL validate that the question field is present and non-empty
2. WHEN a request to /query/selected is received, THE FastAPI_Backend SHALL validate that both question and selected_text fields are present and non-empty
3. WHEN a request contains a question exceeding 1000 characters, THE FastAPI_Backend SHALL return an HTTP 400 status code
4. WHEN a request to /query/selected contains selected_text exceeding 10000 characters, THE FastAPI_Backend SHALL return an HTTP 400 status code
5. WHEN validation fails, THE FastAPI_Backend SHALL return a JSON response describing which fields are invalid

### Requirement 14: Configuration Management

**User Story:** As a system administrator, I want to configure the system through environment variables, so that I can deploy to different environments without code changes.

#### Acceptance Criteria

1. THE Platform SHALL read OpenAI API credentials from environment variables
2. THE Platform SHALL read Qdrant Cloud connection details from environment variables
3. THE Platform SHALL read configurable parameters (chunk size, top-k results, temperature) from environment variables
4. WHEN a required environment variable is missing, THE FastAPI_Backend SHALL fail to start and log the missing variable name
5. THE Platform SHALL provide default values for optional configuration parameters

### Requirement 15: Response Time Performance

**User Story:** As a reader, I want to receive answers within a reasonable time, so that the chatbot feels responsive.

#### Acceptance Criteria

1. WHEN processing a /query/full request with cached embeddings, THE FastAPI_Backend SHALL return a response within 10 seconds under normal load
2. WHEN processing a /query/selected request, THE FastAPI_Backend SHALL return a response within 5 seconds under normal load
3. WHEN the Vector_Database search takes longer than 3 seconds, THE FastAPI_Backend SHALL log a performance warning
4. WHEN the LLM_Service takes longer than 8 seconds, THE FastAPI_Backend SHALL log a performance warning
