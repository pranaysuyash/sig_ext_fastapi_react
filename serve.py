#!/usr/bin/env python3
"""
Simple HTTP server with routing for A/B test variants.
Handles /buy, /purchase, /gum routes by serving index.html or purchase.html
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class ABTestRouter(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle extensionless landing routes (match Cloudflare Pages _redirects)
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/root':
            self.path = '/root.html'
        elif self.path == '/buy':
            self.path = '/buy.html'
        elif self.path == '/purchase':
            self.path = '/purchase.html'
        elif self.path == '/gum':
            self.path = '/gum.html'
        elif self.path == '/test-variants':
            self.path = '/test-variants.html'
        elif self.path == '/new':
            # Serve new landing page
            self.path = '/web/new_landing_page/index.html'
        elif not os.path.exists(self.path.lstrip('/')):
            # Unknown extensionless route: serve 404 (closer to Pages behavior)
            if '.' not in os.path.basename(self.path):
                self.path = '/404.html'
        
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
    print(f'  • http://127.0.0.1:{PORT}/new       (New Design)')
    print(f'\nPress Ctrl+C to stop\n')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\n👋 Server stopped')
        server.shutdown()
