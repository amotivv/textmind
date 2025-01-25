# TextMind: AI-Powered SMS Chat Application

A Flask-based application that provides AI-powered SMS chat capabilities using ChromaDB for vector storage, with support for both OpenAI and local LLM models. The application processes incoming SMS messages via Telnyx, manages document storage, and provides intelligent responses based on stored knowledge.

## 🌟 Features

- 🤖 AI-powered SMS chat responses using OpenAI GPT-4 or local DeepSeek model
- 📚 Vector database storage using ChromaDB
- 📱 SMS integration via Telnyx
- 📄 Markdown file processing and chunked storage
- 🔍 Semantic search with distance-based filtering

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Telnyx account
- OpenAI API key or OLLAMA installation

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

The application runs on port 5000 in the container, mapped to port 5005 on the host.

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELNYX_API_KEY` | Telnyx API key | `key_xxx` |
| `TELNYX_FROM` | Sender phone number | `+18445550001` |
| `TELNYX_PROFILE_ID` | Telnyx messaging profile ID | `abc85f64-xxxx` |
| `LLM_API_URL` | URL for LLM inference | `http://localhost:11434/api/generate` |
| `USE_OPENAI` | Toggle between OpenAI and OLLAMA | `false` |
| `OPENAI_API_KEY` | OpenAI API key (if using OpenAI) | `sk-xxx` |

### Model Configuration

#### Local LLM Setup (Default)
```env
USE_OPENAI=false
LLM_API_URL=http://localhost:11434/api/generate
```

The application uses the DeepSeek-R1 7B model for local inference.

#### OpenAI Setup
```env
USE_OPENAI=true
OPENAI_API_KEY=your-api-key
```

When using OpenAI, the application uses the GPT-4 model.

## 🔌 API Documentation

### Endpoints

#### POST `/webhook`
Processes incoming SMS messages and generates AI responses.

**Request Body:**
```json
{
  "text": "Your question here",
  "from": "+1234567890"
}
```

**Response:**
```json
{
  "status": "success"
}
```

#### POST `/add_document`
Adds a document to the vector database.

**Request Body:**
```json
{
  "id": "doc1",
  "content": "Document content",
  "metadata": {
    "source_file": "example.md",
    "chunk_index": 1
  }
}
```

#### GET `/search_documents`
Searches documents using semantic similarity.

**Query Parameters:**
- `query` (required): Search query
- `top_k` (optional): Number of results (default: 5)
- `summarize` (optional): Summarize results (default: false)

**Response:**
```json
{
  "documents": ["..."],
  "distances": [0.1, 0.2],
  "metadata": [{...}],
  "summary": "Optional summary if requested"
}
```

#### DELETE `/delete_document`
Removes a document from the database.

**Query Parameters:**
- `id` (required): Document ID to delete

#### POST `/upload_markdown`
Processes and stores markdown files in chunks.

**Form Data:**
- `file`: Markdown file (max 10MB)

## 🔧 Advanced Configuration

### ChromaDB Settings

ChromaDB data is persisted using Docker volumes:
```yaml
volumes:
  - chroma_data:/app/chroma_data
```

### Document Processing

- Markdown files are automatically chunked (500 characters per chunk)
- Search results are filtered by distance threshold (150.0)
- Each document chunk includes metadata:
  - source_file
  - chunk_index
  - uploaded_at

## 🛠️ Development

### Local Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python webhook_receiver.py
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

For support, please open an issue in the GitHub repository.

## 🙏 Acknowledgments

- [Telnyx](https://telnyx.com/) for SMS capabilities
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [OLLAMA](https://ollama.ai/) for local AI models
- [OpenAI](https://openai.com/) for API services