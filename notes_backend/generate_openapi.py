#!/usr/bin/env python3
"""
Generate OpenAPI specification for the Notes API.
Run this script from the notes_backend directory to update the interfaces/openapi.json file.
"""

import json
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def generate_openapi():
    """Generate and save the OpenAPI specification."""
    try:
        from api.main import app
        
        # Get the OpenAPI schema
        openapi_schema = app.openapi()
        
        # Write to interfaces directory
        output_dir = Path(__file__).parent / "interfaces"
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
                
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the notes_backend directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating OpenAPI spec: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_openapi()
