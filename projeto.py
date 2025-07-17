"""
Biblioteca que use:

    - Tkinter -> Biblioteca padrao do Python para Interface Gráfica; Oferece botoes, janelas, caixas de textos, etc.
        - A sila TTK -> é uma modulodentro da Biblioteca Tkinter; Este modulo oferece widgets com um visual mais moderno e personalizavel
        - Messagebox -> é outro modul da Biblioteca Tkinter; Desta vez oferecendo: caixas de dialogo padronizadas, como mensagens de informação, avisos e erros
    - Math -> Contem funções e contantes matematicas. Ultil para calculos complexos, como logaritmos, exponenciais, etc.
    - Json -> Esta Biblioteca é usada para trabalhar com Dados (Javascript Object Notation). Essa biblioteca por exemplo pode ser usada caso voce queira Salvar as configuraçoes do seu programa.
    - Pyperclip -> Imagine que a área de transferência (o clipboard) é uma "gaveta invisível" onde o seu computador guarda temporariamente a última coisa que você copiou.
                    Quando você usa o comando pyperclip.copy("algum texto"), é como se você estivesse colocando o texto "algum texto" dentro dessa gaveta.
                            Quando você usa o comando pyperclip.paste(), o seu código está pedindo para pegar o que está dentro da gaveta.
    - Re -> A sigla 'RE' significa (Regular Expressions ou Expressoes Regulares). Ela é usada para realizar operacoes de busca e manipulacao de textos baseadas em padroes. É muito ultil para: validar formatos de entrada de dados, encontrar e substituir substings e analisar textos de forma flexivel.
                -- O que é Substring? Em programação, substring é uma parte de uma palavra ou frase.
                            Imagine a palavra "programação". Uma substring seria qualquer pedaço dela, como:
                    "pro"
                        "grama"
                            "ação"
                                "ão"

É como se você estivesse recortando um pedaço de um texto maior. A substring é útil quando você precisa encontrar, extrair ou trabalhar com apenas uma parte de uma string (que é o nome técnico para texto). Por exemplo, você pode usar uma substring para verificar se um texto contém uma palavra específica, ou para extrair um código de um número de série.
"""

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
        for i in range(11):  # Ajustado para 11 linhas
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

    def is_valid_expression(self, expr):
        """Valida a expressão usando regex para segurança"""
        # Padrão que permite números, operadores, funções matemáticas e constantes
        pattern = r'^[\d+\-*/().^%πe\s]+|(math\.)?(sin|cos|tan|asin|acos|atan|log|ln|sqrt|factorial|exp|abs|sinh|cosh|tanh|asinh|acosh|atanh)\(?$'
        return re.match(pattern, expr, re.IGNORECASE) is not None

    def prepare_expression(self, expr):
        """Prepara a expressão para avaliação com substituições seguras"""
        # Substitui operadores e constantes
        replacements = [
            (r'\^', '**'),
            (r'π', 'math.pi'),
            (r'e(?![a-zA-Z])', 'math.e'),  # Substitui 'e' apenas quando não for parte de uma função
            (r'mod', '%'),
            (r'√\(', 'math.sqrt('),
            (r'ln\(', 'math.log('),
            (r'log\(', 'math.log10('),
            (r'abs\(', 'math.fabs(')
        ]

        for pattern, replacement in replacements:
            expr = re.sub(pattern, replacement, expr)

        return expr

    def has_balanced_parentheses(self, expr):
        """Verifica parênteses balanceados usando regex"""
        # Remove tudo que não são parênteses e depois verifica balanceamento
        clean_expr = re.sub(r'[^()]', '', expr)
        while re.search(r'\(\)', clean_expr):
            clean_expr = re.sub(r'\(\)', '', clean_expr)
        return len(clean_expr) == 0

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
            self.expressao += 'π'
        elif value == 'e':
            self.expressao += 'e'
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
            self.expressao += f'{value}('
        elif value == 'mod':
            self.expressao += 'mod'
        elif value == 'x²':
            self.expressao += '^2'
        elif value == 'x³':
            self.expressao += '^3'
        elif value == 'x^y':
            self.expressao += '^'
        elif value == '10^x':
            self.expressao += '10^'
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
            # Validação com regex
            if not self.is_valid_expression(self.expressao):
                raise ValueError("Expressão contém caracteres inválidos")

            if not self.has_balanced_parentheses(self.expressao):
                raise ValueError("Parênteses não balanceados")

            # Prepara a expressão
            expr = self.prepare_expression(self.expressao)

            # Calcula o resultado
            resultado = eval(expr, {'math': math, '__builtins__': None})

            # Formata o resultado para remover .0 de números inteiros
            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)

            # Armazena no histórico
            entry = f"{self.expressao} = {resultado}"
            self.historico.append(entry)
            self.save_history()

            # Atualiza o último resultado e a exibição
            self.last_result = resultado
            self.expressao = str(resultado)
        except Exception as e:
            self.handle_calculation_error(e)

        self.update_display()

    def handle_calculation_error(self, error):
        """Trata diferentes tipos de erros com mensagens específicas"""
        error_msg = str(error)

        if re.search(r'division by zero', error_msg, re.IGNORECASE):
            self.expressao = "Erro: Divisão por zero"
        elif re.search(r'math domain error', error_msg, re.IGNORECASE):
            self.expressao = "Erro: Domínio inválido"
        elif re.search(r'factorial', error_msg, re.IGNORECASE):
            self.expressao = "Erro: Fatorial inválido"
        elif re.search(r'balanced', error_msg, re.IGNORECASE):
            self.expressao = "Erro: Parênteses não balanceados"
        else:
            self.expressao = "Erro na expressão"

        print(f"Erro no cálculo: {error_msg}")

    def clear(self):
        self.expressao = ""
        self.update_display()

    def backspace(self):
        # Remove o último caractere, tratando funções especiais
        if re.search(r'math\.\w+\($', self.expressao):
            # Se for uma função matemática, remove toda a função
            self.expressao = re.sub(r'math\.\w+\($', '', self.expressao)
        else:
            self.expressao = self.expressao[:-1]
        self.update_display()

    def copy_result(self):
        # Copia apenas o resultado numérico se houver
        match = re.search(r'[-+]?\d*\.?\d+', self.visor.get())
        if match:
            pyperclip.copy(match.group())
        else:
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
            # Extrai o número do visor usando regex
            match = re.search(r'[-+]?\d*\.?\d+', self.visor.get())
            if match:
                value = float(match.group())
                self.memory += value
                messagebox.showinfo("Memória", f"Valor {value} adicionado à memória. Total: {self.memory}")
            else:
                raise ValueError("Nenhum número válido encontrado")
        except Exception as e:
            messagebox.showerror("Erro", f"Valor inválido para memória: {str(e)}")

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
            # Destaca resultados com regex
            highlighted = re.sub(r'(=.*)', r'\1', item)
            history_text.insert('end', highlighted + '\n\n')

        history_text.config(state='disabled')

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