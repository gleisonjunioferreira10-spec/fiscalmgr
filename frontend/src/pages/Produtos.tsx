import { ChangeEvent, useEffect, useRef, useState } from "react";

import { api } from "../services/api";

interface Produto {
  id: string;
  sku: string;
  descricao: string;
  ncm: string | null;
  cadastro_completo: boolean;
}

interface ErroImportacao {
  linha: number;
  mensagem: string;
}

interface ResultadoImportacao {
  criados: number;
  atualizados: number;
  erros: ErroImportacao[];
}

export default function Produtos() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [resultado, setResultado] = useState<ResultadoImportacao | null>(null);
  const [importando, setImportando] = useState(false);
  const [erroImportacao, setErroImportacao] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  function carregarProdutos() {
    api.get<Produto[]>("/produtos").then((res) => setProdutos(res.data));
  }

  useEffect(() => {
    carregarProdutos();
  }, []);

  async function handleImportar(event: ChangeEvent<HTMLInputElement>) {
    const arquivo = event.target.files?.[0];
    if (!arquivo) return;

    setImportando(true);
    setErroImportacao(null);
    setResultado(null);

    const formData = new FormData();
    formData.append("arquivo", arquivo);

    try {
      const { data } = await api.post<ResultadoImportacao>("/produtos/importar", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResultado(data);
      carregarProdutos();
    } catch {
      setErroImportacao("Não foi possível importar o arquivo. Verifique o formato do CSV.");
    } finally {
      setImportando(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  }

  return (
    <div>
      <h1>Cadastro de Produtos</h1>

      <section>
        <h2>Importar produtos em lote (CSV)</h2>
        <p>Colunas: sku, descricao, ncm, cest, cst_icms, cst_pis, cst_cofins, cfop_padrao, preco_custo, preco_venda</p>
        <input ref={inputRef} type="file" accept=".csv" onChange={handleImportar} disabled={importando} />
        {importando && <p>Importando...</p>}
        {erroImportacao && <p role="alert">{erroImportacao}</p>}
        {resultado && (
          <div>
            <p>
              Criados: {resultado.criados} | Atualizados: {resultado.atualizados} | Erros: {resultado.erros.length}
            </p>
            {resultado.erros.length > 0 && (
              <ul>
                {resultado.erros.map((erro) => (
                  <li key={erro.linha}>Linha {erro.linha}: {erro.mensagem}</li>
                ))}
              </ul>
            )}
          </div>
        )}
      </section>

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
