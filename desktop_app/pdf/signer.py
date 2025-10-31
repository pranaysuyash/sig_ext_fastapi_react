"""PDF signing utilities using pikepdf."""

import io
from typing import List, Dict, Any
from pathlib import Path

import pikepdf
from PIL import Image as PILImage


class PDFSigner:
    """Embed signature images into PDF documents."""
    
    def __init__(self, input_pdf_path: str):
        """
        Initialize signer with input PDF.
        
        Args:
            input_pdf_path: Path to original PDF file
        
        Raises:
            FileNotFoundError: If PDF doesn't exist
            ValueError: If PDF cannot be opened
        """
        if not Path(input_pdf_path).exists():
            raise FileNotFoundError(f"PDF not found: {input_pdf_path}")
        
        try:
            self.pdf = pikepdf.open(input_pdf_path)
        except Exception as e:
            raise ValueError(f"Failed to open PDF: {e}")
        
        self.input_path = input_pdf_path
    
    def add_signature(self, page_num: int, sig_image_path: str, 
                     x: float, y: float, width: float, height: float) -> None:
        """
        Add a signature image to a specific page.
        
        Args:
            page_num: Page number (0-indexed)
            sig_image_path: Path to signature image file
            x, y: Position in PDF coordinates (bottom-left origin)
            width, height: Signature dimensions in PDF points
        
        Note: PDF coordinate system has origin at bottom-left,
              while Qt has origin at top-left. Caller must convert.
        """
        if page_num < 0 or page_num >= len(self.pdf.pages):
            raise ValueError(f"Invalid page number: {page_num}")
        
        page = self.pdf.pages[page_num]
        
        # Load signature image
        sig_image = PILImage.open(sig_image_path)
        
        # Convert to RGB if necessary
        if sig_image.mode not in ('RGB', 'L'):
            sig_image = sig_image.convert('RGB')
        
        # Save to bytes for pikepdf
        image_bytes = io.BytesIO()
        sig_image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        
        # Create PDF image object
        raw_image = pikepdf.Stream(self.pdf, image_bytes.read())
        raw_image.stream_dict = pikepdf.Dictionary(
            Type=pikepdf.Name('/XObject'),
            Subtype=pikepdf.Name('/Image'),
            Width=sig_image.width,
            Height=sig_image.height,
            ColorSpace=pikepdf.Name('/DeviceRGB') if sig_image.mode == 'RGB' else pikepdf.Name('/DeviceGray'),
            BitsPerComponent=8,
            Filter=pikepdf.Name('/FlateDecode')
        )
        pdf_image = raw_image
        
        # Get page dimensions for coordinate conversion
        mediabox = page.MediaBox
        page_height = float(mediabox[3] - mediabox[1])
        
        # Convert Qt coordinates (top-left origin) to PDF coordinates (bottom-left origin)
        y_pdf = page_height - y - height
        
        # Generate unique name for signature image
        if '/Resources' not in page:
            page.Resources = pikepdf.Dictionary()
        if '/XObject' not in page.Resources:
            page.Resources.XObject = pikepdf.Dictionary()
        
        sig_name = f"/Sig{len(page.Resources.XObject)}"
        page.Resources.XObject[sig_name] = pdf_image
        
        # Create drawing commands to place signature
        drawing_commands = f"""
q
{width} 0 0 {height} {x} {y_pdf} cm
{sig_name} Do
Q
"""
        
        # Append to existing content stream
        if '/Contents' in page:
            # Get existing content
            if isinstance(page.Contents, pikepdf.Array):
                # Multiple content streams - append to last one
                existing_content = b''
                for stream in page.Contents:
                    existing_content += pikepdf.Stream(stream).read_bytes()
                new_content = existing_content + drawing_commands.encode('latin-1')
                page.Contents = pikepdf.Stream(self.pdf, new_content)
            else:
                # Single content stream
                existing_content = page.Contents.read_bytes()
                new_content = existing_content + drawing_commands.encode('latin-1')
                page.Contents = pikepdf.Stream(self.pdf, new_content)
        else:
            # No existing content, create new stream
            page.Contents = pikepdf.Stream(self.pdf, drawing_commands.encode('latin-1'))
    
    def save(self, output_path: str) -> None:
        """
        Save the signed PDF to a new file.
        
        Args:
            output_path: Path to save signed PDF
        """
        self.pdf.save(output_path)
    
    def save_to_bytes(self) -> bytes:
        """
        Save the signed PDF to bytes.
        
        Returns:
            PDF file bytes
        """
        buffer = io.BytesIO()
        self.pdf.save(buffer)
        return buffer.getvalue()
    
    def close(self) -> None:
        """Close the PDF."""
        if hasattr(self, 'pdf'):
            try:
                self.pdf.close()
            except Exception:
                pass
    
    def __del__(self):
        self.close()


def sign_pdf(input_pdf_path: str, output_pdf_path: str, 
             signatures: List[Dict[str, Any]]) -> bool:
    """
    Convenience function to sign a PDF in one call.
    
    Args:
        input_pdf_path: Path to original PDF
        output_pdf_path: Path to save signed PDF
        signatures: List of signature dicts with keys:
                   - page: int (page number, 0-indexed)
                   - sig_path: str (path to signature image)
                   - x, y: float (position in PDF coordinates)
                   - width, height: float (dimensions in PDF points)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        signer = PDFSigner(input_pdf_path)
        
        for sig in signatures:
            signer.add_signature(
                page_num=sig["page"],
                sig_image_path=sig["sig_path"],
                x=sig["x"],
                y=sig["y"],
                width=sig["width"],
                height=sig["height"]
            )
        
        signer.save(output_pdf_path)
        signer.close()
        return True
        
    except Exception as e:
        print(f"Error signing PDF: {e}")
        return False
