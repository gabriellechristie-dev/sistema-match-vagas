// pega elementos da tela
const botao = document.getElementById("enviar");
const resultado = document.getElementById("resultado");

// evento de clique no botão
botao.addEventListener("click", () => {

    // pega valor digitado pelo usuário
    const input = document.getElementById("skills");
    const valor = input.value;

    // cria FormData (formato que o Flask espera)
    const formData = new FormData();
    formData.append("skills", valor);

    // envia para o backend
    fetch("/buscar", {
        method: "POST",
        body: formData
    })
    .then(resposta => resposta.json())
    .then(dados => {

        // limpa resultados antigos
        resultado.innerHTML = "";

        // percorre cada vaga retornada pelo backend
        dados.forEach(vaga => {

            // monta o bloco HTML da vaga
            const bloco = `
                <div class="vaga">
                    <h3>${vaga.titulo}</h3>
                    <p>Match: ${vaga.porcentagem.toFixed(1)}%</p>
                    <p>Skills em comum: ${vaga.skills_comuns.join(", ")}</p>
                </div>
                <hr>
            `;

            // adiciona na tela
            resultado.innerHTML += bloco;
        });

    })
    .catch(erro => {
        console.error("Erro na requisição:", erro);
        resultado.innerHTML = "Erro ao buscar vagas.";
    });

});