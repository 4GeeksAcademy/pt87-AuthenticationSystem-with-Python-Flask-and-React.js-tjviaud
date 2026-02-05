import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch(BACKEND_URL + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    sessionStorage.setItem("token", data.token);
    navigate("/private");
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Login</h1>
      <input type="text" placeholder="Email" onChange={e => setEmail(e.target.value)} value={email} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} value={password} />
      <button>Login</button>
    </form>
  );
}