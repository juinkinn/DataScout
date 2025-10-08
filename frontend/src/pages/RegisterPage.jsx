import { useState } from "react";
import { register } from "../api/client";
import { Link, useNavigate } from "react-router-dom";

export default function RegisterPage() {
  const [username,setUsername]=useState("");
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");
  const [toast,setToast]=useState({msg:"",type:"success"});
  const navigate = useNavigate();

  const handleSubmit = async e=>{
    e.preventDefault();
    try{
      await register(username,password,email);
      setToast({msg:"Registration successful!",type:"success"});
      setTimeout(()=>navigate("/login"),1000);
    } catch(err){
      setToast({msg: err.response?.data?.detail||err.message,type:"error"});
    }
  }

  return (
    <div className="container">
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input type="email" placeholder="Email (optional)" value={email} onChange={e=>setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button type="submit">Register</button>
      </form>
      <p style={{marginTop:'12px'}}>
        Already have account? <Link to="/login">Login</Link>
      </p>
      {toast.msg && <div className={`toast ${toast.type}`}>{toast.msg}</div>}
    </div>
  );
}
