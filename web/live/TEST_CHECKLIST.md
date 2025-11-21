# 🚀 Landing Page V2 - Test Checklist

## Quick Test (2 minutes)

Open the page and verify these key features:

```bash
open /Users/pranay/Projects/Data_Science/computer_vision/proj6/signature-extractor-app/web/claude_landing_page_v2/index.html
```

### Visual Check ✓
- [ ] Page loads without errors (check console - F12)
- [ ] Gradient background with floating animated blobs visible
- [ ] Orange CTA buttons showing (not unstyled)
- [ ] Font Awesome icons visible (not boxes or missing)
- [ ] Professional fonts loaded (Inter + Space Grotesk)

### Interactions ✓
- [ ] Scroll down → Progress bar at top fills up
- [ ] Navigation bar gets shadow after scrolling
- [ ] Demo carousel auto-rotates every 3 seconds
- [ ] Click demo dots → Changes step immediately
- [ ] Click tab buttons → Content switches
- [ ] Click FAQ question → Answer expands
- [ ] Scroll down far → "Back to top" button appears
- [ ] Click "Back to top" → Smooth scroll to hero

### Animations ✓
- [ ] Hero section fades in on load
- [ ] Problem cards slide up when scrolled into view
- [ ] Numbers animate (1,200+, 12,847, etc.) when visible
- [ ] Cards have subtle 3D tilt on hover (desktop)
- [ ] CTA buttons lift up on hover

### Responsive ✓
- [ ] Resize browser → Layout adapts
- [ ] On mobile width → Hamburger menu appears
- [ ] Touch/click works on all buttons

## Common Issues & Fixes

### ❌ Icons showing as boxes
**Fix**: Font Awesome CDN not loaded
- Check `<head>` has Font Awesome link
- Hard refresh (Cmd + Shift + R)

### ❌ No animations
**Fix**: JavaScript not loaded
- Check console for errors
- Verify `main.js` and `animations.js` exist

### ❌ Styles broken/ugly
**Fix**: CSS not loaded properly
- Check `style.css` path in HTML
- Hard refresh browser cache

### ❌ Demo carousel not working
**Fix**: Missing data-step attributes
- Should auto-fix after first interaction
- Check console for JavaScript errors

## Browser Testing

Test in these browsers (if available):
- [ ] Chrome/Brave (primary)
- [ ] Safari (WebKit)
- [ ] Firefox (Gecko)

## Mobile Testing

Test on actual devices or Chrome DevTools:
- [ ] iPhone SE (375px width)
- [ ] iPhone 12 Pro (390px)
- [ ] iPad (768px)

## Performance Check

Open DevTools → Network:
- [ ] Total page size < 1MB (without images)
- [ ] Page loads in < 2 seconds
- [ ] No 404 errors for resources

## Before Going Live

### Must Complete:
1. **Add Screenshots**
   - Take 4 app screenshots
   - Save to `/assets/screenshots/`
   - Name: step1-upload.png, step2-select.png, etc.
   - Optimize images (< 200KB each)

2. **Update CTA Links**
   - Replace all CTA button `#` with Gumroad link
   - Test purchase flow

3. **Add Social Links**
   - Update footer social media URLs
   - Add your Twitter, LinkedIn, GitHub

4. **Update Meta Tags**
   - Add Open Graph image
   - Test with Facebook debugger
   - Test with Twitter card validator

5. **Test on Real Mobile Device**
   - Touch interactions work
   - Page loads fast on 4G
   - No horizontal scroll

### Nice to Have:
- [ ] Add demo video instead of carousel
- [ ] Google Analytics tracking
- [ ] Hotjar or similar for user behavior
- [ ] Chat widget (if offering support)
- [ ] Exit-intent popup (optional)

## Deploy Checklist

When ready to deploy:
- [ ] All images optimized
- [ ] All links working
- [ ] Mobile tested
- [ ] Purchase flow tested
- [ ] Analytics tracking added
- [ ] Domain pointed correctly
- [ ] SSL certificate active
- [ ] 301 redirects configured (if replacing old page)

## Success Metrics to Track

After launch, monitor:
- Bounce rate (target: < 60%)
- Time on page (target: > 90 seconds)
- Scroll depth (target: 70% reach pricing)
- CTA click rate (target: > 15%)
- Conversion rate (target: > 2%)

---

**Current Status**: ✅ CSS Complete, ✅ JS Complete, ⚠️ Needs Screenshots

**Ready to test**: YES - Open index.html now!
