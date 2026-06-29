import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/AuthContext";

export default function Registro() {
  const { registrar } = useAuth();
  const navigate = useNavigate();
  const [nomeEmpresa, setNomeEmpresa] = useState("");
  const [cnpj, setCnpj] = useState("");
  const [nomeUsuario, setNomeUsuario] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setErro(null);
    try {
      await registrar({
        empresa: { nome: nomeEmpresa, cnpj },
        nome_usuario: nomeUsuario,
        email,
        senha,
      });
      navigate("/");
    } catch {
      setErro("Não foi possível cadastrar. Verifique os dados informados.");
    }
  }

  return (
    <div>
      <h1>Cadastrar empresa — Gerente Fiscal</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Nome da empresa
            <input value={nomeEmpresa} onChange={(e) => setNomeEmpresa(e.target.value)} required />
          </label>
        </div>
        <div>
          <label>
            CNPJ
            <input value={cnpj} onChange={(e) => setCnpj(e.target.value)} required />
          </label>
        </div>
        <div>
          <label>
            Seu nome
            <input value={nomeUsuario} onChange={(e) => setNomeUsuario(e.target.value)} required />
          </label>
        </div>
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
        <button type="submit">Cadastrar</button>
      </form>
      <p>
        Já tem conta? <Link to="/login">Entrar</Link>
      </p>
    </div>
  );
}
