import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate instead of useHistory

const LoginSignup = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [raag, setRaag] = useState("");
  const [artist, setArtist] = useState("");
  const navigate = useNavigate(); 

  // const authenticateUser = (username, password) => {
  //   // Dummy authentication function
  //   return true; // Always returns true for now
  // };

  const authenticateUser = async (username, password) => {
    console.log("in authenticate user");
    try {
    //   const response = await fetch("http://192.168.49.2:32001/api/get-artist-rec/?artist_name=Ajoy%20Chakraborty", {
    //     method: "GET",
    //   });

      const response = await fetch("http://192.168.49.2:32001/users/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });
     

      if (response.ok) {
        const data = await response.json();
        return { authenticated: data.authenticated, message: data.message };
        // return { authenticated: true, message: data.message };
      } else {
        const errorData = await response.json();
        return { authenticated: false, message: errorData.message };
      }

    } catch (error) {
      console.error("Error during authentication:", error);
      return { authenticated: false, message: "Network error. Please try again." };
    }
  };



  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("hi")
    if (isLogin) {
      console.log("isLogin");
      const result = await authenticateUser(username, password);
      if (result.authenticated) {
        console.log("Redirecting to /main");
        navigate("/main");
        console.log("Redirection attempted"); // Redirect on successful login
      } else {
        alert(result.message);
        setUsername("");
        setPassword("");
      }
    } else {
      alert("Signup functionality is not yet integrated.");
      setIsLogin(true);
    }
  };

  return (
    <div>
      <h2>{isLogin ? "Login" : "Signup"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {!isLogin && (
          <>
            <div>
              <label>Preferred Raag:</label>
              <select value={raag} onChange={(e) => setRaag(e.target.value)} required>
                <option value="Yaman">Yaman</option>
                <option value="Todi">Todi</option>
                <option value="Bhimpalasi">Bhimpalasi</option>
              </select>
            </div>

            <div>
              <label>Preferred Artist:</label>
              <select value={artist} onChange={(e) => setArtist(e.target.value)} required>
                <option value="Ajoy Chakraborty">Ajoy Chakraborty</option>
                <option value="Kaushiki Chakraborty">Kaushiki Chakraborty</option>
                <option value="Buddhadev Dasgupta">Buddhadev Dasgupta</option>
              </select>
            </div>
          </>
        )}

        <div>
          <button type="submit">{isLogin ? "Login" : "Signup"}</button>
        </div>
      </form>
      <button onClick={() => setIsLogin(!isLogin)}>
        Switch to {isLogin ? "Signup" : "Login"}
      </button>
    </div>
  );
};

export default LoginSignup;
