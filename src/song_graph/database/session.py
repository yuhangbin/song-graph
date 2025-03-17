"""
Database session management for PostgreSQL.
"""

from dotenv import load_dotenv
from contextlib import contextmanager


load_dotenv()

import os
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

from song_graph.models.song import Base

class DatabaseConfig:
    """Database configuration settings."""
    
    def __init__(
        self,
        host: str = os.getenv("POSTGRES_HOST", "localhost"),
        port: int = int(os.getenv("POSTGRES_PORT", "15432")),
        database: str = os.getenv("POSTGRES_DB", "song_graph"),
        user: str = os.getenv("POSTGRES_USER", "postgres"),
        password: str = os.getenv("POSTGRES_PASSWORD", "password"),
        echo: bool = bool(os.getenv("SQL_ECHO", "False").lower() == "true")
    ):
        """
        Initialize database configuration.
        
        Args:
            host: Database host
            port: Database port
            database: Database name
            user: Database user
            password: Database password
            echo: Whether to echo SQL statements
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.echo = echo

    @property
    def database_url(self) -> str:
        """Get the database URL."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


# TODO: thread safe
class SessionManager:
    """Manage database sessions."""
    
    _instance = None
    _engine = None
    _session_factory = None

    def __new__(cls):
        """Create a singleton instance."""
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def init_db(self, config: DatabaseConfig = None) -> None:
        """
        Initialize the database connection.
        
        Args:
            config: Database configuration. If None, uses default configuration.
        """
        if config is None:
            config = DatabaseConfig()

        if self._engine is None:
            self._engine = create_engine(
                config.database_url,
                echo=config.echo,
                pool_pre_ping=True  # Enable connection health checks
            )
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )

    def create_tables(self) -> None:
        """Create all tables defined in the models."""
        if self._engine is None:
            raise RuntimeError("Database not initialized. Call init_db first.")
        Base.metadata.create_all(self._engine)

    def drop_tables(self) -> None:
        """Drop all tables defined in the models."""
        if self._engine is None:
            raise RuntimeError("Database not initialized. Call init_db first.")
        Base.metadata.drop_all(self._engine)

    @property
    def engine(self) -> Engine:
        """Get the SQLAlchemy engine."""
        if self._engine is None:
            raise RuntimeError("Database not initialized. Call init_db first.")
        return self._engine

    def get_session(self) -> Session:
        """Get a new database session."""
        if self._session_factory is None:
            raise RuntimeError("Database not initialized. Call init_db first.")
        return self._session_factory()

    @contextmanager
    def get_db(self) -> Generator[Session, None, None]:
        """
        Get a database session as a context manager.
        
        Yields:
            A database session that will be automatically closed.
        """
        if self._session_factory is None:
            raise RuntimeError("Database not initialized. Call init_db first.")
            
        session = self._session_factory()
        try:
            yield session
        finally:
            session.close()


# Global instance of SessionManager
session_manager = SessionManager() 


# test_db.py
from song_graph.database.session import session_manager

def test_connection():
    session_manager.init_db()
    with session_manager.get_db() as db:
        result = db.execute(text("SELECT 1")).scalar()
        print("Database connection successful!")

if __name__ == "__main__":
    test_connection()