# Help & Troubleshooting

This guide covers common questions and quick fixes for the desktop app.

## PDF Signing Features (NEW)

**Q: How do I sign a PDF with my extracted signature?**

1. Extract and save signatures to your library (existing workflow)
2. Go to **PDF → Open PDF** (Ctrl+Shift+O) to load a PDF document
3. Currently uses programmatic API - full UI coming soon
4. Signatures are embedded using pikepdf (QPDF library)
5. All operations are logged for audit compliance

**Q: Where are audit logs stored?**

- Location: `~/.signature_extractor/audit_logs/`
- Format: JSONL (one JSON object per line)
- View logs: **PDF → View Audit Logs**
- Each log entry includes: timestamp, operation, user, details

**Q: PDF menu doesn't appear**

- PDF features require `pypdfium2` and `pikepdf` libraries
- Install: `pip install pypdfium2 pikepdf`
- App gracefully degrades without them (signature extraction still works)

**Q: Can I verify signed PDFs?**

- Yes! Open signed PDFs in any standard PDF viewer (Preview, Adobe, etc.)
- Signatures are embedded as images in the PDF structure
- Audit logs provide compliance trail with timestamps

## Quick Answers

- Clean Viewport vs Clear Selection

  - Clear Selection: removes the current rubber‑band and hides preview/result panes.
  - Clean Viewport: clears source/preview/result panes, resets session id, and disables dependent actions until a new upload.

- Source Rotate vs Preview/Result Rotate

  - Source rotate re‑uploads a rotated image (new session) and clears selection because coordinates change.
  - Preview/Result rotate is view‑only for display; it does not change underlying pixels.

- Rotation‑Aware Selection

  - Selections survive zoom/pan/fit/resize/rotation. The app stores the 4 selection corners in scene space and maps a normalized bounding box back to image pixels.
  - See Coordinate Mapping for details.

- Zoom % and Fit

  - Use the editable Zoom % combo (e.g., 125%, 50%) or choose Fit to scale the image to the active pane.
  - Reset Viewport returns the active pane to default zoom, pan, and rotation.

- Footer vs Console Logs
  - Footer shows: Viewport size, Image size, Visible bounds, Zoom %, Rotation °, Selection box.
  - After this update, the numbers match because mapping uses scene‑space bounds (rotation‑aware) and clamping.

## Common Issues

- My photo is rotated; should I rotate before selecting?

  - Yes. Rotate the source if the image is mis‑oriented, then make your selection. Source rotation re‑uploads a corrected image and resets the selection.

- I don’t see the preview/result panes

  - They only appear after a valid selection (non‑zero area). Use Selection mode (🎯) to draw a box.

- Zooming makes coordinates look off

  - Coordinates are always reported in image pixels. Zoom or Fit only affects display scale. If you suspect a mismatch, try Reset Viewport and confirm Visible bounds updates as expected.

- Threshold Auto/Manual

  - Toggling Auto disables the slider and computes a selection‑specific threshold. Switch back to manual to fine‑tune.

- Backend isn’t responding
  - Ensure FastAPI is running on 127.0.0.1:8001. Health check: http://127.0.0.1:8001/health

## Keyboard Shortcuts

See docs/SHORTCUTS.md for a full list: Open, Copy, Export, Zoom In/Out, Reset, Fit, Rotate CW/CCW.

**PDF Shortcuts**:

- `Ctrl+Shift+O` — Open PDF
- `Ctrl+Shift+S` — Save signed PDF
- `Ctrl+Shift+W` — Close PDF

## Deep Dives

- **PDF Features**: docs/PDF_QUICK_START.md (workflow guide)
- **PDF Implementation**: docs/PDF_FEATURE_IMPLEMENTATION.md (technical details)
- Desktop UI Spec: docs/desktop-frontend/pyqt-spec.md
- Coordinate Mapping: docs/COORDINATE_MAPPING.md
- Export Options: docs/EXPORT_OPTIONS.md

If you still have issues, capture a screenshot of the footer metrics and your console output and include your OS + steps to reproduce.
