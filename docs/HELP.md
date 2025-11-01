# Help & FAQ

Frequently asked questions and quick answers for the Signature Extractor desktop app.

## Getting Started

**Q: How do I extract a signature from an image?**

1. Click **"Open & Upload Image"** or press `Ctrl+O`
2. Select the image file containing your signature
3. Use the selection tool (🎯) to draw a box around the signature
4. Adjust the threshold slider if needed (or use Auto)
5. Click **"Export"** or **"Copy"** to get your signature

**Q: What image formats are supported?**

PNG, JPG, and JPEG files are supported. The app automatically handles EXIF orientation correction for photos taken with mobile devices.

**Q: How do I save signatures for later use?**

After extracting a signature, click **"Save to Library"** to store it in your personal signature collection. You can access saved signatures from the "My Signatures" list.

## PDF Signing (NEW)

**Q: How do I sign a PDF with my extracted signature?**

1. First extract and save signatures to your library (see above)
2. Go to the **PDF Signing** tab
3. Click **"Open PDF"** to load your document
4. Select a signature from the library
5. Click on the PDF where you want to place the signature
6. Click **"Save Signed PDF"** when done

**Q: Can I sign multiple pages at once?**

Yes! Click **"Apply to Multiple Pages"** to place the same signature on several pages simultaneously.

**Q: Where can I find my signed PDFs?**

Signed PDFs are saved wherever you choose in the file dialog. The app will suggest a name like `document_signed.pdf`.

## Common Issues

### The selection doesn't look right

- Make sure you're using **Selection mode** (🎯 button)
- Try adjusting the threshold slider
- Use the **Auto** threshold option for automatic optimization
- Zoom in for more precise selection

### I don't see the preview/result panes

The preview and result panes only appear after you make a valid selection. Draw a selection box on the source image first.

### My image is rotated incorrectly

- Use the **Rotate** buttons to correct orientation
- Source rotation will re-upload the corrected image
- Preview/result rotation is for display only

### The app says "Backend: Offline"

- Make sure the backend server is running on port 8001
- Check the health endpoint: `http://127.0.0.1:8001/health`
- Restart the application if needed

### PDF features don't work

- PDF signing requires additional libraries
- Install with: `pip install pypdfium2 PyMuPDF pikepdf`
- The app works without PDF features for signature extraction

## Tips & Tricks

**Q: How do I get better extraction results?**

- Use high-contrast signatures on plain backgrounds
- Avoid shadows or complex backgrounds
- Try different threshold values
- Use the Auto threshold for automatic optimization

**Q: Can I reuse signatures across documents?**

Yes! Save signatures to your library and reuse them anytime. Each saved signature includes metadata about how it was extracted.

**Q: How do I clear everything and start over?**

Click **"Clean Viewport"** to reset the entire workspace, or **"Clear Selection"** to just remove the current selection.

## Keyboard Shortcuts

See **Help → Keyboard Shortcuts** for the complete list, including:

- `Ctrl+O` — Open image
- `Ctrl+C` — Copy result
- `Ctrl+E` — Export
- `Ctrl+0` — Reset viewport
- `Ctrl+1` — Fit to view
- `Ctrl+[` / `Ctrl+]` — Rotate

## Need More Help?

- Check the **Keyboard Shortcuts** in the Help menu
- For technical implementation details, see `docs/TECHNICAL_DETAILS.md`
- Report issues with screenshots of the footer information
