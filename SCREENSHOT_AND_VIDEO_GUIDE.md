# 📸 Complete Screenshot & Video Creation Guide

**For:** SignKit Launch  
**Date:** Sunday, November 16, 2025  
**Time Needed:** ~6 hours total

---

## 📸 PART 1: SCREENSHOTS (2-3 hours)

### Preparation (15 minutes)

#### 1. Set Up Your Workspace
```bash
# Create screenshot folder
mkdir -p ~/Desktop/SignKit-Screenshots-Nov16

# Prepare sample files
# You'll need:
# - A signature image (scan or photo)
# - A sample PDF document
```

#### 2. Clean Your Desktop
- Close unnecessary applications
- Hide menu bar items (optional)
- Set desktop to clean wallpaper
- Disable notifications (Do Not Disturb)

#### 3. Open SignKit
```bash
# Launch the app
open /Applications/SignatureExtractor.app

# Or from your build
open dist/SignatureExtractor_ARM64.app
```

---

### Screenshot List (12 screenshots)

#### Screenshot 1: Main Interface (Hero Shot)
**What:** Clean main window showing the interface  
**How:**
1. Open SignKit
2. Make sure window is clean (no image loaded)
3. Press `Cmd+Shift+4` → Space → Click window
4. Save as: `01-main-interface.png`

**Caption:** "SignKit - Professional signature extraction and PDF signing"

---

#### Screenshot 2: Load Image Dialog
**What:** File picker showing image selection  
**How:**
1. Click "Open Image" or File → Open
2. Navigate to your signature image
3. Press `Cmd+Shift+4` → Capture dialog
4. Save as: `02-load-image.png`

**Caption:** "Load signature images from any source"

---

#### Screenshot 3: Image Loaded
**What:** Signature image displayed in the viewer  
**How:**
1. Open your signature image
2. Make sure it's clearly visible
3. Press `Cmd+Shift+4` → Space → Click window
4. Save as: `03-image-loaded.png`

**Caption:** "View and analyze your signature image"

---

#### Screenshot 4: Drawing Selection
**What:** Selection rectangle being drawn around signature  
**How:**
1. Click "Selection Mode" button
2. Start drawing selection around signature
3. While holding mouse, press `Cmd+Shift+4` with other hand
4. Capture the selection in progress
5. Save as: `04-drawing-selection.png`

**Caption:** "Draw a selection around your signature"

---

#### Screenshot 5: Selection Complete
**What:** Completed selection rectangle around signature  
**How:**
1. Complete the selection rectangle
2. Press `Cmd+Shift+4` → Space → Click window
3. Save as: `05-selection-complete.png`

**Caption:** "Precise selection tools for perfect extraction"

---

#### Screenshot 6: Threshold Adjustment
**What:** Threshold slider being adjusted, showing preview  
**How:**
1. Adjust threshold slider to show effect
2. Make sure preview pane shows the result
3. Press `Cmd+Shift+4` → Space → Click window
4. Save as: `06-threshold-adjustment.png`

**Caption:** "Fine-tune extraction with real-time preview"

---

#### Screenshot 7: Extraction Result
**What:** Clean extracted signature in preview pane  
**How:**
1. Click "Preview" or "Extract" button
2. Wait for extraction to complete
3. Make sure result looks clean
4. Press `Cmd+Shift+4` → Space → Click window
5. Save as: `07-extraction-result.png`

**Caption:** "Get clean, professional results every time"

---

#### Screenshot 8: Signature Library
**What:** Library view showing saved signatures  
**How:**
1. Save the extracted signature to library
2. Click on Library tab or view
3. Show multiple signatures if possible
4. Press `Cmd+Shift+4` → Space → Click window
5. Save as: `08-signature-library.png`

**Caption:** "Organize and manage your signature collection"

---

#### Screenshot 9: PDF Tab Interface
**What:** PDF tab showing the interface  
**How:**
1. Click on "PDF" tab
2. Show clean PDF interface
3. Press `Cmd+Shift+4` → Space → Click window
4. Save as: `09-pdf-tab.png`

**Caption:** "Built-in PDF signing capabilities"

---

#### Screenshot 10: Load Signature Button (NEW FEATURE!)
**What:** The new "Load..." button in PDF tab  
**How:**
1. In PDF tab, locate the "Load..." button
2. Highlight or hover over it
3. Press `Cmd+Shift+4` → Capture the button area
4. Save as: `10-load-signature-button.png`

**Caption:** "Quickly load signatures from files (NEW!)"

---

#### Screenshot 11: PDF with Signature Placement
**What:** PDF document with signature being placed  
**How:**
1. Open a PDF document
2. Load or select a signature
3. Drag signature onto PDF (capture mid-drag if possible)
4. Press `Cmd+Shift+4` → Space → Click window
5. Save as: `11-pdf-signature-placement.png`

**Caption:** "Drag and drop signatures onto your PDFs"

---

#### Screenshot 12: Completed Signed PDF
**What:** Final PDF with signature placed  
**How:**
1. Complete signature placement
2. Show final result
3. Press `Cmd+Shift+4` → Space → Click window
4. Save as: `12-signed-pdf-complete.png`

**Caption:** "Professional signed documents in seconds"

---

### Post-Processing (30 minutes)

#### 1. Review Screenshots
```bash
# Open folder
open ~/Desktop/SignKit-Screenshots-Nov16

# Review each screenshot:
# - Is it clear and sharp?
# - Does it show the right feature?
# - Is the window properly captured?
# - Any sensitive info visible?
```

#### 2. Compress Images
**Option A: Using ImageOptim (Recommended)**
```bash
# Install ImageOptim (if not installed)
brew install --cask imageoptim

# Drag all screenshots into ImageOptim
# It will compress them automatically
# Target: 200-500KB per image
```

**Option B: Using TinyPNG Website**
1. Go to https://tinypng.com
2. Upload all screenshots
3. Download compressed versions
4. Replace originals

**Option C: Using Command Line**
```bash
# Install pngquant
brew install pngquant

# Compress all PNGs
cd ~/Desktop/SignKit-Screenshots-Nov16
for file in *.png; do
    pngquant --quality=65-80 --ext .png --force "$file"
done
```

#### 3. Rename for Upload
```bash
# Rename with descriptive names
cd ~/Desktop/SignKit-Screenshots-Nov16

mv 01-main-interface.png "SignKit-Main-Interface.png"
mv 02-load-image.png "SignKit-Load-Image.png"
mv 03-image-loaded.png "SignKit-Image-Loaded.png"
mv 04-drawing-selection.png "SignKit-Drawing-Selection.png"
mv 05-selection-complete.png "SignKit-Selection-Complete.png"
mv 06-threshold-adjustment.png "SignKit-Threshold-Adjustment.png"
mv 07-extraction-result.png "SignKit-Extraction-Result.png"
mv 08-signature-library.png "SignKit-Signature-Library.png"
mv 09-pdf-tab.png "SignKit-PDF-Tab.png"
mv 10-load-signature-button.png "SignKit-Load-Signature-NEW.png"
mv 11-pdf-signature-placement.png "SignKit-PDF-Placement.png"
mv 12-signed-pdf-complete.png "SignKit-Signed-PDF.png"
```

---

## 🎥 PART 2: DEMO VIDEO (2-3 hours)

### Preparation (15 minutes)

#### 1. Plan Your Script
**Total Duration:** 60-90 seconds

**Timing Breakdown:**
- Intro: 5 seconds
- Load & Select: 20 seconds
- Extract & Save: 15 seconds
- PDF Signing: 30 seconds
- Outro: 5 seconds

#### 2. Prepare Files
```bash
# You'll need:
# - Clean signature image
# - Sample PDF document
# - Clean desktop
# - SignKit app ready
```

#### 3. Set Up Recording
```bash
# Close unnecessary apps
# Hide menu bar (optional)
# Disable notifications
# Set Do Not Disturb mode
# Test audio (if adding voiceover)
```

---

### Recording (30-45 minutes)

#### Step 1: Start Recording
```bash
# Press Cmd+Shift+5
# Select "Record Entire Screen" or "Record Selected Portion"
# Click Options:
#   - Microphone: None (or your mic if adding voiceover)
#   - Show Mouse Clicks: Yes (recommended)
#   - Save to: Desktop
# Click "Record"
```

#### Step 2: Perform Workflow (60-90 seconds)

**0:00-0:05 - Intro**
- Show SignKit main interface
- Pause for 2 seconds

**0:05-0:15 - Load Image**
- Click "Open Image"
- Select signature image
- Image loads and displays

**0:15-0:25 - Draw Selection**
- Click "Selection Mode"
- Draw rectangle around signature
- Show selection clearly

**0:25-0:35 - Adjust Threshold**
- Move threshold slider
- Show preview updating
- Get clean result

**0:35-0:40 - Extract**
- Click "Preview" or "Extract"
- Show clean extracted signature

**0:40-0:45 - Save to Library**
- Click "Save to Library"
- Show save dialog
- Signature saved

**0:45-0:50 - Switch to PDF Tab**
- Click "PDF" tab
- Show PDF interface

**0:50-0:55 - Open PDF**
- Click "Open PDF"
- Select sample PDF
- PDF loads

**0:55-1:05 - Load Signature (NEW!)**
- Click "Load..." button
- Select signature from file
- Or select from library

**1:05-1:15 - Place Signature**
- Drag signature onto PDF
- Position it properly
- Show placement

**1:15-1:20 - Save PDF**
- Click "Save" or "Save As"
- Show save dialog
- PDF saved

**1:20-1:25 - Outro**
- Show final signed PDF
- Pause for 2 seconds

#### Step 3: Stop Recording
```bash
# Click Stop button in menu bar
# Or press Cmd+Control+Esc
# Video saves to Desktop
```

---

### Editing (45-60 minutes)

#### Option A: Quick Edit with QuickTime (Recommended)

```bash
# Open video
open ~/Desktop/Screen\ Recording*.mov

# In QuickTime:
# 1. Trim start/end
#    Edit → Trim → Drag yellow handles
#
# 2. Cut mistakes (if any)
#    Move playhead to cut point
#    Edit → Split Clip
#    Select unwanted part
#    Edit → Delete
#
# 3. Export
#    File → Export As → 1080p
#    Save as: SignKit_Demo_v1.mp4
```

#### Option B: Advanced Edit with iMovie

```bash
# Open iMovie
# Create new project
# Import video
# Add to timeline

# Editing:
# 1. Trim clips
# 2. Add text overlays (optional):
#    - "SignKit - Professional Signature Extraction"
#    - "Extract signatures from images"
#    - "Sign PDFs with ease"
#    - "Available now - $29 one-time"
#
# 3. Add transitions (optional)
# 4. Adjust speed (optional)
#
# Export:
# File → Share → File
# Resolution: 1080p
# Quality: High
# Save as: SignKit_Demo_v1.mp4
```

#### Option C: Add Text Overlays (Optional)

**Text to add:**
- 0:00: "SignKit"
- 0:05: "Extract signatures from images"
- 0:45: "Sign PDFs with ease"
- 1:20: "Available now - $29 one-time"

---

### Upload to YouTube (15 minutes)

#### 1. Go to YouTube Studio
```
https://studio.youtube.com
```

#### 2. Upload Video
- Click "Create" → "Upload videos"
- Select `SignKit_Demo_v1.mp4`
- Wait for upload

#### 3. Video Details
**Title:**
```
SignKit - Professional Signature Extraction & PDF Signing
```

**Description:**
```
SignKit is a powerful desktop application for extracting signatures from images and signing PDFs.

✨ Features:
- Smart signature extraction
- Clean, professional results
- Built-in PDF signing
- Signature library management
- 100% offline - complete privacy
- Works on macOS, Windows, Linux

💰 Pricing: $29 one-time payment (no subscription)

🔗 Get SignKit: https://signkit.work

#SignKit #PDFSigning #SignatureExtraction #Productivity
```

**Visibility:**
- Select "Unlisted" (not Public)
- This allows you to share the link without it appearing in search

**Thumbnail:**
- Use Screenshot 1 (main interface) as thumbnail
- Or create custom thumbnail with logo

#### 4. Get Shareable Link
- Click "Share" button
- Copy link (format: https://youtu.be/XXXXXXXXXXX)
- Save this link for Gumroad

---

## 📤 PART 3: UPLOAD TO GUMROAD (30 minutes)

### Step 1: Go to Product Page
```
https://pranaysuyash.gumroad.com/l/signkit-v1
```

### Step 2: Edit Product
- Click "Edit product"
- Scroll to "Product images" section

### Step 3: Upload Screenshots
1. Click "Add images"
2. Select all 12 screenshots
3. Wait for upload
4. Arrange in order:
   1. Main Interface (hero)
   2. Load Image
   3. Image Loaded
   4. Drawing Selection
   5. Selection Complete
   6. Threshold Adjustment
   7. Extraction Result
   8. Signature Library
   9. PDF Tab
   10. Load Signature (NEW!)
   11. PDF Placement
   12. Signed PDF

### Step 4: Add Captions
For each screenshot, add the caption from the list above.

### Step 5: Add Video
1. Scroll to "Product video" section
2. Click "Add video"
3. Paste YouTube link
4. Video will embed automatically

### Step 6: Save Changes
- Scroll to bottom
- Click "Save"
- Wait for confirmation

### Step 7: Preview
- Click "View product page"
- Check all screenshots load
- Check video plays
- Verify everything looks good

---

## ✅ CHECKLIST

### Screenshots
- [ ] 12 screenshots captured
- [ ] All screenshots reviewed
- [ ] Images compressed (200-500KB each)
- [ ] Files renamed descriptively
- [ ] Saved to organized folder

### Video
- [ ] Workflow recorded (60-90 seconds)
- [ ] Video edited and trimmed
- [ ] Exported as 1080p MP4
- [ ] Uploaded to YouTube (unlisted)
- [ ] Shareable link obtained

### Gumroad
- [ ] All screenshots uploaded
- [ ] Screenshots arranged in order
- [ ] Captions added to each
- [ ] Video embedded
- [ ] Changes saved
- [ ] Product page previewed

---

## 🎯 QUALITY CHECKLIST

### Screenshots Should Be:
- ✅ Clear and sharp (not blurry)
- ✅ Properly sized (1920x1080 or similar)
- ✅ Compressed (200-500KB each)
- ✅ No sensitive information visible
- ✅ Clean interface (no clutter)
- ✅ Consistent style

### Video Should Be:
- ✅ 60-90 seconds long
- ✅ 1080p resolution
- ✅ Smooth playback (no lag)
- ✅ Clear demonstration
- ✅ Complete workflow shown
- ✅ Professional quality

---

## 💡 TIPS

### For Screenshots:
- Use `Cmd+Shift+4` then `Space` to capture windows cleanly
- Take multiple shots and pick the best
- Ensure good lighting if capturing physical screen
- Use clean, professional sample documents
- Show real functionality, not mockups

### For Video:
- Practice the workflow before recording
- Move mouse slowly and deliberately
- Pause briefly at each step
- Don't rush - clarity over speed
- Record multiple takes if needed
- Keep it under 90 seconds

### For Gumroad:
- First screenshot is most important (hero shot)
- Arrange screenshots to tell a story
- Use descriptive captions
- Video should auto-play on page
- Test on mobile view too

---

## 🚀 AFTER COMPLETION

Once screenshots and video are uploaded:

1. ✅ Test product page on desktop
2. ✅ Test product page on mobile
3. ✅ Share link with friend for feedback
4. ✅ Make any final adjustments
5. ✅ Prepare for Monday launch!

---

## 📞 NEED HELP?

**Screenshot Issues:**
- Blurry images: Use `Cmd+Shift+4` + `Space` for window capture
- Wrong size: Capture full window, not partial
- Too large: Compress with ImageOptim

**Video Issues:**
- Too long: Edit in QuickTime or iMovie
- Poor quality: Re-record at 1080p
- Laggy: Close other apps before recording

**Upload Issues:**
- Slow upload: Compress files more
- Wrong format: Convert to PNG (screenshots) or MP4 (video)
- Not displaying: Clear browser cache and retry

---

**Total Time Estimate:**
- Screenshots: 2-3 hours
- Video: 2-3 hours
- Upload: 30 minutes
- **Total: 5-7 hours**

**You've got this!** 🚀
