import tkinter as tk
from tkinter import ttk
import time
import tracemalloc

from Jarras import bfs_jarras, reconstruir_camino
from Laberinto import resolver_laberinto
from Puzzle import resolver_puzzle, OBJETIVO, vecinos

PROBLEMAS = {
    "Jarras": "jarras",
    "Laberinto": "laberinto",
    "8-Puzzle": "puzzle"
}

MAX_SIZE = 700

class AppBFSSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BFS - Selector de Problema")
        self.geometry("720x750")

        # Selector de problema
        tk.Label(self, text="Selecciona el problema:").pack(pady=5)
        self.problema_var = tk.StringVar(value="Jarras")
        ttk.Combobox(self, textvariable=self.problema_var, values=list(PROBLEMAS.keys())).pack(pady=5)
        
        # Frame para botones de control
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="Iniciar", command=self.iniciar).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Reiniciar", command=self.reiniciar).pack(side=tk.LEFT, padx=5)
        
        # Botones de navegación
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=5)
        
        self.btn_anterior = tk.Button(nav_frame, text="◀ Anterior", command=self.paso_anterior, state=tk.DISABLED)
        self.btn_siguiente = tk.Button(nav_frame, text="Siguiente ▶", command=self.paso_siguiente, state=tk.DISABLED)
        self.btn_anterior.pack(side=tk.LEFT, padx=10)
        self.btn_siguiente.pack(side=tk.LEFT, padx=10)
        
        self.lbl_pasos = tk.Label(self, text="Paso: 0/0")
        self.lbl_pasos.pack(pady=5)

        # Área de visualización
        self.display_frame = tk.Frame(self)
        self.display_frame.pack(pady=10)
        
        # Canvas para laberinto
        self.canvas_lab = None
        
        # Frame para puzzle
        self.frame_puzzle = None
        self.botones = []
        
        # Área de texto para métricas
        self.resultado_texto = tk.Text(self, height=8, width=80, state="disabled")
        self.resultado_texto.pack(pady=10)

        # Variables de estado
        self.pasos = []
        self.index_paso = 0
        self.metricas = ""
        self.problema_actual = None
        
        # Para laberinto
        self.lab = None
        self.visitados = None
        self.camino = None
        self.size_lab = 10
        self.cell = MAX_SIZE // self.size_lab
        
        # Para puzzle
        self.camino_puzzle = []
        self.estado_inicial_puzzle = None

    def iniciar(self):
        problema = self.problema_var.get()
        self.problema_actual = PROBLEMAS[problema]
        
        # Limpiar área de visualización anterior
        self.limpiar_display()
        
        if self.problema_actual == "jarras":
            self.iniciar_jarras()
        elif self.problema_actual == "laberinto":
            self.iniciar_laberinto()
        elif self.problema_actual == "puzzle":
            self.iniciar_puzzle()
    
    def limpiar_display(self):
        """Limpia el área de visualización según el problema actual"""
        if self.canvas_lab:
            self.canvas_lab.destroy()
            self.canvas_lab = None
        
        if self.frame_puzzle:
            self.frame_puzzle.destroy()
            self.frame_puzzle = None
            self.botones = []

    # -----------------------------
    # Jarras BFS
    # -----------------------------
    def iniciar_jarras(self):
        tracemalloc.start()
        t0 = time.perf_counter()
        camino, estado_final, estados_visitados, tamaño_cola = bfs_jarras()
        t1 = time.perf_counter()
        mem_actual, mem_max = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        if estado_final:
            self.pasos = reconstruir_camino(camino, estado_final)
            self.metricas = (f"\n--- Métricas ---\n"
                             f"Tiempo: {t1-t0:.6f}s | Estados explorados: {estados_visitados} | "
                             f"Cola final: {tamaño_cola} | Memoria: {mem_max/1024:.2f} KB")
        else:
            self.pasos = ["No se encontró solución"]
            self.metricas = ""
        
        self.index_paso = 0
        self.actualizar_navegacion()
        self.mostrar_paso_jarras()

    def mostrar_paso_jarras(self):
        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete(1.0, tk.END)
        
        if self.pasos:
            if isinstance(self.pasos[self.index_paso], str):
                self.resultado_texto.insert(tk.END, self.pasos[self.index_paso])
            else:
                self.resultado_texto.insert(tk.END, f"Paso {self.index_paso + 1}/{len(self.pasos)}:\n")
                self.resultado_texto.insert(tk.END, str(self.pasos[self.index_paso]))
            
            if self.index_paso == len(self.pasos) - 1:
                self.resultado_texto.insert(tk.END, self.metricas)
        
        self.resultado_texto.config(state="disabled")

    # -----------------------------
    # Laberinto BFS con navegación por pasos
    # -----------------------------
    def iniciar_laberinto(self):
        # Crear canvas
        self.canvas_lab = tk.Canvas(self.display_frame, 
                                   width=self.size_lab*self.cell, 
                                   height=self.size_lab*self.cell,
                                   bg='white')
        self.canvas_lab.pack()
        
        # Resolver laberinto
        resultado = resolver_laberinto(self.size_lab)
        self.lab = resultado["laberinto"]
        self.visitados = list(resultado["visitados"])
        self.camino = resultado["camino"]
        
        # Crear lista de pasos para la animación
        self.pasos = []
        
        # Paso 0: Estado inicial (solo verde y rojo)
        self.pasos.append(('inicio', None))
        
        # Pasos intermedios: mostrar exploración
        for i, pos in enumerate(self.visitados):
            if pos != (0,0) and pos != (self.size_lab-1, self.size_lab-1):
                self.pasos.append(('explorar', pos))
        
        # Pasos finales: mostrar camino solución
        for i, pos in enumerate(self.camino):
            if pos != (0,0) and pos != (self.size_lab-1, self.size_lab-1):
                self.pasos.append(('camino', pos))
        
        self.metricas = (f"\n--- Métricas ---\n"
                        f"Tiempo: {resultado['tiempo']:.6f}s | "
                        f"Nodos explorados: {resultado['nodos_explorados']} | "
                        f"Memoria: {resultado['memoria']:.2f} KB")
        
        self.index_paso = 0
        self.actualizar_navegacion()
        self.mostrar_paso_laberinto()

    def dibujar_base_laberinto(self):
        """Dibuja la estructura base del laberinto"""
        for i in range(self.size_lab):
            for j in range(self.size_lab):
                color = "white" if self.lab[i][j] == 0 else "black"
                self.canvas_lab.create_rectangle(
                    j*self.cell, i*self.cell, 
                    (j+1)*self.cell, (i+1)*self.cell, 
                    fill=color, outline="gray"
                )
        
        # Marcar inicio y fin
        self.canvas_lab.create_rectangle(0, 0, self.cell, self.cell, 
                                        fill="green", outline="gray")
        self.canvas_lab.create_rectangle(
            (self.size_lab-1)*self.cell, (self.size_lab-1)*self.cell,
            self.size_lab*self.cell, self.size_lab*self.cell,
            fill="red", outline="gray"
        )

    def mostrar_paso_laberinto(self):
        """Muestra el paso actual del laberinto"""
        self.canvas_lab.delete("all")
        self.dibujar_base_laberinto()
        
        # Dibujar todos los pasos hasta el índice actual
        for i in range(1, self.index_paso + 1):
            if i < len(self.pasos):
                tipo, pos = self.pasos[i]
                if pos:
                    x, y = pos
                    color = "blue" if tipo == 'explorar' else "yellow"
                    self.canvas_lab.create_rectangle(
                        y*self.cell, x*self.cell,
                        (y+1)*self.cell, (x+1)*self.cell,
                        fill=color, outline="gray"
                    )
        
        # Actualizar texto de métricas si estamos al final
        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, f"Paso {self.index_paso}/{len(self.pasos)-1}")
        
        if self.index_paso == len(self.pasos) - 1:
            self.resultado_texto.insert(tk.END, self.metricas)
        
        self.resultado_texto.config(state="disabled")
        self.lbl_pasos.config(text=f"Paso: {self.index_paso}/{len(self.pasos)-1}")

    # -----------------------------
    # Puzzle BFS con navegación por pasos
    # -----------------------------
    def iniciar_puzzle(self):
        # Crear frame para puzzle
        self.frame_puzzle = tk.Frame(self.display_frame)
        self.frame_puzzle.pack()
        
        # Crear botones del puzzle
        self.botones = []
        for i in range(9):
            b = tk.Button(self.frame_puzzle, width=4, height=2, 
                         font=("Arial", 24), state='normal')
            b.grid(row=i//3, column=i%3)
            self.botones.append(b)
        
        # Generar estado inicial aleatorio
        estado = list(OBJETIVO)
        for _ in range(30):
            i = estado.index(0)
            fila, col = i // 3, i % 3
            movimientos = []
            if fila > 0: movimientos.append(-3)
            if fila < 2: movimientos.append(3)
            if col > 0: movimientos.append(-1)
            if col < 2: movimientos.append(1)
            if movimientos:
                j = i + random.choice(movimientos)
                estado[i], estado[j] = estado[j], estado[i]
        
        self.estado_inicial_puzzle = tuple(estado)
        
        # Resolver puzzle
        resultado = resolver_puzzle(self.estado_inicial_puzzle)
        self.camino_puzzle = resultado["camino"]
        self.pasos = self.camino_puzzle
        
        self.metricas = (f"\n--- Métricas ---\n"
                        f"Tiempo: {resultado['tiempo']:.6f}s | "
                        f"Memoria: {resultado['memoria']:.2f} KB | "
                        f"Pasos totales: {resultado['pasos']-1}")
        
        self.index_paso = 0
        self.actualizar_navegacion()
        self.mostrar_paso_puzzle()

    def mostrar_paso_puzzle(self):
        """Muestra el paso actual del puzzle"""
        if self.index_paso < len(self.camino_puzzle):
            estado = self.camino_puzzle[self.index_paso]
            for i in range(9):
                val = estado[i]
                self.botones[i]["text"] = "" if val == 0 else str(val)
        
        # Actualizar texto
        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, f"Paso {self.index_paso}/{len(self.camino_puzzle)-1}")
        
        if self.index_paso == len(self.camino_puzzle) - 1:
            self.resultado_texto.insert(tk.END, self.metricas)
        
        self.resultado_texto.config(state="disabled")
        self.lbl_pasos.config(text=f"Paso: {self.index_paso}/{len(self.camino_puzzle)-1}")

    # -----------------------------
    # Navegación y control
    # -----------------------------
    def actualizar_navegacion(self):
        """Actualiza el estado de los botones de navegación"""
        if len(self.pasos) > 1:
            self.btn_siguiente.config(state=tk.NORMAL if self.index_paso < len(self.pasos)-1 else tk.DISABLED)
            self.btn_anterior.config(state=tk.NORMAL if self.index_paso > 0 else tk.DISABLED)
        else:
            self.btn_siguiente.config(state=tk.DISABLED)
            self.btn_anterior.config(state=tk.DISABLED)

    def paso_siguiente(self):
        if self.index_paso < len(self.pasos) - 1:
            self.index_paso += 1
            self.actualizar_navegacion()
            
            if self.problema_actual == "jarras":
                self.mostrar_paso_jarras()
            elif self.problema_actual == "laberinto":
                self.mostrar_paso_laberinto()
            elif self.problema_actual == "puzzle":
                self.mostrar_paso_puzzle()

    def paso_anterior(self):
        if self.index_paso > 0:
            self.index_paso -= 1
            self.actualizar_navegacion()
            
            if self.problema_actual == "jarras":
                self.mostrar_paso_jarras()
            elif self.problema_actual == "laberinto":
                self.mostrar_paso_laberinto()
            elif self.problema_actual == "puzzle":
                self.mostrar_paso_puzzle()

    def reiniciar(self):
        """Reinicia la animación al primer paso"""
        if self.pasos:
            self.index_paso = 0
            self.actualizar_navegacion()
            
            if self.problema_actual == "jarras":
                self.mostrar_paso_jarras()
            elif self.problema_actual == "laberinto":
                self.mostrar_paso_laberinto()
            elif self.problema_actual == "puzzle":
                self.mostrar_paso_puzzle()


if __name__ == "__main__":
    import random  # Necesario para puzzle
    app = AppBFSSelector()
    app.mainloop()