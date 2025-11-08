import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.path.join(BASE_DIR, 'database', 'civicosafe.db')

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)  # 10 second timeout
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    # Enable WAL mode for better concurrency (if possible)
    cursor = conn.cursor()
    try:
        cursor.execute('PRAGMA journal_mode = WAL')
    except sqlite3.OperationalError:
        # If WAL mode fails (read-only database), continue with default mode
        pass
    try:
        cursor.execute('PRAGMA synchronous = NORMAL')
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute('PRAGMA busy_timeout = 5000')  # Wait up to 5 seconds if locked
    except sqlite3.OperationalError:
        pass
    cursor.close()
    return conn

def init_database():
    """Initialize database tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'member',
                verified INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Incidents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                location TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'general',
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'active',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                phone TEXT,
                address TEXT,
                role TEXT DEFAULT 'member',
                block_captain INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Emergency contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emergency_contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default emergency contacts
        cursor.execute('''
            INSERT OR IGNORE INTO emergency_contacts (name, phone, type, description) VALUES 
            ('Emergency Services', '911', 'emergency', 'Police, Fire, Medical'),
            ('Police Department', '555-0100', 'police', 'Local police station'),
            ('Fire Department', '555-0101', 'fire', 'Local fire station'),
            ('Medical Emergency', '555-0102', 'medical', 'Ambulance services')
        ''')
        
        conn.commit()
        print('✅ Database tables initialized')
        
    except Exception as e:
        conn.rollback()
        print(f'❌ Error initializing database: {e}')
        raise
    finally:
        conn.close()

def query(sql, params=()):
    """Execute SELECT query and return all rows"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        # Convert Row objects to dictionaries
        return [dict(row) for row in rows]
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get(sql, params=()):
    """Execute SELECT query and return single row"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def run(sql, params=()):
    """Execute INSERT/UPDATE/DELETE query"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        last_id = cursor.lastrowid
        changes = cursor.rowcount
        return {'id': last_id, 'changes': changes}
    except sqlite3.OperationalError as e:
        if conn:
            conn.rollback()
        if 'locked' in str(e).lower():
            raise Exception('Database is locked. Please wait a moment and try again.')
        raise e
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

