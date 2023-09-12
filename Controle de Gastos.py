import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

types = [
    'Mercado', 'Alimentação', 'Viagem', 'Transporte',
    'Energia', 'Água', 'Internet', 'Roupas', 'Lazer',
    'Aluguel', 'Saúde', 'Outro'
]
months = [
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro"
]

class Despesa:

    def __init__(self):
        pass

    def add_expense(self): #add expense to the csv list
        try:
            self.df_expense = pd.read_csv('despesas.csv')
        except:
            self.df_expense = pd.DataFrame()

        self.df1 = pd.DataFrame(
            {
                "Tipo": [type.get()],
                "Valor": [value.get()],
                "Data": [date.get()],
                "Descrição": [description.get()],
            }
        )
        self.df_expense = pd.concat([self.df_expense, self.df1])
        self.df_expense.to_csv('despesas.csv', index=False)

    def list_expense(self):
        pass



class Orcamento:

    def __init__(self):
        pass

    def add_budget(self): #add budget to the csv list
        try:
            self.df_budget = pd.read_csv('orçamento.csv')
        except:
            self.df_budget = pd.DataFrame(
                {'Mês': months,
                 'Valor': 0
                 })

        self.df_budget.loc[self.df_budget['Mês'] == budget_month.get(), ['Valor']] = budget_value.get()

        self.df_budget.to_csv('orçamento.csv', index=False)

window = tk.Tk()

window.geometry("800x700+100+100")
window.title("Controle de Gastos")

despesa = Despesa()
orcamento = Orcamento()

title = tk.Label(
    text="Controle de Gastos",
    bg="#6EBAF8",
    width=30,
    height=3,
    font=("algerian", 20),
    padx=10,
    pady=10,
    relief="ridge",
    borderwidth=20
)
title.grid(
    row=0,
    column=0,
    columnspan=4,
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

budget_month = ttk.Combobox(window, values=months)
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

expense_title = tk.Label(
    text="Despesa",
    relief="ridge",
)
expense_title.grid(
    row=4,
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
    row=5,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)

type = ttk.Combobox(window, values=types)
type.grid(
    row=5,
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
    row=6,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)

value = tk.Entry(
    textvariable=tk.DoubleVar()
)
value.grid(
    row=6,
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
    row=7,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)

date = DateEntry(window, selectmode='day', date_pattern='dd-MM-yyyy')
date.grid(
    row=7,
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
    row=8,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)

description = tk.Entry()
description.grid(
    row=8,
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
    row=9,
    column=0,
    columnspan=4,
    sticky="nsew",
    padx=10,
    pady=10
)

list_expense = tk.Button(
    text='Listar despesas',
    #command=
)
list_expense.grid(
    row=10,
    column=0,
    columnspan=4,
    sticky="nsew",
    padx=10,
    pady=10
)

window.mainloop()