#!/usr/bin/env python3
"""
Startup script for the Notes API application.
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    import uvicorn
    from src.config import settings
    
    # Create data directory if specified
    if settings.data_file:
        data_dir = os.path.dirname(settings.data_file)
        if data_dir:
            os.makedirs(data_dir, exist_ok=True)
    
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Server will be available at: http://{settings.host}:{settings.port}")
    print(f"API documentation at: http://{settings.host}:{settings.port}/docs")
    
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
