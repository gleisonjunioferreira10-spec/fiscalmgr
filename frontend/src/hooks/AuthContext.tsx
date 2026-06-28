import { createContext, useContext, useState, ReactNode } from "react";

import { api, TOKEN_STORAGE_KEY } from "../services/api";

interface RegistroPayload {
  empresa: { nome: string; cnpj: string };
  nome_usuario: string;
  email: string;
  senha: string;
}

interface AuthContextValue {
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, senha: string) => Promise<void>;
  registrar: (payload: RegistroPayload) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem(TOKEN_STORAGE_KEY));

  function salvarToken(novoToken: string) {
    localStorage.setItem(TOKEN_STORAGE_KEY, novoToken);
    setToken(novoToken);
  }

  async function login(email: string, senha: string) {
    const { data } = await api.post<{ access_token: string }>("/auth/login", { email, senha });
    salvarToken(data.access_token);
  }

  async function registrar(payload: RegistroPayload) {
    const { data } = await api.post<{ access_token: string }>("/auth/registro", payload);
    salvarToken(data.access_token);
  }

  function logout() {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    setToken(null);
  }

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: !!token, login, registrar, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth deve ser usado dentro de AuthProvider");
  return context;
}
