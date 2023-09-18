import tkinter as tk
from tkinter import ttk

class MinhaClasse:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("ComboBox com evento de mudança de valor")

        # Crie uma ComboBox com algumas opções
        opcoes = ["Opção 1", "Opção 2", "Opção 3", "Opção 4"]
        self.combo = ttk.Combobox(self.janela, values=opcoes)
        self.combo.pack()

        # Configure um evento para a ComboBox quando uma opção é selecionada
        self.combo.bind("<<ComboboxSelected>>", self.selecionar_valor)

        # Crie um rótulo para exibir o valor selecionado
        self.label_valor = tk.Label(self.janela, text="")
        self.label_valor.pack()

    # Função chamada quando a ComboBox é alterada
    def selecionar_valor(self, event):
        valor_selecionado = self.combo.get()
        self.label_valor.config(text=f"Valor selecionado: {valor_selecionado}")

# Crie a janela principal e instancie a classe
janela = tk.Tk()
app = MinhaClasse(janela)

janela.mainloop()
