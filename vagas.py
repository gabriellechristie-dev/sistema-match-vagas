from flask import Flask, render_template, request, jsonify
import json
import unicodedata
import string

app = Flask(__name__)

# ----------------------
# FRONT
# ----------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------
# NORMALIZAÇÃO 
# ----------------------
def normalizar(texto):
    texto = texto.lower()

    # remove acentos
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join([c for c in texto if not unicodedata.combining(c)])

    # remove pontuação
    texto = texto.translate(str.maketrans("", "", string.punctuation))

    lista = texto.split()

    # remove duplicados
    lista_limpa = []
    for palavra in lista:
        if palavra not in lista_limpa:
            lista_limpa.append(palavra)

    return lista_limpa


# ----------------------
# MATCH DE SKILLS
# ----------------------
def calcular_match(skills_usuario, skills_vagas):
    lista_usuario = normalizar(skills_usuario)
    lista_vagas = normalizar(skills_vagas)

    comuns = []

    for skill in lista_usuario:
        if skill in lista_vagas:
            comuns.append(skill)

    total_comuns = len(comuns)
    total_vagas = len(lista_vagas)

    if total_vagas == 0:
        return 0, []

    porcentagem = (total_comuns / total_vagas) * 100

    return porcentagem, comuns


# ----------------------
# CARREGA VAGAS
# ----------------------
def buscar_vagas():
    with open("vagas.json", "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


# ----------------------
# PROCESSA BUSCA
# ----------------------
def processar_busca(skills_usuario):
    vagas = buscar_vagas()
    resultado = []

    for vaga in vagas:
        titulo = vaga["titulo"]
        skills_vaga = vaga["skills"]

        porcentagem, comuns = calcular_match(skills_usuario, skills_vaga)

        resultado.append({
            "titulo": titulo,
            "porcentagem": porcentagem,
            "skills_comuns": comuns
        })

    resultado_ordenado = sorted(
        resultado,
        key=lambda x: x["porcentagem"],
        reverse=True
    )

    return resultado_ordenado


# ----------------------
# API BUSCAR
# ----------------------
@app.route("/buscar", methods=["POST"])
def buscar():
    skills = request.form["skills"]
    resultado = processar_busca(skills)
    return jsonify(resultado)


# ----------------------
# RODAR APP
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)