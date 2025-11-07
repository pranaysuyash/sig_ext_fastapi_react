"""
License restriction helpers for UI components.
This module provides functions that check licenses and show restriction dialogs.
"""

from typing import Optional
from PySide6.QtWidgets import QWidget

from .storage import OperationType, LicenseValidator
# Import will be done at runtime to avoid circular imports
# from ..views.license_restriction_dialog import show_restriction_dialog


def check_and_enforce_export_license(parent: Optional[QWidget] = None) -> bool:
    """
    Check license before export operations and show restriction dialog if needed.
    
    Args:
        parent: Parent widget for the restriction dialog
        
    Returns:
        True if operation should proceed, False if blocked
    """
    allowed, reason = LicenseValidator.is_operation_allowed(OperationType.EXPORT)
    
    if allowed:
        return True
    
    # Import at runtime to avoid circular imports
    from desktop_app.views.license_restriction_dialog import show_restriction_dialog
    
    # Show restriction dialog and return whether license was activated
    return show_restriction_dialog(OperationType.EXPORT, parent)


def check_and_enforce_pdf_operations_license(parent: Optional[QWidget] = None) -> bool:
    """
    Check license before PDF paste/save operations and show restriction dialog if needed.
    
    Args:
        parent: Parent widget for the restriction dialog
        
    Returns:
        True if operation should proceed, False if blocked
    """
    allowed, reason = LicenseValidator.is_operation_allowed(OperationType.PDF_OPERATIONS)
    
    if allowed:
        return True
    
    # Import at runtime to avoid circular imports
    from desktop_app.views.license_restriction_dialog import show_restriction_dialog
    
    # Show restriction dialog and return whether license was activated
    return show_restriction_dialog(OperationType.PDF_OPERATIONS, parent)


def is_export_allowed() -> bool:
    """
    Quick check if export operations are allowed (without showing dialogs).
    
    Returns:
        True if export is allowed, False if blocked
    """
    allowed, _ = LicenseValidator.is_operation_allowed(OperationType.EXPORT)
    return allowed


def is_pdf_operations_allowed() -> bool:
    """
    Quick check if PDF operations are allowed (without showing dialogs).
    
    Returns:
        True if PDF operations are allowed, False if blocked
    """
    allowed, _ = LicenseValidator.is_operation_allowed(OperationType.PDF_OPERATIONS)
    return allowed


def get_restriction_reason(operation_type: OperationType) -> str:
    """
    Get the reason why an operation is restricted.
    
    Args:
        operation_type: The type of operation to check
        
    Returns:
        Human-readable reason for restriction, or empty string if allowed
    """
    allowed, reason = LicenseValidator.is_operation_allowed(operation_type)
    return "" if allowed else reason