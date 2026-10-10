# GusPhone — Site institucional e e-commerce

Site profissional para GusPhone — loja de smartphones, produtos Apple e assistência técnica.

## Estrutura

```
pj4/
├── index.html           # Página principal
├── privacidade.html     # Política de privacidade
├── vercel.json          # Configuração de deploy na Vercel
├── PRODUCT.md           # Documento de produto (Impeccable)
├── .impeccable/         # Configurações de design (Impeccable)
│   ├── surfaces/index.md
│   └── ...
├── css/
│   └── styles.css       # Estilos
├── js/
│   ├── config.js        # Dados da empresa (WhatsApp, endereço, redes)
│   ├── catalog.js       # Catálogo de produtos e serviços
│   ├── icons.js         # Ícones SVG inline
│   └── main.js          # Comportamento do site
└── assets/
    ├── logo.png         # Logotipo da marca (substituir quando disponível)
    ├── favicon.svg      # Ícone da aba
    ├── phones/          # Fotos de smartphones
    └── accessories/     # Fotos de acessórios
```

## Configuração

1. **WhatsApp**: edite `js/config.js` e preencha o número oficial da loja:
   ```js
   window.GUSPHONE = {
     whatsapp: "5511999990000",  // DDI + DDD + número, sem pontuação
     address: "Endereço completo",
     hours: "Seg-Sex: 9h-19h",
     socials: [{name: "Instagram", url: "https://..."}]
   };
   ```

2. **Catálogo**: edite `js/catalog.js` para adicionar produtos reais. Retire `demo: true` quando os dados forem confirmados.

3. **Logotipo**: coloque `logo.png` em `assets/`.

## Imagens

As fotos de smartphones e da bancada técnica devem ser adicionadas manualmente:

```bash
# Plano A: gerar com Gemini (requires API key)
python assets/generate_phone_assets.py

# Plano B: copiar fotos reais para:
assets/phones/
├── iphone-16-pro.png
├── iphone-16.png
├── iphone-15.png
├── galaxy-s25-ultra.png
├── galaxy-s25.png
├── galaxy-a56.png
├── pixel-9-pro.png
├── xiaomi-15.png
├── moto-edge-50-pro.png
├── hero-phones.png
└── bench.png

assets/accessories/
├── cases.png
├── glass.png
├── chargers.png
├── cables.png
└── earbuds.png
```

## Deploy local

```bash
python -m http.server 8000
open http://localhost:8000
```

## Deploy na Vercel

```bash
vercel
```

## Semântica e acessibilidade

- Títulos em h2/h3 para seções e cards.
- Botões com `aria-pressed` para filtros.
- Modal com `role="dialog"` e `aria-modal`.
- Navegação com `aria-label` e `aria-current`.
- Imagens com `alt` descritivo.
- Foco visível (`:focus-visible`).

## Notas técnicas

- CSS moderno com variáveis CSS e Grid/Flexbox.
- Sem dependências externas (exceto fontes do Google Fonts).
- JavaScript vanilla (sem framework).
- Página única, navegação por scroll e âncoras.
- WhatsApp como canal de conversão principal.
