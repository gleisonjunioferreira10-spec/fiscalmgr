import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setErro(null);
    try {
      await login(email, senha);
      navigate("/");
    } catch {
      setErro("Credenciais inválidas");
    }
  }

  return (
    <div>
      <h1>Entrar — Gerente Fiscal</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            E-mail
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </label>
        </div>
        <div>
          <label>
            Senha
            <input type="password" value={senha} onChange={(e) => setSenha(e.target.value)} required />
          </label>
        </div>
        {erro && <p role="alert">{erro}</p>}
        <button type="submit">Entrar</button>
      </form>
      <p>
        Não tem conta? <Link to="/registro">Cadastre sua empresa</Link>
      </p>
    </div>
  );
}
