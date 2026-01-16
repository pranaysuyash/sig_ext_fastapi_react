"""Smoke test for MainWindow mixin contract compliance."""

import pytest
from unittest.mock import Mock


PySide6 = pytest.importorskip("PySide6")


def test_main_window_mixin_contract():
    """Verify all mixin methods exist on MainWindow before instantiation."""
    # Import here to catch import errors
    from desktop_app.api.client import ApiClient
    from desktop_app.state.session import SessionState
    from desktop_app.views.main_window import MainWindow

    # Create minimal mocks
    mock_client = Mock(spec=ApiClient)
    mock_client.base_url = "http://127.0.0.1:8001"
    mock_session = Mock(spec=SessionState)

    # Instantiate window
    try:
        window = MainWindow(mock_client, mock_session)

        # Verify mixin methods exist
        required_methods = [
            # From ExtractionTabMixin
            '_setup_extraction_ui',
            '_on_tab_changed',
            'on_open',
            'on_export',
            'on_save_to_library',

            # From PdfTabMixin
            '_setup_pdf_ui',

            # From ThemeMixin
            '_apply_theme',
            '_setup_dark_mode_support',

            # From ToolbarMixin
            '_setup_main_toolbar',

            # From PaneStatusMixin
            '_init_status_bar',
            'defer_coordinate_update',

            # From NativeDialogsMixin
            '_native_open_file',
            '_open_document',
            '_open_url',

            # Health check
            '_check_backend_health',
        ]

        missing_methods = []
        for method in required_methods:
            if not hasattr(window, method):
                missing_methods.append(method)

        # Cleanup
        window.close()

        # Assert no missing methods
        assert not missing_methods, f"Missing mixin methods: {missing_methods}"

    except Exception as e:
        pytest.fail(f"MainWindow instantiation failed: {e}")


def test_main_window_responsive_breakpoints():
    """Verify responsive breakpoint handler exists."""
    from desktop_app.api.client import ApiClient
    from desktop_app.state.session import SessionState
    from desktop_app.views.main_window import MainWindow

    mock_client = Mock(spec=ApiClient)
    mock_client.base_url = "http://127.0.0.1:8001"
    mock_session = Mock(spec=SessionState)

    window = MainWindow(mock_client, mock_session)

    # Verify responsive attributes
    assert hasattr(window, '_is_compact')
    assert hasattr(window, '_is_narrow')
    assert hasattr(window, '_apply_responsive_breakpoints')

    window.close()


if __name__ == "__main__":
    # Run smoke test standalone
    print("Running MainWindow mixin contract smoke test...")
    test_main_window_mixin_contract()
    print("✓ All mixin methods exist")

    test_main_window_responsive_breakpoints()
    print("✓ Responsive breakpoints configured")

    print("\n✅ All smoke tests passed!")
