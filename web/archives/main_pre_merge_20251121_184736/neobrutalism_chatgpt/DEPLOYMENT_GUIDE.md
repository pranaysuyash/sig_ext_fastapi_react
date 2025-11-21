# SignKit Landing Page - Deployment Guide

**Date:** November 18, 2025  
**Domain:** signkit.work  
**Goal:** Deploy landing page to S3 + CloudFront with HTTPS

---

## 📦 Files to Deploy

### **1. Core Files** (Required)
```
web/neobrutalism_chatgpt/
├── index.html                    # Main landing page
├── screenshots/
│   ├── screenshot-1.png         # Empty interface (118KB)
│   ├── screenshot-2.png         # Signature extraction (376KB)
│   └── screenshot-3.png         # PDF signing (169KB)
└── og-image.png                 # Social sharing image (376KB)
```

### **2. Asset Dependencies** (Required)
```
assets/files/
├── signkit_icon_16x16.png       # Favicon 16x16
├── signkit_icon_32x32.png       # Favicon 32x32
├── signkit_icon_64x64.png       # Logo in header
└── signkit_icon_256x256.png     # Apple touch icon
```

### **Total Size:** ~1.2MB (optimized for web)

---

## ☁️ Simpler Option: Cloudflare-only (No CloudFront)

If you're already using Cloudflare as your DNS and CDN, you can skip CloudFront entirely and point Cloudflare directly to your S3 static website. This is the fastest to set up and lowest complexity/cost for a static single-page site.

### Quick Steps (10–15 minutes)

1. S3 Static Website

- Create S3 bucket `signkit.work` (or any bucket) and enable Static website hosting with `index.html`.
- Add a public read bucket policy (as shown below in Phase 2.2).
- Upload the files (Phase 2.3 commands work the same).

1. Cloudflare DNS

- Add a CNAME record:
  - Name: `@` (apex) → Target: your S3 website endpoint, e.g. `signkit.work.s3-website-us-east-1.amazonaws.com`
  - Proxy status: Proxied (orange cloud ON)
- Add another CNAME for `www` → target the same S3 website endpoint; Proxy: ON.
- Cloudflare automatically flattens CNAME at apex.

1. Cloudflare SSL/TLS

- Set SSL/TLS mode to Flexible (HTTPS between visitor and Cloudflare; HTTP from Cloudflare to S3 website endpoint).
- Enable HTTP Strict Transport Security (HSTS) only if you are certain HTTPS works everywhere and you won’t switch back.

1. Cache and Performance

- Rules → Cache Rules: Cache Everything for `signkit.work/*`, Edge TTL 1 day (or as you prefer). HTML can be 1h for quick updates.
- Turn on Brotli compression and Early Hints (Speed → Optimization).

1. Redirects (Optional)

- If you prefer redirecting `www` → apex, use Cloudflare Rules → Redirect Rules: `www.signkit.work/*` → `https://signkit.work/$1` (301).

1. Purge Cache after updates

- Cloudflare → Caching → Purge Cache → Purge Everything (or specific paths).

That’s it: `https://signkit.work` will be served by Cloudflare globally without CloudFront.

### When to choose CloudFront instead

- You want AWS-native features like Origin Access Control/private S3 origin, Lambda@Edge, signed URLs, or granular cache behaviors per path.
- You want HTTPS between CDN and origin for S3 website endpoints (CloudFront can use S3 REST endpoint with HTTPS; Cloudflare Flexible uses HTTP to website endpoint).
- You prefer all infra to stay within AWS.

If none of the above are required, Cloudflare-only is perfectly fine and simpler.

---

## 🚀 Step-by-Step Deployment

### **Phase 1: Prepare Files for Upload**

#### Option A: Use current structure (recommended)
```bash
cd /Users/pranay/Projects/Data_Science/computer_vision/proj6/signature-extractor-app

# Create deployment directory
mkdir -p deploy-landing

# Copy HTML and screenshots
cp web/neobrutalism_chatgpt/index.html deploy-landing/
cp -r web/neobrutalism_chatgpt/screenshots deploy-landing/
cp web/neobrutalism_chatgpt/og-image.png deploy-landing/

# Create assets directory structure
mkdir -p deploy-landing/assets/files

# Copy icons
cp assets/files/signkit_icon_16x16.png deploy-landing/assets/files/
cp assets/files/signkit_icon_32x32.png deploy-landing/assets/files/
cp assets/files/signkit_icon_64x64.png deploy-landing/assets/files/
cp assets/files/signkit_icon_256x256.png deploy-landing/assets/files/

# Verify structure
tree deploy-landing
```

**Expected structure:**
```
deploy-landing/
├── index.html
├── og-image.png
├── assets/
│   └── files/
│       ├── signkit_icon_16x16.png
│       ├── signkit_icon_32x32.png
│       ├── signkit_icon_64x64.png
│       └── signkit_icon_256x256.png
└── screenshots/
    ├── screenshot-1.png
    ├── screenshot-2.png
    └── screenshot-3.png
```

---

### **Phase 2: AWS S3 Setup**

#### **2.1 Create S3 Bucket**
```bash
# AWS CLI (or use AWS Console)
aws s3 mb s3://signkit.work --region us-east-1

# Enable static website hosting
aws s3 website s3://signkit.work \
  --index-document index.html \
  --error-document index.html
```

**Via AWS Console:**
1. Go to S3 Console → Create Bucket
2. **Bucket name:** `signkit.work`
3. **Region:** `us-east-1` (recommended for CloudFront)
4. **Block Public Access:** Uncheck all (we'll use bucket policy)
5. Click **Create Bucket**

#### **2.2 Configure Bucket Policy**
In S3 Console → `signkit.work` → Permissions → Bucket Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::signkit.work/*"
    }
  ]
}
```

#### **2.3 Upload Files**
```bash
cd deploy-landing

# Upload with correct content types and caching
aws s3 sync . s3://signkit.work \
  --exclude ".DS_Store" \
  --exclude "*.md" \
  --cache-control "max-age=86400" \
  --metadata-directive REPLACE

# Set longer cache for images (7 days)
aws s3 sync screenshots/ s3://signkit.work/screenshots/ \
  --cache-control "max-age=604800" \
  --metadata-directive REPLACE

aws s3 sync assets/ s3://signkit.work/assets/ \
  --cache-control "max-age=604800" \
  --metadata-directive REPLACE

# Set HTML with shorter cache (1 hour for easy updates)
aws s3 cp index.html s3://signkit.work/index.html \
  --content-type "text/html; charset=utf-8" \
  --cache-control "max-age=3600" \
  --metadata-directive REPLACE
```

**Verify upload:**
```bash
aws s3 ls s3://signkit.work/ --recursive --human-readable
```

---

### **Phase 3: CloudFront CDN Setup** (Recommended)

#### **Why CloudFront?**
- ✅ Free SSL certificate (AWS Certificate Manager)
- ✅ Global CDN (faster load times worldwide)
- ✅ Better SEO (Google loves HTTPS + speed)
- ✅ DDoS protection
- ✅ Custom error pages
- ✅ ~$0.50-2/month for typical traffic

#### **3.1 Request SSL Certificate (AWS Certificate Manager)**
**IMPORTANT:** Must be done in `us-east-1` region for CloudFront!

1. Go to **AWS Certificate Manager** (ACM) in `us-east-1`
2. Click **Request Certificate**
3. **Domain names:**
   - `signkit.work`
   - `www.signkit.work`
4. **Validation method:** DNS validation
5. Click **Request**
6. **Add CNAME records to Cloudflare** (see Phase 4)

**Wait for validation** (~5-30 minutes after adding DNS records)

#### **3.2 Create CloudFront Distribution**
In CloudFront Console:

**Origin Settings:**
- **Origin Domain:** `signkit.work.s3-website-us-east-1.amazonaws.com` (use S3 website endpoint, NOT bucket endpoint)
- **Protocol:** HTTP only (S3 website endpoint doesn't support HTTPS)
- **Origin ID:** `S3-signkit-work`

**Default Cache Behavior:**
- **Viewer Protocol Policy:** Redirect HTTP to HTTPS
- **Allowed HTTP Methods:** GET, HEAD, OPTIONS
- **Cache Policy:** Managed-CachingOptimized
- **Compress Objects:** Yes

**Distribution Settings:**
- **Alternate Domain Names (CNAMEs):**
  - `signkit.work`
  - `www.signkit.work`
- **Custom SSL Certificate:** Select your ACM certificate
- **Supported HTTP Versions:** HTTP/2, HTTP/3
- **Default Root Object:** `index.html`
- **Standard Logging:** Off (or enable to S3 bucket)

**Custom Error Responses:**
Add error response:
- **HTTP Error Code:** 404
- **Customize Error Response:** Yes
- **Response Page Path:** `/index.html`
- **HTTP Response Code:** 200

Click **Create Distribution**

**Note the CloudFront domain:** e.g., `d111111abcdef8.cloudfront.net`

---

### **Phase 4: Cloudflare DNS Configuration**

Since your nameservers are already on Cloudflare:

#### **4.1 Add ACM Validation Records** (if not done yet)
From ACM console, copy the CNAME record:
- **Name:** `_xxxxxxxxxxxxx.signkit.work`
- **Value:** `_yyyyyyyyyyy.acm-validations.aws.`

In Cloudflare:
1. Go to DNS settings for `signkit.work`
2. Add **CNAME record**:
   - **Type:** CNAME
   - **Name:** `_xxxxxxxxxxxxx` (just the subdomain part)
   - **Target:** Validation value from ACM
   - **Proxy status:** DNS only (gray cloud)
   - **TTL:** Auto

#### **4.2 Point Domain to CloudFront**

**Option A: Using CNAME (recommended for www)**
1. In Cloudflare DNS:
   - **Type:** CNAME
   - **Name:** `www`
   - **Target:** `d111111abcdef8.cloudfront.net` (your CloudFront domain)
   - **Proxy status:** DNS only (gray cloud) 
   - **TTL:** Auto

**Option B: Using A Record + ALIAS (for apex domain)**
CloudFront doesn't give you an IP, so you need:
1. Use Cloudflare's **CNAME flattening** feature
2. Add CNAME record:
   - **Type:** CNAME
   - **Name:** `@` (apex)
   - **Target:** `d111111abcdef8.cloudfront.net`
   - **Proxy status:** DNS only (gray cloud)
   - **TTL:** Auto

**IMPORTANT:** Turn OFF Cloudflare proxy (gray cloud icon) to let CloudFront handle SSL and caching!

#### **4.3 Redirect www → apex (or vice versa)**

**Option 1: CloudFront handles both** (current setup)
- Both `signkit.work` and `www.signkit.work` point to CloudFront
- CloudFront serves same content for both

**Option 2: Cloudflare Page Rule redirect** (if you prefer)
1. Enable proxy on `www` (orange cloud)
2. Go to **Rules → Page Rules**
3. Add rule:
   - **URL:** `www.signkit.work/*`
   - **Setting:** Forwarding URL (301 permanent)
   - **Destination:** `https://signkit.work/$1`

---

### **Phase 5: Namecheap Configuration**

Since nameservers are on Cloudflare, no action needed in Namecheap unless:

1. Go to Namecheap Dashboard → Domain List → `signkit.work`
2. **Nameservers:** Should show:
   ```
   Custom DNS
   ns1.cloudflare.com
   ns2.cloudflare.com
   ```
3. ✅ If correct, no changes needed

---

### **Phase 6: Verification & Testing**

#### **6.1 Wait for Propagation**
- **CloudFront deployment:** 15-20 minutes
- **DNS changes:** 5-60 minutes
- **ACM certificate validation:** 5-30 minutes

#### **6.2 Test Endpoints**
```bash
# Check S3 direct (should work)
curl -I http://signkit.work.s3-website-us-east-1.amazonaws.com

# Check CloudFront (should work after deployment)
curl -I https://signkit.work

# Check www redirect
curl -I https://www.signkit.work

# Check HTTPS redirect
curl -I http://signkit.work
```

#### **6.3 Test in Browser**
1. Open `https://signkit.work` (should load with HTTPS)
2. Check DevTools → Network → verify assets load
3. Test on mobile (responsive design)
4. Share link on Twitter/LinkedIn → verify OG image appears

#### **6.4 Performance Testing**
- **GTmetrix:** https://gtmetrix.com
- **PageSpeed Insights:** https://pagespeed.web.dev
- **Pingdom:** https://tools.pingdom.com

**Target scores:**
- Load time: <2s
- Page size: <1.5MB ✅ (currently ~1.2MB)
- Requests: <20 ✅ (currently ~10)

---

## 📝 Quick Command Reference

### **Deploy Updates**
```bash
# Update HTML only
aws s3 cp web/neobrutalism_chatgpt/index.html s3://signkit.work/index.html \
  --content-type "text/html; charset=utf-8" \
  --cache-control "max-age=3600"

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"

# Or just index.html
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/index.html"
```

### **Update Screenshots**
```bash
# Upload new screenshots
aws s3 sync web/neobrutalism_chatgpt/screenshots/ s3://signkit.work/screenshots/ \
  --cache-control "max-age=604800"

# Invalidate
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/screenshots/*"
```

---

## 💰 Cost Estimate

### **AWS Costs (Monthly)**
- **S3 Storage:** $0.023/GB → ~$0.03/month (1.2MB)
- **S3 Requests:** $0.0004/1000 → ~$0.01/month (negligible)
- **CloudFront Data Transfer:**
  - First 10 TB/month: $0.085/GB
  - Estimate 1,000 visitors × 1.2MB = 1.2GB → ~$0.10/month
- **CloudFront Requests:** $0.0075/10,000 → ~$0.01/month
- **SSL Certificate (ACM):** FREE ✅

**Total: ~$0.15-0.50/month** for typical launch traffic

### **At Scale (10,000 visitors/month):**
- Data transfer: 12GB × $0.085 = $1.02
- **Total: ~$1.50/month**

---

## 🔧 Troubleshooting

### **Issue: 403 Forbidden on S3**
**Fix:** Check bucket policy allows public read:
```bash
aws s3api get-bucket-policy --bucket signkit.work
```

### **Issue: CloudFront shows old version**
**Fix:** Invalidate cache:
```bash
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"
```

### **Issue: SSL certificate pending validation**
**Fix:** Check Cloudflare DNS has ACM validation CNAME

### **Issue: Images not loading**
**Fix:** Check paths in HTML match S3 structure:
- HTML: `../../assets/files/signkit_icon_64x64.png`
- S3: `s3://signkit.work/assets/files/signkit_icon_64x64.png`

### **Issue: Page loads slow**
**Fix:** 
1. Enable CloudFront compression (should be on)
2. Check cache-control headers
3. Verify images are optimized (<500KB each)

---

## ✅ Final Checklist

- [ ] S3 bucket created (`signkit.work`)
- [ ] Files uploaded to S3 with correct structure
- [ ] Bucket policy allows public read
- [ ] ACM certificate requested in `us-east-1`
- [ ] ACM validation CNAME added to Cloudflare
- [ ] Certificate status: **Issued** ✅
- [ ] CloudFront distribution created
- [ ] CloudFront custom domain: `signkit.work`, `www.signkit.work`
- [ ] CloudFront SSL certificate selected
- [ ] Cloudflare DNS points to CloudFront
- [ ] Cloudflare proxy: **OFF** (gray cloud)
- [ ] Test: `https://signkit.work` loads correctly
- [ ] Test: HTTPS redirect works
- [ ] Test: OG image shows on social share
- [ ] Test: All screenshots load
- [ ] Analytics: Plausible tracking works

---

## 🚀 Go Live!

Once all checks pass:
1. Share on Twitter/LinkedIn with screenshot
2. Post on Product Hunt (schedule launch)
3. Share in relevant Reddit communities
4. Update Gumroad product page with live link

**Your landing page is now live at:** `https://signkit.work` 🎉
