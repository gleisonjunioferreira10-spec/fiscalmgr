import { useEffect, useState } from "react";

import { api } from "../services/api";

interface ResumoAuditoria {
  total_produtos: number;
  produtos_cadastro_incompleto: number;
  validacoes_por_status: Record<string, number>;
}

export default function Dashboard() {
  const [resumo, setResumo] = useState<ResumoAuditoria | null>(null);

  useEffect(() => {
    api.get<ResumoAuditoria>("/dashboard/auditoria").then((res) => setResumo(res.data));
  }, []);

  if (!resumo) return <p>Carregando dashboard fiscal...</p>;

  return (
    <div>
      <h1>Dashboard de Auditoria Fiscal</h1>
      <p>Total de produtos: {resumo.total_produtos}</p>
      <p>Produtos com cadastro incompleto: {resumo.produtos_cadastro_incompleto}</p>
      <ul>
        {Object.entries(resumo.validacoes_por_status).map(([status, total]) => (
          <li key={status}>{status}: {total}</li>
        ))}
      </ul>
    </div>
  );
}
