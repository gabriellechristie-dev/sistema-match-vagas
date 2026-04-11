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

    # aceita lista ou string
    if isinstance(texto, list):
        texto = " ".join(texto)

    texto = texto.lower()

    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join([c for c in texto if not unicodedata.combining(c)])

    texto = texto.translate(str.maketrans("", "", string.punctuation))

    lista = texto.split()

    lista_limpa = []
    for palavra in lista:
        if palavra not in lista_limpa:
            lista_limpa.append(palavra)

    return lista_limpa


# ----------------------
# MATCH
# ----------------------
def calcular_match(skills_usuario, skills_vagas):
    lista_usuario = normalizar(skills_usuario)
    lista_vagas = normalizar(skills_vagas)

    comuns = [s for s in lista_usuario if s in lista_vagas]

    if len(lista_vagas) == 0:
        return 0, []

    porcentagem = (len(comuns) / len(lista_vagas)) * 100

    return porcentagem, comuns


# ----------------------
# CARREGAR JSON
# ----------------------
def buscar_vagas():
    with open("vagas.json", "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


# ----------------------
# PROCESSAR
# ----------------------
def processar_busca(skills_usuario):
    vagas = buscar_vagas()
    resultado = []

    for vaga in vagas:
        porcentagem, comuns = calcular_match(skills_usuario, vaga.get("skills", []))

        resultado.append({
            "titulo": vaga.get("titulo", "Sem título"),
            "empresa": vaga.get("empresa", "Não informado"),
            "local": vaga.get("local", "Não informado"),
            "porcentagem": porcentagem,
            "skills_comuns": comuns
        })

    return sorted(resultado, key=lambda x: x["porcentagem"], reverse=True)


# ----------------------
# API
# ----------------------
@app.route("/buscar", methods=["POST"])
def buscar():
    skills = request.form.get("skills", "")
    resultado = processar_busca(skills)
    return jsonify(resultado)


# ----------------------
# RUN
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)