# Subway Surfers Video Generator

Automated video generator that creates "Subway Surfers" style videos with TTS narration and karaoke captions. All videos stored in Vercel Blob cloud storage.

## Features

- **Free TTS**: Microsoft Edge TTS with natural voices
- **Karaoke Captions**: Word-by-word synchronized highlighting
- **Cloud Storage**: Videos automatically uploaded to Vercel Blob
- **Vertical Format**: 1080x1920 for TikTok/Instagram/YouTube Shorts
- **Auto Cleanup**: Temporary files deleted after processing

## Quick Start

### 1. Install

```bash
npm install
```

### 2. Set Up Vercel Blob

1. Create Blob store: https://vercel.com/dashboard/stores
2. Upload your `subway_surfers.mp4` background video
3. Connect the Blob store to your Vercel project (auto-adds token)
4. Copy the background video's public URL

### 3. Environment Variables

Create `.env.local`:

```bash
# Auto-injected when you connect Blob store to Vercel project
BLOB_READ_WRITE_TOKEN=vercel_blob_rw_xxxxx

# URL of your uploaded background video
NEXT_PUBLIC_BACKGROUND_VIDEO_URL=https://xxxxx.blob.vercel-storage.com/subway_surfers.mp4
```

### 4. Run

```bash
npm run dev
```

Visit http://localhost:3000

## Deploy to Vercel

1. Push to GitHub
2. Import project in Vercel
3. Set **Root Directory**: `subway-surfers-frontend`
4. Connect Blob store to project
5. Add: `NEXT_PUBLIC_BACKGROUND_VIDEO_URL`
6. Deploy

**Note**: Vercel Pro ($20/mo) required for production (free tier has 10s timeout, rendering takes 30-60s).

## How It Works

1. User inputs text
2. Edge TTS generates audio + word timings
3. Remotion renders video (background + audio + captions)
4. Video uploads to Vercel Blob
5. Temp files cleaned up
6. User gets download link

## Tech Stack

- Next.js 14
- Remotion (video rendering)
- Edge TTS (text-to-speech)
- Vercel Blob (cloud storage)
- TypeScript

## Project Structure

```
app/
├── api/
│   ├── generate-audio/    # TTS generation
│   └── render-video/      # Video rendering + upload
└── page.tsx               # Main UI
remotion/
├── Background.tsx         # Background video layer
├── Captions.tsx          # Karaoke captions
├── Audio.tsx             # Audio layer
└── Root.tsx              # Remotion composition
lib/
├── tts.ts                # TTS utilities
└── subtitles.ts          # Timing calculations
```

## Troubleshooting

### Build fails
- Verify Root Directory: `subway-surfers-frontend`
- Clear build cache in Vercel

### Video not loading
- Check `NEXT_PUBLIC_BACKGROUND_VIDEO_URL` is set
- Verify URL is publicly accessible

### Rendering times out
- Upgrade to Vercel Pro for 300s timeout
- Free tier has 10s limit

## Cost

- **Free**: Testing only (10s timeout)
- **Pro ($20/mo)**: Production use (300s timeout, ~1000 videos/month)

## License

Educational and personal use.
