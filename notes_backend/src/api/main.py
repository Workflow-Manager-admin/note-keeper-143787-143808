from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Handle both relative and absolute imports
try:
    from ..config import settings
    from ..routers import notes_router
    from ..services.database import db
except ImportError:
    # Fallback for when running as script
    from config import settings
    from routers import notes_router
    from services.database import db

# Initialize FastAPI app with comprehensive metadata
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check endpoints"
        },
        {
            "name": "notes",
            "description": "Operations with notes. Create, read, update, and delete notes."
        }
    ]
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database with data file if configured
if settings.data_file:
    db.data_file = settings.data_file
    db._load_from_file()

# Include routers
app.include_router(notes_router)


# PUBLIC_INTERFACE
@app.get("/", tags=["health"], summary="Health Check", 
         description="Check if the API is running and healthy")
def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Health status message
    """
    return {
        "message": "Healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


# PUBLIC_INTERFACE
@app.get("/info", tags=["health"], summary="API Information",
         description="Get information about the API")
def api_info():
    """
    Get API information including name, version, and description.
    
    Returns:
        dict: API information
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "endpoints": {
            "notes": "/notes",
            "health": "/",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
