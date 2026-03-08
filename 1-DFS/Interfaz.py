import tkinter as tk
from tkinter import ttk
import time
import tracemalloc
import random

from Jarras import dfs_jarras, reconstruir_camino
from Laberinto import resolver_laberinto_dfs
from Puzzle import resolver_puzzle_dfs, OBJETIVO


PROBLEMAS = {
    "Jarras": "jarras",
    "Laberinto": "laberinto",
    "8-Puzzle": "puzzle"
}

MAX_SIZE = 700


class AppDFSSelector(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("DFS - Selector de Problema")
        self.geometry("720x750")

        tk.Label(self, text="Selecciona el problema:").pack(pady=5)

        self.problema_var = tk.StringVar(value="Jarras")

        ttk.Combobox(
            self,
            textvariable=self.problema_var,
            values=list(PROBLEMAS.keys())
        ).pack(pady=5)

        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Iniciar", command=self.iniciar).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Reiniciar", command=self.reiniciar).pack(side=tk.LEFT, padx=5)

        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=5)

        self.btn_anterior = tk.Button(nav_frame, text="◀ Anterior", command=self.paso_anterior, state=tk.DISABLED)
        self.btn_siguiente = tk.Button(nav_frame, text="Siguiente ▶", command=self.paso_siguiente, state=tk.DISABLED)

        self.btn_anterior.pack(side=tk.LEFT, padx=10)
        self.btn_siguiente.pack(side=tk.LEFT, padx=10)

        self.lbl_pasos = tk.Label(self, text="Paso: 0/0")
        self.lbl_pasos.pack(pady=5)

        self.display_frame = tk.Frame(self)
        self.display_frame.pack(pady=10)

        self.canvas_lab = None
        self.frame_puzzle = None
        self.botones = []

        self.resultado_texto = tk.Text(self, height=8, width=80, state="disabled")
        self.resultado_texto.pack(pady=10)

        self.pasos = []
        self.index_paso = 0
        self.metricas = ""
        self.problema_actual = None

        self.lab = None
        self.visitados = None
        self.camino = None
        self.size_lab = 10
        self.cell = MAX_SIZE // self.size_lab

    def iniciar(self):

        problema = self.problema_var.get()
        self.problema_actual = PROBLEMAS[problema]

        self.limpiar_display()

        if self.problema_actual == "jarras":
            self.iniciar_jarras()

        elif self.problema_actual == "laberinto":
            self.iniciar_laberinto()

        elif self.problema_actual == "puzzle":
            self.iniciar_puzzle()

    def limpiar_display(self):

        if self.canvas_lab:
            self.canvas_lab.destroy()
            self.canvas_lab = None

        if self.frame_puzzle:
            self.frame_puzzle.destroy()
            self.frame_puzzle = None
            self.botones = []

    # -----------------------------
    # JARRAS
    # -----------------------------

    def iniciar_jarras(self):

        tracemalloc.start()
        t0 = time.perf_counter()

        camino, estado_final, visitados, pila = dfs_jarras()

        t1 = time.perf_counter()
        mem_actual, mem_max = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        if estado_final:

            self.pasos = reconstruir_camino(camino, estado_final)

            self.metricas = (
                f"\n--- Métricas DFS ---\n"
                f"Tiempo: {t1-t0:.6f}s\n"
                f"Estados explorados: {visitados}\n"
                f"Pila final: {pila}\n"
                f"Memoria: {mem_max/1024:.2f} KB"
            )

        else:
            self.pasos = ["No se encontró solución"]

        self.index_paso = 0
        self.actualizar_navegacion()
        self.mostrar_paso_jarras()

    def mostrar_paso_jarras(self):

        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete(1.0, tk.END)

        self.resultado_texto.insert(tk.END, str(self.pasos[self.index_paso]))

        if self.index_paso == len(self.pasos)-1:
            self.resultado_texto.insert(tk.END, self.metricas)

        self.resultado_texto.config(state="disabled")

    # -----------------------------
    # LABERINTO
    # -----------------------------

    def iniciar_laberinto(self):

        self.canvas_lab = tk.Canvas(
            self.display_frame,
            width=self.size_lab*self.cell,
            height=self.size_lab*self.cell
        )

        self.canvas_lab.pack()

        resultado = resolver_laberinto_dfs(self.size_lab)

        self.lab = resultado["laberinto"]
        self.visitados = list(resultado["visitados"])
        self.camino = resultado["camino"]

        self.pasos = []

        self.pasos.append(("inicio", None))

        for pos in self.visitados:
            self.pasos.append(("explorar", pos))

        for pos in self.camino:
            self.pasos.append(("camino", pos))

        self.metricas = (
            f"\n--- Métricas DFS ---\n"
            f"Tiempo: {resultado['tiempo']:.6f}s\n"
            f"Nodos explorados: {resultado['nodos_explorados']}\n"
            f"Memoria: {resultado['memoria']:.2f} KB"
        )

        self.index_paso = 0
        self.actualizar_navegacion()

        self.animar()

    def dibujar_base_laberinto(self):

        for i in range(self.size_lab):
            for j in range(self.size_lab):

                color = "white" if self.lab[i][j] == 0 else "black"

                self.canvas_lab.create_rectangle(
                    j*self.cell,
                    i*self.cell,
                    (j+1)*self.cell,
                    (i+1)*self.cell,
                    fill=color,
                    outline="gray"
                )

        self.canvas_lab.create_rectangle(0,0,self.cell,self.cell,fill="green")

        self.canvas_lab.create_rectangle(
            (self.size_lab-1)*self.cell,
            (self.size_lab-1)*self.cell,
            self.size_lab*self.cell,
            self.size_lab*self.cell,
            fill="red"
        )

    def mostrar_paso_laberinto(self):

        self.canvas_lab.delete("all")
        self.dibujar_base_laberinto()

        for i in range(1, self.index_paso+1):

            tipo, pos = self.pasos[i]

            if pos:

                x, y = pos
                color = "blue" if tipo == "explorar" else "yellow"

                self.canvas_lab.create_rectangle(
                    y*self.cell,
                    x*self.cell,
                    (y+1)*self.cell,
                    (x+1)*self.cell,
                    fill=color
                )

        self.lbl_pasos.config(text=f"Paso: {self.index_paso}/{len(self.pasos)-1}")

    # -----------------------------
    # PUZZLE
    # -----------------------------

    def iniciar_puzzle(self):

        self.frame_puzzle = tk.Frame(self.display_frame)
        self.frame_puzzle.pack()

        self.botones = []

        for i in range(9):

            b = tk.Button(self.frame_puzzle,width=4,height=2,font=("Arial",24))
            b.grid(row=i//3,column=i%3)

            self.botones.append(b)

        estado = list(OBJETIVO)

        for _ in range(30):

            i = estado.index(0)

            movimientos = [-3,3,-1,1]

            j = i + random.choice(movimientos)

            if 0 <= j < 9:
                estado[i],estado[j] = estado[j],estado[i]

        estado_inicial = tuple(estado)

        resultado = resolver_puzzle_dfs(estado_inicial)

        self.camino_puzzle = resultado["camino"]

        self.pasos = self.camino_puzzle

        self.metricas = (
            f"\n--- Métricas DFS ---\n"
            f"Tiempo: {resultado['tiempo']:.6f}s\n"
            f"Memoria: {resultado['memoria']:.2f} KB\n"
            f"Pasos totales: {len(self.camino_puzzle)-1}"
        )

        self.index_paso = 0
        self.actualizar_navegacion()

        self.animar()

    def mostrar_paso_puzzle(self):

        estado = self.camino_puzzle[self.index_paso]

        for i in range(9):

            val = estado[i]
            self.botones[i]["text"] = "" if val == 0 else str(val)

        self.lbl_pasos.config(text=f"Paso: {self.index_paso}/{len(self.camino_puzzle)-1}")

    # -----------------------------
    # ANIMACION
    # -----------------------------

    def animar(self):

        if self.index_paso < len(self.pasos)-1:

            self.index_paso += 1
            self.actualizar_navegacion()

            if self.problema_actual=="laberinto":
                self.mostrar_paso_laberinto()

            elif self.problema_actual=="puzzle":
                self.mostrar_paso_puzzle()

            self.after(200, self.animar)

    # -----------------------------
    # CONTROL
    # -----------------------------

    def actualizar_navegacion(self):

        self.btn_siguiente.config(state=tk.NORMAL if self.index_paso < len(self.pasos)-1 else tk.DISABLED)
        self.btn_anterior.config(state=tk.NORMAL if self.index_paso > 0 else tk.DISABLED)

    def paso_siguiente(self):

        if self.index_paso < len(self.pasos)-1:

            self.index_paso += 1
            self.actualizar_navegacion()

            if self.problema_actual=="jarras":
                self.mostrar_paso_jarras()

            elif self.problema_actual=="laberinto":
                self.mostrar_paso_laberinto()

            elif self.problema_actual=="puzzle":
                self.mostrar_paso_puzzle()

    def paso_anterior(self):

        if self.index_paso > 0:

            self.index_paso -= 1
            self.actualizar_navegacion()

            if self.problema_actual=="jarras":
                self.mostrar_paso_jarras()

            elif self.problema_actual=="laberinto":
                self.mostrar_paso_laberinto()

            elif self.problema_actual=="puzzle":
                self.mostrar_paso_puzzle()

    def reiniciar(self):

        self.index_paso = 0
        self.actualizar_navegacion()


if __name__ == "__main__":

    app = AppDFSSelector()
    app.mainloop()