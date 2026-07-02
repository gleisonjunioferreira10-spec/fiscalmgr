# Site institucional — MGR Atacado e Varejo

Site simples (HTML/CSS/JS puro, sem build) para apresentar a empresa MGR Atacado e Varejo.
É independente do sistema fiscal (`backend/` e `frontend/`) deste repositório.

## Páginas

- `index.html` — Início (apresentação, diferenciais, chamadas para as outras páginas)
- `historia.html` — Nossa História (como a empresa começou, missão/visão/valores, trajetória)
- `parceiros.html` — Parceiros (fornecedores/marcas parceiras)
- `produtos.html` — Produtos (categorias de produtos)
- `contato.html` — Contato (WhatsApp, telefone, e-mail, endereço e formulário)

Todas as páginas compartilham o mesmo cabeçalho (menu) e rodapé, definidos em cada arquivo HTML
e estilizados por `assets/styles.css`.

## Ver o site localmente

Abra o arquivo `index.html` diretamente no navegador, ou rode um servidor simples:

```bash
cd site
python3 -m http.server 8080
```

Depois acesse http://localhost:8080

## O que personalizar antes de publicar

1. **Contato** (em todas as páginas, botão flutuante do WhatsApp, e em `contato.html`):
   - Troque `55SEUNUMEROAQUI` pelo número de WhatsApp real, no formato `55DDDNUMERO` (ex: `5511999999999`).
   - Ajuste telefone, e-mail, endereço e horário de atendimento.
2. **Nossa História** (`historia.html`): troque os textos de "Como tudo começou", missão/visão/valores
   e a linha do tempo pela história real da empresa (fundação, marcos importantes, etc.).
3. **Parceiros** (`parceiros.html`): troque os blocos "Parceiro 1, 2, 3..." pelos nomes reais e,
   se tiver as logos, troque o texto "Logo" dentro de `.parceiro__logo` por uma tag `<img>`.
4. **Produtos** (`produtos.html`): troque "Categoria 1/2/3/4" pelas categorias reais de produtos.
5. **Formulário de contato**: hoje ele só mostra um aviso ao enviar — ainda não envia e-mail nem WhatsApp.
   Para funcionar de verdade, ligue-o a um serviço como Formspree, EmailJS, ou um endpoint próprio.
6. **Logo/cores**: as cores estão em `assets/styles.css` (`:root`, variáveis `--azul` e `--laranja`).
   Se a empresa tiver uma logo em imagem, adicione o arquivo em `assets/` e troque o texto do `.logo`
   (presente no `<header>` de cada página) por uma tag `<img>`.

## Adicionar uma nova página/aba

1. Copie um dos arquivos HTML existentes como modelo (cabeçalho, rodapé e botão do WhatsApp são iguais em todos).
2. Adicione um link para a nova página no `<nav id="nav">` de **todas** as páginas.
3. Marque o link da página atual com a classe `nav__link--ativo` em cada arquivo.

## Publicar o site

Por ser estático, pode ser publicado gratuitamente em:

- **GitHub Pages**: em Settings > Pages do repositório, aponte para a pasta `site/` (ou publique-a em um repositório próprio).
- **Netlify / Vercel**: importe o repositório e configure a pasta `site/` como raiz de publicação.
