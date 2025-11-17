# SignKit App Icon - Usage Guide

Extracted from your cover image! The fountain pen nib icon is ready to use.

## 📦 **What You Have**

### **PNG Files (All Sizes)**
- `signkit_icon_1024x1024.png` - App Store, high-res marketing
- `signkit_icon_512x512.png` - macOS app icon base
- `signkit_icon_256x256.png` - macOS, Windows
- `signkit_icon_128x128.png` - macOS, Windows
- `signkit_icon_64x64.png` - macOS, Windows
- `signkit_icon_32x32.png` - macOS, Windows, taskbar
- `signkit_icon_16x16.png` - Windows taskbar, favicon
- `signkit_icon_600x600.png` - Gumroad thumbnail (alternative)

### **Windows Icon**
- `signkit_icon.ico` - Multi-resolution Windows icon (ready to use!)

---

## 🍎 **For macOS (.icns file)**

You'll need to create this on your Mac using the `iconutil` command.

### **Quick Command (Run on Mac):**

```bash
# 1. Create iconset folder
mkdir SignKit.iconset

# 2. Copy icons with proper naming
cp signkit_icon_16x16.png SignKit.iconset/icon_16x16.png
cp signkit_icon_32x32.png SignKit.iconset/icon_16x16@2x.png
cp signkit_icon_32x32.png SignKit.iconset/icon_32x32.png
cp signkit_icon_64x64.png SignKit.iconset/icon_32x32@2x.png
cp signkit_icon_128x128.png SignKit.iconset/icon_128x128.png
cp signkit_icon_256x256.png SignKit.iconset/icon_128x128@2x.png
cp signkit_icon_256x256.png SignKit.iconset/icon_256x256.png
cp signkit_icon_512x512.png SignKit.iconset/icon_256x256@2x.png
cp signkit_icon_512x512.png SignKit.iconset/icon_512x512.png
cp signkit_icon_1024x1024.png SignKit.iconset/icon_512x512@2x.png

# 3. Convert to .icns
iconutil -c icns SignKit.iconset

# 4. Result: SignKit.icns (ready to use!)
```

---

## 🪟 **For Windows**

Just use `signkit_icon.ico` - it's ready to go!

In your PyInstaller spec file:
```python
icon='signkit_icon.ico'
```

---

## 🌐 **For Web/Gumroad**

- **Gumroad Thumbnail**: Use `signkit_icon_600x600.png`
- **Favicon**: Use `signkit_icon_32x32.png` or `signkit_icon_16x16.png`
- **Social Media**: Use `signkit_icon_512x512.png` or `signkit_icon_1024x1024.png`

---

## 📱 **For PyInstaller (macOS)**

After creating the .icns file:

```python
# In your .spec file
app = BUNDLE(
    exe,
    name='SignKit.app',
    icon='SignKit.icns',  # Your generated .icns file
    bundle_identifier='com.pranaysuyash.signkit'
)
```

---

## 📱 **For PyInstaller (Windows)**

```python
# In your .spec file
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    name='SignKit',
    icon='signkit_icon.ico',  # Already created!
)
```

---

## ✅ **Icon Checklist**

- [x] PNG icons (all sizes) ✅
- [x] Windows .ico file ✅
- [ ] macOS .icns file (create on Mac using commands above)
- [ ] Add to PyInstaller spec file
- [ ] Upload 600x600 to Gumroad as thumbnail

---

## 🎨 **Icon Design**

The icon features:
- White fountain pen nib (signature/writing symbol)
- Blue accent line (brand color)
- Circular dark background
- Clean, minimal, professional design
- Perfect for both light and dark themes

---

**All files are ready in `/mnt/user-data/outputs/`**

Download and use! 🚀
