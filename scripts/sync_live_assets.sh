#!/usr/bin/env bash
set -euo pipefail

# Create web/live/assets/files if missing and copy files from root assets
SRC_DIR="$(pwd)/assets/files"
DEST_DIR="$(pwd)/web/live/assets/files"

if [ ! -d "$SRC_DIR" ]; then
    echo "Source assets not found: $SRC_DIR"
    exit 1
fi

mkdir -p "$DEST_DIR"
cp -R "$SRC_DIR/"* "$DEST_DIR/"

echo "Copied assets from $SRC_DIR to $DEST_DIR"
