# TODO - November 19, 2025

## Landing Page (signkit.work) - URGENT

### 🔴 Critical: Fix 308 Redirect Loop
**Status**: All clean URLs (/buy, /root, /gum, /purchase) return HTTP 308 redirect to themselves
**Problem**: Cloudflare Pages is not properly handling the `_redirects` file
**Last Known State**: 
- ✅ `_redirects` file created and deployed (maps /buy → /buy.html, etc.)
- ✅ User purged Cloudflare cache
- ✅ User removed Page Rules
- ❌ 308 redirects still persist on all URLs except root

**Potential Causes**:
1. `.pages-include` file lists non-existent HTML files (root.html, buy.html, gum.html)
   - These files don't exist - routing is JS-based in index.html
   - Cloudflare might be expecting these files, causing 308s
2. Cloudflare Pages build settings may need adjustment:
   - Build output directory: Should be root (`.`)
   - Build command: Should be empty/none
3. `_redirects` file may not be in the correct format for Cloudflare

**Next Steps**:
1. Check/fix `.pages-include` - remove non-existent HTML file references
2. Verify Cloudflare Pages build settings (Build output dir = root, no build command)
3. Possibly simplify `_redirects` to test if basic routing works
4. Consider alternative: Use Cloudflare Workers for routing instead of `_redirects`
5. Test with a simple redirect first (e.g., /test → /index.html)

**Files to Check**:
- `_redirects` (just deployed)
- `.pages-include` (has problematic entries)
- `wrangler.toml` (pages_build_output_dir = ".")
- Cloudflare Pages dashboard settings

---

## Landing Page - A/B Testing

### ✅ Completed on Nov 18
- Auto A/B split functionality working
- Claude variant updated with "Own Forever" messaging (no fake discounts)
- ChatGPT variant updated with iframe positioning
- Analytics tracking in place
- All variants accessible via query params: `?variant=chatgpt` or `?variant=claude`

### Monitoring Required
- Track conversion rates on both variants
- Monitor which variant performs better
- Ready to adjust based on data

---

## Desktop App - No Active Issues

### Current State
- ✅ All builds complete (macOS ARM64, Intel, Linux, Windows)
- ✅ DMG files generated and ready
- ✅ Backend working with SQLite/PostgreSQL
- ✅ PDF features complete
- ✅ License validation working
- ✅ UI polish complete

### On Hold
- Product launch delayed until landing page is fully functional
- Marketing materials ready but waiting for stable landing page

---

## Priority Order for Nov 19

1. **MUST FIX**: Landing page 308 redirects (blocking all purchases)
2. Test purchase flow end-to-end once redirects are fixed
3. Monitor A/B test performance
4. If landing page is stable, begin soft launch preparation

---

## Notes from Nov 18

### What Worked
- `.gitignore` updated on landing-page branch to prevent accidental commits of desktop app files
- Landing page branch now protected from pollution
- All A/B test variants deployed and functional (except routing)

### What Didn't Work
- Multiple attempts to fix Cloudflare redirects failed
- `_redirects` file exists but not being processed by Cloudflare
- Cache purging and Page Rule removal had no effect

### Lessons Learned
- Cloudflare Pages routing is more complex than expected
- Need to verify build output structure matches Cloudflare expectations
- `.pages-include` file can cause confusion if it lists non-existent files
