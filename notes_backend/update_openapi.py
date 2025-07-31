#!/usr/bin/env python3
"""
Simple script to generate and update the OpenAPI specification.
"""

import subprocess
import sys
from pathlib import Path

def generate_openapi_spec():
    """Generate OpenAPI spec by running the FastAPI app and extracting the schema."""
    
    # Create a temporary script to extract the OpenAPI schema
    temp_script = """
import sys
import os
sys.path.insert(0, 'src')

# Mock environment to avoid config issues
os.environ.setdefault('APP_NAME', 'Notes API')
os.environ.setdefault('HOST', '0.0.0.0')
os.environ.setdefault('PORT', '8000')

from api.main import app
import json

# Generate the schema
schema = app.openapi()

# Write to interfaces directory
import os
os.makedirs('interfaces', exist_ok=True)
with open('interfaces/openapi.json', 'w') as f:
    json.dump(schema, f, indent=2)

print("OpenAPI spec generated successfully!")
print(f"Endpoints found: {len(schema.get('paths', {}))}")
for path in schema.get('paths', {}):
    print(f"  {path}")
"""
    
    # Write temporary script
    temp_file = Path("temp_openapi_gen.py")
    temp_file.write_text(temp_script)
    
    try:
        # Run the temporary script
        result = subprocess.run([sys.executable, str(temp_file)], 
                              capture_output=True, text=True, cwd=Path.cwd())
        
        if result.returncode == 0:
            print("✅ OpenAPI specification updated successfully!")
            print(result.stdout)
        else:
            print("❌ Error generating OpenAPI spec:")
            print(result.stderr)
            return False
            
    finally:
        # Clean up temporary file
        if temp_file.exists():
            temp_file.unlink()
    
    return result.returncode == 0

if __name__ == "__main__":
    success = generate_openapi_spec()
    sys.exit(0 if success else 1)
