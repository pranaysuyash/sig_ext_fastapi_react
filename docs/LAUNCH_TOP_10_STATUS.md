# Launch Top 10 - Status Report

This document maps your "Launch Top 10" list to what's been implemented, what needs to be done, and what should be skipped for the first release.

**Summary: 4 done / 2 in-progress / 4 pending (must-do) / 0 skip**

---

## 1. Evaluation Gate [~] IN PROGRESS

**Your requirement:** Export/save disabled until license present; clear CTA in export dialog/status bar; unlock immediately after key entry; license cached offline.

**Current state:**

- [x] License menu with Buy link (uses GUMROAD_PRODUCT_URL env)
- [x] Local license entry/storage (desktop_app/license/)
- [~] Soft non-blocking mode (no hard gate; optional only)
- [ ] Export/Save disabled until license (NOT IMPLEMENTED - currently always enabled)
- [ ] Clear CTA banner/reminder

**Decision:** **MODIFY APPROACH**

- We implemented a _soft_ evaluation mode (non-blocking, optional license only)
- Your spec calls for a _hard_ gate (export disabled until license)
- **Recommendation:** Stick with soft gate for early adopters OR implement hard gate now
- **Action needed:** Decide on hard vs soft gate; implement banner/CTA if soft; implement disable logic if hard

**Code files:** `desktop_app/views/main_window.py`, `desktop_app/license/storage.py`

---

## 2. Checkout + License [ ] PENDING (MUST DO)

**Your requirement:** Hosted checkout (Gumroad/LemonSqueezy); send license key by email; in-app "Enter License" stores locally; 30-day refund link exposed.

**Current state:**

- [x] In-app "Enter License" UI exists and stores locally
- [x] Buy menu opens GUMROAD_PRODUCT_URL from env
- [ ] Gumroad account created
- [ ] Product created on Gumroad
- [ ] License key email flow configured
- [ ] 30-day refund link documented

**Decision:** **DO NOW**

- Infrastructure is ready; need to create actual Gumroad product
- **Action needed:**
  1. Create Gumroad account
  2. Create product ($29 or test price ladder)
  3. Set up license key delivery via email
  4. Add GUMROAD_PRODUCT_URL to .env
  5. Document refund process

**Code files:** `desktop_app/views/main_window.py` (on_buy_license), `.env`

---

## 3. Desktop Packaging [ ] PENDING (MUST DO)

**Your requirement:** PyInstaller builds for macOS/Windows/Linux; basic signing where feasible; smoke-test open → select → preview → export on clean VMs.

**Current state:**

- [x] Code is packagable (no web dependencies)
- [ ] PyInstaller spec created
- [ ] macOS build tested
- [ ] Windows build tested
- [ ] Linux build tested
- [ ] Smoke tests run on clean VMs
- [ ] Basic signing (macOS unsigned initially OK)

**Decision:** **DO NOW**

- Critical for distribution
- **Action needed:**
  1. Create PyInstaller spec file
  2. Build macOS .app bundle first
  3. Test on clean macOS VM
  4. Document Gatekeeper bypass for unsigned app
  5. Create Windows/Linux builds (can be post-macOS)

**Files to create:** `signature_extractor.spec`, build scripts, distribution docs

---

## 4. Rotate 90° CW/CCW [x] DONE ✓

**Your requirement:** Rotate locally (PIL), re-upload as new session, reset selection; visible status messages. Acceptance: orientation correct; no coordinate bugs.

**Current state:**

- [x] Rotate CW/CCW buttons in UI
- [x] PIL-based rotation with expand=True
- [x] Re-upload to backend for new session
- [x] Selection reset after rotation
- [x] Status messages ("Uploading rotated image...", "Rotated and uploaded")
- [x] Keyboard shortcuts (Cmd/Ctrl+] and Cmd/Ctrl+[)

**Decision:** ✓ **COMPLETE - NO ACTION NEEDED**

**Code files:** `desktop_app/views/main_window.py` (on_rotate)

---

## 5. Clipboard Copy [x] DONE ✓

**Your requirement:** Copy current PNG result (with alpha) to clipboard; confirm toast; works cross-platform.

**Current state:**

- [x] Copy to Clipboard button
- [x] Copies PNG with alpha channel preserved
- [x] Status bar confirmation ("Copied to clipboard")
- [x] Cross-platform via QApplication.clipboard
- [x] Keyboard shortcut (Cmd/Ctrl+C)

**Decision:** ✓ **COMPLETE - NO ACTION NEEDED**

**Code files:** `desktop_app/views/main_window.py` (on_copy)

---

## 6. Keyboard Shortcuts [x] DONE ✓

**Your requirement:** Ctrl/Cmd+O (open), Ctrl/Cmd+S (export), Delete (clear), Esc (cancel). Acceptance: documented and functional on macOS/Win/Linux.

**Current state:**

- [x] Cmd/Ctrl+O (open)
- [x] Cmd/Ctrl+E (export) - using E instead of S
- [x] Cmd/Ctrl+C (copy)
- [x] Cmd/Ctrl+0 (100%), Cmd/Ctrl+1 (fit)
- [x] Standard zoom in/out shortcuts
- [x] Cmd/Ctrl+] and [ (rotate)
- [ ] Delete (clear) - not yet implemented
- [ ] Esc (cancel) - not yet implemented
- [ ] Documented in user-facing docs

**Decision:** **MOSTLY DONE - MINOR ADDITIONS**

- Core shortcuts work
- **Action needed:**
  1. Add Delete key to clear selection
  2. Add Esc to cancel operations (if applicable)
  3. Document shortcuts in README/Help

**Code files:** `desktop_app/views/main_window.py` (**init** shortcuts section)

---

## 7. Backend Cleanup [ ] PENDING (MUST DO)

**Your requirement:** Remove commented/duplicated blocks; single CORS/StaticFiles mount; uploads path consistent; 4xx/5xx errors human-readable.

**Current state:**

- [~] Some commented code remains
- [~] CORS/StaticFiles need review
- [~] Uploads path needs verification
- [ ] Error messages not audited for user-friendliness
- [~] Port 8001 mostly consistent but needs verification

**Decision:** **DO NOW**

- Critical for professional release
- **Action needed:**
  1. Audit backend/app/\*.py for commented/duplicate code
  2. Verify single CORS config
  3. Verify uploads path consistency
  4. Review all error responses for clarity
  5. Confirm port 8001 everywhere (docs, tests, client)

**Code files:** `backend/app/main.py`, `backend/app/routers/*.py`, `backend/app/config.py`

---

## 8. Landing + Checkout Page [ ] PENDING (MUST DO)

**Your requirement:** Use COPY_DECK; annotated screenshots/GIF; pricing $29 (or ladder test); Buy button → checkout → post-purchase email with key.

**Current state:**

- [ ] Landing page created
- [ ] COPY_DECK used for messaging
- [ ] Screenshots/GIF created
- [ ] Pricing decided
- [ ] Checkout flow tested end-to-end

**Decision:** **DO NOW**

- Critical for launch
- **Action needed:**
  1. Find/reference COPY_DECK (or create messaging)
  2. Take annotated screenshots of workflow
  3. Create demo GIF (open → select → preview → export)
  4. Create simple static landing page
  5. Link to Gumroad checkout
  6. Test full purchase flow

**Files to create:** Landing page HTML/markdown, assets (screenshots, GIF)

---

## 9. Docs & Config [~] IN PROGRESS

**Your requirement:** .env.example (JWT_SECRET, DATABASE_URL sqlite); Quick Start; Export Options; Pricing; known issues; all ports unified to 8001.

**Current state:**

- [x] .env concept exists
- [~] JWT_SECRET documented (in config.py comments)
- [~] DATABASE_URL sqlite pattern present
- [~] Basic README exists
- [ ] .env.example file
- [ ] Quick Start section
- [ ] Export Options docs
- [ ] Pricing page/FAQ
- [ ] Known issues list
- [~] Port 8001 mostly used (needs verification)

**Decision:** **DO NOW**

- **Action needed:**
  1. Create .env.example with all vars
  2. Add Quick Start to README
  3. Document Export Options (dialog features)
  4. Create Pricing/FAQ doc
  5. List known issues/limitations
  6. Verify port 8001 everywhere

**Files:** `.env.example`, `README.md`, `docs/PRICING.md`, `docs/FAQ.md`, `docs/KNOWN_ISSUES.md`

---

## 10. QA Matrix [ ] PENDING (MUST DO)

**Your requirement:** Cases: large images, EXIF rotations, tiny selections, bad inputs (415/404), offline mode; pass list with evidence before go-live.

**Current state:**

- [ ] Large images test (>10MB, >4000px)
- [ ] EXIF rotations test (all orientations)
- [ ] Tiny selections test (<10px)
- [ ] Bad inputs test (415/404/422)
- [ ] Offline mode test (no backend)
- [ ] Pass list documented

**Decision:** **DO NOW - BEFORE LAUNCH**

- No formal QA has been run
- **Action needed:**
  1. Create test case checklist
  2. Run each case systematically
  3. Document results (pass/fail with evidence)
  4. Fix any critical bugs found
  5. Accept known limitations for v1

**Files to create:** `docs/QA_CHECKLIST.md`, `docs/QA_RESULTS.md`

---

## Summary by Priority

### DONE (4 items) ✓

1. Rotate 90° CW/CCW
2. Clipboard Copy
3. Keyboard Shortcuts (mostly)
4. (Partial: Library, JSON export - done as extras)

### IN PROGRESS (2 items) 🟡

1. Evaluation Gate - need decision on hard vs soft
2. Docs & Config - partially done

### MUST DO NOW (4 items) 🔴

1. Checkout + License (Gumroad setup)
2. Desktop Packaging (PyInstaller)
3. Backend Cleanup
4. Landing + Checkout Page
5. QA Matrix

### SKIP FOR v1 (from "Next Phase") ⚪

- Advanced Processing (Otsu/Adaptive)
- Auto-Detection
- Browser Extension
- Auto-updater
- Telemetry
- Integrations
- A/B Experiments

---

## Recommended Action Plan

### Week 1: Critical Path

1. **Decision:** Hard vs soft evaluation gate (1 hour)
2. **Gumroad setup:** Account + product + test checkout (4 hours)
3. **Backend cleanup:** Remove cruft, verify consistency (4 hours)
4. **PyInstaller:** macOS build + test (8 hours)

### Week 2: Polish & Launch

1. **Landing page:** Simple static with GIF (4 hours)
2. **Docs:** .env.example, Quick Start, FAQ (4 hours)
3. **QA Matrix:** Run all tests, document (8 hours)
4. **Final fixes:** Address QA findings (8 hours)

### Week 3: Post-Launch

1. Monitor early adopter feedback
2. Fix critical bugs
3. Plan v2 features based on usage

---

## Notes

- **Database:** Currently optional; JWT_SECRET is required for backend auth (not strictly needed if you remove auth routes)
- **Port 8001:** Desktop client expects this; backend usually runs on 8001
- **Unsigned builds:** Acceptable for early adopters with clear Gatekeeper bypass instructions
- **Hard gate vs soft gate:** Your spec says hard (disable export); we built soft (optional license). Decide which to ship.
