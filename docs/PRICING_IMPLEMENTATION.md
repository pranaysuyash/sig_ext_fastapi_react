# Pricing Implementation Plan — Signature Extractor

This complements docs/PRICING.md by describing how to implement trial, licensing, payments, and upgrades.

## Offers (from PRICING.md)
- Free Trial: 7 days + 10 extractions
- Lifetime Desktop: $49 one-time
- Pro: $12/month or $99/year
- Team/Enterprise: Deferred

## Payment & Licensing Options
- Paddle or Lemon Squeezy: Handles VAT, invoicing, license keys, and trials (recommended for indie desktop)
- Stripe + self-rolled licensing: Requires more infra (webhooks, license store)

Recommendation: Start with Paddle/Lemon Squeezy to ship faster, then revisit if needs change.

## License Model
- Lifetime: Per-user license key, no time limits
- Pro: Subscription license tied to email; license checks on renewal
- Offline-friendly: License file cached locally; periodic background validation when online

## Trial Enforcement
- Local counters: Start date + extraction count stored in user config dir
- Messaging: Status bar and dialogs (“3 days, 5 extractions remaining”)
- Expiry behavior: View-only mode (no exports) after limit
- Optional server-side check: When online, verify eligibility to reduce abuse

## Upgrade Flows
- In-app “Upgrade” entry points: status bar banner, export dialog notice, About menu
- Redemption: Paste license key → stored locally; unlocks features immediately
- License sync: On each app start (if online), refresh entitlements

## Refunds & Transitions
- Refund within 14 days for Lifetime; revoke license via provider webhook
- Pro cancellation: End of billing period; app downgrades to Lifetime or Trial as applicable

## Price Localization & Coupons
- Use provider geo-pricing; create regional price lists
- Coupon codes for launch/partners; limited-time discounts

## Data Model (Local)
- `~/.signature_extractor/config.json`
  - `trial_started_at`, `trial_extractions_used`
  - `license_key`, `license_type` (lifetime/pro)
  - `last_validation_at`

## UI Touchpoints
- Trial banners: Status bar + About dialog
- Upgrade modal: Clear benefits, price, “Enter License Key” field
- Post-purchase: Success toast + “Thanks for supporting!”

## Metrics
- Trial start → conversion rate
- Time to first value (TTFV): First successful export latency
- Churn (Pro): Cancellation reasons (survey link)

## Roadmap Hooks
- Add “Manage License” menu
- Background worker to validate license weekly (when online)
- Grace periods and friendly error states

