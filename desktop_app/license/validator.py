"""
License validation helpers for UI components.
This module provides convenient functions for checking license restrictions.
"""

from typing import Tuple
from .storage import LicenseValidator, OperationType


def check_export_license() -> bool:
    """
    Check license before export operations.
    
    Returns:
        True if operation should proceed, False if blocked
    """
    allowed, _ = LicenseValidator.is_operation_allowed(OperationType.EXPORT)
    return allowed


def check_pdf_operations_license() -> bool:
    """
    Check license before PDF paste/save operations.
    
    Returns:
        True if operation should proceed, False if blocked
    """
    allowed, _ = LicenseValidator.is_operation_allowed(OperationType.PDF_OPERATIONS)
    return allowed


def get_operation_restriction_info(operation_type: OperationType) -> Tuple[bool, str]:
    """
    Get detailed information about operation restrictions.
    
    Args:
        operation_type: The type of operation to check
        
    Returns:
        (allowed: bool, reason: str)
    """
    return LicenseValidator.is_operation_allowed(operation_type)


def get_license_status_info() -> Tuple[bool, str, bool]:
    """
    Get comprehensive license status information.
    
    Returns:
        (is_licensed: bool, status_message: str, is_test: bool)
    """
    return LicenseValidator.get_license_status()