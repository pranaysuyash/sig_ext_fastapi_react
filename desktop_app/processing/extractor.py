"""Local signature extraction engine.

This module provides local image processing capabilities for signature extraction,
eliminating the need for backend API calls and enabling offline-first operation.

SECURITY ARCHITECTURE:
=====================
This module implements defense-in-depth security with multiple validation layers:

1. File Extension Check
   - First line of defense (weakest)
   - Blocks obvious non-image files (.exe, .pdf, .zip)
   - Easy to bypass by renaming files

2. Magic Number Validation (File Signature)
   - Second line of defense (strong)
   - Reads actual file binary headers
   - Cannot be bypassed by simple file renaming
   - See SecurityValidator.validate_image_file() for implementation details

3. File Size Limits
   - Prevents denial-of-service via huge files
   - 50MB max to balance security vs. usability
   - Protects against memory exhaustion attacks

4. Image Dimension Validation
   - Prevents memory exhaustion from maliciously crafted images
   - Max 10,000 x 10,000 pixels per dimension
   - Max 50 megapixels total
   - A 10000x10000 image at 24-bit color = ~286MB in memory

5. PIL/Pillow Verification
   - PIL.Image.verify() checks file structure integrity
   - Detects corrupted or malformed images
   - Prevents crashes from crafted files exploiting image library bugs

6. Path Sanitization
   - Prevents directory traversal attacks (../../../etc/passwd)
   - Blocks access to system directories (/etc, /bin, /sys, etc.)
   - See SecurityValidator.sanitize_path() for implementation

WHY THIS MATTERS:
================
User-uploaded files are the #1 attack vector in web and desktop applications:
- Malicious files can exploit bugs in image processing libraries (CVE history)
- Large files can exhaust system memory (DoS attack)
- Path traversal can expose sensitive system files
- File type spoofing can bypass naive validation

Real-world examples:
- ImageTragick (CVE-2016-3714): ImageMagick RCE via crafted image files
- LibPNG vulnerabilities: Buffer overflows from malformed PNG chunks
- JPEG parsing bugs: Crashes and potential code execution

This multi-layer approach ensures the app is production-ready and secure.
"""

from __future__ import annotations

import logging
import os
import tempfile
import time
import uuid
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

import cv2
import numpy as np
from PIL import Image

LOG = logging.getLogger(__name__)


@dataclass
class ProcessingParams:
    """Parameters for signature processing."""
    threshold: int
    color: str
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        if not (0 <= self.threshold <= 255):
            raise ValueError(f"Threshold must be between 0 and 255, got {self.threshold}")
        
        # Validate color format
        if not self.color.startswith("#") or len(self.color) != 7:
            raise ValueError(f"Color must be in #RRGGBB format, got {self.color}")
        
        try:
            int(self.color[1:], 16)
        except ValueError:
            raise ValueError(f"Invalid hex color format: {self.color}")


@dataclass
class ProcessingSession:
    """Represents an image processing session."""
    session_id: str
    original_image: np.ndarray
    processed_image: Optional[np.ndarray]
    created_at: float
    file_path: str
    dimensions: Tuple[int, int]
    processing_params: Optional[ProcessingParams] = None
    
    @property
    def width(self) -> int:
        """Get image width."""
        return self.dimensions[1]
    
    @property
    def height(self) -> int:
        """Get image height."""
        return self.dimensions[0]


class SecurityValidator:
    """Validates file inputs for security.
    
    This class performs multiple layers of validation to protect against:
    1. File type spoofing attacks (renaming malicious files to .jpg/.png)
    2. Path traversal attacks (accessing system files)
    3. Memory exhaustion attacks (processing huge images)
    4. Malformed file attacks (corrupted or crafted files that crash the app)
    
    Security is critical because:
    - Users can upload any file from their system
    - Malicious files could exploit image processing libraries (PIL, OpenCV)
    - Without validation, attackers could crash the app or potentially execute code
    """
    
    ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg', 'image/jpg'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}
    
    # Magic number signatures for image validation
    # Note: These are kept for reference but validation uses prefix matching (see validate_image_file)
    IMAGE_SIGNATURES = {
        b'\x89PNG\r\n\x1a\n': 'image/png',
        b'\xff\xd8\xff\xe0': 'image/jpeg',  # JFIF
        b'\xff\xd8\xff\xe1': 'image/jpeg',  # EXIF
        b'\xff\xd8\xff\xe2': 'image/jpeg',  # Canon
        b'\xff\xd8\xff\xe3': 'image/jpeg',  # Samsung
        b'\xff\xd8\xff\xe8': 'image/jpeg',  # SPIFF
        b'\xff\xd8\xff\xdb': 'image/jpeg',  # Raw JPEG
        b'\xff\xd8\xff\xee': 'image/jpeg',  # Adobe JPEG
        b'\xff\xd8\xff\xfe': 'image/jpeg',  # JPEG with comment
    }
    
    # Maximum image dimensions to prevent memory exhaustion
    MAX_IMAGE_WIDTH = 10000
    MAX_IMAGE_HEIGHT = 10000
    MAX_PIXELS = 50_000_000  # 50 megapixels
    
    @classmethod
    def validate_image_file(cls, file_path: str) -> None:
        """Validate image file for security and format compliance.
        
        Args:
            file_path: Path to the image file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is invalid or unsafe
        """
        path = Path(file_path)
        
        # Check file exists
        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {file_path}")
        
        # Check file size
        file_size = path.stat().st_size
        if file_size > cls.MAX_FILE_SIZE:
            raise ValueError(f"File too large: {file_size} bytes (max {cls.MAX_FILE_SIZE})")
        
        if file_size == 0:
            raise ValueError("File is empty")
        
        # Check file extension
        if path.suffix.lower() not in cls.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file extension: {path.suffix}")
        
        # Validate magic numbers (file signatures)
        # CRITICAL SECURITY: Magic numbers prevent file type spoofing
        # 
        # WHY THIS IS NEEDED:
        # - File extensions (.jpg, .png) can be easily faked by renaming files
        # - A malicious .exe file renamed to .jpg would pass extension checks
        # - Magic numbers are the ACTUAL file format identifiers in the binary data
        # 
        # HOW IT WORKS:
        # - Every file format has a unique signature in its first few bytes
        # - PNG: Always starts with \x89PNG\r\n\x1a\n (8 bytes)
        # - JPEG: Always starts with \xff\xd8\xff (3 bytes) followed by marker
        # 
        # IMPLEMENTATION STRATEGY:
        # - PNG: Exact match required (signature is always the same)
        # - JPEG: Prefix match (\xff\xd8\xff) because the 4th byte varies:
        #   * \xe0 = JFIF (most common, from photo editing software)
        #   * \xe1 = EXIF (from digital cameras with metadata)
        #   * \xe2 = Canon cameras
        #   * \xfe = JPEG with comment
        #   * Many more variants exist
        # 
        # BUGFIX HISTORY:
        # - Original implementation checked only specific JPEG markers (e0, e1, db, ee)
        # - Failed for images from certain cameras/software with different markers
        # - Fixed by checking universal JPEG prefix (\xff\xd8\xff) instead
        # - This accepts ALL valid JPEG files while still preventing spoofed files
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16)
                
            valid_signature = False
            
            # Check PNG signature (exact match required)
            if header.startswith(b'\x89PNG\r\n\x1a\n'):
                valid_signature = True
            # Check JPEG signature (universal prefix match)
            # Accepts any JPEG variant (JFIF, EXIF, Canon, Samsung, etc.)
            elif header.startswith(b'\xff\xd8\xff'):
                valid_signature = True
            
            if not valid_signature:
                raise ValueError("Invalid image file format (magic number check failed)")
                
        except (OSError, IOError) as e:
            raise ValueError(f"Cannot read file: {e}")
        
        # Additional PIL validation and dimension checking
        try:
            with Image.open(file_path) as img:
                img.verify()  # Verify it's a valid image
                
            # Re-open for dimension checking (verify() closes the image)
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Check image dimensions
                if width > cls.MAX_IMAGE_WIDTH or height > cls.MAX_IMAGE_HEIGHT:
                    raise ValueError(
                        f"Image too large: {width}x{height} pixels "
                        f"(max {cls.MAX_IMAGE_WIDTH}x{cls.MAX_IMAGE_HEIGHT})"
                    )
                
                # Check total pixel count
                total_pixels = width * height
                if total_pixels > cls.MAX_PIXELS:
                    raise ValueError(
                        f"Image has too many pixels: {total_pixels:,} "
                        f"(max {cls.MAX_PIXELS:,})"
                    )
                
        except Exception as e:
            raise ValueError(f"Invalid image file: {e}")
    
    @classmethod
    def sanitize_path(cls, file_path: str) -> str:
        """Sanitize file path to prevent directory traversal and other attacks.
        
        Args:
            file_path: Input file path
            
        Returns:
            Sanitized absolute path
            
        Raises:
            ValueError: If path is unsafe
        """
        if not file_path or not isinstance(file_path, str):
            raise ValueError("File path must be a non-empty string")
        
        # Check for null bytes (can cause issues on some systems)
        if '\x00' in file_path:
            raise ValueError("File path contains null bytes")
        
        # Check for directory traversal attempts
        if '..' in file_path:
            raise ValueError("Directory traversal not allowed")
        
        # Check for suspicious absolute paths (security risk)
        if os.path.isabs(file_path):
            # Block access to critical system directories (but allow temp dirs)
            dangerous_paths = ['/etc/', '/bin/', '/usr/bin/', '/sbin/', '/usr/sbin/', 
                             '/root/', '/sys/', '/proc/', '/dev/',
                             'C:\\Windows\\System32\\', 'C:\\Program Files\\']
            
            normalized_path = os.path.normpath(file_path).lower()
            for dangerous in dangerous_paths:
                if normalized_path.startswith(dangerous.lower()):
                    raise ValueError(f"Access to system directory not allowed: {file_path}")
            
            # Special check for /var but allow temp directories
            if normalized_path.startswith('/var/') and not any(temp_dir in normalized_path for temp_dir in ['/tmp/', '/temp/', '/folders/']):
                raise ValueError(f"Access to system directory not allowed: {file_path}")
            
            # Check path length for absolute paths
            if len(file_path) > 4096:
                raise ValueError("File path too long")
        
        # Convert to absolute path and resolve any symlinks/.. components
        try:
            abs_path = os.path.abspath(os.path.realpath(file_path))
        except (OSError, ValueError) as e:
            raise ValueError(f"Invalid file path: {e}")
        
        # Ensure the resolved path is what we expect
        if abs_path != os.path.normpath(abs_path):
            raise ValueError(f"Unsafe file path after normalization: {file_path}")
        
        # Check for suspicious characters (Windows-specific)
        if os.name == 'nt':
            suspicious_chars = '<>:"|?*'
            if any(char in file_path for char in suspicious_chars):
                raise ValueError(f"File path contains suspicious characters: {file_path}")
        
        return abs_path


class SignatureExtractor:
    """Local image processing engine for signature extraction."""
    
    # Resource limits to prevent abuse
    MAX_SESSIONS = 100
    MAX_TEMP_FILES = 50
    
    def __init__(self):
        """Initialize the signature extractor."""
        self.sessions: Dict[str, ProcessingSession] = {}
        self._temp_files: set = set()
        
    def create_session(self, image_path: str) -> str:
        """Create new processing session with image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Session ID for the created session
            
        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If image file is invalid or unsafe
        """
        # Check resource limits
        if len(self.sessions) >= self.MAX_SESSIONS:
            # Clean up old sessions to make room
            self._cleanup_old_sessions()
            
        if len(self.sessions) >= self.MAX_SESSIONS:
            raise ValueError(f"Too many active sessions (max {self.MAX_SESSIONS})")
        
        # Validate and sanitize input
        sanitized_path = SecurityValidator.sanitize_path(image_path)
        SecurityValidator.validate_image_file(sanitized_path)
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        try:
            # Load and validate image using OpenCV
            image = cv2.imread(sanitized_path, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError(f"Could not load image: {sanitized_path}")
            
            # Get image dimensions
            height, width = image.shape[:2]
            
            # Create session
            session = ProcessingSession(
                session_id=session_id,
                original_image=image,
                processed_image=None,
                created_at=time.time(),
                file_path=sanitized_path,
                dimensions=(height, width)
            )
            
            self.sessions[session_id] = session
            
            LOG.info(f"Created session {session_id} for image {sanitized_path} ({width}x{height})")
            return session_id
            
        except Exception as e:
            LOG.error(f"Failed to create session for {sanitized_path}: {e}")
            raise
    
    def get_session(self, session_id: str) -> Optional[ProcessingSession]:
        """Get processing session by ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            ProcessingSession if found, None otherwise
        """
        return self.sessions.get(session_id)
    
    def process_selection(
        self,
        session_id: str,
        x1: int, y1: int, x2: int, y2: int,
        threshold: int,
        color: str
    ) -> bytes:
        """Process selected region with given parameters.
        
        Args:
            session_id: Session identifier
            x1, y1, x2, y2: Selection coordinates
            threshold: Threshold value for binary processing
            color: Target color in #RRGGBB format
            
        Returns:
            PNG image bytes of processed signature
            
        Raises:
            ValueError: If session not found or parameters invalid
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        # Validate parameters
        params = ProcessingParams(threshold=threshold, color=color)
        self._validate_coordinates(x1, y1, x2, y2, session.width, session.height)
        
        try:
            # Ensure coordinates are within image bounds
            height, width = session.original_image.shape[:2]
            x1 = max(0, min(x1, width))
            x2 = max(0, min(x2, width))
            y1 = max(0, min(y1, height))
            y2 = max(0, min(y2, height))
            
            # Validate selection area
            if x2 <= x1 or y2 <= y1:
                raise ValueError("Invalid selection area")
            
            # Log processing info without sensitive data
            LOG.info(f"Processing selection {width}x{height} area with threshold={threshold}")
            
            # Crop the selected region
            cropped_image = session.original_image[y1:y2, x1:x2]
            
            # Convert to grayscale for thresholding
            gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to create binary mask
            _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
            
            # Convert color hex string (#RRGGBB) to BGR tuple for OpenCV
            hex_color = color.lstrip("#")
            r_val = int(hex_color[0:2], 16)
            g_val = int(hex_color[2:4], 16)
            b_val = int(hex_color[4:6], 16)
            color_bgr = (b_val, g_val, r_val)
            
            # Create colored image
            color_image = np.zeros_like(cropped_image, dtype=np.uint8)
            color_image[:, :] = color_bgr
            
            # Apply mask to create colored signature
            result_image = cv2.bitwise_and(color_image, color_image, mask=mask)
            
            # Convert BGR to RGB for PIL
            result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
            
            # Add alpha channel for transparency
            r_channel, g_channel, b_channel = cv2.split(result_image_rgb)
            alpha = mask
            final_image = cv2.merge([r_channel, g_channel, b_channel, alpha])
            
            # Convert to PIL Image and save as PNG bytes
            final_image_pil = Image.fromarray(final_image, 'RGBA')
            
            # Save to bytes
            image_io = BytesIO()
            final_image_pil.save(image_io, format="PNG")
            image_bytes = image_io.getvalue()
            
            # Store processed image in session
            session.processed_image = final_image
            session.processing_params = params
            
            LOG.info(f"Successfully processed selection, output size: {len(image_bytes)} bytes")
            return image_bytes
            
        except Exception as e:
            LOG.error(f"Failed to process selection for session {session_id}: {e}")
            raise
    
    def rotate_image(self, session_id: str, angle: float) -> str:
        """Rotate image and create new session.
        
        Args:
            session_id: Original session identifier
            angle: Rotation angle in degrees (positive = clockwise)
            
        Returns:
            New session ID for rotated image
            
        Raises:
            ValueError: If session not found
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        try:
            # Get image dimensions
            height, width = session.original_image.shape[:2]
            center = (width // 2, height // 2)
            
            # Create rotation matrix
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            
            # Calculate new dimensions to fit rotated image
            cos_val = abs(rotation_matrix[0, 0])
            sin_val = abs(rotation_matrix[0, 1])
            new_width = int((height * sin_val) + (width * cos_val))
            new_height = int((height * cos_val) + (width * sin_val))
            
            # Adjust rotation matrix for new center
            rotation_matrix[0, 2] += (new_width / 2) - center[0]
            rotation_matrix[1, 2] += (new_height / 2) - center[1]
            
            # Apply rotation
            rotated_image = cv2.warpAffine(
                session.original_image,
                rotation_matrix,
                (new_width, new_height),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(255, 255, 255)  # White background
            )
            
            # Save rotated image to temporary file with secure permissions
            temp_fd, temp_path = tempfile.mkstemp(suffix='.png', prefix='rotated_')
            self._temp_files.add(temp_path)
            
            try:
                os.close(temp_fd)  # Close file descriptor, keep the file
                
                # Set secure file permissions (owner read/write only)
                os.chmod(temp_path, 0o600)
                
                cv2.imwrite(temp_path, rotated_image)
                
                # Create new session with rotated image
                new_session_id = self.create_session(temp_path)
                
                LOG.info(f"Rotated image by {angle}° for session {session_id}, new session: {new_session_id}")
                return new_session_id
                
            except Exception:
                # Clean up temp file on error
                try:
                    os.unlink(temp_path)
                    self._temp_files.discard(temp_path)
                except OSError:
                    pass
                raise
                
        except Exception as e:
            LOG.error(f"Failed to rotate image for session {session_id}: {e}")
            raise
    
    def cleanup_session(self, session_id: str) -> None:
        """Clean up session and associated resources.
        
        Args:
            session_id: Session identifier to clean up
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            LOG.debug(f"Cleaned up session {session_id}")
    
    def _cleanup_old_sessions(self) -> None:
        """Clean up old sessions to free resources."""
        if len(self.sessions) < self.MAX_SESSIONS:
            return  # No need to cleanup yet
        
        # Sort sessions by creation time and remove oldest ones
        sorted_sessions = sorted(
            self.sessions.items(),
            key=lambda x: x[1].created_at
        )
        
        # Remove oldest sessions to get below the limit
        # Remove enough to get to 75% of max capacity
        target_count = int(self.MAX_SESSIONS * 0.75)
        sessions_to_remove = len(sorted_sessions) - target_count
        
        if sessions_to_remove > 0:
            for session_id, _ in sorted_sessions[:sessions_to_remove]:
                self.cleanup_session(session_id)
            
            LOG.info(f"Cleaned up {sessions_to_remove} old sessions")

    def _validate_coordinates(self, x1: int, y1: int, x2: int, y2: int, 
                            max_width: int, max_height: int) -> None:
        """Validate coordinate bounds and ranges.
        
        Args:
            x1, y1, x2, y2: Coordinate values to validate
            max_width, max_height: Maximum allowed coordinate values
            
        Raises:
            ValueError: If coordinates are invalid or out of bounds
        """
        # Check coordinate types and ranges
        coords = [('x1', x1), ('y1', y1), ('x2', x2), ('y2', y2)]
        for name, value in coords:
            if not isinstance(value, int):
                raise ValueError(f"{name} must be an integer, got {type(value).__name__}")
            if value < 0:
                raise ValueError(f"{name} must be non-negative, got {value}")
        
        # Check selection area first
        if x2 <= x1:
            raise ValueError(f"x2 must be > x1, got x1={x1}, x2={x2}")
        if y2 <= y1:
            raise ValueError(f"y2 must be > y1, got y1={y1}, y2={y2}")
        
        # Check selection size (prevent extremely large selections) before bounds
        width = x2 - x1
        height = y2 - y1
        max_selection_pixels = 25_000_000  # 25 megapixels
        
        if width * height > max_selection_pixels:
            raise ValueError(
                f"Selection too large: {width}x{height} pixels "
                f"(max {max_selection_pixels:,} pixels)"
            )
        
        # Check bounds after size validation
        if x1 >= max_width or x2 >= max_width:
            raise ValueError(f"X coordinates must be < {max_width}, got x1={x1}, x2={x2}")
        if y1 >= max_height or y2 >= max_height:
            raise ValueError(f"Y coordinates must be < {max_height}, got y1={y1}, y2={y2}")

    def cleanup_all(self) -> None:
        """Clean up all sessions and temporary files securely."""
        # Clear session data from memory
        for session in self.sessions.values():
            # Overwrite image data in memory (best effort)
            if session.original_image is not None:
                session.original_image.fill(0)
            if session.processed_image is not None:
                session.processed_image.fill(0)
        
        self.sessions.clear()
        
        # Securely clean up temporary files
        for temp_file in list(self._temp_files):
            try:
                if os.path.exists(temp_file):
                    # Overwrite file content before deletion (best effort)
                    try:
                        file_size = os.path.getsize(temp_file)
                        with open(temp_file, 'r+b') as f:
                            f.write(b'\x00' * file_size)
                            f.flush()
                            os.fsync(f.fileno())
                    except (OSError, IOError):
                        pass  # Continue with normal deletion if overwrite fails
                    
                    # Delete the file
                    os.unlink(temp_file)
                    LOG.debug(f"Securely cleaned up temp file: {os.path.basename(temp_file)}")
            except OSError as e:
                LOG.warning(f"Failed to clean up temp file {os.path.basename(temp_file)}: {e}")
        
        self._temp_files.clear()
        LOG.debug("Completed secure cleanup of all sessions and temporary files")
    
    def __del__(self):
        """Cleanup on destruction."""
        try:
            self.cleanup_all()
        except Exception:
            pass  # Ignore errors during cleanup