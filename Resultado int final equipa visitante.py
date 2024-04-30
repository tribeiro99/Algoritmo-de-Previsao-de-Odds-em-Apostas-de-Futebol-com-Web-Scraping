import requests
from bs4 import BeautifulSoup

def calculate_odd(probability):
    return 1 / (probability / 100)

def process_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        away_tables = soup.find_all("table", class_="stat-correctscore")

        if len(away_tables) >= 4:
            tabela_resultado_intervalo_fora = away_tables[2]
            tabela_resultado_final_fora = away_tables[3]

            resultado_intervalo_fora = {}
            linhas_resultado_intervalo_fora = tabela_resultado_intervalo_fora.find_all("tr")
            for linha in linhas_resultado_intervalo_fora[1:-1]:
                colunas = linha.find_all("td")
                resultado = colunas[0].text.strip()
                percentagem = colunas[1].text.strip()
                resultado_intervalo_fora[resultado] = percentagem

            resultado_final_fora = {}
            linhas_resultado_final_fora = tabela_resultado_final_fora.find_all("tr")
            for linha in linhas_resultado_final_fora[1:-1]:
                colunas = linha.find_all("td")
                resultado = colunas[0].text.strip()
                percentagem = colunas[1].text.strip()
                resultado_final_fora[resultado] = percentagem

            print("Resultados ao Intervalo da equipa visitante:")
            for resultado, percentagem in resultado_intervalo_fora.items():
                odd = calculate_odd(float(percentagem.split('%')[0]))
                print(f"{resultado}: {percentagem} ({odd:.4f})")

            print("\nResultados Finais da equipa visitante:")
            for resultado, percentagem in resultado_final_fora.items():
                odd = calculate_odd(float(percentagem.split('%')[0]))
                print(f"{resultado}: {percentagem} ({odd:.4f})")
        else:
            print("Não foram encontradas tabelas para a equipa visitante.")
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')

if __name__ == "__main__":
    url_away = input("Por favor coloque o URL da equipa visitante: ")
    process_data(url_away)
