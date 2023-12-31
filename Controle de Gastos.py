import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.messagebox import askquestion
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

graph_type = ['Por mês', 'Por tipo', 'Por orçamento']  # graphic types

def confirm():

    answer = askquestion("Confirmação", "Deseja realmente excluir?")
    if answer == "yes":
        return True


def error():

    tk.messagebox.showerror(title="Erro", message="Valores inválidos")


class Despesa:

    def __init__(self):

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

    def __init__(self):
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
        else:
            error()

    def add_type_budget(self):  # add budget to a expense type
        if budget_type.get() and budget_type_value.get():
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
        else:
            error()

    def list_type_budget(self):  # create a list of budget per type

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
        self.canvas_per_month = None
        self.canvas_per_type = None
        self.canvas_per_budget = None
        self.budget_month_type = None
        pass

    def per_month(self):  # create a graphic of expense e budget per month

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

        figure = Figure(figsize=(8, 4))
        figure.subplots_adjust(bottom=0.2)
        subplot = figure.add_subplot(111)
        height = 0.35
        index = np.arange(len(df_expense['Mês']))
        subplot.bar(index-height/2, df_expense['Valor'], height, tick_label=df_expense['Mês'])
        subplot.bar(index+height/2, df_budget['Valor'], height)
        subplot.set_xticklabels(df_expense['Mês'], rotation=45)



        canvas = FigureCanvasTkAgg(figure)
        self.canvas_per_month = canvas.get_tk_widget()
        self.canvas_per_month.grid(
            row=2,
            column=5,
            rowspan=10,
            sticky="nsew",
            padx=10,
            pady=10
        )

    def per_type(self):  # create a graphic of expenses per type

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

        figure = Figure(figsize=(8, 4))
        figure.subplots_adjust(bottom=0.2)
        subplot = figure.add_subplot(111)
        subplot.bar(df_expense['Tipo'], df_expense['Valor'])
        subplot.set_xticklabels(df_expense['Tipo'], rotation=45)

        canvas = FigureCanvasTkAgg(figure)
        self.canvas_per_type = canvas.get_tk_widget()
        self.canvas_per_type.grid(
            row=2,
            column=5,
            rowspan=10,
            sticky="nsew",
            padx=10,
            pady=10
        )

    def per_budget_type(self, *event):  # create a graphic of expenses per budget type on selected month

        if self.canvas_per_budget is not None:
            self.canvas_per_budget.destroy()

        try:
            df_budget = pd.read_csv('orçamento_tipo.csv')
        except:
            df_budget = pd.DataFrame(
                {'Tipo': months,
                 'Orçamento': 0
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
        df_expense = df_expense.groupby(by=['Tipo', 'Mês'], as_index=False)['Valor'].sum()
        df_expense['Mês'] = df_expense['Mês'].map(months)
        month = self.budget_month_type.get()
        df_expense = df_expense.loc[df_expense['Mês'] == month]
        df_total = df_budget.merge(df_expense, on='Tipo', how='left')
        df_total = df_total.fillna(0)

        figure = Figure(figsize=(8, 4))
        figure.subplots_adjust(bottom=0.2)
        subplot = figure.add_subplot(111)
        height = 0.35
        index = np.arange(len(df_total['Tipo']))
        subplot.bar(index - height / 2, df_total['Valor'], height, tick_label=df_total['Tipo'])
        subplot.bar(index + height / 2, df_total['Orçamento'], height)
        subplot.set_xticklabels(df_total['Tipo'], rotation=45)

        canvas = FigureCanvasTkAgg(figure)
        self.canvas_per_budget = canvas.get_tk_widget()
        self.canvas_per_budget.grid(
            row=3,
            column=5,
            rowspan=9,
            sticky="nsew",
            padx=10,
            pady=10
        )

    def select_graph(self, *event):  # create a graphic of the selected option
        if select_graphics.get() == graph_type[0]:

            if self.canvas_per_type is not None:
                self.canvas_per_type.destroy()
            if self.canvas_per_budget is not None:
                print('per_budget')
                self.canvas_per_budget.destroy()
            if self.budget_month_type is not None:
                self.budget_month_type.destroy()

            grafico.per_month()


        elif select_graphics.get() == graph_type[1]:

            if self.canvas_per_month is not None:
                self.canvas_per_month.destroy()
            if self.canvas_per_budget is not None:
                self.canvas_per_budget.destroy()
            if self.budget_month_type is not None:
                self.budget_month_type.destroy()

            grafico.per_type()

        elif select_graphics.get() == graph_type[2]:

            if self.canvas_per_type is not None:
                self.canvas_per_type.destroy()
            if self.canvas_per_month is not None:
                self.canvas_per_month.destroy()
            if self.budget_month_type is not None:
                self.budget_month_type.destroy()

            self.budget_month_type = ttk.Combobox(window, values=list(months.values()))
            self.budget_month_type.grid(
                row=2,
                column=5,
                sticky="nsew",
                padx=10,
                pady=10
            )
            self.budget_month_type.bind("<<ComboboxSelected>>", grafico.per_budget_type)



window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
window.title("Controle de Gastos")

grafico = Graphics()
despesa = Despesa()
orcamento = Orcamento()

'''
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
'''
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


'''
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
'''

select_graphics = ttk.Combobox(window, values=graph_type)
select_graphics.grid(
    row=1,
    column=5,
    sticky="nsew",
    padx=10,
    pady=10

)
select_graphics.bind("<<ComboboxSelected>>", grafico.select_graph)

window.mainloop()