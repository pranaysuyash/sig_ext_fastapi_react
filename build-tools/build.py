#!/usr/bin/env python3
"""
Build script for packaging Signature Extractor using PyInstaller.

This script provides a convenient interface for building the application
for different platforms and configurations.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


def run_command(cmd: List[str], cwd: str = None) -> int:
    """Run a command and return the exit code."""
    print(f"Running: {' '.join(cmd)}")
    if cwd:
        print(f"Working directory: {cwd}")

    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode


def check_dependencies():
    """Check if required dependencies are available."""
    print("Checking dependencies...")

    try:
        import PyInstaller
        print(f"✓ PyInstaller found: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False

    # Check if main script exists
    main_script = Path("desktop_app/main.py")
    if not main_script.exists():
        print(f"❌ Main script not found: {main_script}")
        return False
    print(f"✓ Main script found: {main_script}")

    return True


def clean_build_dirs():
    """Clean previous build directories."""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)

    # Clean Python cache files
    for cache_dir in Path(".").rglob("__pycache__"):
        print(f"Cleaning cache: {cache_dir}")
        shutil.rmtree(cache_dir)


def build_application(
    one_file: bool = False,
    debug: bool = False,
    windowed: bool = True,
    clean: bool = True,
    spec_file: str = None
) -> int:
    """Build the application using PyInstaller."""

    if clean:
        clean_build_dirs()

    # Prepare PyInstaller command
    cmd = ["python", "-m", "PyInstaller"]

    # Use spec file if provided, otherwise create command from options
    if spec_file and Path(spec_file).exists():
        cmd.append(spec_file)
    else:
        spec_file = "signature_extractor.spec"
        if Path(spec_file).exists():
            cmd.append(spec_file)
        else:
            # Build without spec file
            cmd.extend([
                "desktop_app/main.py",
                "--name", "SignatureExtractor",
                "--add-data", ".env.example:.",
                "--add-data", "docs:docs",
                "--add-data", "backend:backend",
            ])

            if one_file:
                cmd.append("--onefile")
            else:
                cmd.append("--onedir")

            if debug:
                cmd.append("--debug")
                cmd.append("--log-level", "DEBUG")

            if windowed:
                cmd.append("--windowed")  # --noconsole
            else:
                cmd.append("--console")

    # Additional options
    if not debug:
        cmd.append("--clean")

    print(f"Building application with command: {' '.join(cmd)}")

    # Run PyInstaller
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("✓ Build completed successfully!")

        # Show output directory
        dist_dir = Path("dist")
        if dist_dir.exists():
            print(f"Output directory: {dist_dir.absolute()}")

            # List built files
            for item in dist_dir.iterdir():
                if item.is_file():
                    size_mb = item.stat().st_size / (1024 * 1024)
                    print(f"  - {item.name} ({size_mb:.1f} MB)")
                elif item.is_dir():
                    print(f"  - {item.name}/ (directory)")
    else:
        print("❌ Build failed!")

    return result.returncode


def create_installer_scripts():
    """Create platform-specific installer scripts."""
    print("Creating installer scripts...")

    # macOS script
    macos_script = """#!/bin/bash
# macOS Installation Script for Signature Extractor

set -e

APP_NAME="SignatureExtractor"
APP_DIR="/Applications/$APP_NAME.app"

echo "Installing Signature Extractor..."

# Check if app is running
if pgrep -f "$APP_NAME" > /dev/null; then
    echo "Please quit Signature Extractor before installing."
    exit 1
fi

# Remove existing installation
if [ -d "$APP_DIR" ]; then
    echo "Removing existing installation..."
    sudo rm -rf "$APP_DIR"
fi

# Create Applications directory if needed
if [ ! -d "/Applications" ]; then
    echo "Creating Applications directory..."
    sudo mkdir -p "/Applications"
fi

# Copy application
echo "Copying application to /Applications..."
sudo cp -R "dist/$APP_NAME.app" "/Applications/"

# Set permissions
sudo chown -R root:admin "$APP_DIR"
sudo chmod -R 755 "$APP_DIR"

echo "Installation complete!"
echo "You can now launch Signature Extractor from your Applications folder."
"""

    with open("install_macos.sh", "w") as f:
        f.write(macos_script)
    os.chmod("install_macos.sh", 0o755)
    print("✓ Created install_macos.sh")

    # Windows script
    windows_script = """@echo off
REM Windows Installation Script for Signature Extractor

set APP_NAME=SignatureExtractor
set INSTALL_DIR=%ProgramFiles%\\%APP_NAME%

echo Installing Signature Extractor...

REM Check if app is running
tasklist /FI "IMAGENAME eq %APP_NAME%.exe" 2>NUL | find /I "%APP_NAME%.exe" >NUL
if %ERRORLEVEL% == 0 (
    echo Please quit Signature Extractor before installing.
    pause
    exit /b 1
)

REM Create installation directory
if not exist "%INSTALL_DIR%" (
    echo Creating installation directory...
    mkdir "%INSTALL_DIR%"
)

REM Copy application files
echo Copying application files...
xcopy "dist\\%APP_NAME%\*" "%INSTALL_DIR%\\" /E /Y

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%USERPROFILE%\\Desktop\\Signature Extractor.lnk');$s.TargetPath='%INSTALL_DIR%\\%APP_NAME%.exe';$s.Save()"

REM Create Start Menu shortcut
echo Creating Start Menu shortcut...
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Signature Extractor.lnk');$s.TargetPath='%INSTALL_DIR%\\%APP_NAME%.exe';$s.Save()"

echo Installation complete!
echo You can now launch Signature Extractor from your desktop or Start Menu.
pause
"""

    with open("install_windows.bat", "w") as f:
        f.write(windows_script)
    print("✓ Created install_windows.bat")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build Signature Extractor application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build.py                    # Build with default settings (one-dir, windowed)
  python build.py --one-file         # Build as single executable
  python build.py --debug            # Build with debug information
  python build.py --console          # Build with console window
  python build.py --clean-only       # Only clean build directories
  python build.py --create-scripts   # Create installer scripts
        """
    )

    parser.add_argument("--one-file", action="store_true",
                       help="Build as single executable file")
    parser.add_argument("--debug", action="store_true",
                       help="Build with debug information")
    parser.add_argument("--console", action="store_true",
                       help="Build with console window (no GUI)")
    parser.add_argument("--clean", action="store_true", default=True,
                       help="Clean build directories before building")
    parser.add_argument("--no-clean", dest="clean", action="store_false",
                       help="Don't clean build directories before building")
    parser.add_argument("--clean-only", action="store_true",
                       help="Only clean build directories, don't build")
    parser.add_argument("--spec", type=str, default="signature_extractor.spec",
                       help="Use specific spec file")
    parser.add_argument("--create-scripts", action="store_true",
                       help="Create installer scripts")
    parser.add_argument("--no-deps-check", action="store_true",
                       help="Skip dependency checking")

    args = parser.parse_args()

    print("Signature Extractor Build Script")
    print("=" * 40)

    # Check dependencies
    if not args.no_deps_check:
        if not check_dependencies():
            sys.exit(1)

    # Handle clean-only
    if args.clean_only:
        clean_build_dirs()
        print("✓ Build directories cleaned.")
        return

    # Create installer scripts if requested
    if args.create_scripts:
        create_installer_scripts()

    # Build application
    if not args.create_scripts or args.clean_only:
        return_code = build_application(
            one_file=args.one_file,
            debug=args.debug,
            windowed=not args.console,
            clean=args.clean,
            spec_file=args.spec
        )

        if return_code != 0:
            print("Build failed with exit code:", return_code)
            sys.exit(return_code)


if __name__ == "__main__":
    main()