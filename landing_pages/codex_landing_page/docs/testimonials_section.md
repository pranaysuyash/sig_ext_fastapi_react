# Social Proof & Testimonials Section

## Purpose
- Build credibility with quotes from industry-specific roles who rely on trustworthy signature extraction.

## Content Structure
1. **Headline:** "Trusted by teams who can’t compromise on signature integrity"
2. **Testimonials Grid:**
   - Three cards featuring:
     - Legal Operations Director (Amicus Law Group) citing 70% reduction in contract prep time.
     - Compliance Manager (Northline Bank) highlighting on-prem audit logs.
     - Senior Product Designer (FluxSign SaaS) praising export fidelity.
3. **Logos Row:** Carousel of grayscale client logos; shifts to color on hover.
4. **Security Badges:** Inline icons for "SOC2-ready", "HIPAA-friendly", "GDPR compliant" with tooltip definitions.

## Visual Treatment
- Masonry layout with staggered card heights for energy.
- Each testimonial card has glassmorphism effect, soft inner shadow, and accent gradient border.
- Add signature-like underline accent under customer names for thematic alignment.

## Interaction & Motion
- Cards fade in & rise slightly on scroll.
- Hover reveals extended quote via smooth height transition while keeping layout stable.
- Security badge tooltips appear on focus/hover with accessible `role="tooltip"` semantics.

## Copy Guidelines
- Include measurable outcomes ("cut redlines from 3 days to 12 hours").
- Attribute quotes with name, title, and company; include optional link to case study.
- Keep tone authentic; avoid buzzwords.

## Accessibility Considerations
- Provide alt text for logos, e.g., `alt="Amicus Law Group logo"`.
- Ensure tooltip content is keyboard accessible and dismissible.
- Provide high-contrast text on translucent surfaces (use subtle dark overlay behind text).
