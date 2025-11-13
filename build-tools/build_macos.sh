#!/bin/bash
# Build script for macOS app bundle

set -e  # Exit on error

echo "=================================="
echo "Signature Extractor - macOS Build"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "Project root: $PROJECT_ROOT"
echo ""

# Check if venv is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}Warning: Virtual environment not activated${NC}"
    echo "Attempting to activate venv..."
    
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo -e "${GREEN}✓ Virtual environment activated${NC}"
    else
        echo -e "${RED}✗ Virtual environment not found!${NC}"
        echo "Please run: python3 -m venv venv && source venv/bin/activate"
        exit 1
    fi
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if PyInstaller is installed
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo -e "${YELLOW}PyInstaller not found. Installing...${NC}"
    pip install pyinstaller
fi

# Check other required packages
echo "Checking required packages..."
REQUIRED_PACKAGES=("PySide6" "pillow" "opencv-python" "numpy" "requests")
MISSING_PACKAGES=()

for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if ! python -c "import ${pkg//-/_}" 2>/dev/null; then
        MISSING_PACKAGES+=("$pkg")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo -e "${YELLOW}Missing packages: ${MISSING_PACKAGES[*]}${NC}"
    echo "Installing missing packages..."
    pip install "${MISSING_PACKAGES[@]}"
fi

echo -e "${GREEN}✓ All required packages available${NC}"
echo ""

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist
echo -e "${GREEN}✓ Cleaned build directories${NC}"
echo ""

# Build the application
echo "Building macOS application..."
echo "This may take 3-5 minutes..."
echo ""

# Use the macOS-specific spec file
SPEC_FILE="build-tools/SignatureExtractor_macOS.spec"

if [ ! -f "$SPEC_FILE" ]; then
    echo -e "${RED}✗ Spec file not found: $SPEC_FILE${NC}"
    exit 1
fi

# Run PyInstaller
python -m PyInstaller \
    --clean \
    --noconfirm \
    "$SPEC_FILE"

# Check if build was successful
if [ ! -d "dist/SignatureExtractor.app" ]; then
    echo -e "${RED}✗ Build failed - .app bundle not found${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Build completed successfully!${NC}"
echo ""

# Show build info
APP_PATH="dist/SignatureExtractor.app"
APP_SIZE=$(du -sh "$APP_PATH" | cut -f1)

echo "Build Information:"
echo "=================="
echo "App Bundle: $APP_PATH"
echo "Size: $APP_SIZE"
echo "Architecture: $(file "$APP_PATH/Contents/MacOS/SignatureExtractor" | cut -d: -f2)"
echo ""

# Test if the app can be opened (basic validation)
echo "Validating app bundle structure..."
if [ -f "$APP_PATH/Contents/MacOS/SignatureExtractor" ]; then
    echo -e "${GREEN}✓ Executable found${NC}"
else
    echo -e "${RED}✗ Executable not found${NC}"
    exit 1
fi

if [ -f "$APP_PATH/Contents/Info.plist" ]; then
    echo -e "${GREEN}✓ Info.plist found${NC}"
else
    echo -e "${RED}✗ Info.plist not found${NC}"
    exit 1
fi

echo ""
echo "Next Steps:"
echo "==========="
echo "1. Test the app:"
echo "   open dist/SignatureExtractor.app"
echo ""
echo "2. Create DMG for distribution (optional):"
echo "   hdiutil create -volname 'Signature Extractor' -srcfolder dist/SignatureExtractor.app -ov -format UDZO dist/SignatureExtractor.dmg"
echo ""
echo "3. For first run, you may need to:"
echo "   - Right-click the app and select 'Open'"
echo "   - Or: System Preferences > Security & Privacy > Open Anyway"
echo ""
echo -e "${GREEN}Build complete!${NC}"
