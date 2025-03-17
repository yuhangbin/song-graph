"""
Database connection test module.
"""

import logging
from sqlalchemy import text
from song_graph.database.session import session_manager
from song_graph.models.song import Song

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """Test database connection and basic operations."""
    try:
        # Initialize database
        logger.info("Initializing database connection...")
        session_manager.init_db()
        
        # Test connection
        logger.info("Testing database connection...")
        with session_manager.get_db() as db:
            result = db.execute(text("SELECT 1")).scalar()
            logger.info(f"Basic query test result: {result}")
            
            # Test table creation
            logger.info("Testing table creation...")
            session_manager.create_tables()
            
            # Test basic insert
            logger.info("Testing basic insert operation...")
            test_song = Song(
                title="Test Song",
                artist_id=1,
                release_date=None,
                album_id=None
            )
            db.add(test_song)
            db.commit()
            
            # Test basic select
            logger.info("Testing basic select operation...")
            inserted_song = db.query(Song).first()
            logger.info(f"Retrieved song: {inserted_song}")
            
            # Cleanup
            logger.info("Cleaning up test data...")
            db.delete(test_song)
            db.commit()
            
        logger.info("All database tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if not success:
        logger.error("Database connection test failed!")
        exit(1)
    logger.info("Database connection test passed!") 