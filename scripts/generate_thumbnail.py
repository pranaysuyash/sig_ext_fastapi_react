from PIL import Image, ImageDraw, ImageFont
import os

def create_thumbnail(output_path):
    # Dimensions
    width = 240
    height = 240
    
    # Create image with dark blue/slate background
    # Gradient-ish effect by drawing lines? Or just solid for now to be safe and clean.
    # Let's do a nice solid dark slate blue: #1e293b (Slate 800)
    bg_color = (30, 41, 59) 
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add a subtle border/accent
    # Cyan accent: #06b6d4 (Cyan 500)
    accent_color = (6, 182, 212)
    
    # Draw a stylized "document" shape
    doc_w = 120
    doc_h = 150
    doc_x = (width - doc_w) // 2
    doc_y = (height - doc_h) // 2
    
    # White document
    draw.rectangle([doc_x, doc_y, doc_x + doc_w, doc_y + doc_h], fill=(255, 255, 255))
    
    # "Signature" line (Cyan)
    sig_start_x = doc_x + 20
    sig_start_y = doc_y + 100
    sig_end_x = doc_x + doc_w - 20
    sig_end_y = doc_y + 100
    
    # Draw a squiggly line to represent a signature
    points = [
        (sig_start_x, sig_start_y),
        (sig_start_x + 10, sig_start_y - 10),
        (sig_start_x + 20, sig_start_y + 5),
        (sig_start_x + 30, sig_start_y - 15),
        (sig_start_x + 40, sig_start_y + 0),
        (sig_start_x + 50, sig_start_y - 10),
        (sig_start_x + 60, sig_start_y + 5),
        (sig_start_x + 70, sig_start_y - 5),
        (sig_end_x, sig_end_y)
    ]
    draw.line(points, fill=accent_color, width=4)
    
    # Text "SignKit" at the bottom? Or maybe just the icon is enough?
    # Let's add "SignKit" text below the document if it fits, or inside.
    # Actually, for a 240x240 thumbnail, a clear icon is better.
    # Let's put a "Pen" overlay?
    
    # Simple Pen
    pen_color = (15, 23, 42) # Darker slate
    pen_w = 15
    pen_h = 80
    pen_x = doc_x + doc_w - 20
    pen_y = doc_y + 80
    
    # Draw pen body (angled) - keeping it simple with straight rectangle for now to avoid complex math in this quick script
    # draw.rectangle([pen_x, pen_y, pen_x + pen_w, pen_y + pen_h], fill=pen_color)
    
    # Let's stick to the "Document with Signature" look. It's clean.
    
    # Add some "text lines" above the signature
    line_color = (203, 213, 225) # Slate 300
    draw.line([(doc_x + 20, doc_y + 30), (doc_x + doc_w - 20, doc_y + 30)], fill=line_color, width=3)
    draw.line([(doc_x + 20, doc_y + 50), (doc_x + doc_w - 20, doc_y + 50)], fill=line_color, width=3)
    draw.line([(doc_x + 20, doc_y + 70), (doc_x + 60, doc_y + 70)], fill=line_color, width=3)

    # Save
    img.save(output_path)
    print(f"Thumbnail generated at {output_path}")

if __name__ == "__main__":
    output_path = "/Users/pranay/Projects/Data_Science/computer_vision/proj6/signature-extractor-app/promotional_material/product_hunt/ph_thumbnail_v2.png"
    create_thumbnail(output_path)
