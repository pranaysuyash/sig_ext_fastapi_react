from PIL import Image
import os

def process_thumbnail(input_path, output_path):
    try:
        img = Image.open(input_path)
        # Resize to 240x240 using high-quality resampling
        img = img.resize((240, 240), Image.Resampling.LANCZOS)
        img.save(output_path, "PNG")
        print(f"Thumbnail saved to {output_path}")
    except Exception as e:
        print(f"Error processing thumbnail: {e}")

if __name__ == "__main__":
    input_path = "/Users/pranay/.gemini/antigravity/brain/cc6beac1-424d-445b-b5ee-e0e674a32b05/uploaded_image_1764253318234.jpg"
    output_path = "/Users/pranay/Projects/Data_Science/computer_vision/proj6/signature-extractor-app/promotional_material/product_hunt/ph_thumbnail.png"
    process_thumbnail(input_path, output_path)
