import React from "react";
import { Route, Routes } from "react-router-dom"; // Import Routes instead of Switch
import LoginSignup from "../components/LoginSignup";
import MainPage from "../components/MainPage"; // Assuming you already have this component

const AppRoutes = () => {
  return (
    <Routes> {/* Use Routes instead of Switch */}
      <Route path="/" element={<LoginSignup />} /> {/* Use element prop instead of component */}
      <Route path="/main" element={<MainPage />} />
    </Routes>
  );
};

export default AppRoutes;
