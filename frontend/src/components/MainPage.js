import React, { useState } from "react";
import OptionsSelector from "./OptionsSelector";
import AudioList from "./AudioList";
import AudioPlayer from "./AudioPlayer";
import "./MainPage.css"; // Import the CSS file for styling

function MainPage() {
  const [selectedOption, setSelectedOption] = useState(null);
  const [dropdownOptions, setDropdownOptions] = useState([]);
  const [selectedDropdownValue, setSelectedDropdownValue] = useState("");
  const [audioList, setAudioList] = useState([]);
  const [selectedAudio, setSelectedAudio] = useState(null);

  // Function to handle the option selection
  const handleOptionSelect = (option) => {
    setSelectedOption(option);
    setAudioList([]);
    setSelectedAudio(null);
    setSelectedDropdownValue("");

    // Update dropdown options based on selected option
    if (option === "Search by raag") {
      setDropdownOptions(["Yaman", "Todi", "Bhimpalasi"]);
    } else if (option === "Search by artist") {
      setDropdownOptions(["Ajoy Chakraborty", "Kaushiki Chakraborty", "Buddhadev Dasgupta"]);
    }
  };

  // Function to handle dropdown selection
  const handleDropdownSelect = (value) => {
    setSelectedDropdownValue(value);

    // Replace this with the actual function to fetch audio list based on the dropdown value
    const fetchAudioList = (dropdownValue) => {
        if (dropdownValue === "Yaman") return ["/audios/JVKE-golden-hour-Karaoke-Version.mp3", "/audios/drone_sample_2.mp3"];
        if (dropdownValue === "Ajoy Chakraborty") return ["/audios/drone_sample_2.mp3", "/audios/JVKE-golden-hour-Karaoke-Version.mp3"];
        return ["/audios/Default-Song-1.mp3", "/audios/Default-Song-2.mp3"];
      };

    const audios = fetchAudioList(value);
    setAudioList(audios);
  };

  // Function to handle audio selection
  const handleAudioSelect = (audio) => {
    setSelectedAudio(audio);
    // Fetch a new list of recommendations based on selected audio
    const fetchNewAudioList = (selectedAudio) => {
      return ["Related Audio 1", "Related Audio 2"];
    };
    setAudioList(fetchNewAudioList(audio));
  };

  return (
    <div className="App">
      <h1 className="header">Hindustani Classical Music Recommender</h1>
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
