"""Export dialog with professional options for signature extraction results."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QRadioButton, QButtonGroup, QCheckBox, QSpinBox, QGroupBox,
    QFileDialog, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QColor
from PIL import Image
import io


class ExportDialog(QDialog):
    """Dialog for exporting processed signatures with professional options."""
    
    def __init__(self, png_bytes: bytes, parent=None):
        super().__init__(parent)
        self.png_bytes = png_bytes
        self.result_path = None
        
        self.setWindowTitle("Export Options")
        self.setModal(True)
        self.resize(480, 520)
        
        layout = QVBoxLayout(self)
        
        # Format options
        format_group = QGroupBox("Format")
        format_layout = QVBoxLayout()
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG (Recommended)", "JPEG (No Transparency)", "PNG-8 (Smaller)"])
        self.format_combo.currentIndexChanged.connect(self._on_format_changed)
        format_layout.addWidget(self.format_combo)
        
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        # Background options
        bg_group = QGroupBox("Background")
        bg_layout = QVBoxLayout()
        
        self.bg_button_group = QButtonGroup(self)
        self.bg_transparent = QRadioButton("Transparent (PNG only)")
        self.bg_white = QRadioButton("White")
        self.bg_black = QRadioButton("Black")
        self.bg_custom = QRadioButton("Custom Color")
        
        self.bg_transparent.setChecked(True)
        
        for rb in (self.bg_transparent, self.bg_white, self.bg_black, self.bg_custom):
            self.bg_button_group.addButton(rb)
            bg_layout.addWidget(rb)
        
        self.bg_custom_btn = QPushButton("Pick Color...")
        self.bg_custom_btn.clicked.connect(self._pick_custom_bg)
        self.bg_custom_btn.setEnabled(False)
        self.bg_custom.toggled.connect(lambda checked: self.bg_custom_btn.setEnabled(checked))
        bg_layout.addWidget(self.bg_custom_btn)
        
        self._custom_bg_color = QColor(255, 255, 255)
        
        bg_group.setLayout(bg_layout)
        layout.addWidget(bg_group)
        
        # Crop/Trim options
        crop_group = QGroupBox("Canvas Options")
        crop_layout = QVBoxLayout()
        
        self.trim_checkbox = QCheckBox("Trim to content bounds (remove empty space)")
        self.trim_checkbox.setChecked(False)
        crop_layout.addWidget(self.trim_checkbox)
        
        padding_row = QHBoxLayout()
        padding_row.addWidget(QLabel("Padding (pixels):"))
        self.padding_spin = QSpinBox()
        self.padding_spin.setRange(0, 100)
        self.padding_spin.setValue(0)
        self.padding_spin.setEnabled(False)
        self.trim_checkbox.toggled.connect(self.padding_spin.setEnabled)
        padding_row.addWidget(self.padding_spin)
        padding_row.addStretch(1)
        crop_layout.addLayout(padding_row)
        
        crop_group.setLayout(crop_layout)
        layout.addWidget(crop_group)
        
        # Quality options (for JPEG)
        quality_group = QGroupBox("Quality")
        quality_layout = QHBoxLayout()
        
        quality_layout.addWidget(QLabel("JPEG Quality:"))
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(90)
        self.quality_spin.setSuffix("%")
        self.quality_spin.setEnabled(False)
        quality_layout.addWidget(self.quality_spin)
        quality_layout.addStretch(1)
        
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        
        export_btn = QPushButton("💾 Export...")
        export_btn.setDefault(True)
        export_btn.clicked.connect(self._export)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        # Preview info
        info_label = QLabel("💡 Tip: Use transparent PNG for signatures, white/black backgrounds for document embedding.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-size: 11px; padding: 8px;")
        layout.addWidget(info_label)
        
    def _on_format_changed(self, index):
        """Enable/disable options based on format."""
        is_jpeg = "JPEG" in self.format_combo.currentText()
        
        # JPEG doesn't support transparency
        if is_jpeg:
            self.bg_transparent.setEnabled(False)
            if self.bg_transparent.isChecked():
                self.bg_white.setChecked(True)
            self.quality_spin.setEnabled(True)
        else:
            self.bg_transparent.setEnabled(True)
            self.quality_spin.setEnabled(False)
    
    def _pick_custom_bg(self):
        from PySide6.QtWidgets import QColorDialog
        color = QColorDialog.getColor(self._custom_bg_color, self, "Pick Background Color")
        if color.isValid():
            self._custom_bg_color = color
    
    def _export(self):
        """Perform the export with selected options."""
        try:
            # Load the PNG bytes
            pil_image = Image.open(io.BytesIO(self.png_bytes))
            
            # Ensure RGBA mode for processing
            if pil_image.mode != 'RGBA':
                pil_image = pil_image.convert('RGBA')
            
            # Apply background if not transparent
            if not self.bg_transparent.isChecked():
                # Determine background color
                if self.bg_white.isChecked():
                    bg_color = (255, 255, 255, 255)
                elif self.bg_black.isChecked():
                    bg_color = (0, 0, 0, 255)
                else:  # custom
                    bg_color = (
                        self._custom_bg_color.red(),
                        self._custom_bg_color.green(),
                        self._custom_bg_color.blue(),
                        255
                    )
                
                # Composite onto background
                background = Image.new('RGBA', pil_image.size, bg_color)
                pil_image = Image.alpha_composite(background, pil_image)
            
            # Trim to content bounds if requested
            if self.trim_checkbox.isChecked():
                pil_image = self._trim_to_content(pil_image, self.padding_spin.value())
            
            # Determine format and extension
            format_text = self.format_combo.currentText()
            if "JPEG" in format_text:
                ext = "*.jpg *.jpeg"
                save_format = "JPEG"
                pil_image = pil_image.convert('RGB')  # JPEG doesn't support alpha
            elif "PNG-8" in format_text:
                ext = "*.png"
                save_format = "PNG"
                # Convert to P mode (palette) for smaller file size
                pil_image = pil_image.convert('P', palette=Image.ADAPTIVE, colors=256)
            else:  # PNG-24
                ext = "*.png"
                save_format = "PNG"
            
            # Get save path
            default_name = "signature.png" if save_format == "PNG" else "signature.jpg"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export As",
                default_name,
                f"{save_format} Image ({ext})"
            )
            
            if not file_path:
                return
            
            # Save with appropriate options
            save_kwargs = {}
            if save_format == "JPEG":
                save_kwargs['quality'] = self.quality_spin.value()
                save_kwargs['optimize'] = True
            elif save_format == "PNG":
                save_kwargs['optimize'] = True
            
            pil_image.save(file_path, save_format, **save_kwargs)
            
            self.result_path = file_path
            self.accept()
            
            QMessageBox.information(self, "Export Successful", f"Saved to:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Error: {str(e)}")
    
    def _trim_to_content(self, image: Image.Image, padding: int = 0) -> Image.Image:
        """Trim image to content bounding box with optional padding."""
        if image.mode != 'RGBA':
            return image
        
        # Get alpha channel
        alpha = image.split()[-1]
        
        # Find bounding box of non-transparent pixels
        bbox = alpha.getbbox()
        
        if bbox is None:
            # Image is completely transparent, return as-is
            return image
        
        # Add padding
        x1, y1, x2, y2 = bbox
        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(image.width, x2 + padding)
        y2 = min(image.height, y2 + padding)
        
        # Crop to bounding box
        return image.crop((x1, y1, x2, y2))
