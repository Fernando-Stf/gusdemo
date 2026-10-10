/* Ícones de traço único, 24px, sem preenchimento. Um peso só em todo o site. */
window.ICONS = {
  phone:
    '<rect x="8" y="3" width="8" height="18" rx="2"/><path d="M11 18.5h2"/>',
  case:
    '<rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M10 6h4"/>',
  audio:
    '<path d="M4.5 13.5v-2a7.5 7.5 0 0 1 15 0v2"/><rect x="3.5" y="13" width="3.5" height="6" rx="1.2"/><rect x="17" y="13" width="3.5" height="6" rx="1.2"/>',
  plug:
    '<path d="M8 8V3.5M16 8V3.5"/><path d="M6.5 8h11v4.5a5.5 5.5 0 0 1-11 0V8Z"/><path d="M12 18v3"/>',
  wrench:
    '<path d="M14.7 6.3a3.4 3.4 0 0 0-4.6 4.4L4.5 16.3 7.7 19.5l5.6-5.6a3.4 3.4 0 0 0 4.4-4.6L15.5 11.5 12.5 8.5l2.2-2.2Z"/>',
  search:
    '<circle cx="11" cy="11" r="6"/><path d="M15.8 15.8 20 20"/>',
  display:
    '<rect x="4" y="3.5" width="16" height="13" rx="1.5"/><path d="M9 20.5h6M12 16.5v4"/>',
  battery:
    '<rect x="3.5" y="7.5" width="15" height="9" rx="1.5"/><path d="M18.5 10.5H20a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1h-1.5"/><path d="M6.5 12h4"/>',
  person:
    '<circle cx="12" cy="8" r="3.2"/><path d="M5.5 19.5a6.5 6.5 0 0 1 13 0"/>',
  compare:
    '<path d="M5 19V5M5 19h14"/><path d="M9 15V9.5M13 15V7M17 15v-3"/>',
  chat:
    '<path d="M5 16.5 4 20l3.6-1A8 8 0 1 0 5 16.5Z"/>',
};

document.querySelectorAll("[data-ico]").forEach((slot) => {
  const shape = window.ICONS[slot.dataset.ico];
  if (!shape) return;
  slot.innerHTML =
    '<svg viewBox="0 0 24 24" aria-hidden="true">' + shape + "</svg>";
});
