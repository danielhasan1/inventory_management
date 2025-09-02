import sqlite3
from contextlib import contextmanager
import os

path = os.path.dirname(os.path.abspath(__file__))
db_file = "warehouse.db"
db_path = os.path.join(path, db_file)
@contextmanager
def get_db():
    conn = sqlite3.connect(db_path, timeout=5, isolation_level=None, autocommit=False)
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA busy_timeout=3000;")
        yield cursor
    except Exception:
        conn.rollback()  # Add rollback on error
        raise
    else:
        conn.commit()    # Only commit on success
    finally:
        conn.close()


def create_tables():
    with get_db() as db:
        db.execute('''
        CREATE TABLE IF NOT EXISTS locations (
        id VARCHAR(64) PRIMARY KEY,
        name VARCHAR(64) UNIQUE NOT NULL,
        status INTEGER NOT NULL CHECK(status IN (0, 1)),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        ''')

        db.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
        id VARCHAR(64) PRIMARY KEY,
        item_id VARCHAR(64) NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity >= 0) DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        location_id VARCHAR(64) NOT NULL,
        FOREIGN KEY(location_id) REFERENCES locations(id));
        ''')


create_tables()

