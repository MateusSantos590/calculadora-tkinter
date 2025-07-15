import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import math
import json
import pyperclip
import re


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_ui()

    def setup_window(self):
        self.root.title("Calculadora Científica Premium")
        self.root.geometry("500x800")
        self.root.resizable(False, False)
        self.tema_claro = False
        self.apply_theme()

    def setup_variables(self):
        self.expressao = ""
        self.historico = self.load_history()
        self.last_result = None
        self.memory = 0
        self.deg_rad_mode = "deg"  # deg/rad para trigonometria

    def setup_ui(self):
        # Configuração do grid
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)

        # Visor
        self.visor = ttk.Entry(self.root, font=('Arial', 32), justify='right')
        self.visor.grid(row=0, column=0, columnspan=5, padx=10, pady=20, ipady=15, sticky="nsew")

        # Botões científicos (linhas 1-3)
        sci_buttons = [
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('π', 1, 3), ('e', 1, 4),
            ('asin', 2, 0), ('acos', 2, 1), ('atan', 2, 2), ('ln', 2, 3), ('log', 2, 4),
            ('(', 3, 0), (')', 3, 1), ('^', 3, 2), ('√', 3, 3), ('mod', 3, 4),
            ('x²', 4, 0), ('x³', 4, 1), ('x^y', 4, 2), ('10^x', 4, 3), ('e^x', 4, 4),
            ('1/x', 5, 0), ('|x|', 5, 1), ('n!', 5, 2), ('°⟲rad', 5, 3), ('hyp', 5, 4),
        ]

        # Botões numéricos e operações básicas
        num_buttons = [
            ('7', 6, 0), ('8', 6, 1), ('9', 6, 2), ('/', 6, 3), ('C', 6, 4),
            ('4', 7, 0), ('5', 7, 1), ('6', 7, 2), ('*', 7, 3), ('%', 7, 4),
            ('1', 8, 0), ('2', 8, 1), ('3', 8, 2), ('-', 8, 3), ('ANS', 8, 4),
            ('0', 9, 0), ('.', 9, 1), ('=', 9, 2), ('+', 9, 3), ('⌫', 9, 4),
        ]

        # Botões especiais (linha 10)
        special_buttons = [
            ('Copy', 10, 0), ('Tema', 10, 1), ('Hist', 10, 2), ('M+', 10, 3), ('MR', 10, 4)
        ]

        # Criar botões científicos
        for text, row, col in sci_buttons:
            ttk.Button(self.root, text=text, command=lambda t=text: self.button_click(t)).grid(
                row=row, column=col, sticky="nsew", padx=2, pady=2)

        # Criar botões numéricos
        for text, row, col in num_buttons:
            ttk.Button(self.root, text=text, command=lambda t=text: self.button_click(t)).grid(
                row=row, column=col, sticky="nsew", padx=2, pady=2)

        # Criar botões especiais
        for text, row, col in special_buttons:
            if text == 'Copy':
                cmd = self.copy_result
            elif text == 'Tema':
                cmd = self.toggle_theme
            elif text == 'Hist':
                cmd = self.show_history
            elif text == 'M+':
                cmd = self.memory_add
            elif text == 'MR':
                cmd = self.memory_recall

            ttk.Button(self.root, text=text, command=cmd).grid(
                row=row, column=col, sticky="nsew", padx=2, pady=2)

    def button_click(self, value):
        if value == '=':
            self.calculate()
        elif value == 'C':
            self.clear()
        elif value == '⌫':
            self.backspace()
        elif value == 'ANS' and self.last_result:
            self.expressao += str(self.last_result)
        elif value == 'π':
            self.expressao += str(math.pi)
        elif value == 'e':
            self.expressao += str(math.e)
        elif value == '°⟲rad':
            self.toggle_deg_rad()
            return
        elif value in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
            if self.deg_rad_mode == "deg":
                self.expressao += f'math.{value}(math.radians('
            else:
                self.expressao += f'math.{value}('
        elif value == 'hyp':
            self.show_hyperbolic_menu()
            return
        elif value in ['ln', 'log', '√']:
            self.expressao += f'math.{value[:3]}(' if value != '√' else 'math.sqrt('
        elif value == 'mod':
            self.expressao += '%'
        elif value == 'x²':
            self.expressao += '**2'
        elif value == 'x³':
            self.expressao += '**3'
        elif value == 'x^y':
            self.expressao += '**'
        elif value == '10^x':
            self.expressao += '10**'
        elif value == 'e^x':
            self.expressao += 'math.exp('
        elif value == '1/x':
            self.expressao += '1/('
        elif value == '|x|':
            self.expressao += 'abs('
        elif value == 'n!':
            self.expressao += 'math.factorial('
        else:
            self.expressao += str(value)

        self.update_display()

    def toggle_deg_rad(self):
        self.deg_rad_mode = "rad" if self.deg_rad_mode == "deg" else "deg"
        messagebox.showinfo("Modo Trigonométrico", f"Modo alterado para {self.deg_rad_mode.upper()}")

    def show_hyperbolic_menu(self):
        menu = tk.Toplevel(self.root)
        menu.title("Funções Hiperbólicas")
        menu.geometry("300x200")

        buttons = [
            ('sinh', lambda: self.add_hyperbolic_func('sinh')),
            ('cosh', lambda: self.add_hyperbolic_func('cosh')),
            ('tanh', lambda: self.add_hyperbolic_func('tanh')),
            ('asinh', lambda: self.add_hyperbolic_func('asinh')),
            ('acosh', lambda: self.add_hyperbolic_func('acosh')),
            ('atanh', lambda: self.add_hyperbolic_func('atanh'))
        ]

        for i, (text, cmd) in enumerate(buttons):
            ttk.Button(menu, text=text, command=cmd).pack(fill='x', padx=5, pady=2)

        ttk.Button(menu, text="Fechar", command=menu.destroy).pack(fill='x', padx=5, pady=10)

    def add_hyperbolic_func(self, func):
        self.expressao += f'math.{func}('
        self.update_display()

    def calculate(self):
        try:
            # Substitui constantes especiais
            expr = self.expressao.replace('^', '**')

            # Verifica parênteses balanceados
            if expr.count('(') != expr.count(')'):
                raise ValueError("Parênteses não balanceados")

            # Calcula o resultado
            resultado = eval(expr, {'math': math})

            # Armazena no histórico
            entry = f"{self.expressao} = {resultado}"
            self.historico.append(entry)
            self.save_history()

            # Atualiza o último resultado e a exibição
            self.last_result = resultado
            self.expressao = str(resultado)
        except Exception as e:
            self.expressao = "Erro"
            print(f"Erro no cálculo: {e}")

        self.update_display()

    def clear(self):
        self.expressao = ""
        self.update_display()

    def backspace(self):
        self.expressao = self.expressao[:-1]
        self.update_display()

    def copy_result(self):
        pyperclip.copy(self.visor.get())

    def toggle_theme(self):
        self.tema_claro = not self.tema_claro
        self.apply_theme()

    def apply_theme(self):
        theme = "arc" if self.tema_claro else "equilux"
        self.root.set_theme(theme)

    def update_display(self):
        self.visor.delete(0, tk.END)
        self.visor.insert(0, self.expressao)

    def memory_add(self):
        try:
            value = float(self.visor.get())
            self.memory += value
            messagebox.showinfo("Memória", f"Valor {value} adicionado à memória. Total: {self.memory}")
        except:
            messagebox.showerror("Erro", "Valor inválido para memória")

    def memory_recall(self):
        self.expressao += str(self.memory)
        self.update_display()

    def load_history(self):
        try:
            with open('calc_history.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_history(self):
        with open('calc_history.json', 'w') as f:
            json.dump(self.historico, f, indent=2)

    def show_history(self):
        history_win = ThemedTk(theme="arc" if self.tema_claro else "equilux")
        history_win.title("Histórico de Cálculos")
        history_win.geometry("500x600")

        frame = ttk.Frame(history_win)
        frame.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')

        history_text = tk.Text(
            frame,
            yscrollcommand=scrollbar.set,
            font=('Consolas', 12),
            wrap='word',
            padx=10,
            pady=10
        )
        history_text.pack(expand=True, fill='both')

        scrollbar.config(command=history_text.yview)

        for item in reversed(self.historico):
            history_text.insert('end', item + '\n\n')

        history_text.config(state='disabled')

        # Botão para limpar histórico
        clear_btn = ttk.Button(frame, text="Limpar Histórico",
                             command=lambda: self.clear_history(history_text))
        clear_btn.pack(pady=5)

    def clear_history(self, history_text):
        self.historico = []
        self.save_history()
        history_text.config(state='normal')
        history_text.delete(1.0, tk.END)
        history_text.config(state='disabled')


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = ScientificCalculator(root)
    root.mainloop()