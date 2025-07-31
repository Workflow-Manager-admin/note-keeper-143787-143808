#!/usr/bin/env python3
"""
Simple test script to verify the Notes API functionality.
Run this script to test all major API endpoints.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from fastapi.testclient import TestClient
from src.api.main import app

def test_notes_api():
    """Test all major API endpoints."""
    client = TestClient(app)
    
    print("🧪 Testing Notes API...")
    
    # Test health check
    print("\n1. Testing health check...")
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    print(f"✅ Health check: {data['message']}")
    
    # Test API info
    print("\n2. Testing API info...")
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    print(f"✅ API Info: {data['name']} v{data['version']}")
    
    # Test creating a note
    print("\n3. Testing note creation...")
    note_data = {
        "title": "Test Note",
        "content": "This is a test note created by the test script."
    }
    response = client.post("/notes/", json=note_data)
    assert response.status_code == 201
    created_note = response.json()
    note_id = created_note["id"]
    print(f"✅ Created note with ID: {note_id}")
    
    # Test getting the note
    print("\n4. Testing note retrieval...")
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    retrieved_note = response.json()
    assert retrieved_note["title"] == note_data["title"]
    print(f"✅ Retrieved note: {retrieved_note['title']}")
    
    # Test updating the note
    print("\n5. Testing note update...")
    update_data = {
        "title": "Updated Test Note",
        "content": "This note has been updated by the test script."
    }
    response = client.put(f"/notes/{note_id}", json=update_data)
    assert response.status_code == 200
    updated_note = response.json()
    assert updated_note["title"] == update_data["title"]
    print(f"✅ Updated note title: {updated_note['title']}")
    
    # Test getting all notes
    print("\n6. Testing notes list...")
    response = client.get("/notes/")
    assert response.status_code == 200
    notes_list = response.json()
    assert len(notes_list["notes"]) >= 1
    print(f"✅ Retrieved {len(notes_list['notes'])} notes")
    
    # Test search
    print("\n7. Testing note search...")
    response = client.get("/notes/search?q=Updated")
    assert response.status_code == 200
    search_results = response.json()
    assert len(search_results) >= 1
    print(f"✅ Search found {len(search_results)} matching notes")
    
    # Test deleting the note
    print("\n8. Testing note deletion...")
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 204
    print("✅ Note deleted successfully")
    
    # Verify note is deleted
    print("\n9. Verifying note deletion...")
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 404
    print("✅ Confirmed note is deleted (404 response)")
    
    # Test error handling
    print("\n10. Testing error handling...")
    response = client.get("/notes/999")
    assert response.status_code == 404
    print("✅ Error handling works correctly")
    
    print("\n🎉 All tests passed! The Notes API is working correctly.")
    print("\nAPI Endpoints tested:")
    print("- GET / (health check)")
    print("- GET /info (API information)")
    print("- POST /notes/ (create note)")
    print("- GET /notes/{id} (get note)")
    print("- PUT /notes/{id} (update note)")
    print("- GET /notes/ (list notes)")
    print("- GET /notes/search (search notes)")
    print("- DELETE /notes/{id} (delete note)")

if __name__ == "__main__":
    try:
        test_notes_api()
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
