from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base model for note data."""
    title: str = Field(..., min_length=1, max_length=200, description="The title of the note")
    content: str = Field(..., description="The content of the note")


class NoteCreate(NoteBase):
    """Model for creating a new note."""
    pass


class NoteUpdate(BaseModel):
    """Model for updating an existing note."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="The title of the note")
    content: Optional[str] = Field(None, description="The content of the note")


class NoteResponse(NoteBase):
    """Model for note response data."""
    id: int = Field(..., description="The unique identifier of the note")
    created_at: datetime = Field(..., description="The timestamp when the note was created")
    updated_at: datetime = Field(..., description="The timestamp when the note was last updated")
    
    class Config:
        from_attributes = True


class NoteListResponse(BaseModel):
    """Model for paginated note list response."""
    notes: list[NoteResponse] = Field(..., description="List of notes")
    total: int = Field(..., description="Total number of notes")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of items per page")
