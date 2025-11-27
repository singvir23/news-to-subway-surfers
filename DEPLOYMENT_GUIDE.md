# Vercel Deployment Guide - Step by Step

## Prerequisites Checklist

Before deploying, make sure you have:
- [ ] A GitHub account
- [ ] A Vercel account (sign up at https://vercel.com with GitHub)
- [ ] The `subway_surfers.mp4` video in `subway-surfers-frontend/public/`
- [ ] All code committed to git

## Step 1: Prepare Your Repository

### 1.1 Commit your code to Git

```bash
cd /Users/viraajsingh/Desktop/Viraaj\'s_Projects/news-to-subway-surfers
git add .
git commit -m "Ready for Vercel deployment with cloud storage"
```

### 1.2 Create a GitHub repository

1. Go to https://github.com/new
2. Name it: `subway-surfers-video-generator`
3. Make it **Private** (recommended since you have API keys)
4. **DO NOT** initialize with README (you already have one)
5. Click "Create repository"

### 1.3 Push to GitHub

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/subway-surfers-video-generator.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**IMPORTANT**: Verify that `subway-surfers-frontend/public/subway_surfers.mp4` was pushed to GitHub. Check the file size in GitHub - it should be ~100MB.

## Step 2: Create Vercel Blob Storage

### 2.1 Go to Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Click on **Storage** tab in the top navigation
3. Click **Create Database**
4. Select **Blob**
5. Name it: `subway-surfers-videos`
6. Click **Create**

### 2.2 Get Your Blob Token
1. In your newly created Blob store, click the **Connect** tab
2. You'll see a code snippet with `BLOB_READ_WRITE_TOKEN`
3. **Copy the entire token** (starts with `vercel_blob_rw_...`)
4. **Save it somewhere safe** - you'll need it in Step 3

## Step 3: Deploy to Vercel

### 3.1 Import Your Project
1. Go to https://vercel.com/new
2. Click **Import Git Repository**
3. Find your `subway-surfers-video-generator` repo
4. Click **Import**

### 3.2 Configure Build Settings

Vercel should auto-detect Next.js, but verify:
- **Framework Preset**: Next.js
- **Root Directory**: `subway-surfers-frontend`
- **Build Command**: `npm run build` (default)
- **Output Directory**: `.next` (default)

### 3.3 Add Environment Variables

**CRITICAL STEP**: Before clicking Deploy, add your environment variable:

1. Expand **Environment Variables** section
2. Add variable:
   - **Name**: `BLOB_READ_WRITE_TOKEN`
   - **Value**: Paste the token from Step 2.2 (starts with `vercel_blob_rw_...`)
   - **Environments**: Check all three (Production, Preview, Development)
3. Click **Add**

### 3.4 Deploy

1. Click **Deploy**
2. Wait 2-5 minutes for the build to complete
3. You'll see a success screen with confetti 🎉

## Step 4: Verify Deployment

### 4.1 Check the deployment
1. Click **Visit** or go to your deployment URL (e.g., `https://subway-surfers-video-generator.vercel.app`)
2. You should see your app interface

### 4.2 Test video generation

1. Paste some test text (e.g., "Hello world, this is a test of the video generator.")
2. Click **Create video**
3. Wait for:
   - Audio generation (~2 seconds)
   - Video rendering (~30-60 seconds)
4. Click **Download video** when complete

### 4.3 Troubleshooting Common Issues

#### Issue: "BLOB_READ_WRITE_TOKEN is not defined"
**Solution**:
1. Go to your Vercel project → Settings → Environment Variables
2. Add `BLOB_READ_WRITE_TOKEN` with your token
3. Redeploy: Deployments → Three dots menu → Redeploy

#### Issue: "subway_surfers.mp4 not found"
**Solution**:
1. Check GitHub repo - is the video file there?
2. If not, the file is too large for GitHub. Options:
   - Use Git LFS (see Step 5 below)
   - Or host the video elsewhere and update `Background.tsx`

#### Issue: Video rendering times out
**Solution**:
1. Go to Vercel project → Settings → Functions
2. Increase timeout to 300 seconds (5 minutes) - requires Pro plan
3. Or optimize video: reduce duration, lower bitrate in `render-video/route.ts`

#### Issue: Build fails
**Solution**:
1. Check build logs in Vercel dashboard
2. Common fixes:
   - Clear Vercel cache: Settings → General → Clear Build Cache
   - Ensure `ROOT_DIRECTORY` is set to `subway-surfers-frontend`
   - Check that all dependencies are in `package.json`

## Step 5: Handle Large Video File (If Needed)

If `subway_surfers.mp4` is too large for GitHub (>100MB):

### Option A: Use Git LFS (Recommended)

```bash
cd /Users/viraajsingh/Desktop/Viraaj\'s_Projects/news-to-subway-surfers

# Install Git LFS (if not installed)
brew install git-lfs  # macOS
# or download from: https://git-lfs.github.com

# Initialize Git LFS
git lfs install

# Track the video file
git lfs track "subway-surfers-frontend/public/subway_surfers.mp4"

# Commit and push
git add .gitattributes
git add subway-surfers-frontend/public/subway_surfers.mp4
git commit -m "Add subway surfers video with Git LFS"
git push
```

### Option B: Host Video Externally

1. Upload `subway_surfers.mp4` to a hosting service:
   - Vercel Blob (manually upload)
   - Cloudflare R2
   - AWS S3
2. Update `Background.tsx` to use the URL:

```typescript
const videoSrc = "https://your-hosted-video-url.com/subway_surfers.mp4";
```

## Step 6: Custom Domain (Optional)

1. Go to Vercel project → Settings → Domains
2. Add your custom domain
3. Follow Vercel's DNS setup instructions

## Step 7: Monitor Usage

### Check Vercel Blob Usage
1. Go to https://vercel.com/dashboard/stores
2. Click on your `subway-surfers-videos` store
3. Check storage and bandwidth usage

### Vercel Free Tier Limits:
- **Blob Storage**: 1 GB
- **Blob Bandwidth**: 100 GB/month
- **Function Duration**: 10 seconds (for video rendering, you'll need Pro)

**For production use**, you'll need Vercel Pro ($20/month) for:
- 300-second function timeout (needed for video rendering)
- More bandwidth

## Step 8: Production Checklist

- [ ] Environment variables set correctly
- [ ] Video renders successfully
- [ ] Videos upload to Blob storage
- [ ] Download links work
- [ ] Temp files are cleaned up
- [ ] Monitor costs/usage

## Maintenance

### Updating Your App

```bash
# Make changes locally
# Test thoroughly
git add .
git commit -m "Description of changes"
git push

# Vercel will auto-deploy on push to main
```

### Viewing Logs

1. Vercel Dashboard → Your Project → Deployments
2. Click on a deployment → Runtime Logs
3. View real-time logs and errors

## Cost Estimation

### Development/Testing (Free Tier)
- Perfect for testing and low usage
- ~10-20 videos/month

### Production (Pro Plan - $20/month)
- Longer function timeouts
- 100 GB Blob bandwidth = ~1000 videos/month (assuming 100MB each)
- Additional bandwidth: $0.40/GB

## Next Steps

1. Test thoroughly on staging
2. Monitor usage and costs
3. Consider upgrading to Pro when needed
4. Set up monitoring/alerts in Vercel

## Support

- Vercel Docs: https://vercel.com/docs
- Vercel Support: https://vercel.com/support
- Check build logs for errors
- Monitor function execution times

---

**You're ready to deploy!** 🚀

Follow each step carefully, and your app will be live in ~10 minutes.
