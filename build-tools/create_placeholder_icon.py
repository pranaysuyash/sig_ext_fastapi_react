#!/usr/bin/env python3
"""
Quick Placeholder Icon Generator for SignKit
Generates a simple but professional-looking icon for immediate use
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_placeholder_icon():
    """Create a professional placeholder icon with 'S' letter"""

    # Icon configuration
    size = 1024
    bg_color = (37, 99, 235, 255)  # Professional blue
    circle_color = (255, 255, 255, 255)  # White
    text_color = (37, 99, 235, 255)  # Blue text

    # Create base image
    img = Image.new('RGBA', (size, size), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw white circle with margin
    margin = 120
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=circle_color
    )

    # Try to use a system font, fall back to default if not available
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",  # macOS
        "/System/Library/Fonts/SFNSDisplay.ttf",  # macOS San Francisco
        "C:\\Windows\\Fonts\\arial.ttf",  # Windows
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
    ]

    font = None
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 550)
                break
        except:
            continue

    if font is None:
        print("⚠️  Warning: Could not load system font, using default")
        font = ImageFont.load_default()

    # Draw letter 'S' centered
    text = "S"

    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size - text_width) // 2 - bbox[0]
    y = (size - text_height) // 2 - bbox[1]

    draw.text((x, y), text, fill=text_color, font=font)

    # Save in multiple sizes
    output_dir = Path(__file__).parent
    icon_dir = output_dir / "icons"
    icon_dir.mkdir(exist_ok=True)

    # Save master
    master_path = output_dir / "icon_1024.png"
    img.save(master_path, "PNG")
    print(f"✅ Created master icon: {master_path}")

    # Generate common sizes
    sizes = [16, 32, 48, 64, 128, 256, 512, 1024]
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        size_path = icon_dir / f"icon_{s}.png"
        resized.save(size_path, "PNG")
        print(f"   Created {s}x{s} icon")

    print(f"\n📁 All icons saved to: {icon_dir}")
    print("\nNext steps:")
    print("1. Convert to .icns (macOS):")
    print(f"   ./create_icns.sh")
    print("2. Convert to .ico (Windows):")
    print(f"   convert icon_1024.png -define icon:auto-resize=256,128,64,48,32,16 SignKit.ico")
    print("3. Or use online tool: https://appicon.co/")
    print("\n💡 For a professional icon, consider hiring a designer on Fiverr ($10-50)")

    return master_path

if __name__ == "__main__":
    print("🎨 SignKit Placeholder Icon Generator\n")
    create_placeholder_icon()
