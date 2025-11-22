"""
Sample Cloudflare uploader (safe to commit in repo). This file contains no secrets.
Copy this file to `tools/upload_to_cloudflare.py`, set your env vars, and run locally.

This sample is intended so developers can see the usage and modify it locally.
Do not commit your API token or account id.
"""
import os
from pathlib import Path

# Copy this file to tools/upload_to_cloudflare.py and use environment variables for tokens.
# Example:
# export CLOUDFLARE_ACCOUNT_ID=xxxx
# export CLOUDFLARE_API_TOKEN=xxxx

# Root path to landing page assets
ROOT = Path(__file__).parents[1]
SCREEN_DIR = ROOT / 'web' / 'live' / 'assets' / 'screenshots'

def main():
    print("This is a template. Copy to tools/upload_to_cloudflare.py and set env vars.")

if __name__ == '__main__':
    main()
