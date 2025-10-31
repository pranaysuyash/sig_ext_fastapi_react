"""Dialog for bulk signature placement across multiple PDF pages."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton,
    QLineEdit, QDialogButtonBox, QGroupBox, QSpinBox, QCheckBox
)


class BulkSignDialog(QDialog):
    """Dialog to configure bulk signature placement."""
    
    def __init__(self, total_pages: int, current_page: int, parent=None):
        super().__init__(parent)
        self.total_pages = total_pages
        self.current_page = current_page
        self.setWindowTitle("Apply Signature to Multiple Pages")
        self.setMinimumWidth(400)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Info label
        info = QLabel(
            f"Apply signature to multiple pages\n"
            f"Current page: {self.current_page + 1} of {self.total_pages}"
        )
        layout.addWidget(info)
        
        # Page selection group
        page_group = QGroupBox("Page Selection")
        page_layout = QVBoxLayout(page_group)
        
        self.current_page_radio = QRadioButton(f"Current page only ({self.current_page + 1})")
        self.current_page_radio.setChecked(True)
        page_layout.addWidget(self.current_page_radio)
        
        self.all_pages_radio = QRadioButton(f"All pages (1-{self.total_pages})")
        page_layout.addWidget(self.all_pages_radio)
        
        self.range_radio = QRadioButton("Page range:")
        page_layout.addWidget(self.range_radio)
        
        # Range input
        range_layout = QHBoxLayout()
        range_layout.addSpacing(30)
        range_layout.addWidget(QLabel("Pages:"))
        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText("e.g., 1,3,5-7,10")
        self.range_input.setEnabled(False)
        self.range_radio.toggled.connect(lambda checked: self.range_input.setEnabled(checked))
        range_layout.addWidget(self.range_input)
        page_layout.addLayout(range_layout)
        
        # Every N pages option
        self.every_n_radio = QRadioButton("Every N pages:")
        page_layout.addWidget(self.every_n_radio)
        
        every_layout = QHBoxLayout()
        every_layout.addSpacing(30)
        every_layout.addWidget(QLabel("Every:"))
        self.every_n_spin = QSpinBox()
        self.every_n_spin.setMinimum(1)
        self.every_n_spin.setMaximum(self.total_pages)
        self.every_n_spin.setValue(2)
        self.every_n_spin.setEnabled(False)
        self.every_n_radio.toggled.connect(lambda checked: self.every_n_spin.setEnabled(checked))
        every_layout.addWidget(self.every_n_spin)
        every_layout.addWidget(QLabel("pages"))
        every_layout.addStretch()
        page_layout.addLayout(every_layout)
        
        layout.addWidget(page_group)
        
        # Position group
        pos_group = QGroupBox("Signature Position")
        pos_layout = QVBoxLayout(pos_group)
        
        self.same_position_check = QCheckBox("Use same position on all pages")
        self.same_position_check.setChecked(True)
        pos_layout.addWidget(self.same_position_check)
        
        pos_help = QLabel(
            "<small>The signature will be placed at the position you click\n"
            "on the current page and repeated at the same position\n"
            "on all selected pages.</small>"
        )
        pos_help.setWordWrap(True)
        pos_layout.addWidget(pos_help)
        
        layout.addWidget(pos_group)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_selected_pages(self) -> list[int]:
        """
        Get the list of selected page numbers (0-indexed).
        
        Returns:
            List of page numbers to apply signature to
        """
        if self.current_page_radio.isChecked():
            return [self.current_page]
        
        elif self.all_pages_radio.isChecked():
            return list(range(self.total_pages))
        
        elif self.range_radio.isChecked():
            # Parse range string like "1,3,5-7,10"
            pages = set()
            range_text = self.range_input.text().strip()
            
            if not range_text:
                return [self.current_page]
            
            try:
                parts = range_text.split(',')
                for part in parts:
                    part = part.strip()
                    if '-' in part:
                        # Range like "5-7"
                        start, end = part.split('-')
                        start = int(start.strip())
                        end = int(end.strip())
                        for p in range(start, end + 1):
                            if 1 <= p <= self.total_pages:
                                pages.add(p - 1)  # Convert to 0-indexed
                    else:
                        # Single page
                        p = int(part)
                        if 1 <= p <= self.total_pages:
                            pages.add(p - 1)  # Convert to 0-indexed
                
                return sorted(list(pages))
            
            except ValueError:
                # Invalid format, return current page
                return [self.current_page]
        
        elif self.every_n_radio.isChecked():
            n = self.every_n_spin.value()
            return list(range(0, self.total_pages, n))
        
        return [self.current_page]
    
    def use_same_position(self) -> bool:
        """Check if signature should use the same position on all pages."""
        return self.same_position_check.isChecked()
