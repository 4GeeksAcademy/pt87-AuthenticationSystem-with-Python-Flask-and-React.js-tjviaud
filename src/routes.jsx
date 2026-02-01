import { BrowserRouter, Routes, Route } from "react-router-dom";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Private from "./pages/Private";

export const RoutesLayout = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/signup" element={<Signup />} />
      <Route path="/login" element={<Login />} />
      <Route path="/private" element={<Private />} />
    </Routes>
  </BrowserRouter>
);