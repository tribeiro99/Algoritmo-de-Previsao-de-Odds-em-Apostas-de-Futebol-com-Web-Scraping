import requests
from bs4 import BeautifulSoup

def calculate_odd(probability):
    return 1 / (probability / 100)

def process_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        tabela_resultado_intervalo_casa = soup.find_all("table", class_="stat-correctscore")[0]

        tabela_resultado_final_casa = tabela_resultado_intervalo_casa.find_next("table", class_="stat-correctscore")

        resultado_intervalo_casa = {}
        linhas_resultado_intervalo_casa = tabela_resultado_intervalo_casa.find_all("tr")
        for linha in linhas_resultado_intervalo_casa[1:-1]:
            colunas = linha.find_all("td")
            resultado = colunas[0].text.strip()
            percentagem = colunas[1].text.strip()
            resultado_intervalo_casa[resultado] = percentagem

        resultado_final_casa = {}
        linhas_resultado_final_casa = tabela_resultado_final_casa.find_all("tr")
        for linha in linhas_resultado_final_casa[1:-1]:
            colunas = linha.find_all("td")
            resultado = colunas[0].text.strip()
            percentagem = colunas[1].text.strip()
            resultado_final_casa[resultado] = percentagem

        print("Resultados ao Intervalo da equipa da casa:")
        for resultado, percentagem in resultado_intervalo_casa.items():
            odd = calculate_odd(float(percentagem.split('%')[0]))
            print(f"{resultado}: {percentagem} ({odd:.4f})")

        print("\nResultados Finais da equipa da casa:")
        for resultado, percentagem in resultado_final_casa.items():
            odd = calculate_odd(float(percentagem.split('%')[0]))
            print(f"{resultado}: {percentagem} ({odd:.4f})")
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')

if __name__ == "__main__":
    url = input("Por favor coloque o URL do jogo: ")
    process_data(url)

