# SignKit - Professional Signature Extractor

<div align="center">

**Extract signatures from documents with precision control**

[![License](https://img.shields.io/badge/license-Commercial-blue.svg)](legal/EULA.md)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)](#installation)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](docs/CHANGELOG.md)

[Download](#download) • [Features](#features) • [Documentation](docs/) • [Support](#support)

</div>

---

## Overview

SignKit (formerly Signature Extractor) is a professional desktop application that extracts signatures from images and documents with pixel-perfect precision. Designed for legal professionals, businesses, and anyone who needs to digitize signatures while maintaining complete privacy.

### Why SignKit?

- **🔒 Privacy-First**: All processing happens locally on your machine - no cloud uploads
- **🎯 Precision Controls**: Zoom, pan, rotate, and fine-tune threshold for perfect extraction
- **📄 PDF Integration**: Sign PDFs directly with your extracted signatures
- **💾 Library Management**: Save and reuse signatures across documents
- **⚡ Offline Operation**: Core features work without internet connection
- **🖥️ Native Desktop**: Professional Qt-based interface for macOS, Windows, and Linux

---

## Features

### Core Capabilities

- **Intelligent Extraction**: OpenCV-based processing removes backgrounds automatically
- **Interactive Selection**: Click-and-drag selection with real-time preview
- **Advanced Controls**:
  - Threshold adjustment (0-255) for black/white separation
  - Custom color selection for signature appearance
  - Rotation support (90° increments)
  - EXIF auto-rotation for mobile photos
- **Export Options**:
  - PNG with transparency (perfect for overlays)
  - JPG with background
  - Metadata export (JSON with coordinates, DPI, timestamp)
  - Copy to clipboard
- **PDF Operations** (Licensed):
  - View PDFs with signature overlay preview
  - Batch PDF signing
  - Audit trail with signing metadata
- **Library Management**:
  - Local storage of extracted signatures
  - Quick access and reuse
  - Timestamped organization

### Technical Highlights

- **Hybrid Architecture**: Desktop-first with optional backend for future cloud features
- **Security**: Input validation, path sanitization, resource limits
- **Cross-Platform**: Native builds for macOS (ARM64/Intel), Windows, Linux
- **Professional UI**: macOS-native styling with light/dark mode support

---

## Download

### Latest Release

**Version 1.0.0** - [Release Notes](docs/CHANGELOG.md)

| Platform | Download | Size | Notes |
|----------|----------|------|-------|
| **macOS (Apple Silicon)** | [SignatureExtractor_ARM64.dmg](#) | ~125MB | M1/M2/M3/M4 Macs |
| **macOS (Intel)** | [SignatureExtractor_Intel.dmg](#) | ~125MB | Intel Macs |
| **Windows 10/11** | [SignatureExtractor-Windows.zip](#) | ~130MB | 64-bit |
| **Linux** | [SignatureExtractor-Linux.AppImage](#) | ~135MB | Ubuntu 20.04+ |

**Purchase**: [Buy License on Gumroad](https://pranaysuyash.gumroad.com/l/signkit-v1) - **$29** (one-time payment)

**Free Trial**: Download and use with limited features. Unlock full functionality with a license.

---

## Installation

### macOS

1. Download the appropriate DMG file for your Mac
2. Open the DMG and drag SignatureExtractor.app to Applications
3. **First launch**: Right-click the app → "Open" → Click "Open" in the dialog
   - This is required for unsigned apps (notarization coming soon)
4. Enter your license key when prompted (or try the free trial)

**Troubleshooting**: If you see "app cannot be opened," go to System Preferences → Security & Privacy → General → Click "Open Anyway"

### Windows

1. Download and extract `SignatureExtractor-Windows.zip`
2. Run `SignatureExtractor.exe`
3. If Windows Defender shows a warning, click "More info" → "Run anyway"
   - This is normal for new applications (code signing coming soon)
4. Create a desktop shortcut for easy access
5. Enter your license key when prompted

### Linux

```bash
# Download AppImage
wget [download-url]/SignatureExtractor-Linux.AppImage

# Make executable
chmod +x SignatureExtractor-Linux.AppImage

# Run
./SignatureExtractor-Linux.AppImage

# Optional: Install system-wide
sudo cp SignatureExtractor-Linux.AppImage /usr/local/bin/signkit
```

**System Requirements**: Ubuntu 20.04+, Fedora 35+, or equivalent

For detailed installation instructions and troubleshooting, see [Installation Guide](docs/INSTALLATION_GUIDE.md).

---

## Quick Start

### Extract Your First Signature

1. **Launch SignatureExtractor**
2. **Upload Image**: Click "Upload Image" or press `Cmd/Ctrl+O`
3. **Select Region**: Click and drag to select the signature area
4. **Adjust Settings**:
   - Move the **Threshold** slider to refine black/white separation
   - Click **Color** to change signature color (optional)
5. **Preview**: See real-time preview of extracted signature
6. **Export**:
   - Click "Save to Library" to save for later use
   - Click "Export PNG" to save as a file
   - Click "Copy" to copy to clipboard

### Sign a PDF

1. Go to the **PDF** tab
2. Click "Open PDF"
3. Select a saved signature from "My Signatures"
4. Click on the PDF where you want to place the signature
5. Resize and position as needed
6. Click "Sign PDF" to save

For detailed workflows and use cases, see [User Guide](docs/USER_GUIDE.md).

---

## Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 5 minutes
- **[User Guide](docs/USER_GUIDE.md)** - Complete feature walkthrough
- **[Installation Guide](docs/INSTALLATION_GUIDE.md)** - Detailed installation instructions
- **[Keyboard Shortcuts](docs/SHORTCUTS.md)** - Speed up your workflow
- **[Use Cases](docs/USE_CASES.md)** - 20+ real-world applications
- **[FAQ](docs/FAQ.md)** - Common questions and answers
- **[Troubleshooting](docs/INSTALLATION_GUIDE.md#troubleshooting)** - Solve common issues

### For Developers

- **[Architecture](docs/ARCHITECTURE_FINAL_DECISION.md)** - System design and decisions
- **[Security](docs/SECURITY.md)** - Security measures and limitations
- **[Contributing](docs/QUICK_START.md#development)** - Build from source
- **[API Documentation](.github/copilot-instructions.md)** - Backend and desktop app APIs

---

## Licensing

### Free Trial

- ✅ Full signature extraction
- ✅ Preview and image controls
- ❌ Export disabled (trial mode)
- ❌ PDF signing disabled

### Paid License ($29 one-time)

- ✅ **Everything in Free Trial**
- ✅ **Unlimited exports** (PNG, JPG, clipboard)
- ✅ **PDF signing** with audit logs
- ✅ **Library management** (save/reuse signatures)
- ✅ **Priority support**
- ✅ **30-day money-back guarantee**

**Test License**: Use `pranay@example.com` for testing (development only)

[Purchase License](https://pranaysuyash.gumroad.com/l/signkit-v1) | [View EULA](legal/EULA.md) | [Privacy Policy](legal/PRIVACY_POLICY.md)

---

## Use Cases

### Legal & Business
- Contract digitization and e-signing
- Document automation workflows
- Client signature collection
- Legal document processing

### Healthcare & Education
- Medical form digitization
- Patient consent forms
- Academic certificate processing
- Educational document management

### Creative & Personal
- Email signature creation
- Graphic design assets
- Art authentication
- Personal document signing

See [Use Cases](docs/USE_CASES.md) for 20+ detailed scenarios.

---

## Support

### Get Help

- **📧 Email**: [support@signkit.work](mailto:support@signkit.work)
- **📚 Documentation**: [docs/](docs/)
- **❓ FAQ**: [docs/FAQ.md](docs/FAQ.md)
- **🐛 Report Issues**: Email support with diagnostic report (Help → Generate Diagnostic Report)

**Response Times**:
- Critical issues: 24-48 hours
- Technical support: 2-3 business days
- General inquiries: 3-5 business days

### Refund Policy

**30-day money-back guarantee** - no questions asked. Email support@signkit.work with your order number.

---

## Technology

### Built With

**Desktop App**:
- PySide6 (Qt6) - Native UI framework
- OpenCV 4.12 - Image processing
- Pillow 12.0 - Image manipulation
- PyMuPDF 1.26 - PDF rendering and signing

**Backend** (optional component):
- FastAPI 0.120 - REST API
- SQLAlchemy 2.0 - Database ORM
- Uvicorn - ASGI server

**Build & Distribution**:
- PyInstaller - Application bundling
- GitHub Actions - CI/CD pipeline
- DMG/AppImage/Installer - Platform-specific packages

---

## Development

### Build from Source

```bash
# Clone repository
git clone https://github.com/pranaysuyash/sig_ext_fastapi_react.git
cd sig_ext_fastapi_react

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r desktop_app/requirements.txt

# Run desktop app
python desktop_app/main.py
```

### Build Distributable

```bash
# Install build tools
pip install -r build-tools/requirements-build.txt

# Build for current platform
python -m PyInstaller build-tools/SignatureExtractor_macOS.spec  # macOS
python -m PyInstaller build-tools/SignatureExtractor_Windows.spec  # Windows
python -m PyInstaller build-tools/SignatureExtractor_Linux.spec  # Linux

# Output in dist/ folder
```

See [Quick Start](docs/QUICK_START.md) for detailed development setup.

---

## Roadmap

### Version 1.1 (Q1 2026)
- [ ] Auto-detection of signatures using contour analysis
- [ ] Batch processing for multiple signatures
- [ ] Cloud backup (optional, opt-in)
- [ ] Browser extension for quick extraction

### Version 1.2 (Q2 2026)
- [ ] OCR integration for signature metadata
- [ ] Template system for recurring documents
- [ ] API tier for developers
- [ ] Mobile companion app

See [Roadmap](docs/ROADMAP.md) for full feature planning.

---

## Privacy & Legal

- **Privacy Policy**: [legal/PRIVACY_POLICY.md](legal/PRIVACY_POLICY.md)
- **Terms of Service**: [legal/TERMS_OF_SERVICE.md](legal/TERMS_OF_SERVICE.md)
- **EULA**: [legal/EULA.md](legal/EULA.md)

**Privacy Commitment**: SignKit processes all signatures locally on your device. No images are uploaded to external servers unless you explicitly enable optional cloud features (coming in future versions).

---

## License

Copyright © 2025 PSRS Tech. All rights reserved.

This is commercial software. See [EULA](legal/EULA.md) for license terms.

**Test/Evaluation License**: Free trial available with limited features.
**Full License**: $29 one-time payment via Gumroad.

---

## Acknowledgments

- OpenCV team for computer vision libraries
- Qt Project for cross-platform UI framework
- PyMuPDF contributors for PDF support
- All beta testers and early adopters

---

<div align="center">

**Made with ❤️ by [PSRS Tech](https://psrstech.com)**

[Website](https://signkit.work) • [Twitter](https://twitter.com/signkit) • [Support](mailto:support@signkit.work)

</div>
