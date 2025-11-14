# Subway Surfers Video Generator

An automated video generator that creates engaging "Subway Surfers Reddit stories" style videos with synchronized TTS narration and karaoke-style captions.

## Features

- **Free TTS**: Uses Edge-TTS with expressive voices (no API keys required)
- **Karaoke Captions**: Word-by-word highlighting synchronized with audio
- **Vertical Format**: 1080x1920 (9:16) optimized for TikTok, Instagram Reels, YouTube Shorts
- **Real-time Preview**: See your video in the browser with Remotion Player
- **Simple Interface**: Just paste text and generate

## Technology Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Remotion**: React-based video composition
- **Edge-TTS**: Free, natural-sounding text-to-speech
- **Tailwind CSS**: Styling

## Getting Started

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

The project is already set up! Just make sure all dependencies are installed:

```bash
npm install
```

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## How to Use

1. **Enter Your Text**: Paste your Reddit story, script, or any text in the input area
2. **Generate Video**: Click the "Generate Video" button
3. **Preview**: Watch your video with synchronized captions in the preview player
4. **Play**: Use the player controls to play, pause, and scrub through the video

## Project Structure

```
subway-surfers-env/
├── app/
│   ├── api/
│   │   └── generate-audio/    # TTS generation endpoint
│   ├── globals.css            # Global styles
│   ├── layout.tsx             # Root layout
│   └── page.tsx               # Main UI
├── remotion/
│   ├── Root.tsx               # Remotion root
│   ├── Composition.tsx        # Main video composition
│   ├── Background.tsx         # Background video layer
│   ├── Captions.tsx           # Caption layer with karaoke effect
│   └── Audio.tsx              # Audio layer
├── lib/
│   ├── tts.ts                 # Edge-TTS utilities
│   └── subtitles.ts           # Subtitle timing utilities
├── public/
│   ├── subway_surfers.mp4     # Background video
│   └── audio/                 # Generated audio files
└── package.json
```

## How It Works

1. **Text Input**: User enters text in the textarea
2. **TTS Generation**: API route uses Edge-TTS to generate speech with word-level timing
3. **Video Composition**: Remotion combines:
   - Background: Looping Subway Surfers gameplay
   - Audio: Generated TTS narration
   - Captions: Synchronized text with karaoke highlighting effect
4. **Preview**: Remotion Player renders the video in real-time

## Caption Styling

Captions use a karaoke-style effect:
- **Current word**: White, 100% opacity, slightly larger
- **Past words**: Gray, 40% opacity
- **Future words**: Hidden (0% opacity)
- **Styling**: Bold font with black stroke outline for readability

## Voice Settings

Currently using `en-US-AriaNeural` (expressive female voice). You can change the voice in [lib/tts.ts](lib/tts.ts:11):

```typescript
const voice = 'en-US-AriaNeural'; // or 'en-US-GuyNeural' for male
```

## Future Enhancements

- Video export functionality (download as MP4)
- Multiple voice options in UI
- Custom caption styling (font, color, position)
- Background video selection
- Batch processing
- Cloud rendering with Remotion Lambda

## Notes

- This is a local development version
- Audio files are stored in `public/audio/`
- The background video loops if text is longer than the video
- Video is optimized for vertical (9:16) social media format

## Troubleshooting

### Server won't start
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Audio not generating
- Check that the `public/audio/` directory exists
- Ensure Edge-TTS is installed: `npm install node-edge-tts`

### Captions not syncing
- Edge-TTS provides word-level timing automatically
- If timings are missing, a fallback estimation is used

## License

This project is for educational and personal use.
