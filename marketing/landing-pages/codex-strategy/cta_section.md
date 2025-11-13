# Primary Call-to-Action Section

## Purpose
- Convert visitors into trial users or demo bookings after they have absorbed proof points.

## Layout
- Full-width section with contrasting background (emerald to teal gradient) to stand out from surrounding blocks.
- Centered glass panel containing CTA copy and two action buttons.
- Accent motion: pulsing outline around the primary CTA every 12 seconds to catch attention without being distracting.

## Copy Strategy
- Headline: "Spin up the desktop app in under 2 minutes."
- Supporting line: "Download the macOS or Windows build, or schedule a guided onboarding with our team."
- Buttons:
  - Primary: "Download for macOS" (solid) with OS icon.
  - Secondary: "Book a 15-min walkthrough" (outlined) leading to calendar.
- Tertiary link below: "Prefer Windows or Linux? Explore installers →".

## Interaction Notes
- Add toggle chips to switch platform preference; update CTA label based on selection via JS.
- Include fallback to email link if scheduling widget fails (progressive enhancement).
- Provide `aria-live` region confirming download support when users switch platforms.

## Trust Reinforcement
- Include compact list (inline icons) for "No credit card", "Offline ready", "SOC2 under review".

## Accessibility & Localization
- Buttons sized for touch targets (min 44px height).
- Ensure gradient passes contrast tests.
- Plan for localization by avoiding embedded line breaks inside copy strings.
