import tkinter as tk
from tkinter import ttk
import random

from Laberinto import resolver_laberinto_dfs
from Puzzle import resolver_puzzle_dfs, OBJETIVO


MAX_SIZE = 650


class AppDFS(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("DFS - Inteligencia Artificial")
        self.geometry("750x850")

        tk.Label(self,text="Selecciona Problema",font=("Arial",14)).pack()

        self.problema = tk.StringVar(value="Laberinto")

        ttk.Combobox(
            self,
            textvariable=self.problema,
            values=["Laberinto","8-Puzzle"]
        ).pack(pady=5)

        tk.Label(self,text="Tamaño Laberinto").pack()

        self.size = tk.StringVar(value="10")

        ttk.Combobox(
            self,
            textvariable=self.size,
            values=["10","20","50"]
        ).pack(pady=5)

        tk.Button(self,text="Iniciar",command=self.iniciar).pack(pady=10)

        self.canvas = None

        self.frame_puzzle = None
        self.botones = []

        self.pasos = []
        self.index = 0

        self.label_metricas = tk.Label(self,text="")
        self.label_metricas.pack()

    def iniciar(self):

        problema = self.problema.get()

        if problema == "Laberinto":
            self.iniciar_laberinto()

        if problema == "8-Puzzle":
            self.iniciar_puzzle()

    def iniciar_laberinto(self):

        size = int(self.size.get())

        cell = MAX_SIZE // size

        if self.canvas:
            self.canvas.destroy()

        self.canvas = tk.Canvas(self,width=size*cell,height=size*cell)
        self.canvas.pack()

        resultado = resolver_laberinto_dfs(size)

        self.lab = resultado["laberinto"]
        self.visitados = resultado["visitados"]
        self.camino = resultado["camino"]

        self.cell = cell
        self.size_lab = size

        self.pasos = self.visitados + self.camino
        self.index = 0

        self.metricas = resultado

        self.animar()

    def dibujar_laberinto(self):

        self.canvas.delete("all")

        for i in range(self.size_lab):
            for j in range(self.size_lab):

                color = "white"

                if self.lab[i][j] == 1:
                    color = "black"

                self.canvas.create_rectangle(
                    j*self.cell,
                    i*self.cell,
                    (j+1)*self.cell,
                    (i+1)*self.cell,
                    fill=color
                )

        self.canvas.create_rectangle(
            0,0,
            self.cell,self.cell,
            fill="green"
        )

        self.canvas.create_rectangle(
            (self.size_lab-1)*self.cell,
            (self.size_lab-1)*self.cell,
            self.size_lab*self.cell,
            self.size_lab*self.cell,
            fill="red"
        )

    def animar(self):

        if self.index >= len(self.pasos):
            self.mostrar_metricas()
            return

        self.dibujar_laberinto()

        for i in range(self.index):

            x,y = self.pasos[i]

            color = "blue"

            if (x,y) in self.camino:
                color = "yellow"

            self.canvas.create_rectangle(
                y*self.cell,
                x*self.cell,
                (y+1)*self.cell,
                (x+1)*self.cell,
                fill=color
            )

        self.index += 1

        self.after(40,self.animar)

    def mostrar_metricas(self):

        self.label_metricas.config(
            text=f"Tiempo: {self.metricas['tiempo']:.6f}s | "
                 f"Nodos: {self.metricas['nodos_explorados']} | "
                 f"Memoria: {self.metricas['memoria']:.2f} KB"
        )

    def iniciar_puzzle(self):

        if self.canvas:
            self.canvas.destroy()

        if self.frame_puzzle:
            self.frame_puzzle.destroy()

        self.frame_puzzle = tk.Frame(self)
        self.frame_puzzle.pack()

        self.botones = []

        for i in range(9):

            b = tk.Button(
                self.frame_puzzle,
                width=4,
                height=2,
                font=("Arial",26)
            )

            b.grid(row=i//3,column=i%3)

            self.botones.append(b)

        estado = list(OBJETIVO)

        for _ in range(40):

            i = estado.index(0)

            mov = random.choice([-3,3,-1,1])

            j = i + mov

            if 0 <= j < 9:
                estado[i],estado[j] = estado[j],estado[i]

        resultado = resolver_puzzle_dfs(tuple(estado))

        self.pasos = resultado["camino"]
        self.index = 0

        self.metricas = resultado

        self.animar_puzzle()

    def animar_puzzle(self):

        if self.index >= len(self.pasos):

            self.label_metricas.config(
                text=f"Tiempo: {self.metricas['tiempo']:.6f}s | "
                     f"Estados: {self.metricas['visitados']} | "
                     f"Memoria: {self.metricas['memoria']:.2f} KB"
            )

            return

        estado = self.pasos[self.index]

        for i in range(9):

            val = estado[i]

            self.botones[i]["text"] = "" if val==0 else str(val)

        self.index += 1

        self.after(400,self.animar_puzzle)


if __name__ == "__main__":

    app = AppDFS()
    app.mainloop()