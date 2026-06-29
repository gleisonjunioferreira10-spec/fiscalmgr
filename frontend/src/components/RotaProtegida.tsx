import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "../hooks/AuthContext";

export default function RotaProtegida() {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
}
