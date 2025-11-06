# FAQ & Support Section

## Purpose
- Resolve common adoption blockers without requiring visitors to leave the page.

## Content Plan
- 6 accordion items covering:
  1. Deployment footprint & offline usage.
  2. Supported document formats and maximum file sizes.
  3. Security posture (local processing, optional cloud sync, encryption at rest).
  4. Team collaboration workflow and user provisioning.
  5. Licensing tiers (Free, Pro, Team, Enterprise) and what unlocks remote processing.
  6. Support SLAs and dedicated onboarding assistance.
- Optional final item: "Still have questions?" with inline form that expands.

## Layout
- Two-column accordion on desktop (3 items each), stacked on mobile.
- Keep accordions flush with subtle border to maintain visual calm between higher-energy sections.

## Interaction & Accessibility
- Accordion built with semantic `<button>` controls and `aria-expanded` toggles.
- Smooth height animation using CSS `grid-template-rows` or `max-height` with transitions, respecting reduced-motion preferences.
- Inline form uses single input and CTA button; provide validation and success message.

## Copy Tone
- Clear, direct, reduces friction. E.g., "Yes—everything runs locally by default. You decide what syncs.".
- Include links to documentation (`docs/HELP.md`, pricing) where relevant.

## Support Hooks
- Provide email alias (`support@signatureextractor.app`) and Slack community invite link placeholder.
- Add note about optional white-glove onboarding for Enterprise tier.
