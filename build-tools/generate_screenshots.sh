#!/bin/bash
# Automated Screenshot Generation for SignKit
# Uses existing screenshot automation scripts

set -e

echo "📸 SignKit Screenshot Generation"
echo "================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Navigate to scripts directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"

cd "$PROJECT_ROOT"

echo "📂 Project root: $PROJECT_ROOT"
echo "📂 Scripts directory: $SCRIPTS_DIR"
echo ""

# Check if screenshot scripts exist
if [ ! -f "$SCRIPTS_DIR/comprehensive_screenshots.py" ]; then
    echo "❌ Screenshot script not found: $SCRIPTS_DIR/comprehensive_screenshots.py"
    exit 1
fi

# Create output directory
OUTPUT_DIR="$PROJECT_ROOT/marketing/screenshots"
mkdir -p "$OUTPUT_DIR"

echo "✨ Running screenshot automation..."
echo ""

# Run comprehensive screenshot script
python3 "$SCRIPTS_DIR/comprehensive_screenshots.py" 2>&1 | tee "$OUTPUT_DIR/screenshot_log.txt"

echo ""
echo "✅ Screenshot generation complete!"
echo ""
echo "📁 Screenshots saved to: $OUTPUT_DIR"
echo ""
echo "Required screenshots for launch:"
echo "  1. Main window with signature extraction"
echo "  2. Selection tool in action"
echo "  3. Threshold adjustment controls"
echo "  4. Preview pane with extracted signature"
echo "  5. Library management view"
echo "  6. PDF signing interface"
echo "  7. Export dialog"
echo ""
echo "Next steps:"
echo "  1. Review screenshots in $OUTPUT_DIR"
echo "  2. Rename to descriptive names (e.g., 01_main_window.png)"
echo "  3. Resize to 1200x800 minimum for Gumroad"
echo "  4. Upload to Gumroad product page"
echo ""
echo "💡 Tip: Use Preview (macOS) or Paint.NET (Windows) to add annotations"
