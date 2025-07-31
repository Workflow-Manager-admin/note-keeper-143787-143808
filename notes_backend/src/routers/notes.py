from typing import List
from fastapi import APIRouter, HTTPException, Query

# Handle both relative and absolute imports
try:
    from ..models import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse
    from ..services import db
except ImportError:
    from models import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse
    from services import db

# Create router with tags for API documentation
router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)


# PUBLIC_INTERFACE
@router.post("/", response_model=NoteResponse, status_code=201, 
             summary="Create a new note",
             description="Create a new note with title and content")
def create_note(note: NoteCreate):
    """
    Create a new note.
    
    Args:
        note: The note data containing title and content
        
    Returns:
        NoteResponse: The created note with ID and timestamps
    """
    try:
        return db.create_note(note)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create note: {str(e)}")


# PUBLIC_INTERFACE
@router.get("/", response_model=NoteListResponse,
            summary="Get all notes",
            description="Retrieve all notes with pagination support")
def get_notes(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Number of notes per page")
):
    """
    Get all notes with pagination.
    
    Args:
        page: Page number (starting from 1)
        per_page: Number of notes per page (max 100)
        
    Returns:
        NoteListResponse: Paginated list of notes
    """
    try:
        skip = (page - 1) * per_page
        notes, total = db.get_notes(skip=skip, limit=per_page)
        
        return NoteListResponse(
            notes=notes,
            total=total,
            page=page,
            per_page=per_page
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve notes: {str(e)}")


# PUBLIC_INTERFACE
@router.get("/search", response_model=List[NoteResponse],
            summary="Search notes",
            description="Search notes by title or content")
def search_notes(q: str = Query(..., min_length=1, description="Search query")):
    """
    Search notes by title or content.
    
    Args:
        q: Search query string
        
    Returns:
        List[NoteResponse]: List of matching notes
    """
    try:
        return db.search_notes(q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search notes: {str(e)}")


# PUBLIC_INTERFACE
@router.get("/{note_id}", response_model=NoteResponse,
            summary="Get a specific note",
            description="Retrieve a specific note by its ID")
def get_note(note_id: int):
    """
    Get a specific note by ID.
    
    Args:
        note_id: The ID of the note to retrieve
        
    Returns:
        NoteResponse: The requested note
        
    Raises:
        HTTPException: 404 if note is not found
    """
    note = db.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@router.put("/{note_id}", response_model=NoteResponse,
            summary="Update a note",
            description="Update an existing note's title and/or content")
def update_note(note_id: int, note_update: NoteUpdate):
    """
    Update an existing note.
    
    Args:
        note_id: The ID of the note to update
        note_update: The updated note data
        
    Returns:
        NoteResponse: The updated note
        
    Raises:
        HTTPException: 404 if note is not found
    """
    updated_note = db.update_note(note_id, note_update)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note


# PUBLIC_INTERFACE
@router.delete("/{note_id}", status_code=204,
               summary="Delete a note",
               description="Delete a note by its ID")
def delete_note(note_id: int):
    """
    Delete a note by ID.
    
    Args:
        note_id: The ID of the note to delete
        
    Raises:
        HTTPException: 404 if note is not found
    """
    if not db.delete_note(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    return None
