import tkinter as tk
from tkinter import ttk
import time
import tracemalloc
from Jarras import bfs_jarras, reconstruir_camino

PROBLEMAS = {
    "Jarras": "jarras",
    "BFS Grafo": "grafo",      # pendiente
    "Laberinto": "laberinto",  # pendiente
    "8-Puzzle": "puzzle"       # pendiente
}

class AppBFS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BFS - Paso a paso")
        self.geometry("600x500")

        # Selección de problema
        self.problema_var = tk.StringVar(value="Jarras")
        tk.Label(self, text="Selecciona el problema:").pack()
        ttk.Combobox(self, textvariable=self.problema_var, values=list(PROBLEMAS.keys())).pack(pady=5)

        # Área de resultados
        self.resultado_texto = tk.Text(self, height=20, width=70, state="disabled")
        self.resultado_texto.pack(pady=10)

        # Botones de control
        frame_botones = tk.Frame(self)
        frame_botones.pack()
        self.btn_anterior = tk.Button(frame_botones, text="Anterior", command=self.paso_anterior)
        self.btn_anterior.grid(row=0, column=0, padx=5)
        self.btn_siguiente = tk.Button(frame_botones, text="Siguiente", command=self.paso_siguiente)
        self.btn_siguiente.grid(row=0, column=1, padx=5)
        self.btn_iniciar = tk.Button(self, text="Iniciar BFS", command=self.iniciar)
        self.btn_iniciar.pack(pady=10)

        # Variables para paso a paso
        self.pasos = []
        self.index_paso = 0
        self.metricas = ""
        self.mostrar_metricas = False

    def iniciar(self):
        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.config(state="disabled")
        self.pasos = []
        self.index_paso = 0
        self.metricas = ""
        self.mostrar_metricas = False
        self.btn_siguiente.config(text="Siguiente", state=tk.NORMAL)

        problema = self.problema_var.get()

        if PROBLEMAS[problema] == "jarras":
            # Medición de tiempo y memoria
            tracemalloc.start()
            inicio_tiempo = time.perf_counter()
            camino, estado_final, estados_visitados, tamaño_cola = bfs_jarras()
            fin_tiempo = time.perf_counter()
            memoria_actual, memoria_max = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            if estado_final:
                self.pasos = reconstruir_camino(camino, estado_final)
                self.metricas = (f"\n--- Métricas ---\n"
                                 f"Tiempo de ejecución: {fin_tiempo - inicio_tiempo:.6f} s\n"
                                 f"Estados explorados: {estados_visitados}\n"
                                 f"Tamaño final de la cola: {tamaño_cola}\n"
                                 f"Memoria máxima usada: {memoria_max/1024:.2f} KB")
            else:
                self.pasos = ["No se encontró solución"]

        else:
            self.pasos = ["Problema pendiente de implementar"]

        self.mostrar_paso()

    def mostrar_paso(self):
        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete(1.0, tk.END)
        if self.pasos:
            self.resultado_texto.insert(tk.END, f"Paso {self.index_paso + 1}/{len(self.pasos)}:\n")
            self.resultado_texto.insert(tk.END, str(self.pasos[self.index_paso]))
            # Último paso: mostrar métricas y cambiar botón
            if self.index_paso == len(self.pasos) - 1:
                self.resultado_texto.insert(tk.END, self.metricas)
                self.btn_siguiente.config(text="Final")
        self.resultado_texto.config(state="disabled")

    def paso_siguiente(self):
        if self.index_paso < len(self.pasos) - 1:
            self.index_paso += 1
            self.mostrar_paso()

    def paso_anterior(self):
        if self.index_paso > 0:
            self.index_paso -= 1
            self.mostrar_paso()


if __name__ == "__main__":
    app = AppBFS()
    app.mainloop()