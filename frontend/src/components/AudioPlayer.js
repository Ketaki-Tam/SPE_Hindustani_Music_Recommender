import React, { useEffect, useRef, useState } from "react";
import metadata from "./metadata.json"; // Adjust the path to your metadata JSON file

function AudioPlayer({ audio }) {
  const audioRef = useRef(null); // Reference to the audio element
  const audioId = parseInt(audio[" Id"], 10); // Replace with your actual key
  const meta = metadata[audioId];
  const [audioUrl, setAudioUrl] = useState(null);

  // Debugging
  console.log("Audio ID:", audioId);
  console.log("Metadata:", meta);

  // Combined useEffect to handle both audio source setup and signed URL fetching
  useEffect(() => {
    if (meta && audioRef.current) {
      console.log("Setting new audio source:", `${meta.Name}mp.mp3`);
      
      // Reload the audio player
      audioRef.current.load();

      // Fetch signed URL
      // fetch(`/api/get_audio?file=${meta.Name}mp.mp3`)
      //   .then((response) => response.json())
      //   .then((data) => {
      //     if (data.signedUrl) {
      //       setAudioUrl(data.signedUrl);
      //     } else {
      //       console.error("Error fetching signed URL:", data.error);
      //     }
      //   })
        // .catch((err) => console.error("Error fetching signed URL:", err));
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
              src={`http://192.168.49.2:32001/api/get-audio/?file_name=${meta.Name}mp.mp3`}// Dynamically updated source
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
