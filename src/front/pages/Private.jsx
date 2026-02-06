import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Private() {
  const [email, setEmail] = useState(null)
  const navigate = useNavigate();
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
  const validateToken = async (token) => {
    if (!token) {
      console.log("Token not found")
      return
    }
    const response = await fetch(BACKEND_URL + "/token", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      }
    })
    if (!response.ok) {
      console.log("User was not found")
      return
    }
    const data = await response.json()
    setEmail(data.email)
    return data
  }
  useEffect(() => {
    const token = sessionStorage.getItem("token");
    validateToken(token)
  }, []);

  return (
    <div>
      <h1>Private Dashboard 🔐</h1>
      <h3>{email ? `Welcome ${email}`:"You must be logged in to see this page"}</h3>
      </div>
  );
}