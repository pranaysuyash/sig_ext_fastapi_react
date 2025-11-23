import logging
import json
import struct
from typing import Optional, Dict, Any, Tuple
from PIL import Image
import io

LOG = logging.getLogger(__name__)

class WatermarkEngine:
    """
    Handles invisible watermarking using LSB (Least Significant Bit) steganography.
    Embeds metadata into the Blue channel of the image.
    """

    def embed_watermark(self, image_data: bytes, metadata: Dict[str, Any]) -> bytes:
        """
        Embed metadata into the image using LSB steganography.
        
        Args:
            image_data: Raw PNG bytes.
            metadata: Dictionary of metadata to embed.
            
        Returns:
            Watermarked PNG bytes.
        """
        try:
            # 1. Prepare payload
            json_str = json.dumps(metadata)
            payload_bytes = json_str.encode('utf-8')
            
            # Add 32-bit length header
            length_header = struct.pack('>I', len(payload_bytes))
            full_payload = length_header + payload_bytes
            
            # Convert payload to bits
            bits = []
            for byte in full_payload:
                for i in range(7, -1, -1):
                    bits.append((byte >> i) & 1)
            
            # 2. Load Image
            img = Image.open(io.BytesIO(image_data))
            img = img.convert("RGBA") # Ensure RGBA
            width, height = img.size
            pixels = img.load()
            
            if len(bits) > width * height:
                LOG.warning("Metadata too large for image size. Watermarking skipped.")
                return image_data
            
            # 3. Embed bits
            bit_idx = 0
            for y in range(height):
                for x in range(width):
                    if bit_idx >= len(bits):
                        break
                        
                    r, g, b, a = pixels[x, y]
                    
                    # Modify LSB of Blue channel
                    # Clear LSB: b & ~1
                    # Set LSB: | bit
                    new_b = (b & ~1) | bits[bit_idx]
                    
                    pixels[x, y] = (r, g, new_b, a)
                    bit_idx += 1
                if bit_idx >= len(bits):
                    break
                    
            # 4. Save
            out_buffer = io.BytesIO()
            img.save(out_buffer, format="PNG")
            return out_buffer.getvalue()
            
        except Exception as e:
            LOG.error(f"Failed to embed watermark: {e}")
            return image_data # Return original on failure

    def verify_watermark(self, image_data: bytes) -> Optional[Dict[str, Any]]:
        """
        Extract and verify metadata from the image.
        
        Args:
            image_data: Raw PNG bytes.
            
        Returns:
            Metadata dictionary if found and valid, None otherwise.
        """
        try:
            img = Image.open(io.BytesIO(image_data))
            img = img.convert("RGBA")
            width, height = img.size
            pixels = img.load()
            
            # 1. Extract bits
            # We need at least 32 bits for length
            extracted_bits = []
            
            # Optimization: We don't need to read all pixels if we find the length early
            # But simpler to read as stream.
            
            # Read header (32 bits)
            header_bits = []
            pixel_iter = ((x, y) for y in range(height) for x in range(width))
            
            for _ in range(32):
                try:
                    x, y = next(pixel_iter)
                    r, g, b, a = pixels[x, y]
                    header_bits.append(b & 1)
                except StopIteration:
                    return None # Image too small
            
            # Reconstruct length
            length_val = 0
            for bit in header_bits:
                length_val = (length_val << 1) | bit
                
            if length_val <= 0 or length_val > 100000: # Sanity check (max 100KB metadata)
                return None
                
            # Read payload
            payload_bits = []
            total_payload_bits = length_val * 8
            
            for _ in range(total_payload_bits):
                try:
                    x, y = next(pixel_iter)
                    r, g, b, a = pixels[x, y]
                    payload_bits.append(b & 1)
                except StopIteration:
                    return None # Unexpected end of data
            
            # Reconstruct bytes
            payload_bytes = bytearray()
            current_byte = 0
            for i, bit in enumerate(payload_bits):
                current_byte = (current_byte << 1) | bit
                if (i + 1) % 8 == 0:
                    payload_bytes.append(current_byte)
                    current_byte = 0
                    
            # Parse JSON
            json_str = payload_bytes.decode('utf-8')
            metadata = json.loads(json_str)
            return metadata
            
        except Exception as e:
            # LOG.debug(f"Watermark verification failed: {e}") # Expected for non-watermarked images
            return None
