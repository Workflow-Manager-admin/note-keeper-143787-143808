# Notes API Deployment Guide

This guide covers deploying the Notes API in various environments.

## Local Development

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### Development with Auto-reload
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment Configuration

Create a `.env` file in the project root:

```env
# Application Settings
APP_NAME=Notes API
APP_VERSION=1.0.0
APP_DESCRIPTION=A REST API for managing notes with full CRUD operations

# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Database Settings (for file persistence)
DATA_FILE=data/notes.json

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

## Production Deployment

### Using Gunicorn (Recommended)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Create a Gunicorn configuration file (`gunicorn.conf.py`):
```python
# Gunicorn configuration
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

3. Run with Gunicorn:
```bash
gunicorn src.api.main:app -c gunicorn.conf.py
```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY run.py .
COPY .env.example .env

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]
```

Build and run:
```bash
docker build -t notes-api .
docker run -p 8000:8000 -v $(pwd)/data:/app/data notes-api
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  notes-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - DATA_FILE=data/notes.json
      - DEBUG=false
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## Cloud Deployment

### AWS ECS/Fargate

1. Push Docker image to ECR
2. Create ECS task definition
3. Deploy as ECS service
4. Use ALB for load balancing

### Google Cloud Run

```bash
# Build and deploy
gcloud run deploy notes-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name notes-api \
  --image notes-api:latest \
  --dns-name-label notes-api \
  --ports 8000
```

### Heroku

Create `Procfile`:
```
web: gunicorn src.api.main:app -c gunicorn.conf.py
```

Deploy:
```bash
heroku create your-notes-api
git push heroku main
```

## Database Migration

### From In-Memory to File Storage

1. Set `DATA_FILE` environment variable
2. Restart the application
3. Data will be persisted to the specified file

### From File to Database

For production, consider migrating to a proper database:

1. **PostgreSQL Example**:
```python
# Add to requirements.txt
asyncpg==0.29.0
sqlalchemy==2.0.23
alembic==1.12.1

# Update database service to use PostgreSQL
```

2. **Migration Script**:
```python
# migration_script.py
import json
import asyncpg
from src.services.database import db

async def migrate_to_postgres():
    # Export current data
    notes, _ = db.get_notes(limit=1000)
    
    # Connect to PostgreSQL
    conn = await asyncpg.connect("postgresql://user:pass@localhost/notes")
    
    # Create table and insert data
    # ... migration logic
```

## Monitoring and Logging

### Add Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Health Check Endpoint
The API includes health check endpoints:
- `GET /` - Basic health check
- `GET /info` - API information

### Metrics (Optional)
Add Prometheus metrics:
```bash
pip install prometheus-fastapi-instrumentator
```

## Security Considerations

### Production Security

1. **HTTPS**: Always use HTTPS in production
2. **Environment Variables**: Never commit secrets to version control
3. **CORS**: Configure specific origins, not `*`
4. **Rate Limiting**: Add rate limiting middleware
5. **Authentication**: Add JWT or OAuth2 authentication

### Example Security Middleware
```python
from fastapi import Security
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response
```

## Performance Optimization

### Caching
Add Redis caching for frequently accessed notes:
```python
import redis
r = redis.Redis(host='localhost', port=6379)
```

### Database Connection Pooling
Use connection pooling for database connections.

### Load Balancing
Use a load balancer (nginx, ALB, etc.) for multiple instances.

## Backup and Recovery

### File-based Storage
```bash
# Backup
cp data/notes.json backups/notes_$(date +%Y%m%d).json

# Restore
cp backups/notes_20240101.json data/notes.json
```

### Database Backup
```bash
# PostgreSQL example
pg_dump notes_db > backup.sql
```

## API Documentation

The API automatically generates documentation:
- **Swagger UI**: http://your-domain/docs
- **ReDoc**: http://your-domain/redoc
- **OpenAPI JSON**: http://your-domain/openapi.json

Update the OpenAPI spec:
```bash
python src/api/generate_openapi.py
```

## Troubleshooting

### Common Issues

1. **Port already in use**:
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>
```

2. **Permission errors**:
```bash
# Ensure data directory is writable
chmod 755 data/
```

3. **Import errors**:
```bash
# Ensure Python path is correct
export PYTHONPATH="${PYTHONPATH}:/path/to/your/project"
```

### Logs Location
- **Local**: Console output
- **Docker**: `docker logs <container_name>`
- **Cloud**: Check cloud provider logs

## Scaling

### Horizontal Scaling
- Deploy multiple instances
- Use load balancer
- Consider database read replicas

### Vertical Scaling
- Increase CPU/Memory
- Tune Gunicorn workers
- Optimize database queries

This deployment guide should help you deploy the Notes API in various environments successfully.
