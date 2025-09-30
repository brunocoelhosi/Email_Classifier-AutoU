document.addEventListener("DOMContentLoaded", function () {
  // 1. Seleciona a área clicável (o div visual)
  const dropArea = document.querySelector(".drop-area");
  // 2. Seleciona o campo de input de arquivo (que está escondido)
  const fileInput = document.getElementById("email-file");
  // 3. Seleciona o span onde está o texto
  const dropText = dropArea.querySelector("span");

  // Adiciona um listener de clique na área visual
  dropArea.addEventListener("click", function () {
    // Ao clicar na área, ele dispara o clique no input de arquivo escondido
    fileInput.click();
  });

  // Opcional: Atualiza o texto visual quando um arquivo é selecionado
  fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
      // Se um arquivo foi selecionado, mostra o nome dele
      dropText.textContent = `Arquivo selecionado: ${fileInput.files[0].name}`;
      dropArea.style.color = "var(--accent-color)"; // Muda a cor do texto
      dropArea.style.border = "2px dashed var(--accent-color)"; // Destaque na borda
    } else {
      // Caso contrário, volta para o texto padrão
      dropText.textContent = "Selecionar Arquivo (txt ou pdf)";
      dropArea.style.color = "var(--text-muted)";
      dropArea.style.border = "2px dashed var(--text-muted)";
    }
  });
});

document.getElementById("copy-btn").addEventListener("click", function () {
  const resposta = document.getElementById("suggested-response").innerText;
  const btn = this;
  const originalText = btn.textContent;

  navigator.clipboard.writeText(resposta).then(() => {
    btn.textContent = "Copiado!";
    btn.classList.add("copiado");
    btn.disabled = true;
    setTimeout(() => {
      btn.textContent = originalText;
      btn.classList.remove("copiado");
      btn.disabled = false;
    }, 2000); // volta ao texto original após 1,5 segundos
  });
});
