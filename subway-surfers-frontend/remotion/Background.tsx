import React from 'react';
import { Video, useCurrentFrame, useVideoConfig, staticFile } from 'remotion';

export const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  // Loop the video if the composition is longer than the video
  // Subway Surfers video will loop seamlessly
  return (
    <Video
      src={staticFile('subway_surfers.mp4')}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        objectFit: 'cover',
      }}
      // Loop the video
      loop
      // Mute the background video (we only want our TTS audio)
      muted
      // Ensure smooth playback
      volume={0}
    />
  );
};
