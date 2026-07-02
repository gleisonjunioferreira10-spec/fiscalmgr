document.getElementById("ano").textContent = new Date().getFullYear();

const menuToggle = document.getElementById("menuToggle");
const nav = document.getElementById("nav");

menuToggle.addEventListener("click", () => {
  const aberto = nav.classList.toggle("nav--aberto");
  menuToggle.setAttribute("aria-expanded", aberto ? "true" : "false");
});

nav.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    nav.classList.remove("nav--aberto");
    menuToggle.setAttribute("aria-expanded", "false");
  });
});

const form = document.getElementById("formContato");
const aviso = document.getElementById("formAviso");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  aviso.hidden = false;
});
