import React from "react";

function AudioList({ audios, onSelect }) {
  // Check if the list is non-empty and has JSON objects with fields
  const fields = audios.length > 0 ? Object.keys(audios[0]) : [];

  return (
    <div>
      <h2>Recommendations</h2>
      {audios.length > 0 ? (
        <table border="1" style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              {fields.map((field) => (
                <th key={field} style={{ padding: "8px", textAlign: "left" }}>
                  {field}
                </th>
              ))}
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {audios.map((audio, index) => (
              <tr key={index}>
                {fields.map((field) => (
                  <td key={field} style={{ padding: "8px" }}>
                    {audio[field]}
                  </td>
                ))}
                <td style={{ padding: "8px" }}>
                  <button onClick={() => onSelect(audio)}>Select</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No recommendations available.</p>
      )}
    </div>
  );
}

export default AudioList;

