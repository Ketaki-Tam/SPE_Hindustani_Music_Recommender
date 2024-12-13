import React, { useState } from "react";
import "./Modal.css"; // For styling the modal

const PreferencesModal = ({ onSavePreferences }) => {
  const [raag, setRaag] = useState("");
  const [artist, setArtist] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (raag && artist) {
      onSavePreferences(raag, artist);
    } else {
      alert("Please select both a raag and an artist.");
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Welcome!</h2>
        <p>Please fill in these choices for initial recommendations</p>
        <form onSubmit={handleSubmit}>
          <label>
            Preferred Raag:
            <select value={raag} onChange={(e) => setRaag(e.target.value)}>
              <option value="" disabled>
                Select a raag
              </option>
              <option value="Yaman">Yaman</option>
              <option value="Todi">Todi</option>
              <option value="Bhimpalasi">Bhimpalasi</option>
              <option value="Jog">Bhimpalasi</option>
            </select>
          </label>
          <label>
            Preferred Artist:
            <select value={artist} onChange={(e) => setArtist(e.target.value)}>
              <option value="" disabled>
                Select an artist
              </option>
              <option value="Ajoy Chakraborty">Ajoy Chakraborty</option>
              <option value="Shahid Parvez">Kaushiki Chakraborty Desikan</option>
              <option value="Omkar Dadarkar">Shahid Parvez</option>
            </select>
          </label>
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
};

export default PreferencesModal;
