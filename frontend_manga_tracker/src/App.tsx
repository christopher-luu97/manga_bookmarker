import "./App.css";
import "./assets/fonts/fonts.css";
import { Header } from "./components/Header";
import { Footer } from "./components/Footer";
import { ApplicationContent } from "./components/ApplicationContent";
import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/login/Login";
import Register from "./components/login/Register";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  useEffect(() => {
    // Check local storage or session storage for an existing token
    // and update isAuthenticated state accordingly
    const token = localStorage.getItem("token");
    console.log(token);
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLoginSuccess = (token: string) => {
    localStorage.setItem("token", token); // Store the token in local storage
    setIsAuthenticated(true);
  };

  const handleRegisterSuccess = () => {
    // Redirect to login page or directly log in the user
    setIsAuthenticated(true); // If directly logging in the user after registration
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
  };

  return (
    <BrowserRouter>
      <div className="App">
        <Header isAuthenticated={isAuthenticated} onLogout={handleLogout} />
        <Routes>
          <Route
            path="/login"
            element={
              !isAuthenticated ? (
                <Login onLoginSuccess={handleLoginSuccess} />
              ) : (
                <Navigate to="/" />
              )
            }
          />
          <Route
            path="/register"
            element={
              !isAuthenticated ? (
                <Register onRegisterSuccess={handleRegisterSuccess} />
              ) : (
                <Navigate to="/" />
              )
            }
          />
          <Route
            path="/"
            element={
              isAuthenticated ? (
                <ApplicationContent />
              ) : (
                <Navigate to="/login" />
              )
            }
          />
        </Routes>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
