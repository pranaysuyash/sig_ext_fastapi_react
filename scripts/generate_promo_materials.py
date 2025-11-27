import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Configuration
SOURCE_DIR = "/Users/pranay/Projects/Data_Science/computer_vision/proj6/signature-extractor-app/screenshots_final"
OUTPUT_DIR = "/Users/pranay/Projects/Data_Science/computer_vision/proj6/signature-extractor-app/promotional_material"
ASSETS_DIR = "/Users/pranay/Projects/Data_Science/computer_vision/proj6/signature-extractor-app/assets"

# Ensure output directories exist
os.makedirs(os.path.join(OUTPUT_DIR, "product_hunt"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "reddit"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "gumroad"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "social_media"), exist_ok=True)

# Map source images to variables for easier access
SCREENSHOTS = {
    "selection": os.path.join(SOURCE_DIR, "06_07_selection_20251114_233428.png"),
    "result": os.path.join(SOURCE_DIR, "10_11_result_20251114_233437.png"),
    "pdf_workflow": os.path.join(SOURCE_DIR, "17_18_pdf_workflow_20251114_233448.png"),
    "main": os.path.join(SOURCE_DIR, "02_03_loaded_20251114_233420.png")
}

# Colors
COLOR_BG = (20, 24, 30) # Dark blue-grey
COLOR_ACCENT = (59, 130, 246) # Blue
COLOR_TEXT = (255, 255, 255)

def get_font(size):
    try:
        # Try to load a system font
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except:
        try:
             return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size)
        except:
            return ImageFont.load_default()

def create_gradient(width, height, start_color, end_color):
    base = Image.new('RGB', (width, height), start_color)
    top = Image.new('RGB', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def create_ph_thumbnail():
    size = (240, 240)
    img = Image.new('RGB', size, COLOR_ACCENT)
    draw = ImageDraw.Draw(img)
    
    # Draw a simple "S" or icon representation
    font = get_font(120)
    text = "S"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    draw.text(((size[0] - text_w) / 2, (size[1] - text_h) / 2 - 20), text, font=font, fill=COLOR_TEXT)
    
    output_path = os.path.join(OUTPUT_DIR, "product_hunt", "ph_thumbnail.png")
    img.save(output_path)
    print(f"Created {output_path}")

def create_ph_gallery_image(name, screenshot_key, title, subtitle):
    size = (1270, 760)
    img = create_gradient(size[0], size[1], (30, 41, 59), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # Add Text
    font_title = get_font(60)
    font_sub = get_font(30)
    
    draw.text((50, 50), title, font=font_title, fill=COLOR_TEXT)
    draw.text((50, 130), subtitle, font=font_sub, fill=(200, 200, 200))
    
    # Add Screenshot
    if screenshot_key in SCREENSHOTS and os.path.exists(SCREENSHOTS[screenshot_key]):
        ss = Image.open(SCREENSHOTS[screenshot_key])
        # Resize to fit nicely
        target_w = 1000
        ratio = target_w / ss.width
        target_h = int(ss.height * ratio)
        ss = ss.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Add a border/shadow effect (simple white border)
        ss = ImageOps.expand(ss, border=5, fill='white')
        
        # Center horizontally, place below text
        x = (size[0] - ss.width) // 2
        y = 200
        img.paste(ss, (x, y))
    
    output_path = os.path.join(OUTPUT_DIR, "product_hunt", f"{name}.png")
    img.save(output_path)
    print(f"Created {output_path}")

def create_reddit_image(name, screenshot_key):
    size = (1200, 675) # 16:9
    img = Image.new('RGB', size, COLOR_BG)
    
    if screenshot_key in SCREENSHOTS and os.path.exists(SCREENSHOTS[screenshot_key]):
        ss = Image.open(SCREENSHOTS[screenshot_key])
        # Resize to fit, maintaining aspect ratio
        img_ratio = size[0] / size[1]
        ss_ratio = ss.width / ss.height
        
        if ss_ratio > img_ratio:
            # Fit to width
            target_w = size[0]
            target_h = int(target_w / ss_ratio)
        else:
            # Fit to height
            target_h = size[1]
            target_w = int(target_h * ss_ratio)
            
        ss = ss.resize((target_w, target_h), Image.Resampling.LANCZOS)
        x = (size[0] - target_w) // 2
        y = (size[1] - target_h) // 2
        img.paste(ss, (x, y))
        
    output_path = os.path.join(OUTPUT_DIR, "reddit", f"{name}.png")
    img.save(output_path)
    print(f"Created {output_path}")

def main():
    # Product Hunt
    create_ph_thumbnail()
    create_ph_gallery_image("ph_hero", "result", "SignKit", "Extract Signatures Offline. Privacy First.")
    create_ph_gallery_image("ph_feature_1", "selection", "Precision Extraction", "Crop, Threshold, and Clean signatures instantly.")
    create_ph_gallery_image("ph_feature_2", "pdf_workflow", "Sign PDFs Directly", "Place extracted signatures on documents without leaving the app.")
    
    # Reddit
    create_reddit_image("reddit_hero", "main")
    create_reddit_image("reddit_feature_upload", "selection")
    create_reddit_image("reddit_feature_place", "pdf_workflow")
    
    # Gumroad
    create_ph_gallery_image("gumroad_cover", "result", "SignKit", "The Privacy-First Signature Tool")

    # Social Media
    create_social_header("twitter_header", (1500, 500), "SignKit", "Privacy-First PDF Signatures")
    create_social_header("linkedin_header", (1128, 191), "SignKit", "Extract Signatures Offline & Sign PDFs")

def create_social_header(name, size, title, subtitle):
    img = create_gradient(size[0], size[1], (30, 41, 59), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # Add Text
    font_title = get_font(int(size[1] * 0.15))
    font_sub = get_font(int(size[1] * 0.08))
    
    # Center text
    bbox_title = draw.textbbox((0, 0), title, font=font_title)
    title_w = bbox_title[2] - bbox_title[0]
    title_h = bbox_title[3] - bbox_title[1]
    
    bbox_sub = draw.textbbox((0, 0), subtitle, font=font_sub)
    sub_w = bbox_sub[2] - bbox_sub[0]
    
    draw.text(((size[0] - title_w) / 2, (size[1] / 2) - title_h), title, font=font_title, fill=COLOR_TEXT)
    draw.text(((size[0] - sub_w) / 2, (size[1] / 2) + 10), subtitle, font=font_sub, fill=(200, 200, 200))
    
    output_path = os.path.join(OUTPUT_DIR, "social_media", f"{name}.png")
    img.save(output_path)
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
