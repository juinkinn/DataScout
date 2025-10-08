import { useState } from "react";
import { login } from "../api/client";
import { Link } from "react-router-dom";

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [toast, setToast] = useState({ msg: "", type: "success" });

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await login(username, password);
      onLogin(res.access_token, username);
      setToast({ msg: "Login successful!", type: "success" });
    } catch(err) {
      setToast({ msg: err.response?.data?.detail || err.message, type: "error" });
    }
  };

  return (
    <div className="container">
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button type="submit">Login</button>
      </form>
      <p style={{marginTop: '12px'}}>
        Don't have account? <Link to="/register">Register</Link>
      </p>
      {toast.msg && <div className={`toast ${toast.type}`}>{toast.msg}</div>}
    </div>
  );
}
