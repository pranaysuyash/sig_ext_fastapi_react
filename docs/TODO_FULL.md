# Full Launch Roadmap

This document mirrors the full backlog we've been tracking. It's grouped by area and uses statuses: [x] done • [~] in progress • [ ] pending • [s] skip/later.

**Progress: 18 done / 6 in-progress / 13 pending / 3 skip-for-now**

Legend:

- Top 10 Launch = must-have for initial release
- Next Phase = implement after launch if needed
- [s] = skip for first release (defer to v2 or optional)

## Top 10 launch gate (10)

- [x] Auto-preview on selection/threshold changes (remove manual Preview)
- [x] Export/Save enablement tied to preview existence
- [x] Rotate CW/CCW with re-upload as new session
- [x] “My Signatures” local library (save/list/delete)
- [x] Library double-click opens into Source pane (re-uploads to backend)
- [x] Fit-to-view improved for transparent images
- [x] Left sidebar fixed width (avoid taking half the window)
- [x] Clearer icons + tooltips; de-dupe emoji vs system icons
- [~] Color swatch reflects current color consistently
- [x] Keyboard shortcuts for common actions (Cmd on macOS / Ctrl on others)

## Desktop UX polish (7)

- [x] Lighter native look on macOS (minimal custom styles)
- [ ] Ensure right pane dominance and splitter behavior across window sizes
- [x] Clipboard: Copy result PNG with transparency
- [ ] Quick export presets (PNG transparent, JPG white background)
- [x] JSON metadata export (bounds, threshold, color)
- [ ] Better status messages + unobtrusive errors
- [ ] Drag-and-drop to open image into Source

## Library behavior (5)

- [x] Save extracted PNG with timestamped filename
- [x] Delete via context menu
- [x] Limit list to 50 recent
- [x] Show human-friendly names and times
- [x] Opening loads into Source and resets preview

## Color and selection (3)

- [ ] Eyedropper / average color from selection
- [ ] Threshold ramp preview (quick compare)
- [ ] Live selection size while dragging; nudge selection with arrow keys

## Backend (3)

- [ ] Clean up commented/duplicate code
- [ ] Confirm port 8001 across docs, tests, and desktop client
- [ ] Smoke tests: /health, upload, process round-trip

## Packaging and distribution (3)

- [ ] PyInstaller spec for macOS bundle
- [ ] Unsigned DMG for early adopters; add Gatekeeper bypass notes
- [ ] Code signing + notarization (post-early access)

## Commerce (2)

- [ ] Create Gumroad product and set GUMROAD_PRODUCT_URL in .env; wire Buy action
- [ ] Product page copy (benefits, usage GIF, FAQ, support/contact)

## Licensing and evaluation (3)

- [~] HIGH: Evaluation Mode Gate (Soft) — non-blocking banner + periodic reminder; no feature gating
- [ ] Optional watermark toggle for evaluation exports (off by default)
- [ ] Local license storage UX polish (Enter/Change license; no hard gate)

## Docs and comms (1)

- [ ] Update README with desktop-only instructions and quickstart screenshots

---

Notes

- This file is the authoritative full list. For a condensed “Top 10” tracker, see docs/TODO.md.
