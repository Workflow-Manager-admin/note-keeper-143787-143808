import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Handle both relative and absolute imports
try:
    from ..models.note import NoteCreate, NoteUpdate, NoteResponse
except ImportError:
    from models.note import NoteCreate, NoteUpdate, NoteResponse


class InMemoryDatabase:
    """Simple in-memory database with optional JSON file persistence."""
    
    def __init__(self, data_file: Optional[str] = None):
        self.data_file = data_file
        self.notes: Dict[int, dict] = {}
        self.next_id = 1
        
        # Load data from file if it exists
        if self.data_file and os.path.exists(self.data_file):
            self._load_from_file()
    
    def _load_from_file(self):
        """Load notes from JSON file."""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.notes = {int(k): v for k, v in data.get('notes', {}).items()}
                self.next_id = data.get('next_id', 1)
        except (json.JSONDecodeError, FileNotFoundError):
            self.notes = {}
            self.next_id = 1
    
    def _save_to_file(self):
        """Save notes to JSON file."""
        if not self.data_file:
            return
            
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump({
                'notes': self.notes,
                'next_id': self.next_id
            }, f, indent=2, default=str)
    
    def create_note(self, note_data: NoteCreate) -> NoteResponse:
        """Create a new note."""
        now = datetime.now()
        note_dict = {
            'id': self.next_id,
            'title': note_data.title,
            'content': note_data.content,
            'created_at': now,
            'updated_at': now
        }
        
        self.notes[self.next_id] = note_dict
        self.next_id += 1
        
        self._save_to_file()
        return NoteResponse(**note_dict)
    
    def get_note(self, note_id: int) -> Optional[NoteResponse]:
        """Get a note by ID."""
        note = self.notes.get(note_id)
        return NoteResponse(**note) if note else None
    
    def get_notes(self, skip: int = 0, limit: int = 100) -> tuple[List[NoteResponse], int]:
        """Get all notes with pagination."""
        all_notes = list(self.notes.values())
        # Sort by created_at descending (newest first)
        all_notes.sort(key=lambda x: x['created_at'], reverse=True)
        
        total = len(all_notes)
        paginated_notes = all_notes[skip:skip + limit]
        
        return [NoteResponse(**note) for note in paginated_notes], total
    
    def update_note(self, note_id: int, note_data: NoteUpdate) -> Optional[NoteResponse]:
        """Update an existing note."""
        if note_id not in self.notes:
            return None
        
        note = self.notes[note_id]
        update_data = note_data.model_dump(exclude_unset=True)
        
        if update_data:
            note.update(update_data)
            note['updated_at'] = datetime.now()
            self._save_to_file()
        
        return NoteResponse(**note)
    
    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID."""
        if note_id in self.notes:
            del self.notes[note_id]
            self._save_to_file()
            return True
        return False
    
    def search_notes(self, query: str) -> List[NoteResponse]:
        """Search notes by title or content."""
        query_lower = query.lower()
        matching_notes = []
        
        for note in self.notes.values():
            if (query_lower in note['title'].lower() or 
                query_lower in note['content'].lower()):
                matching_notes.append(NoteResponse(**note))
        
        # Sort by created_at descending
        matching_notes.sort(key=lambda x: x.created_at, reverse=True)
        return matching_notes


# Global database instance
db = InMemoryDatabase()
