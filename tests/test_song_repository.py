"""
Unit tests for SongRepository.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from song_graph.models.song import Song, Base
from song_graph.repository.song_repository import SongRepository

@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

@pytest.fixture
def song_repository(db_session):
    """Create a test song repository."""
    return SongRepository(db_session)

@pytest.fixture
def sample_song_data():
    """Return sample song data."""
    return {
        "title": "Test Song",
        "artist": "Test Artist",
        "album": "Test Album",
        "year": 2024
    }

def test_singleton_pattern(db_session):
    """Test that SongRepository follows singleton pattern."""
    repo1 = SongRepository(db_session)
    repo2 = SongRepository(db_session)
    assert repo1 is repo2

def test_get_by_id_not_found(song_repository):
    """Test getting a non-existent song by ID."""
    result = song_repository.get_by_id(1)
    assert result is None

def test_get_by_id_found(song_repository, sample_song_data):
    """Test getting an existing song by ID."""
    # Insert a song first
    song = song_repository.insert(sample_song_data)
    
    # Get the song
    result = song_repository.get_by_id(song.id)
    assert result is not None
    assert result.title == sample_song_data["title"]
    assert result.artist == sample_song_data["artist"]

def test_get_by_id_list_empty(song_repository):
    """Test getting songs by empty ID list."""
    result = song_repository.get_by_id_list([])
    assert result == []

def test_get_by_id_list(song_repository, sample_song_data):
    """Test getting multiple songs by ID list."""
    # Insert two songs
    song1 = song_repository.insert(sample_song_data)
    song2 = song_repository.insert({**sample_song_data, "title": "Test Song 2"})
    
    # Get the songs
    result = song_repository.get_by_id_list([song1.id, song2.id])
    assert len(result) == 2
    assert result[0].title == sample_song_data["title"]
    assert result[1].title == "Test Song 2"

def test_insert_single(song_repository, sample_song_data):
    """Test inserting a single song."""
    result = song_repository.insert(sample_song_data)
    assert result.title == sample_song_data["title"]
    assert result.artist == sample_song_data["artist"]
    assert result.id is not None

def test_insert_multiple(song_repository, sample_song_data):
    """Test inserting multiple songs."""
    songs_data = [
        sample_song_data,
        {**sample_song_data, "title": "Test Song 2"}
    ]
    result = song_repository.insert(songs_data)
    assert len(result) == 2
    assert result[0].title == songs_data[0]["title"]
    assert result[1].title == songs_data[1]["title"]

def test_delete_not_found(song_repository):
    """Test deleting a non-existent song."""
    result = song_repository.delete(1)
    assert result is False

def test_delete_success(song_repository, sample_song_data):
    """Test deleting an existing song."""
    # Insert a song first
    song = song_repository.insert(sample_song_data)
    
    # Delete the song
    result = song_repository.delete(song.id)
    assert result is True
    
    # Verify deletion
    assert song_repository.get_by_id(song.id) is None

def test_update_not_found(song_repository, sample_song_data):
    """Test updating a non-existent song."""
    result = song_repository.update(1, {"title": "Updated Title"})
    assert result is None

def test_update_success(song_repository, sample_song_data):
    """Test updating an existing song."""
    # Insert a song first
    song = song_repository.insert(sample_song_data)
    
    # Update the song
    update_data = {"title": "Updated Title"}
    result = song_repository.update(song.id, update_data)
    
    assert result is not None
    assert result.title == "Updated Title"
    assert result.artist == sample_song_data["artist"]  # Unchanged field

def test_update_with_none_values(song_repository, sample_song_data):
    """Test updating a song with None values."""
    # Insert a song first
    song = song_repository.insert(sample_song_data)
    
    # Update with None values
    update_data = {"title": None, "artist": "Updated Artist"}
    result = song_repository.update(song.id, update_data)
    
    assert result is not None
    assert result.title == sample_song_data["title"]  # Should remain unchanged
    assert result.artist == "Updated Artist" 