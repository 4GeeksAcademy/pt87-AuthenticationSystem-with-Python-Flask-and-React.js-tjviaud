import { useNavigate } from "react-router-dom";

export default function LogoutButton() {
  const navigate = useNavigate();

  return (
    <button onClick={() => {
      sessionStorage.removeItem("token");
      navigate("/login");
    }}>
      Logout
    </button>
  );
}