import tkinter as tk
from tkinter import ttk

from Laberinto import resolver_laberinto_dfs
from Puzzle import resolver_puzzle_dfs
from Jarras import resolver_jarras_dfs


MAX_SIZE = 520


class AppDFS(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("DFS - Inteligencia Artificial")
        self.geometry("750x820")

        tk.Label(self,text="Selecciona Problema",font=("Arial",14)).pack()

        self.problema = tk.StringVar(value="Laberinto")

        ttk.Combobox(
            self,
            textvariable=self.problema,
            values=["Jarras","Laberinto","8-Puzzle"]
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
        self.frame_jarras = None

        self.botones = []

        self.pasos = []
        self.index = 0

        self.metricas = None

        self.label_metricas = tk.Label(self,text="",font=("Arial",10))
        self.label_metricas.pack(pady=10)

    def limpiar(self):

        if self.canvas:
            self.canvas.destroy()
            self.canvas = None

        if self.frame_puzzle:
            self.frame_puzzle.destroy()
            self.frame_puzzle = None

        if self.frame_jarras:
            self.frame_jarras.destroy()
            self.frame_jarras = None

    def iniciar(self):

        self.label_metricas.config(text="")

        problema = self.problema.get()

        if problema == "Laberinto":
            self.limpiar()
            self.iniciar_laberinto()

        if problema == "8-Puzzle":
            self.limpiar()
            self.iniciar_puzzle()

        if problema == "Jarras":
            self.limpiar()
            self.iniciar_jarras()

    # ---------------------------------------------------
    # LABERINTO
    # ---------------------------------------------------

    def iniciar_laberinto(self):

        size = int(self.size.get())
        cell = MAX_SIZE // size

        self.canvas = tk.Canvas(
            self,
            width=size*cell,
            height=size*cell,
            bg="white"
        )

        self.canvas.pack(pady=20)

        resultado = resolver_laberinto_dfs(size)

        self.lab = resultado["laberinto"]
        self.visitados = resultado["visitados"]
        self.camino = resultado["camino"]

        self.metricas = resultado

        self.cell = cell
        self.size_lab = size

        self.pasos = self.visitados + self.camino
        self.index = 0

        self.animar_laberinto()

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
                    fill=color,
                    outline="gray"
                )

        self.canvas.create_rectangle(0,0,self.cell,self.cell,fill="green")

        self.canvas.create_rectangle(
            (self.size_lab-1)*self.cell,
            (self.size_lab-1)*self.cell,
            self.size_lab*self.cell,
            self.size_lab*self.cell,
            fill="red"
        )

    def animar_laberinto(self):

        if self.index >= len(self.pasos):

            self.label_metricas.config(
                text=f"Tiempo algoritmo: {self.metricas['tiempo']:.6f}s | "
                     f"Nodos explorados: {self.metricas['nodos_explorados']} | "
                     f"Memoria: {self.metricas['memoria']:.2f} KB"
            )

            return

        self.dibujar_laberinto()

        for i in range(self.index):

            x,y = self.pasos[i]

            color = "#4FC3F7"

            if (x,y) in self.camino:
                color = "#FFD700"

            self.canvas.create_rectangle(
                y*self.cell,
                x*self.cell,
                (y+1)*self.cell,
                (x+1)*self.cell,
                fill=color
            )

        self.index += 1

        self.after(40,self.animar_laberinto)

    # ---------------------------------------------------
    # PUZZLE
    # ---------------------------------------------------

    def iniciar_puzzle(self):

        self.frame_puzzle = tk.Frame(self)
        self.frame_puzzle.pack(pady=20)

        self.botones = []

        for i in range(9):

            b = tk.Button(
                self.frame_puzzle,
                width=4,
                height=2,
                font=("Arial",26)
            )

            b.grid(row=i//3,column=i%3,padx=5,pady=5)

            self.botones.append(b)

        resultado = resolver_puzzle_dfs()

        self.pasos = resultado["camino"]
        self.index = 0

        self.metricas = resultado

        self.animar_puzzle()

    def animar_puzzle(self):

        if self.index >= len(self.pasos):

            self.label_metricas.config(
                text=f"Tiempo algoritmo: {self.metricas['tiempo']:.6f}s | "
                     f"Estados explorados: {self.metricas['visitados']} | "
                     f"Memoria: {self.metricas['memoria']:.2f} KB"
            )

            return

        estado = self.pasos[self.index]

        for i in range(9):

            val = estado[i]
            self.botones[i]["text"] = "" if val==0 else str(val)

        self.index += 1

        self.after(400,self.animar_puzzle)

    # ---------------------------------------------------
    # JARRAS
    # ---------------------------------------------------

    def iniciar_jarras(self):

        self.frame_jarras = tk.Frame(self)
        self.frame_jarras.pack(pady=40)

        self.label_estado = tk.Label(
            self.frame_jarras,
            text="",
            font=("Arial",22)
        )
        self.label_estado.pack()

        resultado = resolver_jarras_dfs()

        self.pasos = resultado["camino"]
        self.index = 0

        self.metricas = resultado

        self.animar_jarras()

    def animar_jarras(self):

        if self.index >= len(self.pasos):

            self.label_metricas.config(
                text=f"Tiempo algoritmo: {self.metricas['tiempo']:.6f}s | "
                     f"Estados explorados: {self.metricas['visitados']} | "
                     f"Memoria: {self.metricas['memoria']:.2f} KB"
            )

            return

        jarra1, jarra2 = self.pasos[self.index]

        self.label_estado.config(
            text=f"Jarra 1: {jarra1}   |   Jarra 2: {jarra2}"
        )

        self.index += 1

        self.after(800,self.animar_jarras)


if __name__ == "__main__":

    app = AppDFS()
    app.mainloop()