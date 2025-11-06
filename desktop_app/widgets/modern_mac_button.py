# modern_mac_button.py
from PySide6.QtCore import Qt, QEasingCurve, Property, QPropertyAnimation, QRectF, QSize
from PySide6.QtGui import (QPainter, QPainterPath, QColor, QPen, QBrush, QFontMetrics,
                            QPalette, QLinearGradient, QRadialGradient)
from PySide6.QtWidgets import (QPushButton, QStyleOptionButton, QStyle,
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
    def __init__(self, text="", parent=None, primary=False, color='blue', glass=True, compact=False):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)

        # Compact mode for sidebars/toolbars, standard for dialogs
        if compact:
            self.setMinimumHeight(32)
            self.setMinimumWidth(60)
        else:
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
        # Don't set stylesheet here - let parent handle exclusion
        self.setObjectName("ModernMacButton")

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
        """Calculate optimal size based on content and compact mode."""
        fm = QFontMetrics(self.font())
        text_width = fm.horizontalAdvance(self.text())

        # Different padding for compact vs standard mode
        if self.minimumHeight() <= 32:  # compact mode
            padding = 20  # 10px on each side
            icon_space = 20 if not self.icon().isNull() else 0
            w = text_width + padding + icon_space
            h = 32
        else:  # standard mode
            padding = 32  # 16px on each side
            icon_space = 24 if not self.icon().isNull() else 0
            w = text_width + padding + icon_space
            h = max(44, fm.height() + 16)

        return QSize(max(w, self.minimumWidth()), h)

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
                    # Dark mode glass - increased opacity for better visibility
                    bg = QColor(255, 255, 255, 45)  # Increased from 25
                    hover_bg = QColor(255, 255, 255, 70)  # Increased from 40
                    fg = QColor(255, 255, 255, 240)
                    border = QColor(255, 255, 255, 80)  # Increased from 60
                    press_overlay = QColor(255, 255, 255, 25)  # Increased from 20
                    inner_glow = QColor(255, 255, 255, 40)  # Increased from 30
                else:
                    # Light mode glass - increased opacity for better visibility
                    bg = QColor(255, 255, 255, 180)  # Increased from 150
                    hover_bg = QColor(255, 255, 255, 210)  # Increased from 180
                    fg = QColor(0, 0, 0, 220)
                    border = QColor(255, 255, 255, 120)  # Increased from 100
                    press_overlay = QColor(0, 0, 0, 20)  # Increased from 15
                    inner_glow = QColor(255, 255, 255, 60)  # Increased from 50
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