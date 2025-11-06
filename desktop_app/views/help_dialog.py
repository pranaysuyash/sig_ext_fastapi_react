"""Help dialog with rendered Markdown content."""

from pathlib import Path
from types import ModuleType
from typing import Optional, TYPE_CHECKING, Any
import sys

from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QPalette

from desktop_app.widgets.modern_mac_button import ModernMacButton


def _create_button(
    text: str = "",
    parent: Optional[QDialog] = None,
    *,
    use_modern_mac: Optional[bool] = None,
    primary: bool = False,
    color: str = 'blue',
    compact: bool = False  # Dialog buttons are typically not compact
) -> QPushButton:
    """Create a button, using ModernMacButton on macOS if available and requested.

    Args:
        text: Button text
        parent: Parent widget
        use_modern_mac: Force modern button (default: auto-detect macOS)
        primary: True for primary action buttons (colored)
        color: One of 'blue', 'purple', 'pink', 'red', 'orange', 'yellow', 'green', 'teal'
        compact: True for smaller buttons (sidebar/toolbar), False for larger (dialogs)
    """
    if use_modern_mac is None:
        use_modern_mac = sys.platform == "darwin"

    if use_modern_mac:
        try:
            btn = ModernMacButton(
                text, parent,
                primary=primary,
                color=color,
                glass=True,
                compact=compact
            )
            return btn
        except (NameError, TypeError):
            # Fallback if ModernMacButton not available or doesn't support compact
            pass

    # Default to standard QPushButton
    return QPushButton(text, parent)

_markdown_runtime: Optional[ModuleType]
try:
    import markdown as _markdown_runtime  # type: ignore[import-untyped]
except ImportError:
    _markdown_runtime = None

MARKDOWN_AVAILABLE = _markdown_runtime is not None
markdown: Optional[ModuleType] = _markdown_runtime


class HelpDialog(QDialog):
    """Dialog to display help documentation with rendered Markdown."""
    
    def __init__(self, markdown_file: str, parent=None):
        """
        Initialize help dialog.
        
        Args:
            markdown_file: Path to markdown file (relative to project root)
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.resize(800, 600)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create text browser
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setOpenLinks(True)
        
        # Set font
        font = QFont("Arial", 11)
        self.text_browser.setFont(font)
        
        # Load and render markdown
        self._load_markdown(markdown_file)
        
        layout.addWidget(self.text_browser)
        
        # Add close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_button = _create_button("Close", self)
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _load_markdown(self, relative_path: str):
        """Load and render markdown file."""
        try:
            # Get current palette for theme-aware colors
            palette = self.palette()
            is_dark = palette.color(QPalette.ColorRole.Window).lightness() < 128
            
            # Theme-aware colors
            if is_dark:
                text_color = "#e0e0e0"
                heading_color = "#ffffff"
                border_color = "#555555"
                code_bg = "#2d2d2d"
                pre_bg = "#1e1e1e"
                table_header_bg = "#3a3a3a"
                link_color = "#4da6ff"
                blockquote_border = "#666666"
                hr_color = "#555555"
            else:
                text_color = "#333333"
                heading_color = "#2c3e50"
                border_color = "#3498db"
                code_bg = "#f4f4f4"
                pre_bg = "#f8f8f8"
                table_header_bg = "#f2f2f2"
                link_color = "#3498db"
                blockquote_border = "#3498db"
                hr_color = "#dddddd"
            
            # Try multiple paths for docs (dev, packaged, Qt resources, web fallback)
            doc_path = None

            # 1. Try Qt resources first (for packaged .qrc bundles)
            resource_path = f":/{relative_path}"
            if QUrl(resource_path).isValid():
                try:
                    from PySide6.QtCore import QFile, QIODevice
                    file = QFile(resource_path)
                    if file.exists() and file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
                        md_content = bytes(file.readAll()).decode('utf-8')
                        file.close()
                        doc_path = "Qt resources"
                except Exception:
                    pass  # Fall through to next method

            # 2. Try relative to project root (development)
            if not doc_path:
                project_root = Path(__file__).resolve().parents[2]
                dev_path = project_root / relative_path
                if dev_path.exists():
                    doc_path = dev_path

            # 3. Try relative to executable (packaged with PyInstaller)
            if not doc_path and hasattr(__import__('sys'), 'frozen'):
                import sys
                if hasattr(sys, '_MEIPASS'):
                    bundle_path = Path(sys._MEIPASS) / relative_path
                    if bundle_path.exists():
                        doc_path = bundle_path

            # 4. Web fallback if all local paths fail
            if not doc_path:
                web_docs = {
                    "docs/HELP.md": "https://docs.signature-extractor.com/help",
                    "docs/SHORTCUTS.md": "https://docs.signature-extractor.com/shortcuts",
                    "docs/TROUBLESHOOTING.md": "https://docs.signature-extractor.com/troubleshooting",
                    "docs/PDF_SETUP.md": "https://docs.signature-extractor.com/pdf-setup",
                }
                web_url = web_docs.get(relative_path)
                if web_url:
                    self.text_browser.setHtml(
                        f"<h2>Documentation Unavailable Locally</h2>"
                        f"<p>Opening documentation online: <a href='{web_url}'>{web_url}</a></p>"
                    )
                    from PySide6.QtGui import QDesktopServices
                    QDesktopServices.openUrl(QUrl(web_url))
                    return
                else:
                    self.text_browser.setHtml(
                        f"<h2>Error</h2>"
                        f"<p>Document not found: {relative_path}</p>"
                        f"<p>Tried: development path, packaged bundle, and online docs.</p>"
                    )
                    return

            # Read markdown content if we found a local file (already read for Qt resources)
            if doc_path != "Qt resources":
                with open(doc_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
            
            # Convert to HTML
            if MARKDOWN_AVAILABLE and markdown is not None:
                html_content = markdown.markdown(
                    md_content,
                    extensions=['fenced_code', 'tables', 'nl2br']
                )
                
                # Add CSS styling with theme-aware colors
                styled_html = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
                            line-height: 1.6;
                            color: {text_color};
                            padding: 20px;
                            max-width: 100%;
                        }}
                        h1 {{
                            color: {heading_color};
                            border-bottom: 2px solid {border_color};
                            padding-bottom: 10px;
                            margin-top: 24px;
                        }}
                        h2 {{
                            color: {heading_color};
                            border-bottom: 1px solid #bdc3c7;
                            padding-bottom: 6px;
                            margin-top: 20px;
                        }}
                        h3 {{
                            color: {heading_color};
                            margin-top: 16px;
                        }}
                        code {{
                            background-color: {code_bg};
                            padding: 2px 6px;
                            border-radius: 3px;
                            font-family: "Courier New", Courier, monospace;
                            font-size: 0.9em;
                            color: #e74c3c;
                        }}
                        pre {{
                            background-color: {pre_bg};
                            border: 1px solid #ddd;
                            border-radius: 4px;
                            padding: 12px;
                            overflow-x: auto;
                        }}
                        pre code {{
                            background-color: transparent;
                            padding: 0;
                            color: {text_color};
                        }}
                        ul, ol {{
                            margin-left: 20px;
                        }}
                        li {{
                            margin: 4px 0;
                        }}
                        blockquote {{
                            border-left: 4px solid {blockquote_border};
                            margin: 16px 0;
                            padding-left: 16px;
                            color: {text_color};
                        }}
                        a {{
                            color: {link_color};
                            text-decoration: none;
                        }}
                        a:hover {{
                            text-decoration: underline;
                        }}
                        table {{
                            border-collapse: collapse;
                            width: 100%;
                            margin: 16px 0;
                        }}
                        th, td {{
                            border: 1px solid #ddd;
                            padding: 8px;
                            text-align: left;
                        }}
                        th {{
                            background-color: {table_header_bg};
                            font-weight: bold;
                        }}
                        strong {{
                            color: {heading_color};
                        }}
                        hr {{
                            border: none;
                            border-top: 1px solid {hr_color};
                            margin: 24px 0;
                        }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """
                
                self.text_browser.setHtml(styled_html)
            else:
                # Fallback: plain text if markdown not available
                self.text_browser.setPlainText(md_content)
                
        except Exception as e:
            self.text_browser.setHtml(f"<h2>Error</h2><p>Failed to load document: {str(e)}</p>")
