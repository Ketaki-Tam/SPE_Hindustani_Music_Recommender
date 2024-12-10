import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginSignup.css"; // import the CSS file for styling

const LoginSignup = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate(); // Hook for navigation

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


  return (
    <div className="login-signup-wrapper">
      <h1>Hindustani Classical Music Recommender</h1>
      <div className="login-signup-container">
        <div className="card">
          <h2>{isLogin ? "Login" : "Signup"}</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <button type="submit" className="primary-button">
                {isLogin ? "Login" : "Signup"}
              </button>
            </div>
          </form>
          <button className="secondary-button" onClick={() => setIsLogin(!isLogin)}>
            Switch to {isLogin ? "Signup" : "Login"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginSignup;
