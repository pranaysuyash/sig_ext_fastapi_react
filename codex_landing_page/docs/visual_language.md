# Visual Language & Motion System

## Palette
- **Primary Gradient:** #1A1744 → #4C3FE1 → #8A5CF6 (evokes precision & trust).
- **Accent Gradient:** #0D8B89 → #3EF5C3 (used sparingly for CTAs).
- **Support Neutrals:** Off-black #0A0D16, steel #1E2433, soft slate #353C4F, light slate #E7EAF6.
- **Status Colors:** Success #5BE7A9, Warning #FFC972, Critical #FF6B6B.

## Typography
- Headings: "Sora" or "Poppins" (geometric sans) with tight letter spacing.
- Body: "Inter" for clarity and modernity.
- Monospace accent for technical details: "JetBrains Mono".
- Maintain modular scale (1.2) to ensure consistency.

## Iconography & Illustration
- Thin-stroke icons with rounded ends to imply crafted precision.
- Abstract vector patterns (blobs, waveforms) representing data flow; keep opacity below 0.2 behind text.
- Use SVG filters for glow/blur to create depth without heavy images.

## Motion Principles
- Ease: `cubic-bezier(0.22, 0.61, 0.36, 1)` for organic feel.
- Duration: 280–420ms for most interactions; hero signature animation 1.4s.
- Stagger entrance animations by 90ms increments for natural rhythm.
- Provide `prefers-reduced-motion` fallbacks; replace animations with static states.

## Layout System
- 12-column CSS grid at 1200px breakpoint; collapses to 6 columns at 768px and 4 columns at 560px.
- Spacing scale: 8px base unit (8, 16, 24, 32, 48, 64).
- Use glassmorphism panels (background rgba(13, 17, 34, 0.65), border 1px rgba(255, 255, 255, 0.2)).

## Imagery Guidelines
- When using product screenshots, apply subtle skew and drop shadow to maintain depth.
- Avoid stock photography; if needed, use abstract gradients or line art representing documents.

## Accessibility
- Minimum text size 16px, hero headline 56px on desktop.
- Ensure interactive targets at least 44px height.
- Test color combinations against WCAG AA.
