import tkinter as tk
from tkinter import ttk
import random
import time
import tracemalloc
from collections import deque

# Importamos la lógica de jarras desde el otro archivo
from Jarras import resolver_jarras_completo, CAP1, CAP2

# --- LÓGICA DEL PUZZLE ---
OBJETIVO_PUZZLE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def vecinos_puzzle(estado):
    lista = []
    i = estado.index(0)
    fila, col = i // 3, i % 3
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nf, nc = fila + dx, col + dy
        if 0 <= nf < 3 and 0 <= nc < 3:
            j = nf * 3 + nc
            nuevo = list(estado)
            nuevo[i], nuevo[j] = nuevo[j], nuevo[i]
            lista.append(tuple(nuevo))
    return lista

def bfs_puzzle_logic(inicio):
    cola = deque([inicio])
    visitados = {inicio}
    padre = {}
    while cola:
        estado = cola.popleft()
        if estado == OBJETIVO_PUZZLE: break
        for v in vecinos_puzzle(estado):
            if v not in visitados:
                cola.append(v)
                visitados.add(v)
                padre[v] = estado
    camino = []
    nodo = OBJETIVO_PUZZLE
    while nodo != inicio:
        camino.append(nodo)
        nodo = padre[nodo]
    camino.append(inicio)
    camino.reverse()
    return camino, len(visitados)

# --- LÓGICA DEL LABERINTO ---
def generar_laberinto_logic(n):
    lab = [[1 for _ in range(n)] for _ in range(n)]
    x, y = 0, 0
    camino_seguro = [(0, 0)]
    while (x, y) != (n - 1, n - 1):
        if x < n - 1 and (y == n - 1 or random.random() < 0.5): x += 1
        elif y < n - 1: y += 1
        camino_seguro.append((x, y))
    for i, j in camino_seguro: lab[i][j] = 0
    for i in range(n):
        for j in range(n):
            if (i, j) not in camino_seguro:
                lab[i][j] = 1 if random.random() < 0.25 else 0
    lab[0][0], lab[n-1][n-1] = 0, 0
    return lab

def bfs_laberinto_logic(lab):
    n = len(lab)
    inicio, meta = (0, 0), (n - 1, n - 1)
    cola = deque([inicio])
    visitados_orden, visitados_set = [], {inicio}
    padre = {}
    while cola:
        curr = cola.popleft()
        visitados_orden.append(curr)
        if curr == meta: break
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = curr[0] + dx, curr[1] + dy
            if 0 <= nx < n and 0 <= ny < n and lab[nx][ny] == 0 and (nx, ny) not in visitados_set:
                cola.append((nx, ny)); visitados_set.add((nx, ny)); padre[(nx, ny)] = curr
    camino = []
    if meta in padre:
        nodo = meta
        while nodo != inicio: camino.append(nodo); nodo = padre[nodo]
        camino.append(inicio); camino.reverse()
    return visitados_orden, camino

# --- INTERFAZ PRINCIPAL ---
class AppBFSSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Solver - Laberinto, Puzzle & Jarras")
        self.geometry("850x950")
        self.configure(bg="#f0f2f5")
        self.reproduciendo = False
        self.pasos = []
        self.index_paso = 0
        self.tipo_actual = ""
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#1a73e8", pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, text="Visualizador de Algoritmos BFS", fg="white", bg="#1a73e8", font=("Segoe UI", 16, "bold")).pack()

        ctrl_frame = tk.Frame(self, pady=10)
        ctrl_frame.pack()

        tk.Label(ctrl_frame, text="Problema:").grid(row=0, column=0, padx=5)
        self.prob_var = tk.StringVar(value="Laberinto")
        ttk.Combobox(ctrl_frame, textvariable=self.prob_var, values=["Laberinto", "8-Puzzle", "Jarras"], state="readonly").grid(row=0, column=1, padx=5)

        tk.Label(ctrl_frame, text="Dimensión (Lab):").grid(row=0, column=2, padx=5)
        self.dim_var = tk.IntVar(value=10)
        ttk.Combobox(ctrl_frame, textvariable=self.dim_var, values=[10, 20, 50], width=5).grid(row=0, column=3, padx=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="🚀 CALCULAR", command=self.iniciar_resolucion).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⏯ PLAY/PAUSA", command=self.toggle_autoplay).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 RESET", command=self.reset_animacion).pack(side=tk.LEFT, padx=5)

        tk.Label(self, text="Velocidad de Animación:").pack()
        self.speed_scale = ttk.Scale(self, from_=800, to_=50, orient=tk.HORIZONTAL, length=200)
        self.speed_scale.set(300)
        self.speed_scale.pack()

        self.canvas = tk.Canvas(self, width=600, height=600, bg="white", bd=2, relief="ridge")
        self.canvas.pack(pady=15)

        self.lbl_status = tk.Label(self, text="Esperando inicio...", font=("Consolas", 11), fg="#5f6368")
        self.lbl_status.pack()

        self.txt_metrics = tk.Text(self, height=5, width=70, state="disabled", bg="#f8f9fa", font=("Consolas", 10))
        self.txt_metrics.pack(pady=10)

    def iniciar_resolucion(self):
        self.reproduciendo = False
        self.tipo_actual = self.prob_var.get()
        self.index_paso = 0
        tracemalloc.start()
        t0 = time.perf_counter()

        if self.tipo_actual == "Laberinto":
            n = self.dim_var.get()
            self.lab_data = generar_laberinto_logic(n)
            visitados, camino = bfs_laberinto_logic(self.lab_data)
            self.pasos = [('base', None)] + [('v', p) for p in visitados] + [('c', p) for p in camino]
            self.cell_size = 600 // n
        elif self.tipo_actual == "8-Puzzle":
            estado = list(OBJETIVO_PUZZLE)
            random.shuffle(estado) 
            camino, _ = bfs_puzzle_logic(tuple(estado))
            self.pasos = [('p', e) for e in camino]
        elif self.tipo_actual == "Jarras":
            res = resolver_jarras_completo()
            self.pasos = [('j', e) for e in res["camino"]]
            self.metricas_data = res

        t1 = time.perf_counter()
        _, mem_max = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        if self.tipo_actual != "Jarras":
            self.metricas = f"Tiempo: {t1-t0:.4f}s | Memoria: {mem_max/1024:.1f}KB | Pasos: {len(self.pasos)}"
        else:
            self.metricas = f"Tiempo: {self.metricas_data['tiempo']:.4f}s | Memoria: {self.metricas_data['memoria']:.1f}KB | Pasos: {self.metricas_data['pasos']}"
        
        self.actualizar_vista()

    def toggle_autoplay(self):
        if not self.pasos: return
        self.reproduciendo = not self.reproduciendo
        if self.reproduciendo: self.ejecutar_paso()

    def ejecutar_paso(self):
        if self.reproduciendo and self.index_paso < len(self.pasos) - 1:
            self.index_paso += 1
            self.actualizar_vista()
            delay = int(self.speed_scale.get())
            self.after(delay, self.ejecutar_paso)
        else:
            self.reproduciendo = False

    def actualizar_vista(self):
        self.canvas.delete("all")
        if self.tipo_actual == "Laberinto":
            self.dibujar_laberinto()
        elif self.tipo_actual == "8-Puzzle":
            self.dibujar_puzzle()
        elif self.tipo_actual == "Jarras":
            self.dibujar_jarras()
        
        self.lbl_status.config(text=f"Progreso: {self.index_paso}/{len(self.pasos)-1}")
        if self.index_paso == len(self.pasos)-1:
            self.escribir_metricas(self.metricas)

    def dibujar_laberinto(self):
        n = self.dim_var.get()
        cs = self.cell_size
        for i in range(n):
            for j in range(n):
                color = "#202124" if self.lab_data[i][j] == 1 else "white"
                if (i, j) == (0, 0): color = "#34a853"
                if (i, j) == (n-1, n-1): color = "#ea4335"
                self.canvas.create_rectangle(j*cs, i*cs, (j+1)*cs, (i+1)*cs, fill=color, outline="" if n>20 else "#bdc3c7")
        for k in range(1, self.index_paso + 1):
            tipo, pos = self.pasos[k]
            if pos:
                r, c = pos
                color = "#8ab4f8" if tipo == 'v' else "#fbbc04"
                self.canvas.create_rectangle(c*cs, r*cs, (c+1)*cs, (r+1)*cs, fill=color, outline="")

    def dibujar_puzzle(self):
        estado = self.pasos[self.index_paso][1]
        for idx, val in enumerate(estado):
            r, c = idx // 3, idx % 3
            x1, y1 = c * 200, r * 200
            if val != 0:
                self.canvas.create_rectangle(x1+5, y1+5, x1+195, y1+195, fill="#1a73e8", outline="white", width=2)
                self.canvas.create_text(x1+100, y1+100, text=str(val), fill="white", font=("Segoe UI", 40, "bold"))
            else:
                self.canvas.create_rectangle(x1, y1, x1+200, y1+200, fill="#f8f9fa", outline="#bdc3c7")

    def dibujar_jarras(self):
        # Dibujar Jarras y Agua
        jarra1_val, jarra2_val = self.pasos[self.index_paso][1]
        
        # Jarra 1 (4L)
        self.canvas.create_rectangle(150, 150, 250, 450, outline="black", width=3)
        alto_agua1 = (jarra1_val / CAP1) * 300
        self.canvas.create_rectangle(153, 448 - alto_agua1, 248, 448, fill="#3498db", outline="")
        self.canvas.create_text(200, 480, text=f"Jarra 4L\n({jarra1_val}L)", font=("Arial", 12, "bold"))

        # Jarra 2 (3L)
        self.canvas.create_rectangle(350, 225, 450, 450, outline="black", width=3)
        alto_agua2 = (jarra2_val / CAP2) * 225
        self.canvas.create_rectangle(353, 448 - alto_agua2, 448, 448, fill="#3498db", outline="")
        self.canvas.create_text(400, 480, text=f"Jarra 3L\n({jarra2_val}L)", font=("Arial", 12, "bold"))
        
        self.canvas.create_text(300, 100, text=f"Estado actual: {jarra1_val, jarra2_val}", font=("Consolas", 14))

    def reset_animacion(self):
        self.reproduciendo = False
        self.index_paso = 0
        self.actualizar_vista()

    def escribir_metricas(self, txt):
        self.txt_metrics.config(state="normal")
        self.txt_metrics.delete(1.0, tk.END)
        self.txt_metrics.insert(tk.END, txt)
        self.txt_metrics.config(state="disabled")

if __name__ == "__main__":
    app = AppBFSSelector()
    app.mainloop()