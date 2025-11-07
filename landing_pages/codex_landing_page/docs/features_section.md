# Feature Showcase Section

## Purpose
- Highlight the three differentiating capabilities that make the product indispensable for document-heavy teams.

## Featured Pillars
1. **Precision Canvas**
   - Interactive viewport with zoom, pan, and rotation controls mirroring the desktop app.
   - Copy: "Lock onto signatures with sub-pixel accuracy using adjustable thresholds and guided zoom presets."
2. **Smart Cleanup Pipeline**
   - Describes adaptive background removal, contrast enhancement, and color isolation with toggle to preview before/after.
   - Copy: "Dial in opacity, background color, and smoothing—no Photoshop required."
3. **Instant Export & Audit Trail**
   - Explains PNG export with transparency, PDF drop-in workflow, and JSONL audit log.
   - Copy: "Ship compliant signatures with traceable metadata every time."

## Layout & Visuals
- Horizontal carousel on desktop that snaps between cards; stacked accordions on mobile.
- Each card contains:
  - Animated line illustration (SVG) representing functionality.
  - Short headline, 2-line description, and "Learn more" micro CTA linking to docs.
- Background gradient shifts subtly as user navigates to reinforce focus.

## Interaction Mechanics
- Carousel built with CSS scroll snap + JS to update active indicator.
- Use `prefers-reduced-motion` to disable auto-slide for motion-sensitive users.
- Provide keyboard support for card navigation (arrow keys).

## Supporting Elements
- Badge row under carousel linking to integration partners (Adobe Acrobat, DocuSign, Notarize) as grayscale logos.
- Subtext referencing cross-platform support and REST API availability.

## Copy Tone
- Direct, confident, avoids hype. Focus on measurable outcomes like "Cut review time by minutes per document".

## Data Hooks
- Include data attributes on cards (`data-feature="canvas"`, etc.) for analytics instrumentation once page is live.
