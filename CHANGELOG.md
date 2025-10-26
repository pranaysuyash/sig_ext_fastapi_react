# Changelog

## [Unreleased] - 2025-10-26

### Added

- **Professional Export Dialog** with industry-standard options:

  - Format selection: PNG-24, PNG-8 (palette), JPEG
  - Background options: Transparent, White, Black, Custom color
  - Trim to content bounds with configurable padding (0-100px)
  - JPEG quality control (1-100%)
  - Defaults to `.png` extension
  - Inspired by Adobe Photoshop and Affinity Photo workflows

- **Save to Library** quick-save button:

  - Auto-generated filenames with timestamp: `signature_YYYYMMDD_HHMMSS.png`
  - Defaults to PNG format with transparency
  - Prepared for integration with persistent library directory

- **Button Tooltips** for clarity:
  - Preview: "Process the selected region with current threshold and color settings"
  - Export: "Export with advanced options (background, trim, format)"
  - Save to Library: "Quick save as PNG to local library"

### Changed

- Renamed "Save Result" button to "Export..." to better reflect professional export workflow
- Export and Save to Library buttons now properly enable/disable based on result availability
- Clear Selection now properly resets both export buttons

### Documentation

- Added `docs/EXPORT_OPTIONS.md` with comprehensive guide:
  - Button function explanations
  - Format recommendations by use case (signatures, documents, web, print)
  - Technical details on trim algorithm, background compositing, format conversion
  - Comparison with industry tools
  - Best practices guide

### Fixed

- Corrected import paths for `ApiClient`, `SessionState`, and `ImageView`
- Export dialog properly handles transparency vs solid backgrounds
- JPEG export correctly removes alpha channel

### Technical

- Export dialog uses PIL for advanced image processing
- Implements alpha_composite for proper background blending
- Adaptive palette quantization for PNG-8 format
- Content-aware trimming using alpha channel bounding box
