# Pricing Implementation Plan — Signature Extractor (No Trial)

This complements docs/PRICING.md by describing how to implement licensing, payments, and upgrade flows with no free trial.

## Offers (from PRICING.md)
- Lifetime Desktop: $29 one-time (initial); consider testing $39 and $49 later
- Pro (future): $12/month or $99/year
- Team/Enterprise: Deferred

## Payment & Licensing Options
- Paddle or Lemon Squeezy: VAT/compliance, license keys, refunds (recommended to ship fast)
- Stripe + self-rolled licensing: Webhooks + license store; more control, more work

Recommendation: Start with Paddle/Lemon Squeezy for checkout + license issuance. Add Stripe later if needed.

## License Model
- Lifetime: Per-user license key; no expiry
- Pro: Subscription tied to email; license checks on renewal (when launched)
- Offline-friendly: Write license file to user config dir; validate offline, refresh in background when online

## Evaluation Mode (No Trial)
- Pre-purchase behavior: Unlimited preview (selection, threshold/color) but export/save disabled
- Optional: Watermark overlay in preview to signal evaluation mode
- Entry points: “Buy Lifetime ($29)” visible in export dialog and status bar

## Upgrade Flows
- In-app “Buy” dialog: Price, benefits, 30‑day refund note, license key field
- Redemption: Paste license key → stored locally → unlocks export immediately
- Sync: On app start (if online), validate license; continue offline if cached

## Refunds & Transitions
- 30‑day money‑back on Lifetime; provider webhook revokes license
- Pro cancellation (future): Downgrade to Lifetime if present; otherwise lock exports

## Price Localization & Coupons
- Use payment provider geo‑pricing
- Launch coupon (e.g., LAUNCH20) valid for first 14 days

## Data Model (Local)
- `~/.signature_extractor/config.json`
  - `license_key`, `license_type` (lifetime/pro)
  - `license_issued_at`, `last_validation_at`
  - `first_run_at`, `install_id`

## UI Touchpoints
- Export dialog: “Export is locked — Buy Lifetime to unlock (30‑day refund)”
- Status bar: “Evaluation mode — Export locked” with “Buy” button
- About/License dialog: Enter key, manage license, refund link

## Metrics
- Website → purchase rate
- First run → purchase rate
- Refund rate (Lifetime)
- (Future) Churn for Pro

## Roadmap Hooks
- “Manage License” menu entry
- Background validator (weekly) with back‑off and privacy‑respectful logs
- Graceful error states and clear messaging if license invalid
