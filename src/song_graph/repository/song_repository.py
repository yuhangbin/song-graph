"""
Repository for song table CRUD operations.
"""

from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update

from song_graph.models.song import Song


class SongRepository:
    """Repository for song table CRUD operations."""
    
    _instance = None
    _db_session = None

    def __new__(cls, db_session: Session = None):
        """
        Create a singleton instance of SongRepository.
        
        Args:
            db_session: SQLAlchemy database session
        """
        # Use double-checked locking pattern for thread safety
        if not hasattr(cls, '_lock'):
            from threading import Lock
            cls._lock = Lock()
            
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SongRepository, cls).__new__(cls)
                    cls._db_session = db_session
        return cls._instance

    def __init__(self, db_session: Session = None):
        """
        Initialize the repository with a database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        if db_session is not None:
            self._db_session = db_session
        self.db = self._db_session

    def get_by_id(self, song_id: int) -> Optional[Song]:
        """
        Get a song by its ID.
        
        Args:
            song_id: The ID of the song to retrieve
            
        Returns:
            The song if found, None otherwise
        """
        return self.db.query(Song).filter(Song.id == song_id).first()

    def get_by_id_list(self, song_ids: List[int]) -> List[Song]:
        """
        Get multiple songs by their IDs.
        
        Args:
            song_ids: List of song IDs to retrieve
            
        Returns:
            List of songs found
        """
        if not song_ids:
            return []
        
        return self.db.query(Song).filter(Song.id.in_(song_ids)).all()

    def insert(self, songs_data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Song, List[Song]]:
        """
        Insert one or multiple songs.
        
        Args:
            songs_data: Dictionary or list of dictionaries with song data
            
        Returns:
            The inserted song(s)
        """
        # Handle single song case
        if isinstance(songs_data, dict):
            song = Song(**songs_data)
            self.db.add(song)
            self.db.flush()
            self.db.commit()
            return song
        
        # Handle multiple songs case
        songs = [Song(**song_data) for song_data in songs_data]
        self.db.add_all(songs)
        self.db.flush()
        self.db.commit()
        return songs

    def delete(self, song_id: int) -> bool:
        """
        Delete a song by its ID.
        
        Args:
            song_id: The ID of the song to delete
            
        Returns:
            True if the song was deleted, False otherwise
        """
        result = self.db.execute(
            delete(Song).where(Song.id == song_id)
        )
        self.db.commit()
        return result.rowcount > 0

    def update(self, song_id: int, update_data: Dict[str, Any]) -> Optional[Song]:
        """
        Update a song by its ID.
        
        Args:
            song_id: The ID of the song to update
            update_data: Dictionary with the fields to update
            
        Returns:
            The updated song if found, None otherwise
        """
        # Remove any None values from update_data
        filtered_data = {k: v for k, v in update_data.items() if v is not None}
        
        if not filtered_data:
            return self.get_by_id(song_id)
        
        # Execute the update
        result = self.db.execute(
            update(Song)
            .where(Song.id == song_id)
            .values(**filtered_data)
        )
        
        if result.rowcount == 0:
            return None
            
        self.db.commit()
        # Return the updated song
        return self.get_by_id(song_id)