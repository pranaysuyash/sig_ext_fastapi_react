# Implementation Plan

- [x] 1. Enhance license validation system
  - Extend existing `LicenseInfo` class with test license support and validation timestamps
  - Create `LicenseValidator` class with operation permission checking
  - Add test license recognition for "pranay@example.com"
  - Implement operation type enumeration for export and PDF operations
  - _Requirements: 1.1, 1.5, 4.1, 4.2, 4.3_

- [x] 2. Create license restriction dialog
  - Implement `LicenseRestrictionDialog` class with clear messaging about trial limitations
  - Add action buttons for license entry, purchase, and cancellation
  - Integrate with existing license dialog for seamless license activation
  - Create operation-specific messaging for export vs PDF restrictions
  - _Requirements: 3.1, 3.2, 3.5_

- [x] 3. Implement export operation restrictions
- [x] 3.1 Add license check to export functionality
  - Modify `on_export` method in extraction view to check license before showing export dialog
  - Create export license validation helper function
  - Show restriction dialog when export is attempted without valid license
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 3.2 Update export dialog integration
  - Ensure export dialog only appears for licensed users
  - Maintain preview functionality for trial users
  - Add license status awareness to export-related UI elements
  - _Requirements: 1.4, 3.3_

- [x] 4. Implement PDF operations restrictions
- [x] 4.1 Add license check to PDF paste operations
  - ✅ Added check_and_enforce_pdf_operations_license() to `_on_pdf_paste_signature` method
  - ✅ Shows restriction dialog for unlicensed paste attempts
  - ✅ Maintains signature preview functionality in trial mode
  - _Requirements: 2.1, 2.2, 2.4_
  - **STATUS: COMPLETED**

- [x] 4.2 Add license check to PDF save operations
  - ✅ Added check_and_enforce_pdf_operations_license() to `on_pdf_save` method
  - ✅ Added check_and_enforce_pdf_operations_license() to `_on_pdf_tab_save` method
  - ✅ Shows restriction dialog for unlicensed save attempts
  - ✅ Allows PDF viewing and signature placement preview in trial mode
  - _Requirements: 2.1, 2.2, 2.4_
  - **STATUS: COMPLETED**

- [ ] 4.3 Update PDF UI elements for trial mode
  - Add trial mode indicators to PDF-related buttons and menus
  - Update tooltips and status messages to reflect licensing requirements
  - Ensure PDF viewing remains fully functional in trial mode
  - _Requirements: 2.4, 3.4_

- [ ] 5. Integrate license status throughout application
- [ ] 5.1 Update main window license menu
  - Enhance license menu to show trial mode status more prominently
  - Add quick access to restricted operations information
  - Update license status display with trial mode messaging
  - _Requirements: 3.4, 4.4_

- [ ] 5.2 Add license validation to toolbar actions
  - Update toolbar export action to respect license restrictions
  - Add license status awareness to PDF-related toolbar actions
  - Provide immediate feedback for restricted operations
  - _Requirements: 1.1, 2.1, 3.1_

- [x] 6. Configure test license and validation
- [x] 6.1 Implement test license configuration
  - ✅ VERIFIED: TEST_LICENSE_EMAIL = "pranay@example.com" in storage.py
  - ✅ Test license enables all functionality identical to purchased licenses
  - ✅ Helper methods for test license detection in LicenseValidator class
  - _Requirements: 4.1, 4.2, 4.3_
  - **STATUS: ALREADY IMPLEMENTED**

- [x] 6.2 Add license validation helpers
  - ✅ VERIFIED: check_and_enforce_export_license() in restrictions.py
  - ✅ check_and_enforce_pdf_operations_license() in restrictions.py
  - ✅ LicenseValidator.is_operation_allowed() for consistent validation
  - ✅ Offline license validation support for test license working
  - _Requirements: 4.4, 4.5_
  - **STATUS: ALREADY IMPLEMENTED**

- [ ] 7. Testing and validation
- [ ] 7.1 Create license restriction tests
  - Write unit tests for license validator functionality
  - Test export and PDF operation restrictions in trial mode
  - Verify test license enables all functionality
  - Test license activation flow and immediate operation retry
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 4.1, 4.2_

- [ ] 7.2 Create integration tests for user workflows
  - Test complete user workflow from trial mode to licensed operation
  - Verify restriction dialogs appear correctly for blocked operations
  - Test license purchase and activation integration
  - Validate trial mode functionality remains intact
  - _Requirements: 3.1, 3.2, 3.3, 3.5_