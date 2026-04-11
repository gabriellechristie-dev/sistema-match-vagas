const botao = document.getElementById("enviar");
const input = document.getElementById("skills");
const resultado = document.getElementById("resultado");

function buscarVagas() {

    const valor = input.value.trim();

    // validação
    if (valor === "") {
        resultado.innerHTML = "Digite pelo menos uma skill.";
        return;
    }

    // loading
    resultado.innerHTML = "Buscando vagas...";

    const formData = new FormData();
    formData.append("skills", valor);

    fetch("/buscar", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(dados => {

        resultado.innerHTML = "";

        const relevantes = dados.filter(v => v.porcentagem > 0);

        if (relevantes.length === 0) {
            resultado.innerHTML = "Nenhuma vaga relevante encontrada.";
            return;
        }

        dados.forEach((vaga, index) => {

            let cor = "#ef4444";
            if (vaga.porcentagem >= 70) cor = "#22c55e";
            else if (vaga.porcentagem >= 30) cor = "#eab308";

            const skillsTexto = vaga.skills_comuns.length > 0
                ? vaga.skills_comuns.join(", ")
                : "Nenhuma skill em comum";

            const destaque = index === 0 ? "destaque" : "";

            const bloco = `
                <div class="vaga ${destaque}">
                    <h3>${vaga.titulo}</h3>
                    <p><strong>Empresa:</strong> ${vaga.empresa}</p>
                    <p><strong>Local:</strong> ${vaga.local}</p>
                    <p><strong>Match:</strong> <span style="color:${cor}">
                        ${vaga.porcentagem.toFixed(1)}%
                    </span></p>
                    <p><strong>Skills:</strong> ${skillsTexto}</p>
                </div>
            `;

            resultado.innerHTML += bloco;
        });

    })
    .catch(() => {
        resultado.innerHTML = "Erro ao buscar vagas.";
    });
}

// clique
botao.addEventListener("click", buscarVagas);

// enter
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        buscarVagas();
    }
});