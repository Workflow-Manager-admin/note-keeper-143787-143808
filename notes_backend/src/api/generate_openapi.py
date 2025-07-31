#!/usr/bin/env python3
"""
Generate OpenAPI specification for the Notes API.
Run this script to update the interfaces/openapi.json file.
"""

import json
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from notes_backend.src.api.main import app

def generate_openapi():
    """Generate and save the OpenAPI specification."""
    # Get the OpenAPI schema
    openapi_schema = app.openapi()
    
    # Write to interfaces directory
    output_dir = Path(__file__).parent.parent.parent / "interfaces"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "openapi.json"
    
    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    
    print(f"✅ OpenAPI specification generated: {output_path}")
    print(f"📊 Found {len(openapi_schema.get('paths', {}))} endpoints")
    
    # Print summary of endpoints
    paths = openapi_schema.get('paths', {})
    for path, methods in paths.items():
        for method, details in methods.items():
            summary = details.get('summary', 'No summary')
            print(f"  {method.upper()} {path} - {summary}")

if __name__ == "__main__":
    generate_openapi()
