import { Route, Routes, Link, useNavigate } from "react-router-dom";

import RotaProtegida from "./components/RotaProtegida";
import { useAuth } from "./hooks/AuthContext";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Produtos from "./pages/Produtos";
import Registro from "./pages/Registro";

export default function App() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div>
      <nav>
        {isAuthenticated ? (
          <>
            <Link to="/">Dashboard</Link> | <Link to="/produtos">Produtos</Link> |{" "}
            <button onClick={handleLogout}>Sair</button>
          </>
        ) : (
          <>
            <Link to="/login">Entrar</Link> | <Link to="/registro">Cadastrar empresa</Link>
          </>
        )}
      </nav>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route element={<RotaProtegida />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/produtos" element={<Produtos />} />
        </Route>
      </Routes>
    </div>
  );
}
