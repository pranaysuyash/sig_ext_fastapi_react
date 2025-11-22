import logging
from typing import Optional, cast
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, 
    QLabel, QPushButton, QSplitter, QMessageBox, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QPixmap, QImage, QColor

from desktop_app.processing.vault import NotaryVault
from desktop_app.resources.icons import get_icon, set_button_icon
from desktop_app.widgets.image_view import ImageView

LOG = logging.getLogger(__name__)

class VaultTab(QWidget):
    """Tab for managing securely stored signatures."""
    
    def __init__(self, vault: NotaryVault):
        super().__init__()
        self.vault = vault
        self._setup_ui()
        self.refresh_list()
        
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # --- Left Panel: Signature List ---
        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_panel.setStyleSheet("background-color: palette(window); border-right: 1px solid palette(mid);")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # Header
        header = QLabel("Notary Vault")
        header.setStyleSheet("font-weight: bold; font-size: 14px; padding: 12px 16px;")
        left_layout.addWidget(header)
        
        # List Widget
        self.sig_list = QListWidget()
        self.sig_list.setFrameShape(QFrame.Shape.NoFrame)
        self.sig_list.setIconSize(QSize(48, 48))
        self.sig_list.currentItemChanged.connect(self._on_selection_changed)
        left_layout.addWidget(self.sig_list)
        
        # Refresh Button (Bottom)
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(12, 12, 12, 12)
        self.refresh_btn = QPushButton("Refresh Vault")
        self.refresh_btn.clicked.connect(self.refresh_list)
        btn_layout.addWidget(self.refresh_btn)
        left_layout.addLayout(btn_layout)
        
        layout.addWidget(left_panel)
        
        # --- Right Panel: Preview & Actions ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(16)
        
        # Info Header
        self.info_label = QLabel("Select a signature to view details")
        self.info_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        right_layout.addWidget(self.info_label)
        
        # Metadata Label
        self.meta_label = QLabel("")
        self.meta_label.setStyleSheet("color: #666;")
        right_layout.addWidget(self.meta_label)
        
        # Preview Area (ImageView)
        self.preview_view = ImageView()
        self.preview_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # Style it to look like a "safe" viewing area
        self.preview_view.setStyleSheet("border: 1px dashed #ccc; border-radius: 8px; background-color: palette(base);")
        right_layout.addWidget(self.preview_view)
        
        # Actions Toolbar
        actions_layout = QHBoxLayout()
        
        self.copy_btn = QPushButton("Copy to Clipboard")
        set_button_icon(self.copy_btn, "copy", "Copy", use_emoji=False)
        self.copy_btn.clicked.connect(self._on_copy)
        self.copy_btn.setEnabled(False)
        
        self.delete_btn = QPushButton("Delete")
        set_button_icon(self.delete_btn, "delete", "Delete", use_emoji=False)
        self.delete_btn.setStyleSheet("color: #d32f2f;")
        self.delete_btn.clicked.connect(self._on_delete)
        self.delete_btn.setEnabled(False)
        
        actions_layout.addWidget(self.copy_btn)
        actions_layout.addStretch()
        actions_layout.addWidget(self.delete_btn)
        
        right_layout.addLayout(actions_layout)
        
        layout.addWidget(right_panel)
        
    def refresh_list(self):
        """Reload signatures from vault."""
        self.sig_list.clear()
        self.preview_view.clear_image()
        self.info_label.setText("Select a signature")
        self.meta_label.setText("")
        self.copy_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        
        try:
            signatures = self.vault.list_signatures()
            for sig in signatures:
                item = QListWidgetItem()
                # Use date as label
                import datetime
                date_str = datetime.datetime.fromtimestamp(sig['created_at']).strftime('%Y-%m-%d %H:%M')
                item.setText(f"{date_str}\n{sig.get('source_name', 'Unknown Source')}")
                item.setData(Qt.ItemDataRole.UserRole, sig['id'])
                item.setData(Qt.ItemDataRole.UserRole + 1, sig)
                
                # Set icon based on health score if available
                score = sig.get('health_score', 0)
                if score >= 80:
                    item.setIcon(get_icon("check")) # Placeholder for Excellent
                elif score >= 50:
                    item.setIcon(get_icon("warning")) # Placeholder for Good
                else:
                    item.setIcon(get_icon("error")) # Placeholder for Poor
                    
                self.sig_list.addItem(item)
                
        except Exception as e:
            LOG.error(f"Failed to list signatures: {e}")
            QMessageBox.critical(self, "Vault Error", f"Failed to load vault: {e}")

    def _on_selection_changed(self, current: QListWidgetItem, previous: QListWidgetItem):
        if not current:
            return
            
        sig_id = current.data(Qt.ItemDataRole.UserRole)
        meta = current.data(Qt.ItemDataRole.UserRole + 1)
        
        self.info_label.setText(f"Signature {sig_id[:8]}...")
        
        # Format metadata
        import datetime
        date_str = datetime.datetime.fromtimestamp(meta['created_at']).strftime('%Y-%m-%d %H:%M:%S')
        details = [
            f"Created: {date_str}",
            f"Source: {meta.get('source_name', 'N/A')}",
            f"Size: {meta.get('size_bytes', 0) / 1024:.1f} KB",
            f"Quality: {meta.get('health_rating', 'Unknown')} ({meta.get('health_score', 0)}/100)"
        ]
        self.meta_label.setText(" • ".join(details))
        
        # Load and decrypt image
        try:
            png_bytes = self.vault.retrieve_signature(sig_id)
            self.preview_view.load_image_bytes(png_bytes)
            self.copy_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        except Exception as e:
            LOG.error(f"Failed to retrieve signature {sig_id}: {e}")
            self.preview_view.clear_image()
            self.info_label.setText("Error loading signature")
            QMessageBox.warning(self, "Decryption Failed", "Could not decrypt this signature.")

    def _on_copy(self):
        """Copy current signature to clipboard."""
        if self.preview_view.pixmap_item and self.preview_view.pixmap_item.pixmap():
            from PySide6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(self.preview_view.pixmap_item.pixmap())
            
            # Flash button or show status
            orig_text = self.copy_btn.text()
            self.copy_btn.setText("Copied!")
            from PySide6.QtCore import QTimer
            QTimer.singleShot(1000, lambda: self.copy_btn.setText(orig_text))

    def _on_delete(self):
        """Delete current signature."""
        item = self.sig_list.currentItem()
        if not item:
            return
            
        sig_id = item.data(Qt.ItemDataRole.UserRole)
        
        confirm = QMessageBox.question(
            self, "Delete Signature",
            "Are you sure you want to permanently delete this signature from the vault?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.vault.delete_signature(sig_id)
                self.refresh_list()
            except Exception as e:
                QMessageBox.critical(self, "Delete Failed", str(e))
