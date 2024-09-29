import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import sys

# Função para redirecionar o print para o Text widget
class RedirectText:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Rolagem automática para o final

    def flush(self):  # Para compatibilidade com o sistema
        pass

# Função para processar os dados com base na URL e nos arquivos selecionados
def process_data():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira o URL do jogo.")
        return
    
    selected_files = [project_files[i] for i in file_listbox.curselection()]
    
    if not selected_files:
        messagebox.showerror("Erro", "Por favor, selecione pelo menos um arquivo para processar.")
        return
    
    for project_file in selected_files:
        try:
            module = importlib.import_module(project_file)
            module.process_data(url)
            print(f"Processed {project_file} successfully.")
        except ImportError:
            print(f"Unable to import {project_file}. Make sure the file exists and contains the 'process_data' function.")
        print("\n" + "=" * 40 + "\n")

# Lista dos arquivos de projeto
project_files = [
    "Abrir marcador CASA",
    "Abrir marcador Visitante",
    "confrontodireto",
    "Resultado int final equipa casa",
    "Resultado int final equipa visitante",
    "ultimos10jogosdaequipadacasa",
    "Ultimos10jogosdaequipavisitante",
    "GOLOS AMBAS EQUIPAS",
    "Tabela classificativa",
    "tabela classificao casa",
    "tabela classificativa home sem selenium",
    "tabela classfica fora",
    "Tabela classificativa AWAY",
    "MINUTOS DO GOLO MARCADO",
    "MINUTOS DO GOLO SOFRIDO CASA",
    "MINUTOS DO GOLO SOFRIDO VISITANTE"
]

# Criando a interface gráfica
root = tk.Tk()
root.title("Processador de Dados do Jogo")
root.geometry("800x800")  # Mantém o tamanho padrão da janela

# Campo de entrada para a URL
url_label = ttk.Label(root, text="Por favor coloque o URL do jogo:")
url_label.pack(pady=10)
url_entry = ttk.Entry(root, width=80)  # Aumenta o campo de entrada
url_entry.pack(pady=5)

# Caixa de seleção múltipla para os arquivos de projeto
file_label = ttk.Label(root, text="Selecione os arquivos para processar:")
file_label.pack(pady=10)

file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10, width=80)  # Aumenta a largura da lista
for file in project_files:
    file_listbox.insert(tk.END, file)
file_listbox.pack(pady=5)

# Botão para iniciar o processamento
process_button = ttk.Button(root, text="Processar", command=process_data)
process_button.pack(pady=10)

# Área de texto para exibir os resultados, agora com tamanho maior
output_text = tk.Text(root, height=30, width=120, font=("Helvetica", 12))  # Aumenta apenas a área de texto
output_text.pack(pady=10, expand=True, fill=tk.BOTH)

# Redireciona o print para a área de texto
sys.stdout = RedirectText(output_text)

# Executa a interface
