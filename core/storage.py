import sqlite3
from pathlib import Path
from typing import List, Dict

DB_PATH = Path("data/user_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT UNIQUE,
            feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT UNIQUE,
            title TEXT,
            url TEXT,
            feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def update_feedback(item_id: str, feedback: str, is_video: bool = False):
    """
    If feedback is None, delete the record.
    Otherwise, insert or update the record.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if feedback is None:
        if is_video:
            c.execute("DELETE FROM videos WHERE video_id = ?", (item_id,))
        else:
            c.execute("DELETE FROM queries WHERE query = ?", (item_id,))
    else:
        if is_video:
            c.execute('''
                INSERT OR REPLACE INTO videos (id, video_id, title, url, feedback, created_at)
                VALUES (
                    (SELECT id FROM videos WHERE video_id = ?),
                    ?,
                    COALESCE((SELECT title FROM videos WHERE video_id = ?), ''),
                    COALESCE((SELECT url FROM videos WHERE video_id = ?), ''),
                    ?,
                    CURRENT_TIMESTAMP
                )
            ''', (item_id, item_id, item_id, item_id, feedback))
        else:
            c.execute('''
                INSERT OR REPLACE INTO queries (id, query, feedback, created_at)
                VALUES (
                    (SELECT id FROM queries WHERE query = ?),
                    ?,
                    ?,
                    CURRENT_TIMESTAMP
                )
            ''', (item_id, item_id, feedback))
    
    conn.commit()
    conn.close()

def get_liked_suggestions() -> List[Dict]:
    """
    Returns a union of liked videos and liked queries.
    Only items with feedback exactly equal to 'like' are returned.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get liked videos.
    c.execute('''
        SELECT video_id, title, url FROM videos
        WHERE feedback = 'like'
        ORDER BY created_at DESC
    ''')
    videos = [{
        'video_id': row[0],
        'title': row[1],
        'url': row[2],
        'type': 'video'
    } for row in c.fetchall()]
    
    # Get liked queries.
    c.execute('''
        SELECT query FROM queries
        WHERE feedback = 'like'
        ORDER BY created_at DESC
    ''')
    queries = [{
        'query': row[0],
        'type': 'query'
    } for row in c.fetchall()]
    
    conn.close()
    return videos + queries
