# formatação de texto (falta mais formatações)
def normalizar(texto):
    texto = texto.lower()
    texto = texto.strip()
    texto = texto.replace(",","")

    lista = texto.split()


    
    lista_limpa = []
    for palavra in lista:
        palavra_limpa = palavra.strip()
        lista_limpa.append(palavra_limpa)

    return lista_limpa
 
# calcular match
def calcular_match(skills_usuario,skills_vagas):
    lista_usuario = normalizar(skills_usuario)
    lista_vagas = normalizar(skills_vagas)
    lista_comuns = []
    for skill in lista_usuario:
        if skill in lista_vagas:
            lista_comuns.append(skill)
    total_comuns = len(lista_comuns)
    total_vagas = len(lista_vagas)
    if total_vagas > 0:
        porcentagem = (total_comuns/total_vagas)*100
        return porcentagem, lista_comuns
    else:
        porcentagem = 0
        lista_comuns = []
        return porcentagem, lista_comuns

# carregar vagas 
import json

def buscar_vagas():
    with open("vagas.json") as arquivo:
        vagas = json.load(arquivo)
    return vagas

# processar busca 
def processar_busca():
    vagas = buscar_vagas()
    resultado = []

    skills_usuario = input("Digite suas skills: ")
    lista_skills_usuario = skills_usuario.split()

    for vaga in vagas:
        titulo_vaga = vaga["titulo"]
        skills_vaga = vaga["skills"]

        porcentagem, comuns = calcular_match(lista_skills_usuario, skills_vaga)

        item = {
            "titulo": titulo_vaga,
            "porcentagem": porcentagem,
            "skills_comuns": comuns
        }

        resultado.append(item)

    resultado_ordenado = sorted(resultado, key=lambda x: x["porcentagem"], reverse=True)

    return resultado_ordenado