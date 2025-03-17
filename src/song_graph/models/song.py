"""
SQLAlchemy model for the songs table.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import text, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Song(Base):
    """
    SQLAlchemy model for the songs table.
    """
    __tablename__ = 'song'

    # Primary Key
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    
    # Basic Information
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    artist_id: Mapped[int] = mapped_column(nullable=False, index=True)
    release_date: Mapped[Optional[datetime]] = mapped_column(index=True)
    album_id: Mapped[Optional[int]] = mapped_column(index=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        """String representation of the song."""
        return f"<Song(id={self.id}, title='{self.title}')>"

    def to_dict(self) -> dict:
        """Convert the song to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'artist_id': self.artist_id,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'album_id': self.album_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }