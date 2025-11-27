# Quick Deploy Guide - No Large Files in Git!

This guide will get your app deployed to Vercel in under 10 minutes without dealing with large video files in Git.

## Overview

- Background video (`subway_surfers.mp4`) is hosted on Vercel Blob
- Generated videos are uploaded to Vercel Blob
- No large files in your Git repository

## Step 1: Commit Code to GitHub

```bash
cd /Users/viraajsingh/Desktop/Viraaj\'s_Projects/news-to-subway-surfers

# Make sure the video is ignored (already done)
git rm --cached subway-surfers-frontend/public/subway_surfers.mp4 2>/dev/null || true

# Commit everything
git add .
git commit -m "Ready for Vercel deployment - videos on cloud"
git push
```

## Step 2: Create Vercel Blob Store

1. Go to https://vercel.com/dashboard
2. Click **Storage** → **Create Database**
3. Select **Blob**
4. Name it: `subway-surfers-videos`
5. Click **Create**
6. **Save your `BLOB_READ_WRITE_TOKEN`** for later

## Step 3: Upload Background Video to Blob

### Option A: Using Vercel Dashboard (Recommended)

1. In your Blob store, click **Upload** button
2. Select `subway-surfers-frontend/public/subway_surfers.mp4`
3. Wait for upload to complete
4. Click on the uploaded file
5. **Copy the public URL** - looks like:
   ```
   https://xxxxxxxxxx.public.blob.vercel-storage.com/subway_surfers-xxxxx.mp4
   ```
6. **Save this URL** - you'll need it in Step 4

### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Upload video (replace YOUR_TOKEN with your BLOB_READ_WRITE_TOKEN)
vercel blob upload subway-surfers-frontend/public/subway_surfers.mp4 \
  --token YOUR_TOKEN

# Copy the URL from the output
```

## Step 4: Deploy to Vercel

1. Go to https://vercel.com/new
2. Import your GitHub repo: `singvir23/news-to-subway-surfers`
3. Configure:
   - **Root Directory**: `subway-surfers-frontend`
   - Framework should auto-detect as Next.js

4. **Add Environment Variables** (CRITICAL):

   Click **Environment Variables** and add these TWO variables:

   **Variable 1:**
   - Name: `BLOB_READ_WRITE_TOKEN`
   - Value: `vercel_blob_rw_xxxxx` (from Step 2)
   - Environments: ✅ Production ✅ Preview ✅ Development

   **Variable 2:**
   - Name: `NEXT_PUBLIC_BACKGROUND_VIDEO_URL`
   - Value: `https://xxxxxxxxxx.public.blob.vercel-storage.com/subway_surfers-xxxxx.mp4` (from Step 3)
   - Environments: ✅ Production ✅ Preview ✅ Development

5. Click **Deploy**

6. Wait 3-5 minutes for deployment ☕

## Step 5: Test Your Deployment

1. Visit your deployment URL (e.g., `https://subway-surfers-video-generator.vercel.app`)
2. Paste test text: "Hello world, this is a test video."
3. Click **Create video**
4. Wait for audio generation (~2 seconds)
5. Wait for video rendering (~30-60 seconds)
6. Click **Download video**

## Troubleshooting

### "Background video not found" or video doesn't load
**Fix:**
- Verify `NEXT_PUBLIC_BACKGROUND_VIDEO_URL` is set in Vercel environment variables
- Make sure the URL is correct and publicly accessible
- Check browser console for errors
- Redeploy: Deployments → ⋯ menu → Redeploy

### "BLOB_READ_WRITE_TOKEN not defined"
**Fix:**
- Go to Settings → Environment Variables
- Verify `BLOB_READ_WRITE_TOKEN` is added
- Redeploy

### Video rendering times out (10 second limit)
**This is expected on free tier.**

**Solution:** Upgrade to Vercel Pro ($20/month) for:
- 300-second function timeout (needed for video rendering)
- More bandwidth

### Build fails
**Fix:**
- Check build logs in Vercel dashboard
- Verify `ROOT_DIRECTORY` is set to `subway-surfers-frontend`
- Try: Settings → General → Clear Build Cache → Redeploy

## Local Development

To test locally:

1. Create `.env.local` in `subway-surfers-frontend/`:
```bash
BLOB_READ_WRITE_TOKEN=vercel_blob_rw_xxxxx
NEXT_PUBLIC_BACKGROUND_VIDEO_URL=https://xxxxxxxxxx.public.blob.vercel-storage.com/subway_surfers-xxxxx.mp4
```

2. Run:
```bash
cd subway-surfers-frontend
npm run dev
```

## What Happens When You Generate a Video

1. **Text Input** → TTS generates audio (saved to Blob temporarily)
2. **Audio** + **Background Video (from Blob)** → Remotion renders video
3. **Final Video** → Uploaded to Blob storage
4. **Cleanup** → Temporary audio files deleted
5. **Response** → You get a download URL to the final video

## Cost Estimates

### Free Tier (Development/Testing)
- Blob: 1 GB storage, 100 GB bandwidth
- Function timeout: 10 seconds (TOO SHORT for video rendering)
- Cost: **$0**
- Suitable for: Testing only

### Pro Tier (Production)
- Blob: 1 GB storage, 100 GB bandwidth included
- Function timeout: 300 seconds (5 minutes) ✅
- Cost: **$20/month**
- Suitable for: ~1000 videos/month

### Additional Costs
- Extra Blob bandwidth: $0.40/GB
- Each video ~100MB = ~1000 videos per 100GB

## Next Steps

1. Test thoroughly on Vercel
2. Monitor Blob storage usage
3. Consider upgrading to Pro when ready for production
4. Set up custom domain (optional)

---

**You're ready!** 🚀

Follow Steps 1-5 and you'll have a working deployment without dealing with large files in Git.
