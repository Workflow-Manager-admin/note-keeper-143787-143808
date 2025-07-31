# Notes Backend API

A FastAPI-based REST API for managing notes with full CRUD operations, built with Python and featuring in-memory storage with optional file persistence.

## Features

- ✅ **Full CRUD Operations**: Create, Read, Update, Delete notes
- ✅ **Data Validation**: Pydantic models for request/response validation
- ✅ **Search Functionality**: Search notes by title or content
- ✅ **Pagination**: Paginated note listing
- ✅ **Error Handling**: Comprehensive error handling with proper HTTP status codes
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- ✅ **CORS Support**: Cross-origin resource sharing enabled
- ✅ **Environment Configuration**: Environment-based configuration
- ✅ **Data Persistence**: Optional JSON file persistence for data storage

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Navigate to the notes_backend directory:
```bash
cd notes_backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

### Running the Application

#### Method 1: Using the run script
```bash
python run.py
```

#### Method 2: Using uvicorn directly
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Health Check
- `GET /` - Health check endpoint
- `GET /info` - API information

### Notes Management
- `POST /notes/` - Create a new note
- `GET /notes/` - Get all notes (with pagination)
- `GET /notes/{note_id}` - Get a specific note by ID
- `PUT /notes/{note_id}` - Update a note
- `DELETE /notes/{note_id}` - Delete a note
- `GET /notes/search?q={query}` - Search notes by title or content

## API Usage Examples

### Create a Note
```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Note",
    "content": "This is the content of my first note."
  }'
```

### Get All Notes
```bash
curl "http://localhost:8000/notes/?page=1&per_page=10"
```

### Get a Specific Note
```bash
curl "http://localhost:8000/notes/1"
```

### Update a Note
```bash
curl -X PUT "http://localhost:8000/notes/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Note Title",
    "content": "Updated content."
  }'
```

### Delete a Note
```bash
curl -X DELETE "http://localhost:8000/notes/1"
```

### Search Notes
```bash
curl "http://localhost:8000/notes/search?q=first"
```

## Data Models

### NoteCreate
```json
{
  "title": "string (required, 1-200 characters)",
  "content": "string (required)"
}
```

### NoteUpdate
```json
{
  "title": "string (optional, 1-200 characters)",
  "content": "string (optional)"
}
```

### NoteResponse
```json
{
  "id": "integer",
  "title": "string",
  "content": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Configuration

The application can be configured using environment variables. See `.env.example` for available options:

- `APP_NAME`: Application name (default: "Notes API")
- `APP_VERSION`: Application version (default: "1.0.0")
- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: 8000)
- `DEBUG`: Enable debug mode (default: false)
- `DATA_FILE`: Path to JSON file for data persistence (optional)
- `CORS_ORIGINS`: Allowed CORS origins (default: ["*"])

## Data Storage

By default, the application uses in-memory storage. To enable data persistence:

1. Set the `DATA_FILE` environment variable in your `.env` file:
```
DATA_FILE=data/notes.json
```

2. The application will automatically create the directory and file if they don't exist.

## Project Structure

```
notes_backend/
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py          # FastAPI app and entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── note.py          # Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   └── notes.py         # Notes API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── database.py      # Database service
│   └── config.py            # Configuration settings
├── interfaces/
│   └── openapi.json         # OpenAPI specification
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables example
├── run.py                  # Application startup script
└── README.md              # This file
```

## Development

### Running Tests
```bash
pytest
```

### Code Quality
The project includes flake8 for code linting:
```bash
flake8 src/
```

### Adding New Features
1. Create new models in `src/models/`
2. Add business logic to `src/services/`
3. Create API endpoints in `src/routers/`
4. Register new routers in `src/api/main.py`

## Docker Support

To run with Docker (if you have a Dockerfile):

```bash
docker build -t notes-api .
docker run -p 8000:8000 notes-api
```

## Production Deployment

For production deployment, consider:

1. **Environment Variables**: Set appropriate production values
2. **Database**: Use a proper database (PostgreSQL, MySQL) instead of in-memory storage
3. **Security**: Add authentication and authorization
4. **Monitoring**: Add logging and monitoring
5. **HTTPS**: Use HTTPS in production
6. **Process Management**: Use a process manager like systemd or supervisor

## Contributing

1. Follow PEP 8 coding standards
2. Add proper docstrings to all public functions
3. Include tests for new features
4. Update documentation as needed

## License

This project is licensed under the MIT License.
