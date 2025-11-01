"""PDF signing utilities.

Primary implementation uses PyMuPDF for robust, standards-compliant image
insertion. Falls back to legacy pikepdf stream editing if PyMuPDF is not
available (not recommended).
"""

import io
from typing import List, Dict, Any, cast
from pathlib import Path

import pikepdf
from PIL import Image as PILImage

# Optional, preferred implementation
try:
    import fitz  # type: ignore  # PyMuPDF
    HAS_PYMUPDF = True
except Exception:
    HAS_PYMUPDF = False
    # Provide a dummy name to satisfy static analyzers when PyMuPDF is not installed
    fitz = cast(Any, None)  # type: ignore

class PDFSigner:
    """Embed signature images into PDF documents.

    Behavior:
    - When PyMuPDF is available, it is used to insert images via Page.insert_image,
      which is reliable and supported by PDF viewers (including Acrobat).
    - If PyMuPDF is unavailable, a legacy pikepdf-based stream approach is used
      as a fallback.
    """

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

        self.input_path = input_pdf_path
        # Prefer PyMuPDF document handle if available
        if HAS_PYMUPDF:
            try:
                self._doc = fitz.open(input_pdf_path)
            except Exception as e:
                raise ValueError(f"Failed to open PDF (PyMuPDF): {e}")
            self._pdf = None
        else:
            try:
                self._pdf = pikepdf.open(input_pdf_path)
            except Exception as e:
                raise ValueError(f"Failed to open PDF (pikepdf): {e}")
            self._doc = None

    def add_signature(
        self, page_num: int, sig_image_path: str, x: float, y: float, width: float, height: float
    ) -> None:
        """
        Add a signature image to a specific page.

        Args:
            page_num: Page number (0-indexed)
            sig_image_path: Path to signature image file
            x, y: Position on page.
            width, height: Signature dimensions.

        Coordinates origin and units:
        - PyMuPDF path (preferred): expects top-left origin in PDF page space
          as used by PyMuPDF's Page.insert_image(). Units are PDF points.
        - Legacy pikepdf path: expects top-left origin as provided by the UI;
          the implementation converts to bottom-left internally. Units are PDF
          points.
        """
        # Preferred implementation: PyMuPDF
        if HAS_PYMUPDF and self._doc is not None:
            if page_num < 0 or page_num >= self._doc.page_count:
                raise ValueError(f"Invalid page number: {page_num}")

            page = self._doc[page_num]

            # PyMuPDF expects top-left origin in page space; units are points
            rect = fitz.Rect(float(x), float(y), float(x + width), float(y + height))

            # Insert image; preserve aspect ratio similar to viewer overlay
            # (image is scaled to fit into rect while maintaining aspect)
            try:
                page.insert_image(rect, filename=sig_image_path, keep_proportion=True, overlay=True)
            except Exception as e:
                raise ValueError(f"Failed to insert image: {e}")
            return

        # Fallback: legacy pikepdf stream editing
        if self._pdf is None:
            raise RuntimeError("No PDF backend available for signing")

        if page_num < 0 or page_num >= len(self._pdf.pages):
            raise ValueError(f"Invalid page number: {page_num}")

        page = self._pdf.pages[page_num]

        # Load signature image; cast to concrete Image type for type checkers
        sig_image = cast(PILImage.Image, PILImage.open(sig_image_path))

        # Preserve RGBA for transparency, convert others to RGB
        if sig_image.mode not in ("RGBA", "RGB", "L"):
            sig_image = sig_image.convert("RGBA")

        image_bytes = io.BytesIO()
        sig_image.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        raw_image = pikepdf.Stream(self._pdf, image_bytes.read())

        if sig_image.mode == "RGBA":
            color_space = pikepdf.Name("/DeviceRGB")
            alpha = sig_image.split()[3]
            alpha_bytes = io.BytesIO()
            alpha.save(alpha_bytes, format="PNG")
            alpha_bytes.seek(0)

            smask = pikepdf.Stream(self._pdf, alpha_bytes.read())
            smask.stream_dict = pikepdf.Dictionary(
                Type=pikepdf.Name("/XObject"),
                Subtype=pikepdf.Name("/Image"),
                Width=alpha.width,
                Height=alpha.height,
                ColorSpace=pikepdf.Name("/DeviceGray"),
                BitsPerComponent=8,
                Filter=pikepdf.Name("/FlateDecode"),
            )

            raw_image.stream_dict = pikepdf.Dictionary(
                Type=pikepdf.Name("/XObject"),
                Subtype=pikepdf.Name("/Image"),
                Width=sig_image.width,
                Height=sig_image.height,
                ColorSpace=color_space,
                BitsPerComponent=8,
                Filter=pikepdf.Name("/FlateDecode"),
                SMask=smask,
            )
        else:
            raw_image.stream_dict = pikepdf.Dictionary(
                Type=pikepdf.Name("/XObject"),
                Subtype=pikepdf.Name("/Image"),
                Width=sig_image.width,
                Height=sig_image.height,
                ColorSpace=pikepdf.Name("/DeviceRGB") if sig_image.mode == "RGB" else pikepdf.Name("/DeviceGray"),
                BitsPerComponent=8,
                Filter=pikepdf.Name("/FlateDecode"),
            )

        pdf_image = raw_image

        mediabox = page.MediaBox
        page_height = float(mediabox[3]) - float(mediabox[1])
        # Convert from top-left origin to bottom-left for PDF content stream
        y_pdf = page_height - y - height

        if "/Resources" not in page:
            page.Resources = pikepdf.Dictionary()
        if "/XObject" not in page.Resources:
            page.Resources.XObject = pikepdf.Dictionary()

        sig_name = f"/Sig{len(page.Resources.XObject)}"
        page.Resources.XObject[sig_name] = pdf_image

        drawing_commands = f"""
q
{width} 0 0 {height} {x} {y_pdf} cm
{sig_name} Do
Q
"""

        if "/Contents" in page:
            if isinstance(page.Contents, pikepdf.Array):
                existing_content = b""
                contents_array_any = cast(Any, page.Contents)
                for stream in contents_array_any:
                    existing_content += pikepdf.Stream(stream).read_bytes()
                new_content = existing_content + drawing_commands.encode("latin-1")
                page.Contents = pikepdf.Stream(self._pdf, new_content)
            else:
                existing_content = page.Contents.read_bytes()
                new_content = existing_content + drawing_commands.encode("latin-1")
                page.Contents = pikepdf.Stream(self._pdf, new_content)
        else:
            page.Contents = pikepdf.Stream(self._pdf, drawing_commands.encode("latin-1"))

    def save(self, output_path: str) -> None:
        """
        Save the signed PDF to a new file.

        Args:
            output_path: Path to save signed PDF
        """
        if HAS_PYMUPDF and self._doc is not None:
            # Use deflate to keep sizes reasonable if images are uncompressed
            self._doc.save(output_path, deflate=True)
        elif self._pdf is not None:
            self._pdf.save(output_path)
        else:
            raise RuntimeError("No PDF backend available for saving")

    def save_to_bytes(self) -> bytes:
        """
        Save the signed PDF to bytes.

        Returns:
            PDF file bytes
        """
        buffer = io.BytesIO()
        if HAS_PYMUPDF and self._doc is not None:
            self._doc.save(buffer, deflate=True)
            return buffer.getvalue()
        elif self._pdf is not None:
            self._pdf.save(buffer)
            return buffer.getvalue()
        else:
            raise RuntimeError("No PDF backend available for saving")

    def close(self) -> None:
        """Close the PDF."""
        try:
            if HAS_PYMUPDF and getattr(self, "_doc", None) is not None:
                self._doc.close()  # type: ignore[union-attr]
        except Exception:
            pass
        try:
            if getattr(self, "_pdf", None) is not None:
                self._pdf.close()  # type: ignore[union-attr]
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
            # Support both point-based coordinates (legacy) and pixel-based
            # viewer coordinates (with dpi / scale metadata). If 'dpi' or
            # 'units' == 'px' is present, convert from pixels to PDF points.
            x = float(sig["x"])
            y = float(sig["y"])
            width = float(sig["width"])
            height = float(sig["height"])

            if sig.get("units") == "px" or ("dpi" in sig or "scale" in sig):
                dpi = float(sig.get("dpi", 150))
                scale = float(sig.get("scale", 1.0))
                if dpi <= 0:
                    dpi = 150.0
                if scale <= 0:
                    scale = 1.0
                px_to_pt = 72.0 / (dpi * scale)
                x *= px_to_pt
                y *= px_to_pt
                width *= px_to_pt
                height *= px_to_pt

            signer.add_signature(
                page_num=int(sig["page"]),
                sig_image_path=str(sig["sig_path"]),
                x=x,
                y=y,
                width=width,
                height=height,
            )
        
        signer.save(output_pdf_path)
        signer.close()
        return True
        
    except Exception as e:
        print(f"Error signing PDF: {e}")
        return False
