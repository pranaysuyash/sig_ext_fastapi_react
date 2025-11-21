# Warm Variant Style Notes

## Theme Goals
- Deliver a welcoming, analog-inspired feel using espresso bases and sunset-inspired accents.
- Avoid purple entirely while still differentiating key interactions with high-contrast colors.
- Maintain the original layout structure for parity across variants.

## Palette Reference
- **Backgrounds:** #1c1a16 (page), #201d17 (hero), #2f2a22 (panels), #2b241c (CTA panel).
- **Primary CTA:** #f05a28 with hover state #d94c1f.
- **Supporting Accents:** #f8a531 (metrics, icons), #3fb28c (trust + links), #a44f2b (secondary wave layer).
- **Typography:** Headings #fff3d6, body copy #f6efe4, muted text #c5bba9.

## Component Treatments
- **Hero:** `hero-waves.svg` adds layered organic shapes in orange/amber with a cream glow; particles shift to amber for cohesion.
- **Signature Canvas:** Uses `linearGradient` with orange → amber → sage; fallback is amber solid.
- **Cards & Timeline:** Warm panels with inset amber or sage borders replace the cool glassmorphism from the original.
- **CTA:** Solid espresso panel with orange primary button and outlined secondary link.

## Motion & Accessibility
- Reuses shared JS interactions (counters, carousel, FAQ, CTA pulse, particles) with updated color tokens.
- `prefers-reduced-motion` handling remains intact.
- Contrast checked against WCAG AA for text on espresso backgrounds.
