import React from "react";

function OptionsSelector({ onSelect }) {
  const options = ["Search by raag", "Search by artist"];

  return (
    <div>
      <h2>Select an Option</h2>
      {options.map((option) => (
        <label key={option} style={{ display: "block", margin: "10px 0" }}>
          <input
            type="radio"
            name="option"
            value={option}
            onChange={() => onSelect(option)}
            style={{ marginRight: "10px" }}
          />
          {option}
        </label>
      ))}
    </div>
  );
}

export default OptionsSelector;
