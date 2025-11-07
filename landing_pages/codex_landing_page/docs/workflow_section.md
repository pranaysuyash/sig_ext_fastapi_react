# Workflow Timeline Section

## Purpose
- Demonstrate the end-to-end signature extraction and signing journey in four digestible steps.
- Reinforce that the app handles both extraction and downstream PDF signing.

## Step Breakdown
1. **Import & Detect**
   - Upload scans, mobile photos, or PDFs; auto-orients via EXIF metadata.
   - Visual: Docked panel screenshot with glowing drag-and-drop zone.
2. **Refine & Isolate**
   - Adjust threshold, contrast, and feathering while zooming/panning.
   - Visual: Animated slider showing before/after cleaning.
3. **Export & Share**
   - Save as transparent PNG, layered PSD, or send to PDF workspace.
   - Visual: Export modal mock with toggle chips.
4. **Sign & Audit**
   - Insert signatures into PDF with placement handles and generate audit log.
   - Visual: PDF canvas with timeline of changes.

## Layout Strategy
- Desktop: Horizontal timeline with numbered nodes connected by pulse animation.
- Mobile: Collapsible accordion with persistent progress indicator at top.
- Include ghosted background image of the desktop UI at low opacity.

## Interaction Details
- Each node triggers detail flyout on hover/focus with microcopy and relevant CTA.
- Use IntersectionObserver to animate nodes (scale + glow) when they enter viewport.

## Copy Style
- Start each step with strong verb: "Import", "Refine", "Export", "Sign".
- Keep descriptions under 18 words for scanning.
- Mention privacy and compliance touchpoints in Step 4.

## Callouts
- Add "Works offline" badge between steps 1 and 2.
- Include subtle note: "Batch processing coming Q1 2026" to show roadmap momentum.
