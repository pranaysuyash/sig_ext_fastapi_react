from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor, QIcon, QKeySequence, QPalette, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from desktop_app.library import storage as lib
from desktop_app.views.bulk_sign_dialog import BulkSignDialog

try:
    from desktop_app.pdf.viewer import PDFViewer
    from desktop_app.pdf.signer import sign_pdf
    from desktop_app.pdf.db_audit import DatabaseAuditLogger as AuditLogger, get_audit_logs_for_pdf

    PDF_AVAILABLE = True
except ImportError as exc:  # pragma: no cover - optional dependency
    PDF_AVAILABLE = False
    PDF_IMPORT_ERROR = exc
else:
    PDF_IMPORT_ERROR = None


class PdfTabMixin:
    """PDF signing tab, audit logging, and signature placement helpers."""

    def _setup_pdf_ui(self) -> None:
        self._pdf_placeholder_tab = None
        self._pdf_tab_index = -1
        if not PDF_AVAILABLE:
            placeholder = QWidget()
            layout = QVBoxLayout(placeholder)
            layout.addStretch()

            # Title
            title = QLabel("📄 PDF Signing Unavailable")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setStyleSheet("font-size: 18px; font-weight: 600; color: #999; margin-bottom: 16px;")
            layout.addWidget(title)

            # Description
            description = QLabel(
                "PDF signing features require additional dependencies.\n\n"
                "To enable PDF signing, install the required libraries:"
            )
            description.setAlignment(Qt.AlignmentFlag.AlignCenter)
            description.setStyleSheet("font-size: 13px; color: #888; margin-bottom: 12px;")
            description.setWordWrap(True)
            layout.addWidget(description)

            # Installation command
            install_cmd = QLabel(
                "<code style='background-color: rgba(100, 100, 100, 0.2); "
                "padding: 8px 16px; border-radius: 6px; font-family: monospace;'>"
                "pip install pypdfium2 pikepdf"
                "</code>"
            )
            install_cmd.setAlignment(Qt.AlignmentFlag.AlignCenter)
            install_cmd.setTextFormat(Qt.TextFormat.RichText)
            install_cmd.setStyleSheet("font-size: 12px; margin: 12px 0;")
            layout.addWidget(install_cmd)

            # Error details if available
            if PDF_IMPORT_ERROR:
                error_label = QLabel(f"<small>Import error: {str(PDF_IMPORT_ERROR)}</small>")
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                error_label.setStyleSheet("font-size: 11px; color: #666; margin-top: 16px;")
                error_label.setWordWrap(True)
                layout.addWidget(error_label)

            # Help button
            help_btn = QPushButton("📖 Installation Help")
            help_btn.clicked.connect(lambda: self._open_document("docs/PDF_SETUP.md"))
            help_btn.setStyleSheet(
                "QPushButton { padding: 8px 16px; font-size: 13px; margin-top: 16px; }"
            )
            help_layout = QHBoxLayout()
            help_layout.addStretch()
            help_layout.addWidget(help_btn)
            help_layout.addStretch()
            layout.addLayout(help_layout)

            layout.addStretch()
            self._pdf_placeholder_tab = placeholder
            self._pdf_tab_index = self.tab_widget.addTab(placeholder, "📄 PDF Signing")

            # Add tooltip to tab explaining why it's disabled
            self.tab_widget.setTabToolTip(
                self._pdf_tab_index,
                "PDF signing features require pypdfium2 and pikepdf libraries"
            )
            return

        pdf_tab = QWidget()
        pdf_layout = QHBoxLayout(pdf_tab)

        # Create left panel exactly like extraction tab
        pdf_left_panel = QWidget()
        pdf_left_panel.setObjectName("pdfControlsPanel")
        pdf_left_panel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        pdf_left_panel.setFixedWidth(300)  # Match extraction tab exactly
        pdf_controls = QVBoxLayout(pdf_left_panel)
        pdf_controls.setContentsMargins(16, 18, 16, 18)  # Match extraction tab
        pdf_controls.setSpacing(10)  # Match extraction tab

        self._init_pdf_controls(pdf_controls)

        self.pdf_viewer = PDFViewer()
        self.pdf_viewer.signature_placed.connect(self._on_pdf_signature_placed)

        pdf_layout.addWidget(pdf_left_panel)
        pdf_layout.addWidget(self.pdf_viewer, 1)

        self._pdf_tab_index = self.tab_widget.addTab(pdf_tab, "📄 PDF Signing")
        self._init_pdf_features()
        self._setup_pdf_menu()

    def _init_pdf_controls(self, pdf_controls: QVBoxLayout) -> None:
        if not PDF_AVAILABLE:
            return

        pdf_controls.addWidget(QLabel("<b>PDF Document</b>"))

        open_pdf_btn = QPushButton("📂 Open PDF...")
        open_pdf_btn.clicked.connect(self._on_pdf_tab_open)
        pdf_controls.addWidget(open_pdf_btn)

        close_pdf_btn = QPushButton("✕ Close PDF")
        close_pdf_btn.clicked.connect(self._on_pdf_tab_close)
        pdf_controls.addWidget(close_pdf_btn)

        save_pdf_btn = QPushButton("💾 Save Signed PDF...")
        save_pdf_btn.clicked.connect(self._on_pdf_tab_save)
        pdf_controls.addWidget(save_pdf_btn)

        pdf_controls.addSpacing(20)

        pdf_controls.addWidget(QLabel("<b>Signature Library</b>"))
        pdf_controls.addWidget(QLabel("Click a signature, then click on PDF to place:"))

        self.pdf_sig_list = QListWidget()
        if sys.platform == "darwin":
            self.pdf_sig_list.setSpacing(3)
            self.pdf_sig_list.setWordWrap(False)
            self.pdf_sig_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pdf_sig_list.setMaximumHeight(300)
        self.pdf_sig_list.itemClicked.connect(self._on_pdf_signature_selected)
        pdf_controls.addWidget(self.pdf_sig_list)

        lib_buttons = QHBoxLayout()
        refresh_sig_btn = QPushButton("🔄 Refresh")
        refresh_sig_btn.clicked.connect(self._refresh_pdf_signature_library)
        lib_buttons.addWidget(refresh_sig_btn)

        paste_sig_btn = QPushButton("📋 Paste")
        paste_sig_btn.setToolTip("Paste signature from clipboard (Ctrl/Cmd+V)")
        paste_sig_btn.clicked.connect(self._on_pdf_paste_signature)
        lib_buttons.addWidget(paste_sig_btn)
        pdf_controls.addLayout(lib_buttons)

        bulk_sign_btn = QPushButton("📄 Apply to Multiple Pages...")
        bulk_sign_btn.setToolTip("Apply signature to multiple pages at once")
        bulk_sign_btn.clicked.connect(self._on_bulk_sign_clicked)
        pdf_controls.addWidget(bulk_sign_btn)

        pdf_controls.addSpacing(20)

        # Instructions panel - let theme system handle styling
        instructions = QLabel(
            "✨ <b>Quick Start</b><br><br>"
            "1️⃣ Click <b>Open PDF</b><br>"
            "2️⃣ Select a signature from library or paste<br>"
            "3️⃣ Click on PDF to place signature<br>"
            "4️⃣ Navigate pages and add more if needed<br>"
            "5️⃣ <b>Save Signed PDF</b> when complete<br><br>"
            "💡 Tip: Use Ctrl+Shift+V to paste from clipboard"
        )
        instructions.setObjectName("instructionsPanel")  # Let theme system style it
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        instructions.setTextFormat(Qt.TextFormat.RichText)
        pdf_controls.addWidget(instructions)

        pdf_controls.addSpacing(10)

        self.pdf_coord_tooltips_cb = QCheckBox("Show coordinate tooltips")
        self.pdf_coord_tooltips_cb.setToolTip("Display PDF page coordinates while hovering/moving/resizing signatures")
        self.pdf_coord_tooltips_cb.setChecked(False)
        self.pdf_coord_tooltips_cb.stateChanged.connect(self._on_pdf_coord_tooltips_toggled)
        pdf_controls.addWidget(self.pdf_coord_tooltips_cb)

        pdf_controls.addStretch()

    def _init_pdf_features(self):
        """Initialize PDF-specific state. Called from __init__ if PDF_AVAILABLE."""
        self.audit_logger: Optional[AuditLogger] = None
        self._pending_sig_path: Optional[str] = None
        self._current_pdf_path: Optional[str] = None
        # Bulk placement state
        self._bulk_pages: list = []
        self._bulk_sig_path: str = ""
        self._bulk_pixmap: Optional[QPixmap] = None
        self._bulk_use_same_pos: bool = False
    
    def _setup_pdf_menu(self):
        """Add PDF menu to menu bar. Called from __init__ if PDF_AVAILABLE."""
        pdf_menu = QMenu("&PDF", self)
        self.menuBar().addMenu(pdf_menu)
        
        open_pdf_act = QAction("&Open PDF...", self)
        open_pdf_act.setShortcut(QKeySequence("Ctrl+Shift+O"))
        open_pdf_act.setStatusTip("Open a PDF file for signing")
        open_pdf_act.triggered.connect(self.on_pdf_open)
        pdf_menu.addAction(open_pdf_act)
        
        close_pdf_act = QAction("&Close PDF", self)
        close_pdf_act.setStatusTip("Close the current PDF")
        close_pdf_act.triggered.connect(self.on_pdf_close)
        pdf_menu.addAction(close_pdf_act)
        
        pdf_menu.addSeparator()
        
        paste_sig_act = QAction("&Paste Signature from Clipboard", self)
        paste_sig_act.setShortcut(QKeySequence("Ctrl+Shift+V"))
        paste_sig_act.setStatusTip("Paste signature from clipboard for placement")
        paste_sig_act.triggered.connect(self._on_pdf_paste_signature)
        pdf_menu.addAction(paste_sig_act)
        
        pdf_menu.addSeparator()
        
        save_pdf_act = QAction("&Save Signed PDF...", self)
        save_pdf_act.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_pdf_act.setStatusTip("Save the signed PDF")
        save_pdf_act.triggered.connect(self.on_pdf_save)
        pdf_menu.addAction(save_pdf_act)
        
        pdf_menu.addSeparator()
        
        view_logs_act = QAction("View &Audit Logs", self)
        view_logs_act.setStatusTip("View audit logs for current PDF")
        view_logs_act.triggered.connect(self.on_pdf_view_audit_logs)
        pdf_menu.addAction(view_logs_act)
    
    def on_pdf_open(self):
        """Open a PDF file for signing."""
        if not PDF_AVAILABLE:
            QMessageBox.warning(self, "Feature Unavailable",
                              "PDF features require pypdfium2 and pikepdf.\n"
                              "Install with: pip install pypdfium2 pikepdf")
            return
        
        path = self._native_open_file("Open PDF", "PDF Files (*.pdf)")
        if not path:
            return
        
        # Initialize PDF state in session
        self.session.init_pdf_state()
        if self.session.pdf_state:
            self.session.pdf_state.current_pdf_path = path
        
        # For now, show a simple message (full viewer integration coming next)
        QMessageBox.information(
            self, "PDF Opened",
            f"PDF opened: {Path(path).name}\n\n"
            "Full PDF viewer with signature placement coming in next phase.\n"
            "You can already:\n"
            "• Use signature library\n"
            "• Sign PDFs programmatically\n"
            "• Track audit logs"
        )
        
        # Initialize audit logger
        self.audit_logger = AuditLogger(path, self.session.user_email)
        self.audit_logger.log_open()
        
        self.statusBar().showMessage(f"Opened PDF: {Path(path).name}")
        if hasattr(self, "_refresh_toolbar_action_states"):
            self._refresh_toolbar_action_states()
    
    def on_pdf_close(self):
        """Close the current PDF."""
        if self.session.pdf_state:
            self.session.clear_pdf_state()
            self.audit_logger = None
            self.statusBar().showMessage("PDF closed")
        else:
            self.statusBar().showMessage("No PDF open")
        if hasattr(self, "_refresh_toolbar_action_states"):
            self._refresh_toolbar_action_states()
    
    def on_pdf_save(self):
        """Save the signed PDF."""
        if not self.session.pdf_state or not self.session.pdf_state.current_pdf_path:
            QMessageBox.warning(self, "No PDF", "No PDF is currently open")
            return
        
        placed_sigs = []
        if hasattr(self, "pdf_viewer") and self.pdf_viewer:
            placed_sigs = self.pdf_viewer.get_placed_signatures()
        elif self.session.pdf_state:
            placed_sigs = list(self.session.pdf_state.placed_signatures)

        if self.session.pdf_state is not None:
            self.session.pdf_state.placed_signatures = list(placed_sigs)
        if not placed_sigs:
            reply = QMessageBox.question(
                self, "No Signatures",
                "No signatures have been placed. Save anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # Ask for output path
        original_name = Path(self.session.pdf_state.current_pdf_path).name
        default_name = f"{Path(original_name).stem}_signed.pdf"
        
        output_path = self._native_save_file("Save Signed PDF", default_name, "PDF Files (*.pdf)")
        if not output_path:
            return
        
        # Sign PDF
        try:
            success = sign_pdf(
                self.session.pdf_state.current_pdf_path,
                output_path,
                placed_sigs
            )
            
            if success:
                # Log save operation
                if self.audit_logger:
                    self.audit_logger.log_save(output_path, len(placed_sigs))
                
                QMessageBox.information(
                    self, "Success",
                    f"Signed PDF saved to:\n{output_path}"
                )
                self.statusBar().showMessage(f"Saved: {Path(output_path).name}")
            else:
                raise Exception("PDF signing failed")
                
        except Exception as e:
            if self.audit_logger:
                self.audit_logger.log_error("save_failed", str(e))
            QMessageBox.critical(self, "Error", f"Failed to save PDF:\n{e}")
        finally:
            if hasattr(self, "_refresh_toolbar_action_states"):
                self._refresh_toolbar_action_states()
    
    def on_pdf_view_audit_logs(self):
        """View audit logs for current PDF."""
        if not self.session.pdf_state or not self.session.pdf_state.current_pdf_path:
            QMessageBox.warning(self, "No PDF", "No PDF is currently open")
            return
        
        logs = get_audit_logs_for_pdf(self.session.pdf_state.current_pdf_path)
        
        if not logs:
            QMessageBox.information(self, "Audit Logs", "No audit logs found for this PDF")
            return
        
        # Display logs in a dialog
        log_text = "\n\n".join([
            f"[{log.timestamp}] {log.operation}\n{log.details}"
            for log in logs
        ])
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Audit Logs")
        dialog.resize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(log_text)
        layout.addWidget(text_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        
        dialog.exec()
    
    # ========== PDF TAB EVENT HANDLERS ==========
    
    def _on_pdf_tab_open(self):
        """Open PDF in the PDF tab viewer."""
        path = self._native_open_file("Open PDF", "PDF Files (*.pdf)")
        if not path:
            return
        
        # Open in viewer
        success = self.pdf_viewer.open_pdf(path)
        if not success:
            return
        
        # Initialize state
        self.session.init_pdf_state()
        if self.session.pdf_state:
            self.session.pdf_state.current_pdf_path = path
        self._current_pdf_path = path
        
        # Initialize audit logger
        self.audit_logger = AuditLogger(path, self.session.user_email)
        self.audit_logger.log_open()
        
        # Refresh signature library
        self._refresh_pdf_signature_library()
        
        self.statusBar().showMessage(f"📄 Opened: {Path(path).name}")
        if hasattr(self, "_refresh_toolbar_action_states"):
            self._refresh_toolbar_action_states()
    
    def _on_tab_changed(self, index: int):
        """Handle tab change - refresh PDF signature library when switching to PDF tab."""
        if PDF_AVAILABLE and index == getattr(self, "_pdf_tab_index", -1):
            self._refresh_pdf_signature_library()
        if hasattr(self, "_update_toolbar_for_tab"):
            self._update_toolbar_for_tab(index)
    
    def _on_pdf_coord_tooltips_toggled(self, state):
        """Toggle coordinate tooltips in PDF viewer."""
        enabled = bool(state)
        if self.pdf_viewer:
            self.pdf_viewer.enable_coordinate_tooltips(enabled)
    
    def _on_source_coord_tooltips_toggled(self, state):
        """Toggle coordinate tooltips in Source, Preview, and Result image views."""
        enabled = bool(state)
        if self.src_view:
            self.src_view.enable_coordinate_tooltips(enabled)
        if self.preview_view:
            self.preview_view.enable_coordinate_tooltips(enabled)
        if self.res_view:
            self.res_view.enable_coordinate_tooltips(enabled)
    
    def _on_pdf_tab_close(self):
        """Close PDF in the PDF tab."""
        self.pdf_viewer.close_pdf()
        if self.session.pdf_state:
            self.session.clear_pdf_state()
        self._current_pdf_path = None
        self.audit_logger = None
        self.statusBar().showMessage("PDF closed")
        if hasattr(self, "_refresh_toolbar_action_states"):
            self._refresh_toolbar_action_states()
    
    def _on_pdf_tab_save(self):
        """Save signed PDF from the PDF tab."""
        if not self._current_pdf_path:
            QMessageBox.warning(self, "No PDF", "No PDF is currently open")
            return
        
        # Get all placed signatures from viewer (already includes sig_path)
        placed_sigs = self.pdf_viewer.get_placed_signatures()
        
        if not placed_sigs:
            reply = QMessageBox.question(
                self, "No Signatures",
                "No signatures have been placed. Save anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # Ask for output path
        original_name = Path(self._current_pdf_path).name
        default_name = f"{Path(original_name).stem}_signed.pdf"
        
        output_path = self._native_save_file("Save Signed PDF", default_name, "PDF Files (*.pdf)")
        if not output_path:
            return
        
        # Sign PDF (placed_sigs already contains sig_path for each signature)
        try:
            success = sign_pdf(
                self._current_pdf_path,
                output_path,
                placed_sigs
            )
            
            if success:
                # Log save operation
                if self.audit_logger:
                    self.audit_logger.log_save(output_path, len(placed_sigs))
                
                QMessageBox.information(
                    self, "Success",
                    f"✅ Signed PDF saved to:\n{output_path}\n\n"
                    f"Signatures placed: {len(placed_sigs)}"
                )
                self.statusBar().showMessage(f"💾 Saved: {Path(output_path).name}")
            else:
                QMessageBox.warning(self, "Error", "Failed to save signed PDF")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving PDF:\n{e}")
            if self.audit_logger:
                self.audit_logger.log_error("save_failed", str(e))
        finally:
            if hasattr(self, "_refresh_toolbar_action_states"):
                self._refresh_toolbar_action_states()
    
    def _on_pdf_signature_selected(self, item):
        """Handle signature selection from library."""
        sig_path = item.data(Qt.ItemDataRole.UserRole)
        if not sig_path or not Path(sig_path).exists():
            return
        
        # Check if PDF is open
        if not self.pdf_viewer or not self.pdf_viewer.renderer:
            QMessageBox.information(
                self, "No PDF Open",
                "Please open a PDF document first before selecting a signature."
            )
            return
        
        # Load signature image
        pixmap = QPixmap(sig_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Error", "Failed to load signature image")
            return
        
        # Store path for later use when saving
        self._pending_sig_path = sig_path
        
        # Set signature for placement in viewer (with path)
        self.pdf_viewer.set_signature_for_placement(pixmap, sig_path)
        
        self.statusBar().showMessage(f"✏️ Click on PDF to place signature: {Path(sig_path).name}")
    
    def _on_pdf_signature_placed(self, page, x, y, width, height):
        """Handle signature placement on PDF."""
        # Check if this is bulk placement
        if self._bulk_pages and self._bulk_pixmap:
            # Apply to all selected pages at same position
            current_page = self.pdf_viewer.current_page
            
            for target_page in self._bulk_pages:
                if target_page == current_page:
                    # Already placed on current page by user click
                    continue
                
                # Navigate to target page and place signature
                self.pdf_viewer.goto_page(target_page)
                self.pdf_viewer.page_view.add_signature_overlay(
                    x, y, width, height,
                    self._bulk_pixmap,
                    self._bulk_sig_path
                )
                
                if self.audit_logger:
                    self.audit_logger.log_place_signature(
                        target_page, self._bulk_sig_path, x, y, width, height
                    )
            
            # Return to original page
            self.pdf_viewer.goto_page(current_page)
            
            self.statusBar().showMessage(
                f"✅ Signature placed on {len(self._bulk_pages)} page(s)"
            )
            
            # Clear bulk state
            self._bulk_pages = []
            self._bulk_sig_path = ""
            self._bulk_pixmap = None
            self._bulk_use_same_pos = False
        else:
            # Single placement
            if self.audit_logger and self._pending_sig_path:
                self.audit_logger.log_place_signature(
                    page, self._pending_sig_path, x, y, width, height
                )
            
            self.statusBar().showMessage(f"✅ Signature placed on page {page + 1}")
    
    def _on_pdf_paste_signature(self):
        """Paste signature from clipboard for placement."""
        import tempfile
        import uuid
        
        # Check if PDF is open
        if not self.pdf_viewer or not self.pdf_viewer.renderer:
            QMessageBox.information(
                self, "No PDF Open",
                "Please open a PDF document first before pasting a signature."
            )
            return
        
        clipboard = QApplication.clipboard()
        pixmap = clipboard.pixmap()
        
        if pixmap.isNull():
            QMessageBox.information(
                self, "No Image in Clipboard",
                "No image found in clipboard.\n\n"
                "Copy a signature from the Extraction tab first."
            )
            return
        
        # Save clipboard image to temp location for tracking
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"clipboard_sig_{uuid.uuid4().hex[:8]}.png")
        
        # Save pixmap to temp file
        if not pixmap.save(temp_path, "PNG"):
            QMessageBox.warning(self, "Error", "Failed to process clipboard image")
            return
        
        self._pending_sig_path = temp_path
        
        # Set signature for placement in viewer (with path)
        self.pdf_viewer.set_signature_for_placement(pixmap, temp_path)
        
        self.statusBar().showMessage("📋 Click on PDF to place clipboard signature")
    
    def _refresh_pdf_signature_library(self):
        """Refresh the signature library list in PDF tab with coordinate tooltips."""
        self.pdf_sig_list.clear()
        
        # Get signatures from library with metadata
        items = lib.list_items()
        
        if not items:
            item = QListWidgetItem("📝 No signatures saved yet")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            item.setForeground(Qt.GlobalColor.gray)
            self.pdf_sig_list.addItem(item)
            
            item2 = QListWidgetItem("💡 Extract & save signatures")
            item2.setFlags(Qt.ItemFlag.NoItemFlags)
            item2.setForeground(Qt.GlobalColor.gray)
            self.pdf_sig_list.addItem(item2)
            
            item3 = QListWidgetItem("   in the Extraction tab first")
            item3.setFlags(Qt.ItemFlag.NoItemFlags)
            item3.setForeground(Qt.GlobalColor.gray)
            self.pdf_sig_list.addItem(item3)
            return
        
        for lib_item in items:
            if not Path(lib_item.path).exists():
                continue
            
            # Create list item with preview
            item = QListWidgetItem(Path(lib_item.path).name)
            
            # Load and scale thumbnail
            pixmap = QPixmap(lib_item.path)
            if not pixmap.isNull():
                thumbnail = pixmap.scaled(
                    80, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                from PySide6.QtGui import QIcon
                item.setIcon(QIcon(thumbnail))
            
            item.setData(Qt.ItemDataRole.UserRole, lib_item.path)
            item.setToolTip(lib_item.tooltip_text)  # Show coordinates in tooltip
            self.pdf_sig_list.addItem(item)
    
    def _on_bulk_sign_clicked(self):
        """Handle bulk signature placement across multiple pages."""
        if not self.pdf_viewer or not self.pdf_viewer.renderer:
            QMessageBox.information(
                self, "No PDF Open",
                "Please open a PDF document first."
            )
            return
        
        # Get selected signature from library
        selected_items = self.pdf_sig_list.selectedItems()
        if not selected_items:
            QMessageBox.information(
                self, "No Signature Selected",
                "Please select a signature from the library first."
            )
            return
        
        sig_path = selected_items[0].data(Qt.ItemDataRole.UserRole)
        if not sig_path or not Path(sig_path).exists():
            QMessageBox.warning(self, "Error", "Signature file not found")
            return
        
        # Load signature
        pixmap = QPixmap(sig_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Error", "Failed to load signature image")
            return
        
        # Show bulk placement dialog
        dialog = BulkSignDialog(
            self.pdf_viewer.renderer.page_count(),
            self.pdf_viewer.current_page,
            self
        )
        
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        selected_pages = dialog.get_selected_pages()
        use_same_pos = dialog.use_same_position()
        
        if not selected_pages:
            return
        
        # Ask user to click where to place signature
        reply = QMessageBox.information(
            self, "Place Signature",
            f"Click on the PDF to choose where to place the signature.\n\n"
            f"It will be applied to {len(selected_pages)} page(s): {', '.join(str(p+1) for p in selected_pages[:5])}"
            f"{'...' if len(selected_pages) > 5 else ''}",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        
        if reply != QMessageBox.StandardButton.Ok:
            return
        
        # Store bulk placement info and set signature for placement
        self._bulk_pages = selected_pages
        self._bulk_sig_path = sig_path
        self._bulk_pixmap = pixmap
        self._bulk_use_same_pos = use_same_pos
        
        self.pdf_viewer.set_signature_for_placement(pixmap, sig_path)
        self.statusBar().showMessage(
            f"📄 Click to place signature on {len(selected_pages)} page(s)"
        )
