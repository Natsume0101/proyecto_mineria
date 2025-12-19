# Streamlit Cloud Deployment Guide
## 5-Minute Setup for Live Demo

This guide walks you through deploying your Mineral Exploration app to Streamlit Cloud (free tier).

---

## Prerequisites

✅ GitHub account  
✅ Streamlit Cloud account (sign up at [share.streamlit.io](https://share.streamlit.io))  
✅ Google Earth Engine account (see [GEE Setup](#google-earth-engine-setup))

---

## Step 1: Google Earth Engine Setup

### 1.1 Create GEE Account
1. Go to [https://earthengine.google.com/signup/](https://earthengine.google.com/signup/)
2. Sign up with your Google account (free for non-commercial use)
3. Wait for approval email (usually instant)

### 1.2 Create Service Account (for Streamlit Cloud)

**Option A: Using Google Cloud Console** (Recommended for deployment)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: `mineral-exploration-app`
3. Enable **Earth Engine API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Earth Engine API"
   - Click "Enable"
4. Create Service Account:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Name: `streamlit-gee-access`
   - Click "Create and Continue"
5. Grant Permissions:
   - Role: "Earth Engine Resource Viewer"
   - Click "Done"
6. Create JSON Key:
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Select "JSON" format
   - Click "Create" (file will download)
   - **Save this file securely** - you'll need it for Streamlit secrets

**Option B: Local Authentication** (For local development only)

```bash
# Install Earth Engine CLI
pip install earthengine-api

# Authenticate
earthengine authenticate

# Test connection
python -c "import ee; ee.Initialize(); print('GEE connected!')"
```

---

## Step 2: Push Code to GitHub

```bash
# Initialize git repository (if not already)
cd proyecto_mineria
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Mineral exploration satellite analysis app"

# Create repository on GitHub (via web interface)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/proyecto_mineria.git
git branch -M main
git push -u origin main
```

### Important: Create `.gitignore`

Create a `.gitignore` file to avoid committing sensitive data:

```gitignore
# Secrets
*.json
service-account-key.json

# Python
__pycache__/
*.py[cod]
*$py.class
.env

# Streamlit
.streamlit/secrets.toml

# IDE
.vscode/
.idea/

# Data
data/*.csv
*.kml
```

---

## Step 3: Configure Streamlit Cloud Secrets

### 3.1 Prepare GEE Credentials

Open the service account JSON key file you downloaded. It looks like:
```json
{
  "type": "service_account",
  "project_id": "mineral-exploration-app",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "streamlit-gee-access@mineral-exploration-app.iam.gserviceaccount.com",
  ...
}
```

### 3.2 Add to Streamlit Secrets

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account
4. Select:
   - Repository: `YOUR_USERNAME/proyecto_mineria`
   - Branch: `main`
   - Main file path: `app.py`
5. **Before deploying**, click "Advanced settings"
6. In the "Secrets" section, paste:

```toml
# Google Earth Engine Service Account
[gee]
type = "service_account"
project_id = "mineral-exploration-app"
private_key_id = "YOUR_PRIVATE_KEY_ID"
private_key = """-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_HERE
-----END PRIVATE KEY-----"""
client_email = "YOUR_SERVICE_ACCOUNT_EMAIL"
client_id = "YOUR_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR_CERT_URL"
```

**Important:** Replace all `YOUR_*` placeholders with values from your JSON key file.

---

## Step 4: Update `analysis_engine.py` for Cloud Authentication

Modify the `__init__` method in `analysis_engine.py`:

```python
import streamlit as st

def __init__(self):
    """Initialize Google Earth Engine with Streamlit secrets"""
    try:
        # Check if running on Streamlit Cloud
        if 'gee' in st.secrets:
            # Use service account authentication
            credentials = ee.ServiceAccountCredentials(
                email=st.secrets['gee']['client_email'],
                key_data=st.secrets['gee']['private_key']
            )
            ee.Initialize(credentials)
        else:
            # Local development - use standard authentication
            ee.Initialize()
        print("✅ Google Earth Engine initialized successfully")
    except Exception as e:
        print(f"❌ GEE initialization error: {e}")
        st.error("Google Earth Engine authentication failed. Check secrets configuration.")
```

Commit and push this change:
```bash
git add analysis_engine.py
git commit -m "Add Streamlit Cloud GEE authentication"
git push
```

---

## Step 5: Deploy!

1. In Streamlit Cloud, click "Deploy"
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://YOUR_USERNAME-proyecto-mineria-app-abc123.streamlit.app`

### Expected Deployment Time
- ⏱️ 1-2 minutes: Dependency installation
- ⏱️ 30 seconds: App initialization
- ⏱️ 10 seconds: GEE authentication
- ✅ **Total: ~3 minutes**

---

## Step 6: Test Your Deployment

1. Open the deployed URL
2. Verify default coordinates are loaded (Andacollo: -30.226, -71.078)
3. Click "GENERATE DRILL TARGETS"
4. Wait 30-60 seconds for analysis
5. Verify:
   - ✅ Map renders with drill targets
   - ✅ Metrics display correctly
   - ✅ CSV/KML downloads work

---

## Troubleshooting

### Error: "GEE Authentication Failed"

**Cause:** Service account credentials not configured correctly

**Fix:**
1. Double-check secrets.toml formatting
2. Ensure private key includes `\n` characters (newlines)
3. Verify service account has Earth Engine API enabled
4. Check project ID matches

### Error: "Not enough quota for GEE requests"

**Cause:** Free tier computation limits (10,000 requests/day)

**Fix:**
1. Reduce analysis radius (use 5-10 km instead of 25 km)
2. Increase cloud cover tolerance (20% → 30%)
3. Wait 24 hours for quota reset
4. Consider upgrading to GEE commercial license

### Error: "Module not found: streamlit_folium"

**Cause:** requirements.txt not properly loaded

**Fix:**
1. Check `requirements.txt` is in root directory
2. Verify all package names are correct (lowercase, hyphens)
3. Restart app deployment

### Slow Performance (>2 minutes analysis)

**Optimization tips:**
- Use smaller radius (5-10 km for demos)
- Reduce sample points in clustering (5000 → 2000)
- Increase cloud cover tolerance for more imagery options
- Use 60m resolution instead of 10m (already default)

---

## Custom Domain (Optional)

Streamlit Cloud allows custom domains on Business plan ($250/month).

For free tier, share the Streamlit URL directly:
- Portfolio: `https://juliegaete-proyecto-mineria.streamlit.app`
- LinkedIn: Add to "Featured" section
- Resume: Include under "Projects"

---

## Monitoring & Analytics

### Streamlit Cloud Dashboard
- View app usage stats
- Monitor errors and logs
- Check deployment status
- View resource usage

### Add Google Analytics (Optional)

Add to `app.py` (before st.set_page_config):
```python
# Google Analytics tracking
import streamlit.components.v1 as components

components.html("""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
""", height=0)
```

---

## Updating Your Deployed App

All changes pushed to GitHub `main` branch will **auto-deploy**:

```bash
# Make changes to code
git add .
git commit -m "Update: improved clustering algorithm"
git push

# Streamlit Cloud will automatically redeploy in 2-3 minutes
```

---

## Cost Summary

| Service | Free Tier | Cost |
|---------|-----------|------|
| **Streamlit Cloud** | 1 private app | $0/month |
| **Google Earth Engine** | 10,000 requests/day | $0/month |
| **GitHub** | Unlimited public repos | $0/month |
| **Sentinel-2 Data** | Unlimited (Copernicus) | $0 |
| **TOTAL** | | **$0/month** ✅ |

---

## Next Steps

1. ✅ Deploy app to Streamlit Cloud
2. 📸 Take screenshots for README
3. 🔗 Add live demo URL to portfolio
4. 📧 Share with mining contacts
5. 💼 Add to LinkedIn projects section
6. 📊 Monitor usage and gather feedback

---

## Support

**Issues?** Open a GitHub issue or contact:
📧 juliegaeteguzman@gmail.com

**GEE Support:** [Google Earth Engine Forum](https://groups.google.com/g/google-earth-engine-developers)

**Streamlit Support:** [Streamlit Community Forum](https://discuss.streamlit.io/)

---

<div align="center">

**🚀 Ready to impress mining executives!**

</div>
