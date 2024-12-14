import React, { useState } from "react";
import PreferencesModal from "./PreferencesModal"; // Import the popup
import OptionsSelector from "./OptionsSelector";
import AudioList from "./AudioList";
import AudioPlayer from "./AudioPlayer";
import "./MainPage.css"; // Import the CSS file for styling

function MainPage() {
  const [isModalOpen, setIsModalOpen] = useState(true);
  const [selectedOption, setSelectedOption] = useState(null);
  const [dropdownOptions, setDropdownOptions] = useState([]);
  const [selectedDropdownValue, setSelectedDropdownValue] = useState("");
  const [audioList, setAudioList] = useState([]);
  const [selectedAudio, setSelectedAudio] = useState(null);

  const handlePreferencesSubmit = async (raag, artist) => {
    try {
      // Construct query parameters
      const query = new URLSearchParams({
        data: JSON.stringify({ raga_id: raag, artist_id: artist }),
      }).toString();
  
      // Send request to Django backend
      const response = await fetch(`http://192.168.49.2:32001/api/give-recs-for-new-vec/?${query}`, {
        method: "GET",
      });
  
      if (response.ok) {
        const data = await response.json();
        if (data.recommendations) {
          setAudioList(data.recommendations); // Set the audio list
          alert("Preferences saved successfully!");
        } else {
          alert("Failed to fetch audio list. Please try again.");
        }
      } else {
        alert("Failed to save preferences. Please check your input and try again.");
      }
    } catch (error) {
      console.error("Error saving preferences:", error);
      alert("An error occurred while saving preferences. Please try again.");
    }
    setIsModalOpen(false)
  };
  

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
    // setAudioList([]);
    // setSelectedAudio(null);
    // setSelectedDropdownValue("");

    if (option === "Search by raag") {
      setDropdownOptions(["Yaman", "Todi", "Bhimpalasi", "Multani", "Shree", "Jog"]);
    } else if (option === "Search by artist") {
      setDropdownOptions(["Ajoy Chakraborty", "Shahid Parvez", "Omkar Dadarkar", "Kaushiki Chakraborty Desikan"]);
    }
  };

  const handleDropdownSelect = (value) => {
    setSelectedDropdownValue(value);
  
    const fetchAudioList = async (dropdownValue) => {
      const [apiUrl, paraKey] =
        selectedOption === "Search by raag"
          ? ["http://192.168.49.2:32001/api/get-raag-rec/", "raag_name"]
          : ["http://192.168.49.2:32001/api/get-artist-rec/", "artist_name"];
  
      // Construct the query parameters
      const query = new URLSearchParams({ [paraKey]: dropdownValue }).toString();
  
      try {
        // Send GET request with query parameters
        const response = await fetch(`${apiUrl}?${query}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          console.error("Error:", errorData);
          return ["Error occurred while fetching audio. Please try again."];
        }
  
        const data = await response.json();
        return data.recommendations;
      } catch (error) {
        console.error("Error fetching audio list:", error);
        return ["Error occurred while fetching audio. Please try again."];
      }
    };
  
    // Call the fetch function and update state
    fetchAudioList(value).then((audios) => setAudioList(audios));
  };
  
    // setAudioList(["RaagArtistAudio1", "RaagArtistAudio2"])


    const handleAudioSelect = async (audio) => {
      setSelectedAudio(audio);
    
      try {
        // Construct the query parameter
        const query = new URLSearchParams({
          data: JSON.stringify(audio),
        }).toString();
    
        // Send the selected audio to the Django backend as a GET request with query parameters
        const response = await fetch(`http://192.168.49.2:32001/api/give-recs-for-chosen-vec/?${query}`, {
          method: "GET",
        });
    
        if (response.ok) {
          const data = await response.json();
          if (data.recommendations) {
            setAudioList(data.recommendations); // Set the audio list returned by the backend
          } else {
            alert("Failed to fetch related audio list. Please try again.");
          }
        } else {
          alert("Failed to fetch related audio list. Please check your input and try again.");
        }
      } catch (error) {
        console.error("Error fetching related audio list:", error);
        alert("An error occurred while fetching related audio. Please try again.");
      }
    };
    


  return (
    <div className="App">
      {isModalOpen && <PreferencesModal onSavePreferences={handlePreferencesSubmit} />}
      <h1 className="header">Hindustani Classical Music Recommender System</h1>
      <div className="top-box-container">
        <div className="left-box">
          <OptionsSelector onSelect={handleOptionSelect} />
          {selectedOption && (
            <div className="dropdown-container">
              <select
                value={selectedDropdownValue}
                onChange={(e) => handleDropdownSelect(e.target.value)}
                className="dropdown"
              >
                <option value="" disabled>
                  Select an option
                </option>
                {dropdownOptions.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
        <div className="right-box">
          {selectedAudio && <AudioPlayer audio={selectedAudio} />}
        </div>
      </div>
      <div className="bottom-box">
        <AudioList audios={audioList} onSelect={handleAudioSelect} />
      </div>
    </div>
  );
}

export default MainPage;
