"""Help dialog with rendered Markdown content."""

from pathlib import Path
from types import ModuleType
from typing import Optional, TYPE_CHECKING

from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont

if TYPE_CHECKING:  # pragma: no cover - type checking only
    import markdown as _markdown_module

try:
    import markdown as _markdown_runtime
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
        
        close_button = QPushButton("Close")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _load_markdown(self, relative_path: str):
        """Load and render markdown file."""
        try:
            # Find project root (2 levels up from this file)
            project_root = Path(__file__).resolve().parents[2]
            doc_path = project_root / relative_path
            
            if not doc_path.exists():
                self.text_browser.setHtml(f"<h2>Error</h2><p>Document not found: {doc_path}</p>")
                return
            
            # Read markdown content
            with open(doc_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Convert to HTML
            if MARKDOWN_AVAILABLE and markdown is not None:
                html_content = markdown.markdown(
                    md_content,
                    extensions=['fenced_code', 'tables', 'nl2br']
                )
                
                # Add CSS styling
                styled_html = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            padding: 20px;
                            max-width: 100%;
                        }}
                        h1 {{
                            color: #2c3e50;
                            border-bottom: 2px solid #3498db;
                            padding-bottom: 10px;
                            margin-top: 24px;
                        }}
                        h2 {{
                            color: #34495e;
                            border-bottom: 1px solid #bdc3c7;
                            padding-bottom: 6px;
                            margin-top: 20px;
                        }}
                        h3 {{
                            color: #34495e;
                            margin-top: 16px;
                        }}
                        code {{
                            background-color: #f4f4f4;
                            padding: 2px 6px;
                            border-radius: 3px;
                            font-family: "Courier New", Courier, monospace;
                            font-size: 0.9em;
                            color: #e74c3c;
                        }}
                        pre {{
                            background-color: #f8f8f8;
                            border: 1px solid #ddd;
                            border-radius: 4px;
                            padding: 12px;
                            overflow-x: auto;
                        }}
                        pre code {{
                            background-color: transparent;
                            padding: 0;
                            color: #333;
                        }}
                        ul, ol {{
                            margin-left: 20px;
                        }}
                        li {{
                            margin: 4px 0;
                        }}
                        blockquote {{
                            border-left: 4px solid #3498db;
                            margin: 16px 0;
                            padding-left: 16px;
                            color: #555;
                        }}
                        a {{
                            color: #3498db;
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
                            background-color: #f2f2f2;
                            font-weight: bold;
                        }}
                        strong {{
                            color: #2c3e50;
                        }}
                        hr {{
                            border: none;
                            border-top: 1px solid #ddd;
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
