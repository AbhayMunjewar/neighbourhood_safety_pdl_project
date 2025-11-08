"""
Simple script to run the Flask app.
Usage: python run.py
"""
from app import app

if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', 3000))
    print(f'🚀 Server running on http://localhost:{port}')
    print(f'📡 API endpoint: http://localhost:{port}/api')
    app.run(host='0.0.0.0', port=port, debug=True)

