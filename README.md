# AI-Powered SMS Chat Application

A Flask-based application that provides AI-powered SMS chat capabilities using ChromaDB for vector storage, with support for both OpenAI and OLLAMA models. The application can process incoming SMS messages via Telnyx, manage document storage, and provide intelligent responses based on stored knowledge.

## 📑 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Configuration](#️-configuration)
- [API Documentation](#-api-documentation)
- [Advanced Configuration](#-advanced-configuration)
- [Development](#️-development)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)
- [Acknowledgments](#-acknowledgments)

## 🌟 Features

- 🤖 AI-powered SMS chat responses
- 📚 Vector database storage using ChromaDB
- 📱 SMS integration via Telnyx
- 📄 Markdown file processing and storage
- 🔄 Flexible model selection (OpenAI or OLLAMA)
- 🔍 Semantic search capabilities

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Telnyx account (for SMS functionality)
- OLLAMA or OpenAI API access

### Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Create and configure your `.env` file:
```bash
cp .env.example .env
```

3. Start the application:
```bash
docker-compose up --build
```

The application will be available at `http://127.0.0.1:5005`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELNYX_API_KEY` | Telnyx API key | `key_xxx` |
| `TELNYX_FROM` | Sender phone number | `+18445550001` |
| `TELNYX_PROFILE_ID` | Telnyx messaging profile ID | `abc85f64-xxxx` |
| `EMBEDDING_API_URL` | URL for embeddings (OLLAMA/OpenAI) | `http://localhost:11434/api/embeddings` |
| `LLM_API_URL` | URL for LLM inference | `http://localhost:11434/api/generate` |
| `USE_OPENAI` | Toggle between OpenAI and OLLAMA | `false` |
| `OPENAI_API_KEY` | OpenAI API key (if using OpenAI) | `sk-xxx` |
| `OPENAI_TEMPERATURE` | Temperature setting for OpenAI | `0.7` |
| `OPENAI_MAX_TOKENS` | Max tokens for responses | `150` |
| `OPENAI_TOP_P` | Top p sampling parameter | `1` |

### Model Configuration

#### OLLAMA Setup

1. Install OLLAMA locally:
```bash
curl https://ollama.ai/install.sh | sh
```

2. Pull required models:
```bash
# For embeddings
ollama pull nomic-embed-text
# For LLM inference
ollama pull mistral
```

3. Configure environment variables for OLLAMA:
```env
EMBEDDING_API_URL=http://localhost:11434/api/embeddings
LLM_API_URL=http://localhost:11434/api/generate
USE_OPENAI=false
```

#### OpenAI Setup

1. Configure environment variables for OpenAI:
```env
USE_OPENAI=true
OPENAI_API_KEY=your-api-key
```

## 🔌 API Documentation

### Base URL
- Local Development: `http://127.0.0.1:5005`

### Endpoints Overview

1. **SMS Webhook**
   - `/webhook` (POST): Process incoming SMS messages
2. **Document Management**
   - `/add_document` (POST): Add documents to ChromaDB
   - `/search_documents` (GET): Search stored documents
   - `/delete_document` (DELETE): Remove documents
   - `/upload_markdown` (POST): Process and store Markdown files

### Detailed API Routes

#### 1. SMS Webhook Endpoint

##### POST `/webhook`
Process incoming SMS messages and generate AI responses.

**Request Body:**
```json
{
  "text": "How is Luminiv Vision Radar different?",
  "from": "+1234567890"
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | The SMS content received |
| `from` | string | Yes | Sender's phone number |

**Response:**
```json
{
  "status": "success"
}
```

#### 2. Document Management Endpoints

##### POST `/add_document`
Add a new document to the vector database.

**Request Body:**
```json
{
  "id": "doc1",
  "content": "This is a document about security solutions.",
  "metadata": {
    "source_file": "security.md",
    "chunk_index": 1,
    "uploaded_at": "2025-01-25T12:00:00Z"
  }
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Unique document identifier |
| `content` | string | Yes | Document content |
| `metadata` | object | No | Additional document metadata |

**Response:**
```json
{
  "message": "Document 'doc1' added successfully."
}
```

##### GET `/search_documents`
Search for documents using semantic similarity.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | Required | Search query text |
| `top_k` | integer | 3 | Number of results to return |
| `summarize` | boolean | false | Whether to summarize results |

**Example Request:**
```
GET /search_documents?query=How+luminiv+is+different?&top_k=3&summarize=true
```

**Response:**
```json
{
  "summary": "Luminiv Radar differs by using radar technology for intrusion detection...",
  "documents": [
    "This is document 1 text",
    "Another relevant document."
  ],
  "distances": [0.1234, 0.2345],
  "metadata": [
    {
      "chunk_index": 1,
      "source_file": "security.md"
    },
    {
      "chunk_index": 2,
      "source_file": "other.md"
    }
  ]
}
```

##### DELETE `/delete_document`
Remove a document from the vector database.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Document ID to delete |

**Response:**
```json
{
  "message": "Document 'doc1' deleted successfully."
}
```

##### POST `/upload_markdown`
Upload and process a Markdown file into the vector database.

**Form Data:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | file | Yes | Markdown file to upload |

**Example Request:**
```bash
curl -X POST http://127.0.0.1:5005/upload_markdown \
  -F "file=@example.md"
```

**Response:**
```json
{
  "message": "Markdown file 'example.md' uploaded and processed successfully.",
  "chunks_uploaded": 5
}
```

### API Error Responses

All endpoints may return the following error responses:

#### 400 Bad Request
```json
{
  "error": "Invalid request parameters",
  "details": "Specific error message"
}
```

#### 404 Not Found
```json
{
  "error": "Resource not found",
  "details": "The requested resource could not be found"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "details": "An unexpected error occurred"
}
```

### Rate Limiting

- Default rate limit: 100 requests per minute per IP
- Webhook endpoint: 200 requests per minute per IP

### API Versioning

The current API version is v1. All endpoints are prefixed with `/api/v1/` although this is optional in the current version.

## 🔧 Advanced Configuration

### ChromaDB Persistence

ChromaDB data is persisted using Docker volumes. Configure the storage location in `docker-compose.yml`:

```yaml
volumes:
  - chroma_data:/app/chroma_data
```

### Model Selection

#### OLLAMA Models

- **Embeddings**: 
  - Default: `nomic-embed-text`
  - Alternatives: `all-minilm`, `e5-large`

- **LLM Inference**:
  - Default: `mistral`
  - Alternatives: `llama2`, `codellama`, `neural-chat`

#### OpenAI Models

- **Embeddings**: 
  - Default: `text-embedding-ada-002`

- **LLM Inference**:
  - Default: `gpt-3.5-turbo`
  - Alternative: `gpt-4`

### Best Practices

1. **Document Management:**
   - Keep document chunks between 200-1000 tokens for optimal performance
   - Include relevant metadata for better document organization

2. **Search Optimization:**
   - Use specific, focused queries for better results
   - Start with default `top_k=3` and adjust based on needs

3. **Markdown Upload:**
   - Structure markdown files with clear headings and sections
   - Keep file sizes under 10MB for optimal processing

## 🛠️ Development

### Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
flask run --port 5005
```

### Testing

```bash
pytest tests/
```

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 🙏 Acknowledgments

- [Telnyx](https://telnyx.com/) for SMS capabilities
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [OLLAMA](https://ollama.ai/) for local AI models
- [OpenAI](https://openai.com/) for API services