import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";
import DatasetsPage from "./pages/DatasetsPage.jsx";

export default function App() {
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState("");

  const handleLogin = (accessToken, user) => {
    setToken(accessToken);
    setUsername(user);
  };

  const handleLogout = () => {
    setToken(null);
    setUsername("");
  };

  return (
    <BrowserRouter>
      <Routes>
        {!token ? (
          <>
            <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="*" element={<Navigate to="/login" />} />
          </>
        ) : (
          <>
            <Route path="/datasets" element={<DatasetsPage token={token} username={username} onLogout={handleLogout} />} />
            <Route path="*" element={<Navigate to="/datasets" />} />
          </>
        )}
      </Routes>
    </BrowserRouter>
  );
}
