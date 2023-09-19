import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
import matplotlib.pyplot as plt
import numpy as np

class MinhaClasse:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Seleção de Tipo de Gráfico")

        # Crie uma ComboBox para selecionar o tipo de gráfico
        opcoes_graficos = ["Gráfico de Barras", "Gráfico de Linhas"]
        self.combo_graficos = ttk.Combobox(self.janela, values=opcoes_graficos)
        self.combo_graficos.pack()

        # Configure um evento para a ComboBox de tipos de gráficos
        self.combo_graficos.bind("<<ComboboxSelected>>", self.selecionar_tipo_grafico)

        # Área para a ComboBox de meses e o gráfico
        self.frame_grafico = ttk.Frame(self.janela)
        self.frame_grafico.pack()

    # Função chamada quando um tipo de gráfico é selecionado
    def selecionar_tipo_grafico(self, event):
        tipo_selecionado = self.combo_graficos.get()

        # Limpa a área do gráfico
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        if tipo_selecionado == "Gráfico de Barras":
            # Crie uma ComboBox para selecionar o mês
            meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio"]
            self.combo_mes = ttk.Combobox(self.frame_grafico, values=meses)
            self.combo_mes.pack()

            # Botão para gerar o gráfico de barras
            botao_gerar = ttk.Button(self.frame_grafico, text="Gerar Gráfico", command=self.criar_grafico_barras)
            botao_gerar.pack()
        elif tipo_selecionado == "Gráfico de Linhas":
            # Crie uma ComboBox para selecionar o mês
            meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio"]
            self.combo_mes = ttk.Combobox(self.frame_grafico, values=meses)
            self.combo_mes.pack()

            # Botão para gerar o gráfico de linhas
            botao_gerar = ttk.Button(self.frame_grafico, text="Gerar Gráfico", command=self.criar_grafico_linhas)
            botao_gerar.pack()

    # Função para criar um gráfico de barras com base no mês selecionado
    def criar_grafico_barras(self):
        mes_selecionado = self.combo_mes.get()

        # Dados de exemplo para o gráfico de barras
        categorias = ['Categoria A', 'Categoria B', 'Categoria C', 'Categoria D', 'Categoria E']
        valores = np.random.randint(10, 100, size=len(categorias))

        # Cria o gráfico de barras
        plt.bar(categorias, valores)
        plt.title(f'Gráfico de Barras para {mes_selecionado}')
        plt.xlabel('Categorias')
        plt.ylabel('Valores')
        plt.xticks(rotation=45)
        plt.show()

    # Função para criar um gráfico de linhas com base no mês selecionado
    def criar_grafico_linhas(self):
        mes_selecionado = self.combo_mes.get()

        # Dados de exemplo para o gráfico de linhas
        dias = np.arange(1, 31)
        valores = np.random.randint(10, 100, size=len(dias))

        # Cria o gráfico de linhas
        plt.plot(dias, valores)
        plt.title(f'Gráfico de Linhas para {mes_selecionado}')
        plt.xlabel('Dias')
        plt.ylabel('Valores')
        plt.show()

# Crie a janela principal e instancie a classe
janela = tk.Tk()
app = MinhaClasse(janela)

janela.mainloop()
