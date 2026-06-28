import { useEffect, useState } from "react";

import { api } from "../services/api";

interface Produto {
  id: string;
  sku: string;
  descricao: string;
  ncm: string | null;
  cadastro_completo: boolean;
}

export default function Produtos() {
  const [produtos, setProdutos] = useState<Produto[]>([]);

  useEffect(() => {
    const empresaId = localStorage.getItem("empresa_id");
    if (!empresaId) return;
    api.get<Produto[]>("/produtos", { params: { empresa_id: empresaId } })
      .then((res) => setProdutos(res.data));
  }, []);

  return (
    <div>
      <h1>Cadastro de Produtos</h1>
      <table>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Descrição</th>
            <th>NCM</th>
            <th>Cadastro completo</th>
          </tr>
        </thead>
        <tbody>
          {produtos.map((produto) => (
            <tr key={produto.id}>
              <td>{produto.sku}</td>
              <td>{produto.descricao}</td>
              <td>{produto.ncm ?? "-"}</td>
              <td>{produto.cadastro_completo ? "Sim" : "Não"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
