from __future__ import annotations

import sys
from typing import Optional

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QColorDialog, QFileDialog


class NativeDialogsMixin:
    """Helpers that wrap Qt dialogs while keeping macOS-native chrome enabled."""

    def _configure_native_dialog(self, dialog: QFileDialog) -> None:
        """Ensure QFileDialog keeps native appearance where available."""
        if sys.platform == "darwin":
            dialog.setOption(QFileDialog.Option.DontUseNativeDialog, False)
            dialog.setOption(QFileDialog.Option.HideNameFilterDetails, True)
            dialog.setLabelText(QFileDialog.DialogLabel.Accept, "Choose")
            dialog.setLabelText(QFileDialog.DialogLabel.LookIn, "Location")
        else:
            dialog.setOption(QFileDialog.Option.DontUseNativeDialog, False)
        dialog.setOption(QFileDialog.Option.DontConfirmOverwrite, False)

    def _native_open_file(
        self,
        title: str,
        name_filter: Optional[str] = None,
        directory: str = "",
    ) -> str:
        dialog = QFileDialog(self, title)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if directory:
            dialog.setDirectory(directory)
        if name_filter:
            dialog.setNameFilter(name_filter)
        self._configure_native_dialog(dialog)
        if dialog.exec():
            files = dialog.selectedFiles()
            return files[0] if files else ""
        return ""

    def _native_open_multiple_files(
        self,
        title: str,
        name_filter: Optional[str] = None,
        directory: str = "",
    ) -> list[str]:
        dialog = QFileDialog(self, title)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        if directory:
            dialog.setDirectory(directory)
        if name_filter:
            dialog.setNameFilter(name_filter)
        self._configure_native_dialog(dialog)
        if dialog.exec():
            return dialog.selectedFiles()
        return []

    def _native_save_file(
        self,
        title: str,
        default_name: str = "",
        name_filter: Optional[str] = None,
        directory: str = "",
    ) -> str:
        dialog = QFileDialog(self, title)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        if directory:
            dialog.setDirectory(directory)
        if default_name:
            dialog.selectFile(default_name)
        if name_filter:
            dialog.setNameFilter(name_filter)
        self._configure_native_dialog(dialog)
        if dialog.exec():
            files = dialog.selectedFiles()
            return files[0] if files else ""
        return ""

    def _native_color_picker(self, initial: str) -> str:
        dialog = QColorDialog(self)
        dialog.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog, False)
        dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, False)
        dialog.setCurrentColor(QColor(initial))
        if dialog.exec():
            chosen = dialog.currentColor()
            return chosen.name()
        return ""


__all__ = ["NativeDialogsMixin"]
