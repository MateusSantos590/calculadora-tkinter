import tkinter as tk
from tkinter import messagebox

class JogoDaVelha:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha")

        self.jogador_atual = "X"
        self.tabuleiro = [["" for _ in range(3)] for _ in range(3)]

        # Cria a matriz de botões para o tabuleiro
        self.botoes = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.botoes[i][j] = tk.Button(
                    root,
                    text="",
                    font=("Helvetica", 24),
                    width=5,
                    height=2,
                    command=lambda i=i, j=j: self.fazer_jogada(i, j)
                )
                self.botoes[i][j].grid(row=i, column=j)

        # Adiciona um botão de reiniciar
        self.reiniciar_botao = tk.Button(
            root,
            text="Reiniciar Jogo",
            font=("Helvetica", 12),
            command=self.reiniciar_jogo
        )
        self.reiniciar_botao.grid(row=3, column=0, columnspan=3, pady=10)

    def fazer_jogada(self, i, j):
        # Verifica se o botão já foi clicado ou se o jogo já terminou
        if self.tabuleiro[i][j] == "" and not self.verificar_vencedor():
            self.tabuleiro[i][j] = self.jogador_atual
            self.botoes[i][j].config(text=self.jogador_atual)

            if self.verificar_vencedor():
                messagebox.showinfo("Fim de Jogo", f"O jogador '{self.jogador_atual}' venceu!")
                self.desativar_botoes()
            elif self.verificar_empate():
                messagebox.showinfo("Fim de Jogo", "O jogo empatou!")
                self.desativar_botoes()
            else:
                self.mudar_jogador()

    def mudar_jogador(self):
        self.jogador_atual = "O" if self.jogador_atual == "X" else "X"

    def verificar_vencedor(self):
        # Verificar linhas e colunas
        for i in range(3):
            if self.tabuleiro[i][0] == self.tabuleiro[i][1] == self.tabuleiro[i][2] != "":
                return True
            if self.tabuleiro[0][i] == self.tabuleiro[1][i] == self.tabuleiro[2][i] != "":
                return True

        # Verificar diagonais
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] != "":
            return True
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] != "":
            return True

        return False

    def verificar_empate(self):
        for linha in self.tabuleiro:
            if "" in linha:
                return False
        return True

    def desativar_botoes(self):
        for i in range(3):
            for j in range(3):
                self.botoes[i][j].config(state=tk.DISABLED)

    def reiniciar_jogo(self):
        self.jogador_atual = "X"
        self.tabuleiro = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.botoes[i][j].config(text="", state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoDaVelha(root)
    root.mainloop()