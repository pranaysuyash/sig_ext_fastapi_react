import json
import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Tuple


APP_DIR_NAME = ".signature_extractor"
LICENSE_FILE = "license.json"

# Test license configuration
TEST_LICENSE_EMAIL = "pranay@example.com"


class OperationType(Enum):
    """Types of operations that can be restricted by licensing."""
    EXPORT = "export"
    PDF_OPERATIONS = "pdf_operations"


def _config_dir() -> str:
    """Return the per-user config directory (e.g., ~/.signature_extractor)."""
    home = os.path.expanduser("~")
    path = os.path.join(home, APP_DIR_NAME)
    os.makedirs(path, exist_ok=True)
    return path


def _license_path() -> str:
    return os.path.join(_config_dir(), LICENSE_FILE)


@dataclass
class LicenseInfo:
    key: str
    email: Optional[str] = None
    is_test_license: bool = False
    validated_at: Optional[datetime] = None
    
    def is_valid(self) -> bool:
        """Check if license is currently valid."""
        return bool(self.key and (len(self.key) >= 6 or self.is_test_license))


def load_license() -> Optional[LicenseInfo]:
    """Load license info from disk, if present."""
    path = _license_path()
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        key = data.get("key", "").strip()
        email = data.get("email")
        is_test_license = data.get("is_test_license", False)
        validated_at_str = data.get("validated_at")
        validated_at = None
        if validated_at_str:
            try:
                validated_at = datetime.fromisoformat(validated_at_str)
            except ValueError:
                pass
        
        if key:
            # Check if this is the test license
            if key == TEST_LICENSE_EMAIL or email == TEST_LICENSE_EMAIL:
                is_test_license = True
            
            return LicenseInfo(
                key=key, 
                email=email, 
                is_test_license=is_test_license,
                validated_at=validated_at
            )
    except Exception:
        # Ignore malformed file
        return None
    return None


def save_license(key: str, email: Optional[str] = None) -> None:
    """Persist license info to disk."""
    key = key.strip()
    is_test_license = key == TEST_LICENSE_EMAIL or email == TEST_LICENSE_EMAIL
    
    data = {
        "key": key,
        "is_test_license": is_test_license,
        "validated_at": datetime.now().isoformat()
    }
    if email:
        data["email"] = email.strip()
    
    with open(_license_path(), "w", encoding="utf-8") as f:
        json.dump(data, f)


def is_licensed() -> bool:
    """Very lightweight local check for MVP: consider any non-empty key as licensed.

    Later, integrate an online verification or signature check if desired.
    """
    info = load_license()
    return bool(info and info.is_valid())


class LicenseValidator:
    """Enhanced license validation with test license support."""
    
    @staticmethod
    def is_test_license(license_key: str) -> bool:
        """Check if license key is the test license."""
        return license_key.strip() == TEST_LICENSE_EMAIL
    
    @staticmethod
    def validate_license_key(key: str) -> bool:
        """Validate license key including test license."""
        key = key.strip()
        if not key:
            return False
        
        # Test license is always valid
        if LicenseValidator.is_test_license(key):
            return True
        
        # Regular license validation (minimum length requirement)
        return len(key) >= 6
    
    @staticmethod
    def is_operation_allowed(operation_type: OperationType) -> Tuple[bool, str]:
        """
        Check if operation is allowed under current license.
        
        Args:
            operation_type: The type of operation to check
            
        Returns:
            (allowed: bool, reason: str)
        """
        license_info = load_license()
        
        if not license_info:
            return False, "No license found. Application is in trial mode."
        
        if not license_info.is_valid():
            return False, "Invalid license. Please check your license key."
        
        # All operations allowed with valid license
        return True, "License valid"
    
    @staticmethod
    def get_license_status() -> Tuple[bool, str, bool]:
        """
        Get comprehensive license status.
        
        Returns:
            (is_licensed: bool, status_message: str, is_test: bool)
        """
        license_info = load_license()
        
        if not license_info:
            return False, "Trial Mode - No License", False
        
        if license_info.is_test_license:
            return True, f"Test License Active ({license_info.key})", True
        
        if license_info.is_valid():
            email_part = f" ({license_info.email})" if license_info.email else ""
            return True, f"Licensed{email_part}", False
        
        return False, "Invalid License", False

# Export the new classes and enums for easy importing
__all__ = [
    'LicenseInfo',
    'LicenseValidator', 
    'OperationType',
    'TEST_LICENSE_EMAIL',
    'load_license',
    'save_license',
    'is_licensed'
]