"""
SQLAlchemy model for the songs table.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, BigInteger, String, Integer, Date,
    Numeric, DateTime, CheckConstraint, text
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Song(Base):
    """
    SQLAlchemy model for the songs table.
    Handles both PostgreSQL and MySQL compatibility.
    """
    __tablename__ = 'songs'

    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Basic Information
    title = Column(String(255), nullable=False, index=True)
    duration_ms = Column(Integer, nullable=False)
    release_date = Column(Date, index=True)
    album_name = Column(String(255))
    
    # Industry Identifiers
    isrc = Column(String(12))  # International Standard Recording Code
    spotify_id = Column(String(22))
    deezer_id = Column(String(20))
    apple_music_id = Column(String(20))
    
    # Musical Features
    # Handle genre differently for PostgreSQL and MySQL
    _genre_postgresql = Column('genre', ARRAY(String), nullable=True)
    _genre_mysql = Column('genre', JSON, nullable=True)
    
    bpm = Column(Integer)  # Beats per minute
    key = Column(String(10))  # Musical key
    
    # Audio Features
    energy = Column(Numeric(3, 2))
    danceability = Column(Numeric(3, 2))
    
    # Timestamps
    created_at = Column(DateTime, nullable=False,
                       server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, nullable=False,
                       server_default=text('CURRENT_TIMESTAMP'),
                       onupdate=datetime.utcnow)

    # Relationships
    artists = relationship("ArtistRole", back_populates="song",
                         cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        CheckConstraint('duration_ms > 0', name='valid_duration'),
        CheckConstraint('energy >= 0 AND energy <= 1', name='valid_energy'),
        CheckConstraint('danceability >= 0 AND danceability <= 1',
                       name='valid_danceability'),
    )

    @hybrid_property
    def genre(self) -> Optional[List[str]]:
        """
        Get the genre list, handling both PostgreSQL and MySQL formats.
        """
        if self._genre_postgresql is not None:
            return self._genre_postgresql
        if self._genre_mysql is not None:
            return self._genre_mysql
        return None

    @genre.setter
    def genre(self, value: Optional[List[str]]) -> None:
        """
        Set the genre list, handling both PostgreSQL and MySQL formats.
        """
        self._genre_postgresql = value
        self._genre_mysql = value

    def __repr__(self) -> str:
        """String representation of the song."""
        return f"<Song(id={self.id}, title='{self.title}')>"

    def to_dict(self) -> dict:
        """Convert the song to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'duration_ms': self.duration_ms,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'album_name': self.album_name,
            'isrc': self.isrc,
            'spotify_id': self.spotify_id,
            'deezer_id': self.deezer_id,
            'apple_music_id': self.apple_music_id,
            'genre': self.genre,
            'bpm': self.bpm,
            'key': self.key,
            'energy': float(self.energy) if self.energy is not None else None,
            'danceability': float(self.danceability) if self.danceability is not None else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 