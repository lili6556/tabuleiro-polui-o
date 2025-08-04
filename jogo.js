function girarDado() {
  const imagemDado = document.getElementById("imagemDado");
  const valorDado = document.getElementById("valorDado");

  let count = 0;
  const intervalo = setInterval(() => {
    const temp = Math.floor(Math.random() * 6) + 1;
    imagemDado.src = `/static/dado${temp}.png`;
    count++;
    if (count >= 10) {
      clearInterval(intervalo);
      const valorFinal = Math.floor(Math.random() * 6) + 1;
      imagemDado.src = `/static/dado${valorFinal}.png`;
      valorDado.textContent = `🎲 Você tirou: ${valorFinal}`;
    }
  }, 100);
}

// Espera o botão carregar antes de conectar o evento
document.addEventListener("DOMContentLoaded", function () {
  const botao = document.getElementById("botaoGirar");
  if (botao) {
    botao.addEventListener("click", girarDado);
  }
});
