import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import init_database

if __name__ == '__main__':
    try:
        init_database()
        print('✅ Database initialized successfully!')
    except Exception as e:
        print(f'❌ Error initializing database: {e}')
        sys.exit(1)

