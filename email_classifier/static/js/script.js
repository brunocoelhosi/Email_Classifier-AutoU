document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("email-form");
  const loadingOverlay = document.getElementById("loading-overlay");
  const copyButton = document.getElementById("copy-btn");

  // Modal de Loading enquanto aguarda resposta da IA
  form.addEventListener("submit", function (event) {
    const emailText = document.getElementById("email-text").value.trim();
    const emailFile = document.getElementById("email-file").files[0];

    if (emailText === "" && !emailFile) {
      alert("Por favor, cole o conteúdo do e-mail ou selecione um arquivo.");
      // Bloqueia o envio do formulário se nenhum conteúdo for fornecido
      event.preventDefault();
      return;
    }

    if (loadingOverlay) {
      loadingOverlay.style.display = "flex";
    }
  });

  // Botão de copiar resposta sugerida
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
      }, 2000); // delay de 2 segundos para reverter o texto do botão
    });
  });

  // Upload de arquivo estilizado
  const dropArea = document.querySelector(".drop-area");
  const fileInput = document.getElementById("email-file");
  const dropText = dropArea.querySelector("span");

  // Ao clicar na área de drop, abre o seletor de arquivos
  dropArea.addEventListener("click", function () {
    fileInput.click();
  });

  // Destaca a área de drop ao selecionar um arquivo
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

  // Rola a tela para os resultados automaticamente
  // Seleciona o elemento que contém a categoria (para verificar se há resultados)
  const categoryBadge = document.getElementById("category-badge");

  // Seleciona o elemento de destino
  const resultsAnchor = document.getElementById("results-anchor"); // Ou 'results-display'

  // Função que verifica e rola a tela
  function scrollToResults() {
    // Verifica se o texto da categoria foi substituído pelos resultados
    // 'Aguardando Email...' é o texto padrão (default_if_none) do Django
    const currentCategory = categoryBadge.textContent.trim();

    if (
      resultsAnchor &&
      currentCategory !== "Aguardando Email..." &&
      currentCategory !== "AGUARDANDO EMAIL..."
    ) {
      resultsAnchor.scrollIntoView({
        behavior: "smooth", // Rola suavemente
        block: "start", // Coloca o topo do elemento no topo da janela
      });
    }
  }
  // Executa a rolagem após o carregamento completo da página
  scrollToResults();
});
