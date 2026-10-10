/* Comportamento do site: busca, filtros, ficha do produto e WhatsApp.
   O número sai de js/config.js. Enquanto estiver vazio, nenhum botão
   abre conversa — todos explicam que o contato ainda não foi informado. */

(function () {
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => [...(root || document).querySelectorAll(sel)];

  const number = (window.GUSPHONE.whatsapp || "").replace(/\D/g, "");
  const hasNumber = number.length >= 10;

  const grade = $("#grade");
  const vazio = $("#vazio");
  const busca = $("#busca");
  const aviso = $("#aviso");
  const ficha = $("#ficha");

  let filtro = "todos";
  let foco = "";
  let toastTimer = 0;
  let ultimoFoco = null;

  /* ---------- WhatsApp ---------- */

  function linkWhatsApp(texto) {
    return "https://wa.me/" + number + "?text=" + encodeURIComponent(texto);
  }

  function avisar(mensagem) {
    aviso.textContent = mensagem;
    aviso.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (aviso.hidden = true), 4200);
  }

  function mensagemDe(nome) {
    return "Olá! Gostaria de consultar a disponibilidade do " + nome + ".";
  }

  /** Liga um controle ao WhatsApp, ou explica por que ainda não abre. */
  function ligarConsulta(el, texto) {
    if (hasNumber) {
      el.href = linkWhatsApp(texto);
      el.target = "_blank";
      el.rel = "noopener";
      return;
    }
    el.setAttribute("aria-disabled", "true");
    el.addEventListener("click", (ev) => {
      ev.preventDefault();
      avisar(
        "O WhatsApp da loja ainda não foi cadastrado. Assim que o número oficial for confirmado, este botão abre a conversa."
      );
    });
  }

  /* ---------- grade de produtos ---------- */

  function cartao(item) {
    const li = document.createElement("li");
    li.className = "card";
    li.dataset.name = (item.brand + " " + item.name).toLowerCase();
    li.dataset.category = item.category;
    li.dataset.focus = item.focus.join(" ");

    const meta = [item.storage, item.condition].filter(Boolean).join(" · ");

    li.innerHTML =
      '<div class="card__photo"><img src="' + item.image + '" alt="' + item.alt + '"></div>' +
      '<p class="card__brand">' + item.brand + "</p>" +
      "<h3>" + item.name + "</h3>" +
      '<p class="card__meta">' + meta + "</p>" +
      '<a class="btn btn--primary" href="#ficha">Consultar disponibilidade</a>';

    $("a", li).addEventListener("click", (ev) => {
      ev.preventDefault();
      abrirFicha(item);
    });
    return li;
  }

  window.CATALOG.forEach((item) => grade.appendChild(cartao(item)));

  const temDemo = window.CATALOG.some((item) => item.demo);
  $("#aviso-demo").hidden = !temDemo;

  /* ---------- acessórios ---------- */

  const listaAcessorios = $("#acessorios-lista");
  window.ACCESSORIES.forEach((item) => {
    const li = document.createElement("li");
    li.className = "acc";
    li.id = "acc-" + item.id;
    li.innerHTML =
      '<img src="' + item.image + '" alt="' + item.alt + '">' +
      "<div><h3>" + item.name + "</h3><p>" + item.text + "</p>" +
      '<a class="link" href="#contato">Consultar disponibilidade</a></div>';
    ligarConsulta($("a", li), mensagemDe(item.name.toLowerCase()));
    listaAcessorios.appendChild(li);
  });

  /* ---------- serviços ---------- */

  const listaServicos = $("#servicos");
  window.SERVICES.forEach((servico) => {
    const li = document.createElement("li");
    li.innerHTML =
      '<svg viewBox="0 0 24 24" aria-hidden="true">' +
      window.ICONS[servico.icon] + "</svg>" +
      "<strong>" + servico.name + "</strong><span>" + servico.text + "</span>";
    listaServicos.appendChild(li);
  });

  ligarConsulta(
    $("#cta-assistencia"),
    "Olá! Gostaria de uma avaliação técnica do meu aparelho."
  );
  ligarConsulta($("#atalho-whatsapp"), "Olá! Gostaria de falar com a GusPhone.");

  /* ---------- busca e filtros ---------- */

  function normaliza(texto) {
    return texto
      .toLowerCase()
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "");
  }

  function aplica() {
    const termo = normaliza(busca.value.trim());
    let visiveis = 0;
    $$(".card", grade).forEach((card) => {
      const casaCategoria = filtro === "todos" || card.dataset.category === filtro;
      const casaFoco = !foco || card.dataset.focus.split(" ").includes(foco);
      const casaBusca = !termo || normaliza(card.dataset.name).includes(termo);
      const mostra = casaCategoria && casaFoco && casaBusca;
      card.hidden = !mostra;
      if (mostra) visiveis += 1;
    });
    vazio.hidden = visiveis > 0;
    $$(".nav a[data-filter]").forEach((link) => {
      link.setAttribute("aria-current", link.dataset.filter === filtro ? "true" : "false");
    });
  }

  function defineFiltro(valor) {
    filtro = valor;
    foco = "";
    $$(".filters button").forEach((botao) => {
      botao.setAttribute("aria-pressed", botao.dataset.filter === valor ? "true" : "false");
    });
    aplica();
  }

  $$(".filters button").forEach((botao) => {
    botao.addEventListener("click", () => defineFiltro(botao.dataset.filter));
  });

  document.addEventListener("click", (ev) => {
    const alvo = ev.target.closest("[data-filter], [data-focus], [data-item]");
    if (!alvo || alvo.closest(".filters")) return;
    if (alvo.dataset.filter) defineFiltro(alvo.dataset.filter);
    if (alvo.dataset.focus) {
      filtro = "todos";
      foco = alvo.dataset.focus;
      $$(".filters button").forEach((botao) => {
        botao.setAttribute("aria-pressed", botao.dataset.filter === "todos" ? "true" : "false");
      });
      aplica();
    }
    if (alvo.dataset.item) {
      const item = $("#acc-" + alvo.dataset.item);
      if (!item) return;
      $$(".acc").forEach((el) => el.classList.remove("is-target"));
      item.classList.add("is-target");
    }
    const menu = $("#menu");
    if (menu.classList.contains("is-open")) fechaMenu();
  });

  busca.addEventListener("input", aplica);
  $("#busca-form").addEventListener("submit", (ev) => {
    ev.preventDefault();
    $("#smartphones").scrollIntoView();
    aplica();
  });
  $("#limpar-busca").addEventListener("click", () => {
    busca.value = "";
    foco = "";
    defineFiltro("todos");
    busca.focus();
  });

  /* ---------- ficha do produto ---------- */

  function linha(rotulo, valor) {
    return "<div><dt>" + rotulo + "</dt><dd>" + valor + "</dd></div>";
  }

  function abrirFicha(item) {
    ultimoFoco = document.activeElement;
    $("#ficha-foto").src = item.image;
    $("#ficha-foto").alt = item.alt;
    $("#ficha-marca").textContent = item.brand;
    $("#ficha-nome").textContent = item.name;

    const dados = [];
    if (item.storage) dados.push(linha("Armazenamento", item.storage));
    if (item.condition) dados.push(linha("Condição", item.condition));
    if (item.color) dados.push(linha("Cor", item.color));
    dados.push(linha("Preço", "Consulte a disponibilidade"));
    $("#ficha-dados").innerHTML = dados.join("");
    $("#ficha-aviso").hidden = !item.demo;

    ligarConsulta($("#ficha-consulta"), mensagemDe(item.name));
    ficha.hidden = false;
    document.body.style.overflow = "hidden";
    $("#ficha-fechar").focus();
  }

  function fecharFicha() {
    ficha.hidden = true;
    document.body.style.overflow = "";
    if (ultimoFoco) ultimoFoco.focus();
  }

  $("#ficha-fechar").addEventListener("click", fecharFicha);
  ficha.addEventListener("click", (ev) => {
    if (ev.target === ficha) fecharFicha();
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && !ficha.hidden) fecharFicha();
  });

  /* ---------- menu compacto ---------- */

  const alterna = $(".nav-toggle");
  function fechaMenu() {
    $("#menu").classList.remove("is-open");
    alterna.setAttribute("aria-expanded", "false");
    $(".sr", alterna).textContent = "Abrir menu";
  }
  alterna.addEventListener("click", () => {
    const aberto = alterna.getAttribute("aria-expanded") === "true";
    $("#menu").classList.toggle("is-open", !aberto);
    alterna.setAttribute("aria-expanded", String(!aberto));
    $(".sr", alterna).textContent = aberto ? "Abrir menu" : "Fechar menu";
  });

  /* ---------- dados confirmados da empresa ---------- */

  const empresa = window.GUSPHONE;

  if (hasNumber) {
    const visivel = numeroVisivel(number);
    $("#contato-whatsapp").innerHTML =
      '<a href="' + linkWhatsApp("Olá! Gostaria de falar com a GusPhone.") +
      '" target="_blank" rel="noopener">' + visivel + "</a>";
    $("#rodape-whatsapp").textContent = "WhatsApp: " + visivel;
    const flutuante = $("#flutuante");
    flutuante.hidden = false;
    ligarConsulta(flutuante, "Olá! Gostaria de falar com a GusPhone.");
  }

  if (empresa.address) {
    $("#contato-endereco").textContent = empresa.address;
    $("#rodape-endereco").textContent = "Endereço: " + empresa.address;
  }
  if (empresa.hours) {
    $("#contato-horario").textContent = empresa.hours;
    $("#rodape-horario").textContent = "Horário: " + empresa.hours;
  }
  if (empresa.socials && empresa.socials.length) {
    const redes = $("#redes");
    redes.hidden = false;
    redes.innerHTML = empresa.socials
      .map((rede) => '<a href="' + rede.url + '" target="_blank" rel="noopener">' + rede.name + "</a>")
      .join(" · ");
  }

  /* O logotipo original substitui o nome em texto quando o arquivo existe. */
  const logo = $(".brand__logo");
  logo.addEventListener("load", () => document.body.classList.add("has-logo"));
  logo.addEventListener("error", () => logo.remove());

  function numeroVisivel(digitos) {
    if (digitos.length < 12) return "+" + digitos;
    return (
      "+" + digitos.slice(0, 2) + " " +
      digitos.slice(2, 4) + " " +
      digitos.slice(4, 9) + "-" + digitos.slice(9)
    );
  }

  aplica();
})();
