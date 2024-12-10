import React, { useEffect, useRef } from "react";
import metadata from "./metadata.json"; // Adjust the path to your metadata JSON file

function AudioPlayer({ audio }) {
  const audioRef = useRef(null); // Reference to the audio element
  const audioId = parseInt(audio[" Id"], 10); // Replace with your actual key
  const meta = metadata[audioId];

  // Debugging
  console.log("Audio ID:", audioId);
  console.log("Metadata:", meta);

  // Load the new audio source dynamically when `meta` changes
  useEffect(() => {
    if (meta && audioRef.current) {
      console.log("Setting new audio source:", `/data/audios/${meta.Name}mp.mp3`);
      audioRef.current.load(); // Reload the audio player
    }
  }, [meta]); // Run this effect whenever `meta` changes

  return (
    <div>
      <h2>Now Playing</h2>
      {meta ? (
        <>
          <p>{`Playing: ${meta.Name}`}</p>
          <audio controls ref={audioRef}>
            <source
              src={`/data/audios/${meta.Name}mp.mp3`} // Dynamically updated source
              type="audio/mpeg"
            />
            Your browser does not support the audio element.
          </audio>
        </>
      ) : (
        <p>Loading audio metadata...</p>
      )}
    </div>
  );
}

export default AudioPlayer;
