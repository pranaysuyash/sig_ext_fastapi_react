# SignKit Linux Installation Guide

## Quick Install

```bash
# Extract the archive
tar -xzf SignKit_Linux.tar.gz

# Make executable
chmod +x SignKit_Linux

# Run the application
./SignKit_Linux
```

## Optional: Desktop Integration

To add SignKit to your application menu with an icon:

### 1. Install the Application

```bash
# Create application directory
sudo mkdir -p /opt/signkit

# Copy the executable
sudo cp SignKit_Linux /opt/signkit/signkit

# Make it executable
sudo chmod +x /opt/signkit/signkit
```

### 2. Install the Icon

```bash
# Copy icon to system icons (requires icon files from assets/files/)
sudo mkdir -p /usr/share/icons/hicolor/512x512/apps
sudo cp signkit_icon_512x512.png /usr/share/icons/hicolor/512x512/apps/signkit.png

sudo mkdir -p /usr/share/icons/hicolor/256x256/apps
sudo cp signkit_icon_256x256.png /usr/share/icons/hicolor/256x256/apps/signkit.png

sudo mkdir -p /usr/share/icons/hicolor/128x128/apps
sudo cp signkit_icon_128x128.png /usr/share/icons/hicolor/128x128/apps/signkit.png

sudo mkdir -p /usr/share/icons/hicolor/64x64/apps
sudo cp signkit_icon_64x64.png /usr/share/icons/hicolor/64x64/apps/signkit.png

sudo mkdir -p /usr/share/icons/hicolor/32x32/apps
sudo cp signkit_icon_32x32.png /usr/share/icons/hicolor/32x32/apps/signkit.png

# Update icon cache
sudo gtk-update-icon-cache /usr/share/icons/hicolor/
```

### 3. Install Desktop Entry

```bash
# Copy desktop file
sudo cp signkit.desktop /usr/share/applications/

# Update desktop database
sudo update-desktop-database /usr/share/applications/
```

### 4. Create Symbolic Link (Optional)

To run SignKit from anywhere:

```bash
sudo ln -s /opt/signkit/signkit /usr/local/bin/signkit
```

Now you can run `signkit` from any terminal.

## User-Level Installation (No sudo required)

If you don't have sudo access:

```bash
# Create local directories
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons/hicolor/{512x512,256x256,128x128,64x64,32x32}/apps

# Copy executable
cp SignKit_Linux ~/.local/bin/signkit
chmod +x ~/.local/bin/signkit

# Copy icons
cp signkit_icon_512x512.png ~/.local/share/icons/hicolor/512x512/apps/signkit.png
cp signkit_icon_256x256.png ~/.local/share/icons/hicolor/256x256/apps/signkit.png
cp signkit_icon_128x128.png ~/.local/share/icons/hicolor/128x128/apps/signkit.png
cp signkit_icon_64x64.png ~/.local/share/icons/hicolor/64x64/apps/signkit.png
cp signkit_icon_32x32.png ~/.local/share/icons/hicolor/32x32/apps/signkit.png

# Update icon cache
gtk-update-icon-cache ~/.local/share/icons/hicolor/ 2>/dev/null || true

# Copy desktop file (edit Exec path first)
sed 's|Exec=signkit|Exec='$HOME'/.local/bin/signkit|' signkit.desktop > ~/.local/share/applications/signkit.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/ 2>/dev/null || true
```

Make sure `~/.local/bin` is in your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Uninstall

### System-wide:
```bash
sudo rm /opt/signkit/signkit
sudo rm /usr/share/applications/signkit.desktop
sudo rm /usr/share/icons/hicolor/*/apps/signkit.png
sudo rmdir /opt/signkit
sudo update-desktop-database /usr/share/applications/
sudo gtk-update-icon-cache /usr/share/icons/hicolor/
```

### User-level:
```bash
rm ~/.local/bin/signkit
rm ~/.local/share/applications/signkit.desktop
rm ~/.local/share/icons/hicolor/*/apps/signkit.png
update-desktop-database ~/.local/share/applications/ 2>/dev/null || true
gtk-update-icon-cache ~/.local/share/icons/hicolor/ 2>/dev/null || true
```

## System Requirements

- **OS**: Ubuntu 20.04+ or equivalent (Debian, Fedora, Arch, etc.)
- **Architecture**: x86_64 (64-bit)
- **RAM**: 4GB minimum (8GB recommended)
- **Display**: X11 or Wayland

## Dependencies

SignKit is built as a standalone executable with all dependencies included. However, you may need these system libraries:

```bash
# Ubuntu/Debian
sudo apt-get install libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 \
  libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
  libxcb-render-util0 libxcb-shape0 libgl1-mesa-glx libegl1-mesa libdbus-1-3

# Fedora
sudo dnf install xcb-util-cursor xcb-util-image xcb-util-keysyms \
  xcb-util-renderutil xcb-util-wm mesa-libGL mesa-libEGL dbus-libs

# Arch
sudo pacman -S xcb-util-cursor xcb-util-image xcb-util-keysyms \
  xcb-util-renderutil xcb-util-wm mesa dbus
```

## Troubleshooting

### Application won't start
- Check if you have the required system libraries installed
- Run from terminal to see error messages: `./SignKit_Linux`
- Verify the file is executable: `chmod +x SignKit_Linux`

### Icon doesn't appear in menu
- Make sure you ran `update-desktop-database` and `gtk-update-icon-cache`
- Log out and log back in
- Try restarting your desktop environment

### Permission denied
- Make sure the file is executable: `chmod +x SignKit_Linux`
- Check file ownership: `ls -l SignKit_Linux`

## Support

For issues or questions:
- Email: support@signkit.work
- Documentation: https://docs.signkit.work
