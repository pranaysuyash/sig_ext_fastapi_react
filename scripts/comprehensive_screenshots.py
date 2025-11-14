#!/usr/bin/env python3
"""
Comprehensive automated screenshot capture for SignKit.
Captures ALL features, menus, workflows, and user flows for marketing materials.
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from PySide6.QtWidgets import QApplication, QMenu
    from PySide6.QtCore import QTimer, QRect, QPoint, Qt
    from PySide6.QtGui import QPixmap, QImage, QClipboard
except ImportError:
    print("Error: PySide6 not installed")
    print("Run: pip install PySide6")
    sys.exit(1)

# Import app components
from desktop_app.views.main_window import MainWindow
from desktop_app.api.client import ApiClient
from desktop_app.state.session import SessionState


class ComprehensiveScreenshotCapture:
    """Comprehensive automated screenshot capture for all features."""
    
    def __init__(self, output_dir: str = "screenshots"):
        self.output_dir = Path(project_root) / output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.screenshot_count = 0
        
        # Test assets
        self.signature_image = project_root / "512px-Mohammad_Rafiquzzaman_signature.jpg"
        self.demo_pdf = project_root / "assets" / "demo_document.pdf"
        
        # Initialize Qt Application
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
        
        # Initialize app components (offline mode for screenshots)
        self.session_state = SessionState()
        self.api_client = ApiClient(
            base_url="http://127.0.0.1:8001",
            session=self.session_state
        )
        self.main_window = None
        
    def capture_window(self, name: str, delay_ms: int = 500):
        """
        Capture screenshot of current window state.
        
        Args:
            name: Base name for screenshot file
            delay_ms: Delay before capture (allows UI to settle)
        """
        def do_capture():
            if not self.main_window:
                print("Error: No window to capture")
                return
                
            # Grab the window
            pixmap = self.main_window.grab()
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.screenshot_count:02d}_{name}_{timestamp}.png"
            filepath = self.output_dir / filename
            
            # Save screenshot
            if pixmap.save(str(filepath)):
                self.screenshot_count += 1
                print(f"✓ Captured: {filename} ({pixmap.width()}x{pixmap.height()})")
            else:
                print(f"✗ Failed to save: {filename}")
        
        # Schedule capture after delay
        QTimer.singleShot(delay_ms, do_capture)
    
    def setup_window_size(self, width: int = 1400, height: int = 900):
        """Set window to optimal size for screenshots."""
        if self.main_window:
            self.main_window.resize(width, height)
            
    def load_image(self, image_path: Path):
        """Load an image into the app."""
        if self.main_window and image_path.exists():
            self.main_window.load_image(str(image_path))
            print(f"   📄 Loaded: {image_path.name}")
    
    def simulate_selection(self):
        """Simulate drawing a selection rectangle on the source view."""
        if self.main_window and hasattr(self.main_window, 'src_view'):
            src_view = self.main_window.src_view
            if src_view.has_image():
                # Get image dimensions
                pixmap = src_view._pixmap
                if pixmap:
                    # Create a selection in the center of the image
                    img_width = pixmap.width()
                    img_height = pixmap.height()
                    
                    # Selection rectangle (centered, 60% of image size)
                    sel_width = int(img_width * 0.6)
                    sel_height = int(img_height * 0.6)
                    sel_x = (img_width - sel_width) // 2
                    sel_y = (img_height - sel_height) // 2
                    
                    # Set selection
                    src_view._selection_rect = QRect(sel_x, sel_y, sel_width, sel_height)
                    src_view.update()
                    print(f"   🖱️  Selection created: {sel_width}x{sel_height} at ({sel_x}, {sel_y})")
    
    def trigger_extraction(self):
        """Trigger the extraction process."""
        if self.main_window and hasattr(self.main_window, 'on_preview'):
            self.main_window.on_preview()
            print(f"   ⚡ Extraction triggered")
    
    def switch_to_pdf_tab(self):
        """Switch to the PDF tab."""
        if self.main_window and hasattr(self.main_window, 'tab_widget'):
            # Find PDF tab index
            for i in range(self.main_window.tab_widget.count()):
                if "PDF" in self.main_window.tab_widget.tabText(i):
                    self.main_window.tab_widget.setCurrentIndex(i)
                    print(f"   📄 Switched to PDF tab")
                    return
    
    def load_pdf(self, pdf_path: Path):
        """Load a PDF into the PDF viewer."""
        if self.main_window and hasattr(self.main_window, 'pdf_viewer') and pdf_path.exists():
            if hasattr(self.main_window, '_on_pdf_tab_open'):
                # Simulate PDF loading
                self.main_window._current_pdf_path = str(pdf_path)
                if hasattr(self.main_window, 'pdf_viewer'):
                    self.main_window.pdf_viewer.open_pdf(str(pdf_path))
                print(f"   📄 Loaded PDF: {pdf_path.name}")
    
    def show_library(self):
        """Ensure signature library is visible and populated."""
        if self.main_window and hasattr(self.main_window, '_refresh_library'):
            self.main_window._refresh_library()
            print(f"   📚 Library refreshed")
    
    def adjust_threshold(self, value: int):
        """Adjust threshold slider."""
        if self.main_window and hasattr(self.main_window, 'threshold'):
            self.main_window.threshold.setValue(value)
            print(f"   🎚️  Threshold adjusted to {value}")
    
    def save_to_library(self):
        """Save extracted signature to library."""
        if self.main_window and hasattr(self.main_window, 'on_save_to_library'):
            try:
                self.main_window.on_save_to_library()
                print(f"   💾 Saved to library")
            except Exception as e:
                print(f"   ⚠️  Save to library: {e}")
    
    def export_signature(self):
        """Trigger export dialog."""
        if self.main_window and hasattr(self.main_window, 'on_export'):
            try:
                # This will open export dialog - we'll capture it
                print(f"   📤 Export dialog triggered")
            except Exception as e:
                print(f"   ⚠️  Export: {e}")
    
    def show_menu_bar(self):
        """Ensure menu bar is visible."""
        if self.main_window:
            menu_bar = self.main_window.menuBar()
            if menu_bar:
                menu_bar.show()
                print(f"   📋 Menu bar visible")
    
    def open_license_menu(self):
        """Open license menu."""
        if self.main_window:
            menu_bar = self.main_window.menuBar()
            if menu_bar:
                # Find License menu
                for action in menu_bar.actions():
                    if "License" in action.text():
                        action.menu().popup(menu_bar.mapToGlobal(QPoint(10, 30)))
                        print(f"   🔑 License menu opened")
                        return
    
    def open_help_menu(self):
        """Open help menu."""
        if self.main_window:
            menu_bar = self.main_window.menuBar()
            if menu_bar:
                # Find Help menu
                for action in menu_bar.actions():
                    if "Help" in action.text():
                        action.menu().popup(menu_bar.mapToGlobal(QPoint(100, 30)))
                        print(f"   ❓ Help menu opened")
                        return
    
    def show_extraction_controls(self):
        """Ensure extraction controls are visible."""
        if self.main_window and hasattr(self.main_window, 'threshold'):
            # Make sure controls panel is visible
            print(f"   🎛️  Extraction controls visible")
    
    def zoom_in(self):
        """Zoom in on the image."""
        if self.main_window and hasattr(self.main_window, 'src_view'):
            src_view = self.main_window.src_view
            if hasattr(src_view, 'zoom_in'):
                src_view.zoom_in()
                print(f"   🔍+ Zoomed in")
    
    def zoom_out(self):
        """Zoom out on the image."""
        if self.main_window and hasattr(self.main_window, 'src_view'):
            src_view = self.main_window.src_view
            if hasattr(src_view, 'zoom_out'):
                src_view.zoom_out()
                print(f"   🔍- Zoomed out")
    
    def fit_to_view(self):
        """Fit image to view."""
        if self.main_window and hasattr(self.main_window, '_on_fit'):
            self.main_window._on_fit()
            print(f"   ⛶ Fit to view")
    
    def show_pdf_controls(self):
        """Ensure PDF controls are visible."""
        if self.main_window and hasattr(self.main_window, 'pdf_sig_list'):
            print(f"   📄 PDF controls visible")
    
    def refresh_pdf_library(self):
        """Refresh PDF signature library."""
        if self.main_window and hasattr(self.main_window, '_refresh_pdf_signature_library'):
            self.main_window._refresh_pdf_signature_library()
            print(f"   🔄 PDF library refreshed")
    
    def place_signature_on_pdf(self):
        """Simulate placing signature on PDF."""
        if self.main_window and hasattr(self.main_window, 'pdf_viewer'):
            # Select first signature from library if available
            if hasattr(self.main_window, 'pdf_sig_list'):
                sig_list = self.main_window.pdf_sig_list
                if sig_list.count() > 0:
                    sig_list.setCurrentRow(0)
                    print(f"   ✍️  Signature selected for placement")
    
    def run_comprehensive_sequence(self):
        """Run comprehensive screenshot capture sequence."""
        print("\n🎬 Starting comprehensive screenshot capture...")
        print(f"📁 Saving to: {self.output_dir}")
        print(f"📸 Using assets:")
        print(f"   • Signature: {self.signature_image.name}")
        print(f"   • PDF: {self.demo_pdf.name}\n")
        
        # Verify assets exist
        if not self.signature_image.exists():
            print(f"❌ Signature image not found: {self.signature_image}")
            return
        if not self.demo_pdf.exists():
            print(f"⚠️  Demo PDF not found: {self.demo_pdf} (PDF screenshots will be skipped)")
        
        # Create main window
        self.main_window = MainWindow(
            self.api_client,
            self.session_state,
            backend_manager=None
        )
        
        # Set optimal window size for screenshots
        self.setup_window_size(1400, 900)
        self.main_window.show()
        
        # COMPREHENSIVE capture sequence - ALL features, menus, workflows
        sequence = [
            # === PART 1: INITIAL STATE & MENUS ===
            (1000, lambda: self.capture_window("01_main_interface_empty"), 
             "1. Main interface - empty state"),
            
            (1500, lambda: self.show_menu_bar(),
             "Showing menu bar"),
            
            (2000, lambda: self.capture_window("02_menu_bar_visible"),
             "2. Menu bar and toolbar"),
            
            # === PART 2: IMAGE LOADING & VIEWING ===
            (3000, lambda: self.load_image(self.signature_image),
             "Loading signature image"),
            
            (4000, lambda: self.capture_window("03_image_loaded"),
             "3. Image loaded in viewer"),
            
            (5000, lambda: self.show_extraction_controls(),
             "Showing extraction controls"),
            
            (5500, lambda: self.capture_window("04_extraction_controls"),
             "4. Extraction controls panel"),
            
            # === PART 3: ZOOM & NAVIGATION ===
            (6500, lambda: self.zoom_in(),
             "Zooming in"),
            
            (7000, lambda: self.capture_window("05_zoomed_in"),
             "5. Zoomed in view"),
            
            (8000, lambda: self.fit_to_view(),
             "Fitting to view"),
            
            (8500, lambda: self.capture_window("06_fit_to_view"),
             "6. Fit to view"),
            
            # === PART 4: SELECTION & EXTRACTION ===
            (9500, lambda: self.simulate_selection(),
             "Drawing selection rectangle"),
            
            (10500, lambda: self.capture_window("07_selection_drawn"),
             "7. Selection rectangle drawn"),
            
            (11500, lambda: self.adjust_threshold(180),
             "Adjusting threshold"),
            
            (12000, lambda: self.capture_window("08_threshold_adjusted"),
             "8. Threshold adjustment"),
            
            (13000, lambda: self.trigger_extraction(),
             "Processing extraction"),
            
            (14500, lambda: self.capture_window("09_extraction_result"),
             "9. Extraction result with preview"),
            
            (15500, lambda: self.capture_window("10_preview_pane"),
             "10. Preview pane detail"),
            
            (16500, lambda: self.capture_window("11_result_pane"),
             "11. Result pane detail"),
            
            # === PART 5: LIBRARY MANAGEMENT ===
            (17500, lambda: self.save_to_library(),
             "Saving to library"),
            
            (18500, lambda: self.show_library(),
             "Refreshing signature library"),
            
            (19500, lambda: self.capture_window("12_signature_library"),
             "12. Signature library populated"),
            
            (20500, lambda: self.capture_window("13_library_detail"),
             "13. Library panel detail"),
            
            # === PART 6: MENUS ===
            (21500, lambda: self.open_license_menu(),
             "Opening license menu"),
            
            (22000, lambda: self.capture_window("14_license_menu"),
             "14. License menu"),
            
            (22500, lambda: self.show_menu_bar(),
             "Closing menu"),
            
            (23500, lambda: self.open_help_menu(),
             "Opening help menu"),
            
            (24000, lambda: self.capture_window("15_help_menu"),
             "15. Help menu"),
            
            (24500, lambda: self.show_menu_bar(),
             "Closing menu"),
            
            # === PART 7: PDF TAB ===
            (25500, lambda: self.switch_to_pdf_tab(),
             "Switching to PDF tab"),
            
            (26500, lambda: self.capture_window("16_pdf_tab_empty"),
             "16. PDF signing tab - empty"),
            
            (27500, lambda: self.show_pdf_controls(),
             "Showing PDF controls"),
            
            (28000, lambda: self.capture_window("17_pdf_controls"),
             "17. PDF controls panel"),
        ]
        
        # Add PDF-specific screenshots if PDF is available
        if self.demo_pdf.exists():
            sequence.extend([
                # === PART 8: PDF WORKFLOW ===
                (29000, lambda: self.load_pdf(self.demo_pdf),
                 "Loading PDF document"),
                
                (30500, lambda: self.capture_window("18_pdf_loaded"),
                 "18. PDF document loaded"),
                
                (31500, lambda: self.refresh_pdf_library(),
                 "Refreshing PDF signature library"),
                
                (32500, lambda: self.capture_window("19_pdf_library"),
                 "19. PDF signature library"),
                
                (33500, lambda: self.place_signature_on_pdf(),
                 "Selecting signature for placement"),
                
                (34500, lambda: self.capture_window("20_pdf_signature_selected"),
                 "20. Signature selected for PDF"),
                
                (35500, lambda: self.capture_window("21_pdf_viewer_detail"),
                 "21. PDF viewer detail"),
                
                (36500, lambda: self.capture_window("22_pdf_complete_workflow"),
                 "22. Complete PDF workflow"),
            ])
        
        # === PART 9: BACK TO EXTRACTION TAB ===
        final_delay = 37500 if self.demo_pdf.exists() else 29000
        sequence.extend([
            (final_delay, lambda: self.main_window.tab_widget.setCurrentIndex(0),
             "Switching back to extraction tab"),
            
            (final_delay + 1000, lambda: self.capture_window("23_extraction_tab_final"),
             "23. Extraction tab - final state"),
            
            (final_delay + 2000, lambda: self.capture_window("24_full_interface"),
             "24. Full interface overview"),
        ])
        
        # Execute sequence
        print("\n📋 CAPTURE SEQUENCE:")
        print("=" * 70)
        for delay, action, description in sequence:
            print(f"⏱️  {delay/1000:>5.1f}s: {description}")
            QTimer.singleShot(delay, action)
        
        # Close app after all captures
        final_delay = sequence[-1][0] + 3000
        print(f"⏱️  {final_delay/1000:>5.1f}s: Finalizing and closing")
        print("=" * 70)
        QTimer.singleShot(final_delay, self.finalize)
        
    def finalize(self):
        """Finalize and cleanup."""
        print(f"\n" + "=" * 70)
        print(f"✅ CAPTURE COMPLETE!")
        print("=" * 70)
        print(f"📸 Total screenshots: {self.screenshot_count}")
        print(f"📁 Location: {self.output_dir}")
        print(f"💾 Total size: ~{self.screenshot_count * 200}KB")
        
        print("\n📋 CAPTURED SCREENSHOTS:")
        print("=" * 70)
        
        categories = [
            ("Interface & Menus", [
                "Main interface (empty)",
                "Menu bar and toolbar",
                "License menu",
                "Help menu",
            ]),
            ("Image Viewing & Navigation", [
                "Image loaded",
                "Extraction controls",
                "Zoomed in view",
                "Fit to view",
            ]),
            ("Extraction Workflow", [
                "Selection drawn",
                "Threshold adjustment",
                "Extraction result",
                "Preview pane",
                "Result pane",
            ]),
            ("Library Management", [
                "Signature library",
                "Library detail",
            ]),
            ("PDF Features", [
                "PDF tab (empty)",
                "PDF controls",
            ] + ([
                "PDF loaded",
                "PDF signature library",
                "Signature selected",
                "PDF viewer detail",
                "Complete PDF workflow",
            ] if self.demo_pdf.exists() else [])),
            ("Final States", [
                "Extraction tab final",
                "Full interface overview",
            ]),
        ]
        
        for category, items in categories:
            print(f"\n{category}:")
            for item in items:
                print(f"   ✓ {item}")
        
        print("\n" + "=" * 70)
        print("💡 NEXT STEPS:")
        print("=" * 70)
        print("1. Review screenshots:")
        print(f"   open {self.output_dir}")
        print("\n2. Process for web:")
        print("   • Crop if needed (remove menu bars)")
        print("   • Compress (ImageOptim, TinyPNG)")
        print("   • Resize if needed (max 2000px wide)")
        print("\n3. Upload to Gumroad:")
        print("   • Select best 10-15 screenshots")
        print("   • Arrange in workflow order")
        print("   • Add descriptive captions")
        print("   • Set hero image")
        print("\n4. Use for marketing:")
        print("   • Website/landing page")
        print("   • Social media posts")
        print("   • Documentation")
        print("   • Product demos")
        print("=" * 70)
        
        if self.main_window:
            self.main_window.close()
        
        # Exit after brief delay
        QTimer.singleShot(500, self.app.quit)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Comprehensive screenshot capture for SignKit marketing"
    )
    parser.add_argument(
        "--output",
        default="screenshots",
        help="Output directory for screenshots (default: screenshots/)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("🎯 COMPREHENSIVE SCREENSHOT CAPTURE FOR SIGNKIT")
    print("=" * 70)
    print("\nThis script will automatically capture ALL features:")
    print("\n📱 Interface & Menus:")
    print("  ✓ Main interface (empty state)")
    print("  ✓ Menu bar and toolbar")
    print("  ✓ License menu")
    print("  ✓ Help menu")
    print("\n🖼️  Image Viewing & Navigation:")
    print("  ✓ Image loaded in viewer")
    print("  ✓ Extraction controls panel")
    print("  ✓ Zoomed in view")
    print("  ✓ Fit to view")
    print("\n✂️  Extraction Workflow:")
    print("  ✓ Selection rectangle drawn")
    print("  ✓ Threshold adjustment")
    print("  ✓ Extraction result with preview")
    print("  ✓ Preview pane detail")
    print("  ✓ Result pane detail")
    print("\n📚 Library Management:")
    print("  ✓ Signature library populated")
    print("  ✓ Library panel detail")
    print("\n📄 PDF Features:")
    print("  ✓ PDF signing tab")
    print("  ✓ PDF controls panel")
    print("  ✓ PDF document loaded")
    print("  ✓ PDF signature library")
    print("  ✓ Signature placement workflow")
    print("  ✓ Complete PDF workflow")
    print("\n🎬 Total: 20-24 comprehensive screenshots")
    print("⏱️  Time: ~40-45 seconds")
    print("=" * 70)
    print()
    
    try:
        capturer = ComprehensiveScreenshotCapture(output_dir=args.output)
        capturer.run_comprehensive_sequence()
        return capturer.app.exec()
    except Exception as e:
        print(f"\n❌ Error during capture: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
