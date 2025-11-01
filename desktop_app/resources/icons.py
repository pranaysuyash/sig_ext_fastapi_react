"""Icon helper utilities.

Prefers platform-native icons (Qt standard pixmaps) and falls back to emoji/text when
necessary. On macOS we disable emoji prefixes to keep controls looking native.
"""

from __future__ import annotations

import sys
from typing import Optional

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyle, QApplication, QPushButton


class IconManager:
    """
    Provides consistent icons across the application.
    Uses Qt's standard icons which adapt to the system theme.
    """
    
    @staticmethod
    def get_icon(icon_type: str) -> QIcon:
        """
        Get a QIcon for the specified type.
        
        Args:
            icon_type: Icon identifier (e.g., 'open', 'save', 'export', etc.)
        
        Returns:
            QIcon object (may be null if not available)
        """
        style = QApplication.style()
        
        icon_map = {
            # File operations
            'open': QStyle.StandardPixmap.SP_DialogOpenButton,
            'save': QStyle.StandardPixmap.SP_DialogSaveButton,
            'export': QStyle.StandardPixmap.SP_DialogSaveButton,
            'folder': QStyle.StandardPixmap.SP_DirIcon,
            'file': QStyle.StandardPixmap.SP_FileIcon,
            'copy': QStyle.StandardPixmap.SP_DialogApplyButton,
            'mode_select': QStyle.StandardPixmap.SP_ArrowCursor,
            'mode_pan': QStyle.StandardPixmap.SP_ArrowForward,

            # Navigation
            'refresh': QStyle.StandardPixmap.SP_BrowserReload,
            'home': QStyle.StandardPixmap.SP_DirHomeIcon,
            'back': QStyle.StandardPixmap.SP_ArrowBack,
            'forward': QStyle.StandardPixmap.SP_ArrowForward,
            'up': QStyle.StandardPixmap.SP_ArrowUp,
            'down': QStyle.StandardPixmap.SP_ArrowDown,
            'left': QStyle.StandardPixmap.SP_ArrowLeft,
            'right': QStyle.StandardPixmap.SP_ArrowRight,
            
            # Actions
            'close': QStyle.StandardPixmap.SP_DialogCloseButton,
            'delete': QStyle.StandardPixmap.SP_TrashIcon,
            'help': QStyle.StandardPixmap.SP_DialogHelpButton,
            'info': QStyle.StandardPixmap.SP_MessageBoxInformation,
            'warning': QStyle.StandardPixmap.SP_MessageBoxWarning,
            'error': QStyle.StandardPixmap.SP_MessageBoxCritical,
            'ok': QStyle.StandardPixmap.SP_DialogOkButton,
            'cancel': QStyle.StandardPixmap.SP_DialogCancelButton,
            'apply': QStyle.StandardPixmap.SP_DialogApplyButton,
            'reset': QStyle.StandardPixmap.SP_DialogResetButton,
            
            # View controls
            'zoom_in': QStyle.StandardPixmap.SP_ArrowUp,
            'zoom_out': QStyle.StandardPixmap.SP_ArrowDown,
            'fit': QStyle.StandardPixmap.SP_TitleBarMaxButton,
            'rotate_cw': QStyle.StandardPixmap.SP_BrowserReload,
            'rotate_ccw': QStyle.StandardPixmap.SP_BrowserReload,
            
            # Media
            'play': QStyle.StandardPixmap.SP_MediaPlay,
            'pause': QStyle.StandardPixmap.SP_MediaPause,
            'stop': QStyle.StandardPixmap.SP_MediaStop,
        }
        
        standard_pixmap = icon_map.get(icon_type)
        if standard_pixmap:
            return style.standardIcon(standard_pixmap)
        
        # Return null icon if not found
        return QIcon()
    
    @staticmethod
    def get_icon_text(icon_type: str) -> str:
        """
        Get emoji fallback text for icons.
        Used when icons are not available or for additional visual flair.
        
        Args:
            icon_type: Icon identifier
        
        Returns:
            Emoji string
        """
        emoji_map = {
            'open': '📂',
            'save': '💾',
            'export': '💾',
            'folder': '📁',
            'file': '📄',
            'color': '🎨',
            'zoom_in': '🔍+',
            'zoom_out': '🔍−',
            'fit': '⊡',
            'reset': '⊙',
            'select': '🎯',
            'clear': '✖',
            'preview': '👁',
            'delete': '🗑',
            'help': '❓',
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'ok': '✓',
            'rotate_cw': '↻',
            'rotate_ccw': '↺',
        }
        
        return emoji_map.get(icon_type, '')


# Convenience functions
def get_icon(icon_type: str) -> QIcon:
    """Get a QIcon for the specified type."""
    return IconManager.get_icon(icon_type)


def get_icon_text(icon_type: str) -> str:
    """Get emoji fallback text for the specified icon type."""
    return IconManager.get_icon_text(icon_type)


def set_button_icon(button: QPushButton, icon_type: str, text: Optional[str] = None, use_emoji: bool = True):
    """
    Set icon and text for a QPushButton.
    
    Args:
        button: QPushButton to modify
        icon_type: Icon identifier
        text: Button text (if None, only icon/emoji is used)
        use_emoji: If True, prepend emoji to text
    """
    if sys.platform == "darwin":
        use_emoji = False

    # Set QIcon
    icon = get_icon(icon_type)
    icon_available = not icon.isNull()
    if icon_available:
        button.setIcon(icon)
    
    # Set text (with or without emoji)
    if text:
        # Avoid double icons: if we set a real icon, skip emoji prefix
        if use_emoji and not icon_available:
            emoji = get_icon_text(icon_type)
            button.setText(f"{emoji} {text}" if emoji else text)
        else:
            button.setText(text)
    elif use_emoji and not icon_available:
        # No text, just emoji
        emoji = get_icon_text(icon_type)
        if emoji:
            button.setText(emoji)
