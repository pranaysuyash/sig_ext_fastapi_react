#!/usr/bin/env python3
"""
Simple HTTP server with routing for A/B test variants.
Handles /buy, /purchase, /gum routes by serving index.html or purchase.html
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class ABTestRouter(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle different routes
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/root':
            # Serve index.html for /root route (control variant)
            self.path = '/index.html'
        elif self.path == '/buy' or self.path == '/gum':
            # Serve index.html for /buy and /gum (JavaScript handles the rest)
            self.path = '/index.html'
        elif self.path == '/purchase':
            # Serve purchase.html for /purchase route
            self.path = '/purchase.html'
        elif self.path.startswith('/test-variants'):
            # Allow test dashboard
            pass
        elif not os.path.exists(self.path.lstrip('/')):
            # If file doesn't exist and not a special route, serve index.html
            # This handles refresh on /buy, /gum routes
            if not '.' in os.path.basename(self.path):
                self.path = '/index.html'
        
        return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    PORT = 8080
    server = HTTPServer(('127.0.0.1', PORT), ABTestRouter)
    print(f'✅ Server running at http://127.0.0.1:{PORT}/')
    print(f'📊 Test dashboard: http://127.0.0.1:{PORT}/test-variants.html')
    print(f'\nVariants available:')
    print(f'  • http://127.0.0.1:{PORT}/          (Root - auto A/B if enabled)')
    print(f'  • http://127.0.0.1:{PORT}/root      (Control)')
    print(f'  • http://127.0.0.1:{PORT}/buy       (Embedded)')
    print(f'  • http://127.0.0.1:{PORT}/purchase  (Claude)')
    print(f'  • http://127.0.0.1:{PORT}/gum       (Redirect)')
    print(f'\nPress Ctrl+C to stop\n')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\n👋 Server stopped')
        server.shutdown()
