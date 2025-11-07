# modern_mac_button.py
from PySide6.QtCore import Qt, QEasingCurve, Property, QPropertyAnimation, QRectF
from PySide6.QtGui import (QPainter, QPainterPath, QColor, QPen, QBrush, QFontMetrics,
                            QPalette, QLinearGradient, QRadialGradient)
from PySide6.QtWidgets import (QApplication, QPushButton, QStyleOptionButton, QStyle,
                                QWidget, QVBoxLayout, QGraphicsDropShadowEffect, QGraphicsBlurEffect)

# Vibrant accent colors
VIBRANT_COLORS = {
    'blue': QColor(0, 122, 255),      # macOS blue
    'purple': QColor(175, 82, 222),   # macOS purple
    'pink': QColor(255, 55, 95),      # macOS pink
    'red': QColor(255, 59, 48),       # macOS red
    'orange': QColor(255, 149, 0),    # macOS orange
    'yellow': QColor(255, 204, 0),    # macOS yellow
    'green': QColor(52, 199, 89),     # macOS green
    'teal': QColor(90, 200, 250),     # macOS teal
}

def system_accent_fallback(palette: QPalette) -> QColor:
    return palette.highlight().color()

class ModernMacButton(QPushButton):
    def __init__(self, text="", parent=None, primary=False, color='blue', glass=True):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(44)
        self.setMinimumWidth(100)
        self.setCheckable(False)

        self._hover = 0.0
        self._pressed = 0.0
        self._primary = primary
        self._glass = glass
        self._color = color

        # Accessibility
        self.setAccessibleName(text or "Button")
        self.setAccessibleDescription("macOS style button with glassmorphism")

        # Enhanced shadow for depth and separation from background
        shadow = QGraphicsDropShadowEffect(self)
        if primary:
            shadow.setBlurRadius(30)
            shadow.setOffset(0, 4)
            shadow.setColor(QColor(0, 0, 0, 60))  # Stronger shadow for primary
        else:
            shadow.setBlurRadius(25)
            shadow.setOffset(0, 3)
            shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

        # Animations for hover and pressed
        self._hover_anim = QPropertyAnimation(self, b"hoverProgress", self)
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._press_anim = QPropertyAnimation(self, b"pressedProgress", self)
        self._press_anim.setDuration(100)
        self._press_anim.setEasingCurve(QEasingCurve.OutQuad)

        # Native focus policy so the ring can show
        self.setFocusPolicy(Qt.StrongFocus)

        # Use Qt style for icon+text layout, we only draw the capsule background + focus ring
        self.setStyleSheet("QPushButton { border: none; background: transparent; }")

    # Animated properties
    def getHover(self): return self._hover
    def setHover(self, v): self._hover = v; self.update()
    hoverProgress = Property(float, getHover, setHover)

    def getPressed(self): return self._pressed
    def setPressed(self, v): self._pressed = v; self.update()
    pressedProgress = Property(float, getPressed, setPressed)

    def enterEvent(self, e):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._press_anim.stop()
            self._press_anim.setStartValue(self._pressed)
            self._press_anim.setEndValue(1.0)
            self._press_anim.start()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self._press_anim.stop()
        self._press_anim.setStartValue(self._pressed)
        self._press_anim.setEndValue(0.0)
        self._press_anim.start()
        super().mouseReleaseEvent(e)

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        w = fm.horizontalAdvance(self.text()) + 32
        h = max(40, fm.height() + 16)
        if not self.icon().isNull():
            w += 24
        return super().sizeHint().expandedTo(QApplication.style().sizeFromContents(
            QStyle.CT_PushButton, QStyleOptionButton(),
            self.rect().size(), self))

    def _colors(self):
        pal = self.palette()
        is_dark = pal.color(QPalette.Window).lightnessF() < 0.5

        # Get vibrant accent color
        accent = VIBRANT_COLORS.get(self._color, VIBRANT_COLORS['blue'])
        text_on_accent = QColor("white")

        if self._primary:
            # Vibrant primary button with glassmorphism
            if self._glass:
                # Semi-transparent glass effect with vibrant color
                base_bg = QColor(accent.red(), accent.green(), accent.blue(), 200)
                hover_bg = QColor(accent.red(), accent.green(), accent.blue(), 230)
                # Bright border for glass effect
                border = QColor(255, 255, 255, 80)
                # Lighter inner glow
                inner_glow = QColor(255, 255, 255, 60)
            else:
                # Solid vibrant button
                base_bg = accent
                hover_bg = QColor(
                    min(int(accent.red() * 1.1), 255),
                    min(int(accent.green() * 1.1), 255),
                    min(int(accent.blue() * 1.1), 255)
                )
                border = QColor(accent.red(), accent.green(), accent.blue(), 150)
                inner_glow = None

            return dict(
                bg=base_bg,
                fg=text_on_accent,
                border=border,
                hover_bg=hover_bg,
                press_overlay=QColor(255, 255, 255, 30),
                focus_ring=accent,
                inner_glow=inner_glow,
                is_glass=self._glass
            )
        else:
            # Secondary/default button with glassmorphism
            if self._glass:
                if is_dark:
                    # Dark mode glass
                    bg = QColor(255, 255, 255, 25)  # White glass
                    hover_bg = QColor(255, 255, 255, 40)
                    fg = QColor(255, 255, 255, 240)
                    border = QColor(255, 255, 255, 60)
                    press_overlay = QColor(255, 255, 255, 20)
                    inner_glow = QColor(255, 255, 255, 30)
                else:
                    # Light mode glass
                    bg = QColor(255, 255, 255, 150)
                    hover_bg = QColor(255, 255, 255, 180)
                    fg = QColor(0, 0, 0, 220)
                    border = QColor(255, 255, 255, 100)
                    press_overlay = QColor(0, 0, 0, 15)
                    inner_glow = QColor(255, 255, 255, 50)
            else:
                # Solid secondary button
                if is_dark:
                    bg = QColor(60, 60, 65)
                    hover_bg = QColor(70, 70, 75)
                    fg = QColor(255, 255, 255, 240)
                    border = QColor(80, 80, 85)
                    press_overlay = QColor(255, 255, 255, 15)
                else:
                    bg = QColor(240, 240, 245)
                    hover_bg = QColor(250, 250, 252)
                    fg = QColor(0, 0, 0, 220)
                    border = QColor(220, 220, 230)
                    press_overlay = QColor(0, 0, 0, 10)
                inner_glow = None

            return dict(
                bg=bg, fg=fg, border=border,
                hover_bg=hover_bg,
                press_overlay=press_overlay,
                focus_ring=QColor(0, 122, 255, 120),
                inner_glow=inner_glow,
                is_glass=self._glass
            )

    def paintEvent(self, event):
        opt = QStyleOptionButton()
        self.initStyleOption(opt)

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        rect = self.rect().adjusted(3, 3, -3, -3)  # room for focus ring and shadow
        radius = 10.0

        colors = self._colors()

        # Interpolate background for hover
        def lerp(a: QColor, b: QColor, t: float) -> QColor:
            return QColor(
                int(a.red() + (b.red() - a.red()) * t),
                int(a.green() + (b.green() - a.green()) * t),
                int(a.blue() + (b.blue() - a.blue()) * t),
                int(a.alpha() + (b.alpha() - a.alpha()) * t),
            )
        bg = lerp(colors["bg"], colors["hover_bg"], self._hover)

        # Capsule path
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)

        # Glassmorphism effects
        if colors.get("is_glass", False):
            # Inner shadow/depth for glass effect
            inner_shadow_path = QPainterPath()
            inner_rect = QRectF(rect).adjusted(1, 1, -1, -1)
            inner_shadow_path.addRoundedRect(inner_rect, radius - 1, radius - 1)

            # Gradient background for depth
            gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())

            # Create gradient with transparency for glass
            grad_start = QColor(bg.red(), bg.green(), bg.blue(), int(bg.alpha() * 1.1))
            grad_end = QColor(bg.red(), bg.green(), bg.blue(), int(bg.alpha() * 0.85))
            gradient.setColorAt(0.0, grad_start)
            gradient.setColorAt(1.0, grad_end)

            p.fillPath(path, QBrush(gradient))

            # Inner glow for glass effect
            if colors.get("inner_glow"):
                inner_glow = colors["inner_glow"]
                glow_gradient = QLinearGradient(rect.topLeft(), rect.center())
                glow_gradient.setColorAt(0.0, inner_glow)
                glow_gradient.setColorAt(1.0, QColor(255, 255, 255, 0))

                glow_path = QPainterPath()
                glow_rect = QRectF(rect.x(), rect.y(), rect.width(), rect.height() * 0.5)
                glow_path.addRoundedRect(glow_rect, radius, radius)

                # Clip to button shape
                p.save()
                p.setClipPath(path)
                p.fillPath(glow_path, QBrush(glow_gradient))
                p.restore()
        else:
            # Solid fill with subtle gradient
            gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
            grad_start = QColor(bg.red(), bg.green(), bg.blue(), bg.alpha())
            grad_end = QColor(
                max(0, bg.red() - 5),
                max(0, bg.green() - 5),
                max(0, bg.blue() - 5),
                bg.alpha()
            )
            gradient.setColorAt(0.0, grad_start)
            gradient.setColorAt(1.0, grad_end)
            p.fillPath(path, QBrush(gradient))

        # Border with enhanced visibility
        border_color = colors["border"]
        pen = QPen(border_color)
        pen.setWidthF(1.5)
        p.setPen(pen)
        p.drawPath(path)

        # Press overlay
        if self._pressed > 0.001:
            overlay = colors["press_overlay"]
            overlay.setAlpha(int(overlay.alpha() * self._pressed))
            p.fillPath(path, overlay)

        # Enhanced focus ring with glow
        if self.hasFocus():
            ring_color = colors["focus_ring"]

            # Outer glow
            for i in range(3):
                glow_alpha = 30 - (i * 10)
                glow_color = QColor(ring_color.red(), ring_color.green(), ring_color.blue(), glow_alpha)
                glow_pen = QPen(glow_color)
                glow_pen.setWidth(6 - i)
                p.setPen(glow_pen)
                outer = QRectF(rect).adjusted(-2 - i, -2 - i, 2 + i, 2 + i)
                glow_path = QPainterPath()
                glow_path.addRoundedRect(outer, radius + 2, radius + 2)
                p.drawPath(glow_path)

            # Main focus ring
            ring_pen = QPen(ring_color)
            ring_pen.setWidth(3)
            p.setPen(ring_pen)
            outer = QRectF(rect).adjusted(-3, -3, 3, 3)
            ring_path = QPainterPath()
            ring_path.addRoundedRect(outer, radius + 2, radius + 2)
            p.drawPath(ring_path)

        # Let style draw icon and text correctly aligned
        opt.palette.setColor(QPalette.ButtonText, colors["fg"])
        self.style().drawControl(QStyle.CE_PushButtonLabel, opt, p, self)

        p.end()

# Demo harness
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QHBoxLayout, QLabel, QScrollArea
    from PySide6.QtGui import QFont

    app = QApplication(sys.argv)

    # Main window with gradient background
    win = QWidget()
    win.setMinimumSize(900, 700)

    # Create gradient background
    win.setStyleSheet("""
        QWidget {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea,
                stop:0.5 #764ba2,
                stop:1 #f093fb
            );
        }
    """)

    main_layout = QVBoxLayout(win)
    main_layout.setContentsMargins(40, 40, 40, 40)
    main_layout.setSpacing(30)

    # Title
    title = QLabel("Modern macOS Buttons with Glassmorphism")
    title_font = QFont()
    title_font.setPointSize(24)
    title_font.setBold(True)
    title.setFont(title_font)
    title.setStyleSheet("color: white; background: transparent;")
    main_layout.addWidget(title)

    # Section: Glass Primary Buttons (Vibrant Colors)
    glass_label = QLabel("Glass Primary Buttons")
    glass_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; background: transparent;")
    main_layout.addWidget(glass_label)

    glass_row1 = QHBoxLayout()
    glass_row1.setSpacing(15)
    for color in ['blue', 'purple', 'pink', 'red']:
        btn = ModernMacButton(color.capitalize(), primary=True, color=color, glass=True)
        glass_row1.addWidget(btn)
    main_layout.addLayout(glass_row1)

    glass_row2 = QHBoxLayout()
    glass_row2.setSpacing(15)
    for color in ['orange', 'yellow', 'green', 'teal']:
        btn = ModernMacButton(color.capitalize(), primary=True, color=color, glass=True)
        glass_row2.addWidget(btn)
    main_layout.addLayout(glass_row2)

    # Section: Solid Primary Buttons
    solid_label = QLabel("Solid Primary Buttons")
    solid_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; background: transparent;")
    main_layout.addWidget(solid_label)

    solid_row = QHBoxLayout()
    solid_row.setSpacing(15)
    for color in ['blue', 'purple', 'green', 'red']:
        btn = ModernMacButton(color.capitalize(), primary=True, color=color, glass=False)
        solid_row.addWidget(btn)
    main_layout.addLayout(solid_row)

    # Section: Glass Secondary Buttons
    secondary_label = QLabel("Glass Secondary Buttons")
    secondary_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; background: transparent;")
    main_layout.addWidget(secondary_label)

    secondary_row = QHBoxLayout()
    secondary_row.setSpacing(15)
    btn_glass_secondary = ModernMacButton("Cancel", primary=False, glass=True)
    btn_glass_secondary2 = ModernMacButton("Dismiss", primary=False, glass=True)
    btn_glass_secondary3 = ModernMacButton("Close", primary=False, glass=True)
    secondary_row.addWidget(btn_glass_secondary)
    secondary_row.addWidget(btn_glass_secondary2)
    secondary_row.addWidget(btn_glass_secondary3)
    main_layout.addLayout(secondary_row)

    # Section: Action buttons
    action_label = QLabel("Action Buttons with Icons")
    action_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; background: transparent;")
    main_layout.addWidget(action_label)

    action_row = QHBoxLayout()
    action_row.setSpacing(15)

    # Create buttons with icons
    btn_save = ModernMacButton("Save", primary=True, color='green', glass=True)
    btn_save.setIcon(win.style().standardIcon(QStyle.SP_DialogSaveButton))

    btn_delete = ModernMacButton("Delete", primary=True, color='red', glass=True)
    btn_delete.setIcon(win.style().standardIcon(QStyle.SP_TrashIcon))

    btn_info = ModernMacButton("Info", primary=True, color='blue', glass=True)
    btn_info.setIcon(win.style().standardIcon(QStyle.SP_MessageBoxInformation))

    action_row.addWidget(btn_save)
    action_row.addWidget(btn_delete)
    action_row.addWidget(btn_info)
    main_layout.addLayout(action_row)

    main_layout.addStretch()

    # Instructions
    instructions = QLabel("Hover, click, and use Tab to see focus effects!")
    instructions.setStyleSheet("color: white; font-size: 14px; background: transparent; font-style: italic;")
    main_layout.addWidget(instructions)

    win.setWindowTitle("Modern macOS Glassmorphism Buttons")
    win.show()
    sys.exit(app.exec())
