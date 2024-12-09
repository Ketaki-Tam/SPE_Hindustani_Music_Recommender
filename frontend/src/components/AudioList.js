import React from "react";

function AudioList({ audios, onSelect }) {
  return (
    <div>
      <h2>Recommendations</h2>
      {audios.length > 0 ? (
        audios.map((audio) => (
          <div key={audio}>
            <span>{audio}</span>
            <button onClick={() => onSelect(audio)}>Select</button>
          </div>
        ))
      ) : (
        <p>No recommendations available.</p>
      )}
    </div>
  );
}

export default AudioList;
