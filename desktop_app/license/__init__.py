"""
License management package for signature extractor application.
"""

from .storage import (
    LicenseInfo,
    LicenseValidator,
    OperationType,
    TEST_LICENSE_EMAIL,
    load_license,
    save_license,
    is_licensed
)

from .validator import (
    check_export_license,
    check_pdf_operations_license,
    get_operation_restriction_info,
    get_license_status_info
)

from .restrictions import (
    check_and_enforce_export_license,
    check_and_enforce_pdf_operations_license,
    is_export_allowed,
    is_pdf_operations_allowed,
    get_restriction_reason
)

__all__ = [
    # Core license storage
    'LicenseInfo',
    'LicenseValidator',
    'OperationType',
    'TEST_LICENSE_EMAIL',
    'load_license',
    'save_license',
    'is_licensed',
    
    # Validation helpers
    'check_export_license',
    'check_pdf_operations_license',
    'get_operation_restriction_info',
    'get_license_status_info',
    
    # Restriction enforcement
    'check_and_enforce_export_license',
    'check_and_enforce_pdf_operations_license',
    'is_export_allowed',
    'is_pdf_operations_allowed',
    'get_restriction_reason'
]