import requests
from bs4 import BeautifulSoup

def calculate_odds(probability):
    return 1 / probability

def process_data(url):

    response = requests.get(url)


    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')


        tabela_abre_marcador = soup.find_all("tbody", class_="loader-container")[0]


        informacoes_abre_marcador = {}
        linhas_abre_marcador = tabela_abre_marcador.find_all("tr")
        for linha in linhas_abre_marcador:
            colunas = linha.find_all("td")
            categoria = colunas[0].text.strip()
            valor = colunas[1].text.strip()
            informacoes_abre_marcador[categoria] = valor


        print("Estatísticas de Abrir o Marcador para CASA")
        for categoria, valor in informacoes_abre_marcador.items():
            print(f"{categoria}: {valor}")


        if 'Abre marcador (qualquer altura)' in informacoes_abre_marcador:
            abre_marcador = int(informacoes_abre_marcador["Abre marcador (qualquer altura)"].split()[0])
            numero_golos = int(informacoes_abre_marcador["Abre marcador (qualquer altura)"].split()[2])
            if abre_marcador > 0 :
               prob_abre_marcador = abre_marcador / numero_golos
               odd_abre_marcador = calculate_odds(prob_abre_marcador)
               print(f"Odd para a equipa da casa abrir o marcador: {odd_abre_marcador:.4f}")
            else:
                 print(f"A equipa abre o marcador 0 vezes em {numero_golos}")

        if '⇒ e está a vencer ao intervalo' in informacoes_abre_marcador:
            vence_intervalo = int(informacoes_abre_marcador["⇒ e está a vencer ao intervalo"].split()[0])
            numero_golos_int = int(informacoes_abre_marcador["⇒ e está a vencer ao intervalo"].split()[2])
            if vence_intervalo > 0:
                prob_vence_intervalo = vence_intervalo / numero_golos_int
                odd_vence_intervalo = calculate_odds(prob_vence_intervalo)
                print(f"Odd para a equipa da casa vencer no intervalo após marcar primeiro: {odd_vence_intervalo:.4f}")
            else:
                print(f"A equipa está a vencer ao int 0 jogos em: {numero_golos_int}")


        if '⇒ e vence no final' in informacoes_abre_marcador:
            vence_final = int(informacoes_abre_marcador["⇒ e vence no final"].split()[0])
            numero_golos_int_final = int(informacoes_abre_marcador["⇒ e vence no final"].split()[2])
            if vence_final > 0 :
               prob_vence_final = vence_final / numero_golos_int_final
               odd_vence_final = calculate_odds(prob_vence_final)
               print(f"Odd para a equipa da casa vencer no final após marcar primeiro: {odd_vence_final:.4f}")
            else:
                print(f" A equipa vence no final dos jogos 0 em {numero_golos_int_final}")



if __name__ == "__main__":
    url = input("Por favor coloque o URL do jogo: ")
    process_data(url)
