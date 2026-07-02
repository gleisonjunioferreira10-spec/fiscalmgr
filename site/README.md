# Site institucional — MGR Atacado e Varejo

Site simples (HTML/CSS/JS puro, sem build) para apresentar a empresa MGR Atacado e Varejo.
É independente do sistema fiscal (`backend/` e `frontend/`) deste repositório.

## Ver o site localmente

Abra o arquivo `index.html` diretamente no navegador, ou rode um servidor simples:

```bash
cd site
python3 -m http.server 8080
```

Depois acesse http://localhost:8080

## O que personalizar antes de publicar

1. **Contato** (`index.html`, seção `#contato` e botão flutuante do WhatsApp):
   - Troque `55SEUNUMEROAQUI` pelo número de WhatsApp real, no formato `55DDDNUMERO` (ex: `5511999999999`).
   - Ajuste telefone, e-mail, endereço e horário de atendimento.
2. **Produtos** (`index.html`, seção `#produtos`): troque "Categoria 1/2/3" pelas categorias reais de produtos.
3. **Sobre** (`index.html`, seção `#sobre`): ajuste o texto com a história real da empresa.
4. **Formulário de contato**: hoje ele só mostra um aviso ao enviar — ainda não envia e-mail nem WhatsApp.
   Para funcionar de verdade, ligue-o a um serviço como Formspree, EmailJS, ou um endpoint próprio.
5. **Logo/cores**: as cores estão em `assets/styles.css` (`:root`, variáveis `--azul` e `--laranja`).
   Se a empresa tiver uma logo em imagem, adicione o arquivo em `assets/` e troque o texto do `.logo` no `index.html` por uma tag `<img>`.

## Publicar o site

Por ser estático, pode ser publicado gratuitamente em:

- **GitHub Pages**: em Settings > Pages do repositório, aponte para a pasta `site/` (ou publique-a em um repositório próprio).
- **Netlify / Vercel**: importe o repositório e configure a pasta `site/` como raiz de publicação.
