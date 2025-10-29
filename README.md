# Signature Extractor App

**Desktop-first signature extraction tool** with precision control for extracting signatures from documents.

✨ **Features**:
- 🎯 Precision selection with zoom/pan controls
- 🎨 Color customization & threshold adjustment
- 🔄 EXIF auto-rotation for mobile photos
- 💾 Export as transparent PNG with metadata
- 🔒 Privacy-focused: all processing happens locally by default
- 🖥️ Desktop app (PyQt/PySide6) with FastAPI backend

## Architecture

- **Frontend**: PySide6 desktop application (macOS, Windows, Linux)
- **Backend**: FastAPI REST API (Python 3.9+)
- **Database**: SQLite (default) or PostgreSQL (optional)
- **Processing**: OpenCV, NumPy, PIL for image manipulation

## Documentation

- **[Use Cases](docs/USE_CASES.md)** — 20+ real-world applications (legal, healthcare, design, e-signing)
- **[Pricing Strategy](docs/PRICING.md)** — Freemium model with Pro/Team/Enterprise tiers
- **[Product Roadmap](docs/ROADMAP.md)** — 8-phase development plan (auto-recognition, integrations, deployment)
- **[Recent Updates](docs/RECENT_UPDATES.md)** — Latest UX fixes and improvements
- **[UI Changes Guide](docs/UI_CHANGES.md)** — Visual before/after walkthrough
- **[Desktop UI Spec](docs/desktop-frontend/pyqt-spec.md)** — Controls (Zoom %, Fit, Reset/Clean, Rotate) and status bar fields
- **[Coordinate Mapping](docs/COORDINATE_MAPPING.md)** — Rotation-aware scene→image mapping details
- **[Shortcuts](docs/SHORTCUTS.md)** — Keyboard shortcuts for common actions
 - **[Help & Troubleshooting](docs/HELP.md)** — Quick fixes and FAQs

## Quick Start

### 1. Backend Setup

Create `.env` at repo root:

```env
JWT_SECRET=replace-with-secure-string

# SQLite (recommended for local use):
DATABASE_URL=sqlite:///backend/data/app.db

# OR PostgreSQL (optional):
# DATABASE_HOSTNAME=localhost
# DATABASE_PORT=5432
# DATABASE_USERNAME=your_user
# DATABASE_PASSWORD=your_password
# DATABASE_NAME=signature_extractor
```

Run backend:

```zsh
# Optional: Initialize DB (auto-creates SQLite file)
python backend/setup_db.py

# Start server
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8001
```

Health check: <http://127.0.0.1:8001/health>

### 2. Desktop App

Install dependencies:

```zsh
pip install PySide6 requests python-dotenv pillow opencv-python numpy
```

Run app:

```zsh
python -m desktop_app.main
```

## Recent Updates (Oct 2025)

✅ **Fixed & Enhanced UX**:
- Selection vs pan conflict (added mode toggle)
- EXIF orientation handling (auto-rotate mobile photos)
- Result visibility (white background for transparency)
- Progressive disclosure (hide panes until selection made)
 - Rotation-aware selection mapping that persists through zoom/pan/fit/resize/rotation
 - New View controls: Zoom In/Out, editable Zoom % combo (with Fit), Reset Viewport, Rotate
 - Clean Viewport action to clear all panes and session; Clear Selection kept separate
 - Status bar shows Viewport, Image, Visible bounds, Zoom, Rotation, Selection

✅ **Documentation**:
- Comprehensive use cases (20+ scenarios)
- Pricing strategy (4 tiers, revenue projections)
- Product roadmap (auto-recognition, integrations, deployment)

✅ **Cleanup**:
- Removed React frontend (simplified to desktop-only)
- SQLite as default DB (no Postgres required)
- Updated all docs and specs

## Use Cases

### Core Applications
1. **Contract Management & E-Signing** — Extract signatures for DocuSign/Adobe Sign
2. **Document Digitization** — Archive paper documents with signature preservation
3. **Identity Verification (KYC)** — Banks, fintech signature consistency checks
4. **Graphic Design & Branding** — Personal signature for emails, business cards
5. **Medical Forms** — Patient consent form signatures for EMR integration

### Advanced Use Cases
- Legal document comparison & forensic analysis
- Real estate transaction processing
- API integration for SaaS platforms
- Browser extension for quick extraction
- Notarization & apostille services
- Insurance claims processing

See **[full use case guide](docs/USE_CASES.md)** for 20+ detailed scenarios.

## Pricing

- 🆓 **Free**: Desktop app with unlimited local extractions
- 💼 **Pro** ($12/mo): Cloud sync, browser extension, batch processing
- 🏢 **Team** ($30/user/mo): Shared workspace, API access, webhooks
- 🚀 **Enterprise** (custom): On-premise, SSO, HIPAA compliance

See **[pricing strategy doc](docs/PRICING.md)** for complete tier comparison and revenue projections.

## Development

### Project Structure

```
signature-extractor-app/
├── backend/                 # FastAPI server
│   ├── app/
│   │   ├── routers/        # Auth & extraction endpoints
│   │   ├── models/         # SQLAlchemy models
│   │   ├── crud/           # Database operations
│   │   └── utils/          # Auth, dependencies
│   ├── uploads/            # Image storage
│   └── setup_db.py         # DB initialization
├── desktop_app/            # PySide6 desktop UI
│   ├── views/              # Main window, widgets
│   ├── api/                # Backend client
│   ├── state/              # Session management
│   └── config.py           # App configuration
├── docs/                   # Documentation
│   ├── USE_CASES.md        # Real-world applications
│   ├── PRICING.md          # Business model
│   ├── ROADMAP.md          # Product development plan
│   └── RECENT_UPDATES.md   # Changelog
└── README.md               # This file
```

### Next Steps (Roadmap Phase 2)

1. **Icons & Visual Polish** — QIcon for buttons, app icon, color theme
2. **Rotate Buttons** — 90° CW/CCW with re-upload
3. **Export Metadata** — JSON output with bbox, timestamp, settings
4. **Auto-Detection** — OCR (Tesseract) and signature recognition (contours/ML)
5. **Browser Extension** — Chrome/Firefox for quick extraction
6. **Packaging** — PyInstaller/Nuitka for distributable binaries

See **[full roadmap](docs/ROADMAP.md)** for 8-phase development plan.

## Contributing

Contributions welcome! Focus areas:
- Desktop UX improvements (icons, themes, shortcuts)
- Image processing enhancements (morphology, edge detection)
- Integration plugins (DocuSign, Zapier, etc.)
- Documentation and tutorials

## License

[Add license here — suggest MIT or Apache 2.0 for open-source]

## Support

- **Issues**: [GitHub Issues](https://github.com/pranaysuyash/sig_ext_fastapi_react/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pranaysuyash/sig_ext_fastapi_react/discussions)
- **Email**: [Add support email]

---

**Built with** ❤️ for professionals who need precision and privacy in signature extraction.
