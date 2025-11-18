#!/usr/bin/env python3
"""
Optimize screenshots for web landing page.
Resizes to 1200x800px and compresses to <500KB.
"""

from PIL import Image
import os

# Define screenshot mappings
screenshots = [
    ("screenshots_final/13_14_library_20251114_233442.png", "main-interface.png"),
    ("screenshots_final/10_11_result_20251114_233437.png", "signature-extraction.png"),
    ("screenshots_final/17_18_pdf_workflow_20251114_233448.png", "pdf-signing.png"),
]

# Create output directory
output_dir = "web/neobrutalism_chatgpt/screenshots"
os.makedirs(output_dir, exist_ok=True)

print("🔄 Optimizing screenshots for web...\n")

for src, dest in screenshots:
    if not os.path.exists(src):
        print(f"⚠️  Source not found: {src}")
        continue
    
    print(f"Processing: {src}")
    
    # Open and resize
    img = Image.open(src)
    
    # Calculate aspect ratio and resize
    img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
    
    # Save with optimization
    output_path = os.path.join(output_dir, dest)
    img.save(output_path, "PNG", optimize=True, quality=85)
    
    # Check file size
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✓ Created: {dest} ({size_mb:.2f}MB)\n")

print("✅ Screenshot optimization complete!")
print(f"📁 Output directory: {output_dir}")
