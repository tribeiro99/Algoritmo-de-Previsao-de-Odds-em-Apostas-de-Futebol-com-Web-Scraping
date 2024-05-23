import importlib
import requests

def get_url():
    url = input("Por favor coloque o URL do jogo: ")
    return url

url = get_url()

project_files = [
    "Abrir marcador CASA",
    "Abrir marcador Visitante",
    "Confronto direto",
    "Resultado int final equipa casa",
    "Resultado int final equipa visitante",
    "Ultimos10jogosdaequipadacasa",
    "Ultimos10jogosdaequipavisitante",
    "GOLOS AMBAS EQUIPAS",
    "Tabela classificativa",
    "tabela classificao casa",
    "TABELA CLASSIFICATIVA HOME SEM SELENIUM",
    "tabela classfica fora",
    "Tabela classificativa AWAY",
    "MINUTOS DO GOLO MARCADO ",
    "MINUTOS DO  GOLO SOFRIDO CASA",
    "MINUTOS DO GOLO SOFRIDO VISITANTE",

]

odd_results = []

for project_file in project_files:
    try:
        module = importlib.import_module(project_file)
        odd_result = module.process_data(url)
        if odd_result is not None:
            odd_results.append(odd_result)
    except ImportError:
        print(f"Unable to import {project_file}. Make sure the file exists and contains the 'process_data' function.")
    print("\n" + "=" * 40 + "\n")

# Calculate average odds
if odd_results:
    average_odd = sum(odd_results) / len(odd_results)

    print(f"ODD CASA GANHAR AJUSTADA : {average_odd:.4f}")
else:
    print("No valid odds found for the specified projects.")
