/**
 * Catálogo demonstrativo.
 *
 * Os modelos existem no mercado, mas NADA aqui foi confirmado como
 * estoque da GusPhone: sem preço, sem quantidade, sem garantia, sem
 * avaliação. `demo: true` marca cada item para o aviso visível no site.
 * Quando o catálogo real chegar, substitua este arquivo e remova `demo`.
 *
 * category: iphone | samsung | android
 * focus: desempenho | fotografia | custo
 * storage e condition só aparecem quando preenchidos.
 */
window.CATALOG = [
  {
    id: "iphone-16-pro",
    name: "iPhone 16 Pro",
    brand: "Apple",
    category: "iphone",
    focus: ["desempenho", "fotografia"],
    storage: "256 GB",
    condition: "Novo",
    color: "Titânio natural",
    image: "assets/phones/iphone-16-pro.png",
    alt: "iPhone 16 Pro em titânio natural, visto de frente, tela acesa com o relógio",
    demo: true,
  },
  {
    id: "iphone-16",
    name: "iPhone 16",
    brand: "Apple",
    category: "iphone",
    focus: ["fotografia", "custo"],
    storage: "128 GB",
    condition: "Novo",
    color: "Ultramarino",
    image: "assets/phones/iphone-16.png",
    alt: "iPhone 16 na cor ultramarino, visto de frente",
    demo: true,
  },
  {
    id: "iphone-15",
    name: "iPhone 15",
    brand: "Apple",
    category: "iphone",
    focus: ["custo", "fotografia"],
    storage: "128 GB",
    condition: "Seminovo",
    color: "Rosa",
    image: "assets/phones/iphone-15.png",
    alt: "iPhone 15 na cor rosa, visto de frente",
    demo: true,
  },
  {
    id: "galaxy-s25-ultra",
    name: "Galaxy S25 Ultra",
    brand: "Samsung",
    category: "samsung",
    focus: ["desempenho", "fotografia"],
    storage: "256 GB",
    condition: "Novo",
    color: "Titânio preto",
    image: "assets/phones/galaxy-s25-ultra.png",
    alt: "Samsung Galaxy S25 Ultra em titânio preto, visto de frente com a S Pen",
    demo: true,
  },
  {
    id: "galaxy-s25",
    name: "Galaxy S25",
    brand: "Samsung",
    category: "samsung",
    focus: ["fotografia", "custo"],
    storage: "256 GB",
    condition: "Novo",
    color: "Azul gelo",
    image: "assets/phones/galaxy-s25.png",
    alt: "Samsung Galaxy S25 na cor azul gelo, visto de frente",
    demo: true,
  },
  {
    id: "galaxy-a56",
    name: "Galaxy A56",
    brand: "Samsung",
    category: "samsung",
    focus: ["custo"],
    storage: "128 GB",
    condition: "Novo",
    color: "Grafite",
    image: "assets/phones/galaxy-a56.png",
    alt: "Samsung Galaxy A56 na cor grafite, visto de frente",
    demo: true,
  },
  {
    id: "pixel-9-pro",
    name: "Pixel 9 Pro",
    brand: "Google",
    category: "android",
    focus: ["fotografia", "desempenho"],
    storage: "128 GB",
    condition: "Novo",
    color: "Porcelana",
    image: "assets/phones/pixel-9-pro.png",
    alt: "Google Pixel 9 Pro na cor porcelana, visto de frente",
    demo: true,
  },
  {
    id: "xiaomi-15",
    name: "Xiaomi 15",
    brand: "Xiaomi",
    category: "android",
    focus: ["desempenho", "custo"],
    storage: "256 GB",
    condition: "Novo",
    color: "Verde",
    image: "assets/phones/xiaomi-15.png",
    alt: "Xiaomi 15 na cor verde, visto de frente",
    demo: true,
  },
  {
    id: "moto-edge-50-pro",
    name: "moto edge 50 pro",
    brand: "Motorola",
    category: "android",
    focus: ["custo", "fotografia"],
    storage: "256 GB",
    condition: "Novo",
    color: "Preto",
    image: "assets/phones/moto-edge-50-pro.png",
    alt: "Motorola moto edge 50 pro na cor preta, visto de frente",
    demo: true,
  },
];

/**
 * Acessórios demonstrativos. Mesma regra: nenhum item foi confirmado
 * como disponível na loja.
 */
window.ACCESSORIES = [
  {
    id: "capinhas",
    name: "Capinhas e proteção",
    text: "Capas para os modelos mais procurados, do transparente ao reforçado.",
    image: "assets/accessories/cases.png",
    alt: "Três capinhas de celular em silicone sobre fundo neutro",
  },
  {
    id: "peliculas",
    name: "Películas",
    text: "Película de vidro aplicada na hora, com recorte para o modelo.",
    image: "assets/accessories/glass.png",
    alt: "Película de vidro para celular ao lado de um pano de limpeza",
  },
  {
    id: "carregadores",
    name: "Carregadores",
    text: "Fontes de parede para recarga rápida, com a potência indicada no corpo.",
    image: "assets/accessories/chargers.png",
    alt: "Carregador de parede branco com cabo USB-C enrolado",
  },
  {
    id: "cabos",
    name: "Cabos",
    text: "Cabos USB-C e Lightning em comprimentos de uso diário.",
    image: "assets/accessories/cables.png",
    alt: "Cabo USB-C trançado na cor grafite, enrolado",
  },
  {
    id: "fones",
    name: "Fones de ouvido",
    text: "Fones com fio e sem fio para quem usa o celular o dia inteiro.",
    image: "assets/accessories/earbuds.png",
    alt: "Par de fones sem fio brancos dentro do estojo aberto",
  },
];

/**
 * Serviços nomeados no briefing. Nenhum prazo, peça ou garantia é
 * afirmado aqui — a avaliação acontece na conversa.
 */
window.SERVICES = [
  {
    id: "diagnostico",
    name: "Diagnóstico técnico",
    text: "Avaliação do aparelho para entender o problema antes de qualquer reparo.",
    icon: "search",
  },
  {
    id: "tela",
    name: "Reparo de tela",
    text: "Troca de tela trincada ou sem imagem, com o defeito conferido na bancada.",
    icon: "display",
  },
  {
    id: "bateria",
    name: "Substituição de bateria",
    text: "Troca da bateria quando o aparelho descarrega rápido ou desliga sozinho.",
    icon: "battery",
  },
  {
    id: "carregamento",
    name: "Problemas de carregamento",
    text: "Avaliação de conector, cabo e fonte quando o aparelho não carrega.",
    icon: "plug",
  },
];
