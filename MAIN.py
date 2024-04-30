import importlib

def get_url():
    url = input("Por favor coloque o URL do jogo: ")
    return url

url = get_url()

project_files = [
    "Confronto direto",
    "Tabela classificativa AWAY",
    "Ultimos10jogosdaequipavisitante",
]

weights = [0.6, 0.2, 0.2]

odd_results = []

for project_file, weight in zip(project_files, weights):
    try:
        module = importlib.import_module(project_file)
        odd_result = module.process_data(url)
        if odd_result is not None:
            weighted_odd = odd_result * weight
            odd_results.append(weighted_odd)
            print(f"ODD AJUSTADA ({project_file}): {weighted_odd:.4f}")
        else:
            print(f"No valid odds found for {project_file}.")
    except ImportError:
        print(f"Unable to import {project_file}. Make sure the file exists and contains the 'process_data' function.")
    print("\n" + "=" * 40 + "\n")

# Calculate weighted average odds
if odd_results:
    average_odd = sum(odd_results) / len(odd_results)

    print(f"ODD VISITANTES GANHAR AJUSTADA: {average_odd:.4f}")
else:
    print("No valid odds found for the specified projects.")
