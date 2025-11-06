# Visual Design & Animations Guide
**Date:** November 4, 2025
**Version:** 1.0

## Table of Contents
1. [Visual Design System](#visual-design-system)
2. [Animation Library](#animation-library)
3. [Interactive Elements](#interactive-elements)
4. [Asset Specifications](#asset-specifications)
5. [Implementation Guide](#implementation-guide)

---

## Visual Design System

### Background Patterns & Textures

**1. Mesh Gradient Background**
```
Usage: Hero section, Final CTA
Style: Soft, animated gradient mesh
Colors: Navy → Blue → Purple
Animation: Slow rotation (60s loop)
```

**2. Geometric Pattern**
```
Usage: Section separators
Style: Subtle dot grid or line pattern
Opacity: 5-10%
Color: Based on section theme
```

**3. Blob Shapes**
```
Usage: Background decorative elements
Style: Organic, animated blobs
Animation: Morph and float
Color: Semi-transparent brand colors
```

### Icon System

**Style Guidelines:**
- Stroke-based (2px stroke weight)
- Rounded line caps
- 24x24px base size
- Scalable to 32px, 48px, 64px
- Consistent visual weight

**Primary Icons:**
```
🎯 Precision: Crosshair target
🔒 Privacy: Lock with shield
📄 PDF: Document with folded corner
✨ Clean: Sparkle/magic wand
⚡ Fast: Lightning bolt
💾 Save: Floppy disk (modern style)
🔍 Zoom: Magnifying glass
🎨 Adjust: Sliders
📤 Export: Arrow out of box
✅ Success: Checkmark in circle
```

### Image Treatment

**Product Screenshots:**
- Subtle shadow: `0 20px 40px rgba(0,0,0,0.1)`
- Rounded corners: 16px
- Optional: Floating effect with shadow
- Border: 1px solid light gray

**Before/After Images:**
- Side-by-side or slider comparison
- Clear labels
- Same dimensions for fair comparison
- Annotations to highlight differences

**Demo GIFs/Videos:**
- Max 30 seconds loop
- Smooth 60fps
- Compressed for web (< 5MB)
- Fallback to poster image

---

## Animation Library

### Entrance Animations

**1. Fade Up**
```css
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-up {
  animation: fadeUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
```

**Usage:** Text content, cards, sections
**Duration:** 600ms
**Easing:** ease-out

**2. Slide In (Left/Right)**
```css
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
```

**Usage:** Alternating content sections
**Duration:** 700ms
**Easing:** ease-out

**3. Scale In**
```css
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

**Usage:** Cards, modals, important elements
**Duration:** 500ms
**Easing:** spring

**4. Stagger Children**
```css
/* Apply delays to child elements */
.stagger-children > *:nth-child(1) { animation-delay: 0ms; }
.stagger-children > *:nth-child(2) { animation-delay: 100ms; }
.stagger-children > *:nth-child(3) { animation-delay: 200ms; }
.stagger-children > *:nth-child(4) { animation-delay: 300ms; }
```

**Usage:** Lists, grids, feature cards
**Delay Increment:** 100ms

### Hover Animations

**1. Button Lift**
```css
.btn {
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}

.btn:active {
  transform: translateY(0);
  box-shadow: 0 5px 10px rgba(0,0,0,0.1);
}
```

**2. Card Hover**
```css
.card {
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}
```

**3. Icon Bounce**
```css
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.icon:hover {
  animation: bounce 0.5s ease;
}
```

**4. Glow Effect**
```css
.glow {
  transition: box-shadow 0.3s;
}

.glow:hover {
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
}
```

### Scroll Animations

**1. Parallax Layers**
```javascript
// Hero background elements move at different speeds
const parallax = () => {
  const scrolled = window.pageYOffset;

  document.querySelector('.layer-1').style.transform =
    `translateY(${scrolled * 0.5}px)`;

  document.querySelector('.layer-2').style.transform =
    `translateY(${scrolled * 0.3}px)`;

  document.querySelector('.layer-3').style.transform =
    `translateY(${scrolled * 0.1}px)`;
};
```

**2. Scroll-Triggered Fade In**
```javascript
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
    }
  });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach(el => {
  observer.observe(el);
});
```

**3. Progress Indicator**
```javascript
const updateProgressBar = () => {
  const windowHeight = window.innerHeight;
  const documentHeight = document.documentElement.scrollHeight;
  const scrollTop = window.pageYOffset;

  const progress = (scrollTop / (documentHeight - windowHeight)) * 100;

  document.querySelector('.progress-bar').style.width = `${progress}%`;
};
```

### Loading Animations

**1. Skeleton Screen**
```css
.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

**2. Spinner**
```css
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

**3. Pulse**
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}
```

### Micro-Interactions

**1. Ripple Effect**
```javascript
const createRipple = (event) => {
  const button = event.currentTarget;
  const circle = document.createElement('span');
  const diameter = Math.max(button.clientWidth, button.clientHeight);
  const radius = diameter / 2;

  circle.style.width = circle.style.height = `${diameter}px`;
  circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
  circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
  circle.classList.add('ripple');

  button.appendChild(circle);

  setTimeout(() => circle.remove(), 600);
};
```

```css
.ripple {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  transform: scale(0);
  animation: ripple-animation 0.6s ease-out;
}

@keyframes ripple-animation {
  to {
    transform: scale(4);
    opacity: 0;
  }
}
```

**2. Toast Notification**
```css
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOutRight {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}

.toast {
  animation: slideInRight 0.3s ease-out;
}

.toast.removing {
  animation: slideOutRight 0.3s ease-in;
}
```

**3. Toggle Switch**
```css
.toggle {
  transition: background-color 0.3s;
}

.toggle-slider {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.toggle:checked + .toggle-slider {
  transform: translateX(20px);
}
```

---

## Interactive Elements

### 1. Before/After Slider

**Functionality:**
- Drag slider to reveal before/after
- Touch-enabled for mobile
- Smooth dragging with momentum
- Labels for each side

**Implementation:**
```javascript
class BeforeAfterSlider {
  constructor(container) {
    this.container = container;
    this.slider = container.querySelector('.slider');
    this.isDragging = false;

    this.init();
  }

  init() {
    this.slider.addEventListener('mousedown', this.startDrag.bind(this));
    document.addEventListener('mousemove', this.drag.bind(this));
    document.addEventListener('mouseup', this.stopDrag.bind(this));

    // Touch events
    this.slider.addEventListener('touchstart', this.startDrag.bind(this));
    document.addEventListener('touchmove', this.drag.bind(this));
    document.addEventListener('touchend', this.stopDrag.bind(this));
  }

  startDrag(e) {
    this.isDragging = true;
    this.container.classList.add('dragging');
  }

  drag(e) {
    if (!this.isDragging) return;

    const x = e.clientX || e.touches[0].clientX;
    const rect = this.container.getBoundingClientRect();
    const position = ((x - rect.left) / rect.width) * 100;

    this.updatePosition(Math.max(0, Math.min(100, position)));
  }

  stopDrag() {
    this.isDragging = false;
    this.container.classList.remove('dragging');
  }

  updatePosition(percent) {
    this.slider.style.left = `${percent}%`;
    this.container.querySelector('.after-image').style.clipPath =
      `inset(0 ${100 - percent}% 0 0)`;
  }
}
```

### 2. Tabbed Interface

**Features:**
- Smooth content transitions
- Keyboard navigation (arrow keys)
- Active state indicators
- Lazy load tab content

**Animation:**
```css
.tab-content {
  opacity: 0;
  transform: translateX(20px);
  transition: opacity 0.3s, transform 0.3s;
}

.tab-content.active {
  opacity: 1;
  transform: translateX(0);
}
```

### 3. Accordion FAQ

**Features:**
- Smooth expand/collapse
- Only one open at a time (optional)
- Search functionality
- Keyboard accessible

**Animation:**
```css
.accordion-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
}

.accordion-item.open .accordion-content {
  max-height: 500px; /* Adjust based on content */
}
```

### 4. Modal/Popup

**Features:**
- Backdrop blur
- Scale-in animation
- Escape key to close
- Focus trap for accessibility

**Animation:**
```css
.modal-backdrop {
  opacity: 0;
  transition: opacity 0.3s;
}

.modal-backdrop.open {
  opacity: 1;
}

.modal {
  transform: scale(0.9);
  opacity: 0;
  transition: transform 0.3s, opacity 0.3s;
}

.modal.open {
  transform: scale(1);
  opacity: 1;
}
```

### 5. Carousel

**Features:**
- Swipe navigation (mobile)
- Auto-play (optional)
- Progress indicators
- Infinite loop

**Animation:**
```css
.carousel-track {
  display: flex;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.carousel-item {
  flex: 0 0 100%;
}
```

---

## Asset Specifications

### Hero Animation Specifications

**Format:** MP4 video or animated GIF
**Dimensions:** 1200x800px
**Duration:** 20-30 seconds (looping)
**File Size:** < 5MB (compressed)

**Content:**
1. **Scene 1 (0-5s):** Document upload
   - Show drag-and-drop or file select
   - Document appears in viewer

2. **Scene 2 (5-10s):** Selection
   - Show selection rectangle
   - Zoom in for precision
   - Adjust selection boundaries

3. **Scene 3 (10-15s):** Processing
   - Show settings panel
   - Threshold adjustment
   - Real-time preview updates

4. **Scene 4 (15-20s):** Export
   - Show clean extracted signature
   - Compare before/after
   - Export button click

**Style:**
- Clean, minimal UI
- Smooth 60fps animation
- Clear visual feedback
- Professional color scheme

### Screenshot Specifications

**Format:** PNG (for transparency)
**Dimensions:** 1920x1080px (2x for retina)
**Compression:** Optimized with pngquant
**File Size:** < 500KB per image

**Required Screenshots:**
1. Main interface (full window)
2. Selection tool (zoomed view)
3. Settings panel (close-up)
4. PDF viewer (showing signature placement)
5. Library view (multiple signatures)
6. Export dialog

**Treatment:**
- Add subtle drop shadow
- Optional: MacBook Pro frame around screenshots
- Ensure UI is clean (no dummy/test data)
- Use professional example documents

### Icon Asset Specifications

**Format:** SVG (vector)
**Dimensions:** 24x24px base
**Stroke:** 2px
**Style:** Outlined, rounded caps
**Color:** Monochrome (colorized via CSS)

**Required Icons:**
- Upload
- Select
- Zoom in/out
- Threshold
- Color picker
- Export
- PDF
- Signature
- Check
- Close
- Menu
- Search
- Help
- Settings

### Logo Specifications

**Format:** SVG (vector)
**Variations:**
- Full logo (icon + text)
- Icon only
- Text only

**Colors:**
- Full color (primary)
- White (on dark backgrounds)
- Black (on light backgrounds)
- Single color (any)

**Sizes:**
- 32x32px (favicon)
- 64x64px (small)
- 128x128px (medium)
- 256x256px (large)
- 512x512px (app icon)

---

## Implementation Guide

### Performance Optimization

**1. Lazy Loading**
```javascript
// Lazy load images below the fold
const lazyImages = document.querySelectorAll('img[data-src]');
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
      imageObserver.unobserve(img);
    }
  });
});

lazyImages.forEach(img => imageObserver.observe(img));
```

**2. Reduce Motion**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**3. GPU Acceleration**
```css
/* Use transform and opacity for smooth animations */
.animated-element {
  will-change: transform, opacity;
  transform: translateZ(0); /* Force GPU rendering */
}
```

### Animation Performance Tips

1. **Use CSS transforms** (not top/left)
   - ✅ `transform: translateY(10px)`
   - ❌ `top: 10px`

2. **Animate opacity**, not display
   - ✅ `opacity: 0` + `visibility: hidden`
   - ❌ `display: none`

3. **Use will-change** sparingly
   - Apply only to animating elements
   - Remove after animation completes

4. **Debounce scroll events**
   ```javascript
   let ticking = false;

   window.addEventListener('scroll', () => {
     if (!ticking) {
       window.requestAnimationFrame(() => {
         doScrollStuff();
         ticking = false;
       });
       ticking = true;
     }
   });
   ```

### Browser Compatibility

**Target Support:**
- Chrome/Edge: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Mobile Safari: iOS 13+
- Mobile Chrome: Android 8+

**Fallbacks:**
```css
/* Provide fallbacks for modern CSS */
.gradient {
  background: #3b82f6; /* Fallback */
  background: linear-gradient(45deg, #3b82f6, #8b5cf6);
}

/* Feature detection */
@supports (backdrop-filter: blur(10px)) {
  .glass {
    backdrop-filter: blur(10px);
  }
}

@supports not (backdrop-filter: blur(10px)) {
  .glass {
    background: rgba(255, 255, 255, 0.95);
  }
}
```

---

## Animation Timing Reference

### Duration Guidelines
- **Micro-interactions**: 100-200ms
- **Small elements**: 200-300ms
- **Medium elements**: 300-500ms
- **Large elements**: 500-700ms
- **Page transitions**: 700-1000ms

### Easing Functions
```css
/* Use appropriate easing for context */
--ease-in-quad: cubic-bezier(0.55, 0.085, 0.68, 0.53);
--ease-in-cubic: cubic-bezier(0.55, 0.055, 0.675, 0.19);
--ease-out-quad: cubic-bezier(0.25, 0.46, 0.45, 0.94);
--ease-out-cubic: cubic-bezier(0.215, 0.61, 0.355, 1);
--ease-in-out-quad: cubic-bezier(0.455, 0.03, 0.515, 0.955);
--ease-in-out-cubic: cubic-bezier(0.645, 0.045, 0.355, 1);
```

**When to use:**
- **Ease-out**: Elements entering screen
- **Ease-in**: Elements leaving screen
- **Ease-in-out**: Elements moving on screen
- **Spring**: Playful interactions, bounces

---

## Summary

This visual and animation guide provides:

1. **Consistent visual language** across all components
2. **Performance-optimized** animation techniques
3. **Accessible** animations with reduced-motion support
4. **Reusable** animation classes and functions
5. **Detailed asset specifications** for designers

The result is a polished, professional landing page that feels fast, smooth, and engaging while maintaining optimal performance across all devices.
