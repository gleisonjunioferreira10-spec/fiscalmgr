import { Route, Routes, Link } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Produtos from "./pages/Produtos";

export default function App() {
  return (
    <div>
      <nav>
        <Link to="/">Dashboard</Link> | <Link to="/produtos">Produtos</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/produtos" element={<Produtos />} />
      </Routes>
    </div>
  );
}
