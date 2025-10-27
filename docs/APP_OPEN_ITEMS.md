# App Open Items (Launch-Focused)

Use this list to track app-side tasks only (no web or backend infra beyond what’s surfaced in-app). Keep this aligned with LAUNCH_TOP_10_STATUS.md.

## In‑App UX/Features
- [x] Rotate 90° CW/CCW with re‑upload and selection reset (main_window.py:on_rotate)
- [x] Clipboard Copy of PNG with alpha (Copy button + Ctrl/Cmd+C)
- [~] Keyboard Shortcuts — Open/Export/Copy/Zoom/Rotate implemented; still add Delete (clear) + Esc (cancel) and document in Help
- [x] Library MVP — auto-save, list, double-click open, context delete (library/storage.py + main_window)
- [x] Export Metadata JSON saved alongside PNG (Export JSON button)
- [ ] Drag‑and‑drop to open image; Recent files (last 5)
- [ ] Improve error toasts: backend offline, 404/415, 500, disk full, large image guidance (friendly, actionable messages)
- [ ] Optional advanced processing: Otsu/Adaptive thresholds, erode/dilate, edge smoothing (post-launch)

## Licensing/Checkout (In‑App Surfaces)
- [x] Wire Buy link (env‑configurable) and “Enter License” dialog to store key locally
- [ ] Finalize Evaluation Mode strategy: either enforce hard gate (disable export/save until licensed) or intentionally ship soft gate with clear CTA copy
- [ ] Surface 30‑day refund link in Help/About

## Platform Polish
- [x] Consistent icons (system icons via resources/icons; emoji only as fallback)
- [~] Tooltips present; still add Keyboard shortcuts cheat sheet under Help
- [x] Native feel: macOS uses default style; platform shortcuts use Cmd vs Ctrl

## Help & Docs (Accessed from App)
- [ ] Help menu links: Quick Start, Export Options, Shortcuts, Troubleshooting, Privacy, Terms/EULA
- [ ] “Report issue / Send diagnostics” opens logs folder + prefilled email template

## Packaging/Release Touchpoints
- [ ] PyInstaller builds for macOS/Windows/Linux; include readme/how‑to
- [ ] “How to open on macOS” instructions for unsigned builds
- [ ] Versioned artifact names and checksums; CHANGELOG entry per release

## Config & Consistency
- [ ] Unify ports to 8001 across desktop docs and in‑app references (desktop_app/README still cites 8000)
- [ ] Add .env.example (API_BASE_URL, JWT_SECRET, DATABASE_URL for SQLite)

## Analytics (Opt‑In)
- [ ] Settings toggle “Help improve the app” (default off)
- [ ] If enabled, minimal events: start, selection, preview rendered, export success, Buy clicked

## Legal/Policy Surfaces
- [ ] Link Privacy Policy, Terms/EULA from Help
- [ ] Third‑party notices from About

## QA Matrix
- [ ] Clean VM tests: macOS/Win/Linux — open → select → preview → rotate → export; EXIF photos; large scans; tiny selections; invalid file types; offline backend
- [ ] Performance: preview latency target; memory sanity on >20MP

## Samples/Assets
- [ ] Bundle or link 6–10 sample documents; confirm licensing
- [ ] Two short GIFs for Quick Start (select/preview, export)

Notes
- When an item moves to “done”, update LAUNCH_TOP_10_STATUS.md with acceptance evidence (e.g., screenshot path, test note).
