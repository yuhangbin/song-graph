"""
FastAPI application for the Song-Graph project.
"""

from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from song_graph.database.session import session_manager
from song_graph.repository.song_repository import SongRepository
from song_graph.models.song import Song

# Initialize FastAPI app
app = FastAPI(
    title="Song-Graph API",
    description="API for managing and analyzing music metadata",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    session_manager.init_db()
    session_manager.create_tables()

# Dependency to get database session
def get_db():
    """Get database session."""
    db = session_manager.get_session()
    try:
        yield db
    finally:
        db.close()

@app.get("/songs/{song_id}", response_model=dict)
def get_song(song_id: int, db: Session = Depends(get_db)):
    """
    Get a song by its ID.
    
    Args:
        song_id: The ID of the song to retrieve
        db: Database session (injected by FastAPI)
        
    Returns:
        The song data as a dictionary
        
    Raises:
        HTTPException: If the song is not found
    """
    repo = SongRepository(db)
    song = repo.get_by_id(song_id)
    
    if song is None:
        raise HTTPException(
            status_code=404,
            detail=f"Song with ID {song_id} not found"
        )
    
    return song.to_dict()

@app.get("/")
def root():
    """Root endpoint returning API information."""
    return {
        "name": "Song-Graph API",
        "version": "1.0.0",
        "description": "API for managing and analyzing music metadata"
    } 