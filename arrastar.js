function permitirArrastar(id) {
  const personagem = document.getElementById(id);
  let offsetX = 0;
  let offsetY = 0;
  let arrastando = false;

  // Para mouse
  personagem.addEventListener("mousedown", (e) => {
    arrastando = true;
    offsetX = e.clientX - personagem.offsetLeft;
    offsetY = e.clientY - personagem.offsetTop;
  });

  document.addEventListener("mousemove", (e) => {
    if (arrastando) {
      personagem.style.left = `${e.clientX - offsetX}px`;
      personagem.style.top = `${e.clientY - offsetY}px`;
    }
  });

  document.addEventListener("mouseup", () => {
    arrastando = false;
  });

  // Para toque (celular)
  personagem.addEventListener("touchstart", (e) => {
    arrastando = true;
    const touch = e.touches[0];
    offsetX = touch.clientX - personagem.offsetLeft;
    offsetY = touch.clientY - personagem.offsetTop;
  });

  document.addEventListener("touchmove", (e) => {
    if (arrastando) {
      const touch = e.touches[0];
      personagem.style.left = `${touch.clientX - offsetX}px`;
      personagem.style.top = `${touch.clientY - offsetY}px`;
    }
  });

  document.addEventListener("touchend", () => {
    arrastando = false;
  });
}

// Ativar para os dois personagens
window.onload = () => {
  permitirArrastar("p1");
  permitirArrastar("p2");
};
