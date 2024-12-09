import React, { useEffect, useRef } from "react";

function AudioPlayer({ audio }) {
  const audioRef = useRef(null);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.load();
    }
  }, [audio]);

  return (
    <div>
      <h2>Now Playing</h2>
      <audio controls ref={audioRef}>
        {/* <source src={`/path/to/audios/${audio}`} type="audio/mpeg" /> */}
        <source src={audio} type="audio/mpeg" />
        Your browser does not support the audio element.
      </audio>
    </div>
  );
}

export default AudioPlayer;
