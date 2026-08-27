import os
import sys
import urllib.parse

# Ensure repository root is on sys.path so 'backend.app' can be imported reliably
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import the existing Flask app instance
from backend.app import app

# WSGI Middleware to ensure PATH_INFO matches the requested URL on Vercel
class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # 1. Primary: Check if path was captured in query string by Vercel rewrite (?__path__=/$1)
        query_string = environ.get('QUERY_STRING', '')
        if '__path__=' in query_string:
            params = urllib.parse.parse_qs(query_string)
            if '__path__' in params and params['__path__']:
                req_path = params['__path__'][0]
                if not req_path.startswith('/'):
                    req_path = '/' + req_path
                environ['PATH_INFO'] = req_path
                clean_params = {k: v for k, v in params.items() if k != '__path__'}
                environ['QUERY_STRING'] = urllib.parse.urlencode(clean_params, doseq=True)
                return self.wsgi_app(environ, start_response)

        # 2. Secondary: Check Vercel forwarding headers
        original_uri = (
            environ.get('HTTP_X_FORWARDED_URI') or
            environ.get('HTTP_X_MATCHED_PATH') or
            environ.get('RAW_URI') or
            ''
        )

        path_info = environ.get('PATH_INFO', '')

        # 3. If Vercel rewrote PATH_INFO to the function name, restore the route
        if path_info in ('/api/index', '/api/index.py', '/api', '/api/'):
            if original_uri and original_uri not in ('/api/index', '/api/index.py'):
                clean_path = original_uri.split('?')[0]
                if clean_path:
                    environ['PATH_INFO'] = clean_path
            else:
                environ['PATH_INFO'] = '/'
        elif path_info.startswith('/api/index/'):
            environ['PATH_INFO'] = path_info[len('/api/index'):]
        elif path_info.startswith('/api/index.py/'):
            environ['PATH_INFO'] = path_info[len('/api/index.py'):]

        # 4. Ensure PATH_INFO is never empty
        if not environ.get('PATH_INFO'):
            environ['PATH_INFO'] = '/'

        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
