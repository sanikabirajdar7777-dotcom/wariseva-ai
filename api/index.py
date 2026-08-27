import os
import sys

# Ensure repository root is on sys.path so 'backend.app' can be imported reliably
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import the existing Flask app instance
from backend.app import app

# Vercel's Python runtime exposes 'app' as the WSGI entry point
if __name__ == '__main__':
    app.run()
