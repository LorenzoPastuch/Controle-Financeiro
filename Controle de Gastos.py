import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.messagebox import askquestion
from tkinter import Canvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window = tk.Tk()

types = [
    'Mercado', 'Alimentação', 'Viagem', 'Transporte',
    'Energia', 'Água', 'Internet', 'Roupas', 'Lazer',
    'Aluguel', 'Saúde', 'Outro'
]
months = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}


def confirm():

    answer = askquestion("Confirmação", "Deseja realmente excluir?")
    if answer == "yes":
        return True


def error():

    tk.messagebox.showerror(title="Erro", message="Valores inválidos")


class Despesa:

    def __init__(self, grafico):

        self.grafico = grafico
        pass

    def add_expense(self):  # add expense to the csv list
        if type.get() and value.get() and date.get():
            try:
                df_expense = pd.read_csv('despesas.csv')
            except:
                df_expense = pd.DataFrame(
                    {
                        "Tipo": [type.get()],
                        "Valor": [value.get()],
                        "Data": [date.get()],
                        "Descrição": [description.get()],
                    }
                )

            df1 = pd.DataFrame(
                {
                    "Tipo": [type.get()],
                    "Valor": [value.get()],
                    "Data": [date.get()],
                    "Descrição": [description.get()],
                }
            )
            df_expense = pd.concat([df_expense, df1])
            df_expense['Ordenation'] = pd.to_datetime(df_expense['Data'], format='%d-%m-%Y')
            df_expense = df_expense.sort_values(by='Ordenation')
            df_expense = df_expense.drop('Ordenation', axis=1)
            df_expense.to_csv('despesas.csv', index=False)

            self.grafico.per_type()
            self.grafico.per_month()

        else:
            error()

    def list_expense(self):

        df_expense = pd.read_csv('despesas.csv', sep=',')

        def exclude(index):  # exclude selected row
            if confirm():
                df_expense.drop(index, inplace=True)
                df_expense.sort_values(by='Data', inplace=True)
                df_expense.to_csv('despesas.csv', index=False)
                expenses.destroy()
                self.list_expense()
                self.grafico.per_type()
                self.grafico.per_month()
            else:
                expenses.focus()

        expenses = tk.Toplevel()

        type = tk.Label(
            expenses,
            text='Tipo'
        )
        type.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        value = tk.Label(
            expenses,
            text='Valor'
        )
        value.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

        date = tk.Label(
            expenses,
            text='Data'
        )
        date.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=10,
            pady=10
        )

        description = tk.Label(
            expenses,
            text='Descrição'
        )
        description.grid(
            row=0,
            column=3,
            sticky="nsew",
            padx=10,
            pady=10
        )

        for i, row in df_expense.iterrows():  # create expenses list
            for j, data in enumerate(row):
                label = tk.Label(expenses, text=data, padx=10, pady=5)
                label.grid(row=i+1, column=j)

                exclude_button = tk.Button(expenses, text='Excluir', padx=10, pady=5, command=lambda i=i: exclude(i))
                exclude_button.grid(row=i+1, column=len(df_expense.columns))


class Orcamento:

    def __init__(self, grafico):
        self.grafico = grafico
        pass

    def add_budget(self):  # add budget to the csv list
        if budget_month.get():
            try:
                df_budget = pd.read_csv('orçamento.csv')
            except:
                df_budget = pd.DataFrame(
                    {'Mês': months,
                     'Valor': 0
                     })
            df_budget.loc[df_budget['Mês'] == budget_month.get(), ['Valor']] = budget_value.get()
            df_budget.to_csv('orçamento.csv', index=False)
            self.grafico.per_type()
            self.grafico.per_month()
        else:
            error()

    def add_type_budget(self):

        try:
            df_type_budget = pd.read_csv('orçamento_tipo.csv')
        except:
            df_type_budget = pd.DataFrame(
                {'Tipo': types,
                 'Orçamento': 0
                 }
            )
        df_type_budget.loc[df_type_budget['Tipo'] == budget_type.get(), ['Orçamento']] = budget_type_value.get()
        df_type_budget.to_csv('orçamento_tipo.csv', index=False)



    def list_type_budget(self):

        try:
            df_type_budget = pd.read_csv('orçamento_tipo.csv')
        except:
            df_type_budget = pd.DataFrame(
                {'Tipo': types,
                 'Orçamento': 0
                 }
            )

        budgets = tk.Toplevel()

        type = tk.Label(
            budgets,
            text='Tipo'
        )
        type.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        value = tk.Label(
            budgets,
            text='Valor'
        )
        value.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

        for i, row in df_type_budget.iterrows():  # create expenses list
            for j, data in enumerate(row):
                label = tk.Label(budgets, text=data, padx=10, pady=5)
                label.grid(row=i+1, column=j)


class Graphics:

    def __init__(self):
        pass

    def per_type(self):

        try:
            df_budget = pd.read_csv('orçamento.csv')
        except:
            df_budget = pd.DataFrame(
                {'Mês': months,
                 'Valor': 0
                 })

        try:
            df_expense = pd.read_csv('despesas.csv')
        except:
            df_expense = pd.DataFrame(
                {
                    "Tipo": [type.get()],
                    "Valor": [value.get()],
                    "Data": [date.get()],
                    "Descrição": [description.get()],
                }
            )

        df_expense = df_expense.groupby(by='Tipo', as_index=False)['Valor'].sum()

        figure = Figure(figsize=(9, 3))
        subplot = figure.add_subplot(111)
        subplot.bar(df_expense['Tipo'], df_expense['Valor'])

        canvas = FigureCanvasTkAgg(figure)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(
            row=9,
            column=5,
            rowspan=6,
            sticky="nsew",
            padx=10,
            pady=10
        )
    def per_month(self):

        try:
            df_budget = pd.read_csv('orçamento.csv')
        except:
            df_budget = pd.DataFrame(
                {'Mês': months,
                 'Valor': 0
                 })

        try:
            df_expense = pd.read_csv('despesas.csv')
        except:
            df_expense = pd.DataFrame(
                {
                    "Tipo": [type.get()],
                    "Valor": [value.get()],
                    "Data": [date.get()],
                    "Descrição": [description.get()],
                }
            )

        df_expense['Data'] = pd.to_datetime(df_expense['Data'], format='%d-%m-%Y')
        df_expense['Mês'] = df_expense['Data'].dt.month
        df_expense = df_expense.groupby(by='Mês', as_index=False)['Valor'].sum()
        df_expense = df_expense.sort_values(by='Mês')
        df_expense['Mês'] = df_expense['Mês'].map(months)

        figure = Figure(figsize=(6, 3))
        subplot = figure.add_subplot(111)
        height = 0.35
        index = np.arange(len(df_expense['Mês']))
        subplot.bar(index-height/2, df_expense['Valor'], height, tick_label=df_expense['Mês'])
        subplot.bar(index+height/2, df_budget['Valor'], height)

        canvas = FigureCanvasTkAgg(figure)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(
            row=2,
            column=5,
            rowspan=6,
            sticky="nsew",
            padx=10,
            pady=10
        )


window.geometry("1450x850+100+100")
window.title("Controle de Gastos")

grafico = Graphics()
despesa = Despesa(grafico)
orcamento = Orcamento(grafico)


title = tk.Label(
    text="Controle de Gastos",
    bg="#6EBAF8",
    width=30,
    height=1,
    font=("algerian", 20),
    padx=10,
    pady=10,
    relief="ridge",
    borderwidth=20
)
title.grid(
    row=0,
    column=0,
    columnspan=5,
    sticky="nsew",
    padx=10,
    pady=10
)

budget_title = tk.Label(
    text="Orçamento",
    relief="ridge",
)
budget_title.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="nsew",
    padx=10,
    pady=10
)

budget_text = tk.Label(
    text='Valor',
    anchor="w",
)
budget_text.grid(
    row=2,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)

budget_value = tk.Entry()
budget_value.grid(
    row=2,
    column=1,
    sticky="nsew",
    padx=10,
    pady=10
)

budget_month_text = tk.Label(
    text='Mês',
    anchor="w",
)
budget_month_text.grid(
    row=2,
    column=2,
    sticky="nsew",
    padx=10,
    pady=10
)

budget_month = ttk.Combobox(window, values=list(months.values()))
budget_month.grid(
    row=2,
    column=3,
    sticky="nsew",
    padx=10,
    pady=10
)

save_budget = tk.Button(
    text='Adicionar orçamento',
    command=orcamento.add_budget
)
save_budget.grid(
    row=3,
    column=0,
    columnspan=4,
    sticky="nsew",
    padx=10,
    pady=10
)






budget_type_value_text = tk.Label(
    text='Valor',
    anchor="w",
)
budget_type_value_text.grid(
    row=4,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)

budget_type_value = tk.Entry()
budget_type_value.grid(
    row=4,
    column=1,
    sticky="nsew",
    padx=10,
    pady=10
)

budget_type_text = tk.Label(
    text='Tipo',
    anchor="w",
)
budget_type_text.grid(
    row=4,
    column=2,
    sticky="nsew",
    padx=10,
    pady=10
)

budget_type = ttk.Combobox(window, values=types)
budget_type.grid(
    row=4,
    column=3,
    sticky="nsew",
    padx=10,
    pady=10
)

save_budget_type = tk.Button(
    text='Adicionar orçamento',
    command=orcamento.add_type_budget
)
save_budget_type.grid(
    row=5,
    column=0,
    columnspan=2,
    sticky="nsew",
    padx=10,
    pady=10
)
list_budget_type = tk.Button(
    text='Listar orçamento',
    command=orcamento.list_type_budget
)
list_budget_type.grid(
    row=5,
    column=2,
    columnspan=2,
    sticky="nsew",
    padx=10,
    pady=10
)








expense_title = tk.Label(
    text="Despesa",
    relief="ridge",
)
expense_title.grid(
    row=6,
    column=0,
    columnspan=4,
    sticky="nsew",
    padx=10,
    pady=10
)

type_text = tk.Label(
    text="Tipo de despesa",
    anchor="w"
)
type_text.grid(
    row=7,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)

type = ttk.Combobox(window, values=types)
type.grid(
    row=7,
    column=1,
    sticky="nsew",
    padx=10,
    pady=10
)

value_text = tk.Label(
    text="Valor",
    anchor="w"
)
value_text.grid(
    row=8,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)

value = tk.Entry(
    textvariable=tk.DoubleVar()
)
value.grid(
    row=8,
    column=1,
    sticky="nsew",
    padx=10,
    pady=10
)

date_text = tk.Label(
    text="Data",
    anchor="w"
)
date_text.grid(
    row=9,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)

date = DateEntry(
    selectmode='day',
    date_pattern='dd-MM-yyyy'
)
date.grid(
    row=9,
    column=1,
    sticky="nsew",
    padx=10,
    pady=10
)

description_text = tk.Label(
    text="Descrição",
    anchor="w"
)
description_text.grid(
    row=10,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)

description = tk.Entry()
description.grid(
    row=10,
    column=1,
    sticky="nsew",
    padx=10,
    pady=10
)

save_expense = tk.Button(
    text='Adicionar despesa',
    command=despesa.add_expense
)
save_expense.grid(
    row=11,
    column=0,
    columnspan=4,
    sticky="nsew",
    padx=10,
    pady=10
)

list_expense = tk.Button(
    text='Listar despesas',
    command=despesa.list_expense
)
list_expense.grid(
    row=12,
    column=0,
    columnspan=4,
    sticky="nsew",
    padx=10,
    pady=10
)

graphic_title = tk.Label(
    text="Grafico",
    relief="ridge",
)
graphic_title.grid(
    row=1,
    column=5,
    columnspan=1,
    sticky="nsew",
    padx=10,
    pady=10
)

grafico.per_month()
grafico.per_type()

window.mainloop()