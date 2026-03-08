import tkinter as tk
from tkinter import ttk
import random
import time
import tracemalloc
from collections import deque

# Intentar importar lógica externa de Jarras
try:
    from Jarras import resolver_jarras_completo, CAP1, CAP2
except ImportError:
    CAP1, CAP2 = 4, 3

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
        self.title("AI Solver - BFS")
        # Ventana más compacta
        self.geometry("750x820")
        self.configure(bg="#f0f2f5")
        
        self.reproduciendo = False
        self.pasos = []
        self.index_paso = 0
        self.tipo_actual = ""
        self.metricas_finales = ""
        
        self.setup_ui()

    def setup_ui(self):
        # Controles superiores
        ctrl_frame = tk.Frame(self, pady=10, bg="#f0f2f5")
        ctrl_frame.pack()

        tk.Label(ctrl_frame, text="Problema:", bg="#f0f2f5", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5)
        self.prob_var = tk.StringVar(value="Laberinto")
        ttk.Combobox(ctrl_frame, textvariable=self.prob_var, values=["Laberinto", "8-Puzzle", "Jarras"], state="readonly", width=12).grid(row=0, column=1, padx=5)

        tk.Label(ctrl_frame, text="Dimensión:", bg="#f0f2f5", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=5)
        self.dim_var = tk.IntVar(value=10)
        ttk.Combobox(ctrl_frame, textvariable=self.dim_var, values=[10, 20, 50], width=5).grid(row=0, column=3, padx=5)

        btn_frame = tk.Frame(self, bg="#f0f2f5")
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="🚀 CALCULAR", command=self.iniciar_resolucion).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⏯ PLAY/PAUSA", command=self.toggle_autoplay).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 RESET", command=self.reset_animacion).pack(side=tk.LEFT, padx=5)

        speed_frame = tk.Frame(self, bg="#f0f2f5")
        speed_frame.pack(pady=5)
        tk.Label(speed_frame, text="Velocidad:", bg="#f0f2f5", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.speed_scale = ttk.Scale(speed_frame, from_=800, to_=10, orient=tk.HORIZONTAL, length=150)
        self.speed_scale.set(300)
        self.speed_scale.pack(side=tk.LEFT, padx=5)

        # REDUCIMOS EL CANVAS DE 600 A 500 PARA QUE TODO SUBA
        self.canvas = tk.Canvas(self, width=500, height=500, bg="white", bd=1, relief="solid", highlightthickness=0)
        self.canvas.pack(pady=5)

        self.lbl_status = tk.Label(self, text="Listo para iniciar", font=("Consolas", 10), bg="#f0f2f5", fg="#5f6368")
        self.lbl_status.pack()

        # ÁREA DE MÉTRICAS (AHORA ESTÁ MÁS ARRIBA)
        self.txt_metrics = tk.Text(self, height=4, width=70, state="disabled", bg="#ffffff", font=("Consolas", 9), relief="flat", padx=10, pady=5)
        self.txt_metrics.pack(pady=5)

    def iniciar_resolucion(self):
        self.reproduciendo = False
        self.tipo_actual = self.prob_var.get()
        self.index_paso = 0
        self.escribir_metricas("Calculando...")
        
        tracemalloc.start()
        t0 = time.perf_counter()

        if self.tipo_actual == "Laberinto":
            n = self.dim_var.get()
            self.lab_data = generar_laberinto_logic(n)
            visitados, camino = bfs_laberinto_logic(self.lab_data)
            self.pasos = [('base', None)] + [('v', p) for p in visitados] + [('c', p) for p in camino]
            # Tamaño basado en 500px
            self.cell_size = 496 // n
        elif self.tipo_actual == "8-Puzzle":
            estado = list(OBJETIVO_PUZZLE)
            random.shuffle(estado) 
            camino, _ = bfs_puzzle_logic(tuple(estado))
            self.pasos = [('p', e) for e in camino]
        elif self.tipo_actual == "Jarras":
            try:
                res = resolver_jarras_completo()
                self.pasos = [('j', e) for e in res["camino"]]
                self.metricas_raw = res
            except:
                self.escribir_metricas("Error: Jarras.py no encontrado")
                return

        t1 = time.perf_counter()
        _, mem_max = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        if self.tipo_actual != "Jarras":
            self.metricas_finales = (f"RESULTADOS: {self.tipo_actual}\n"
                                     f"Tiempo: {t1-t0:.6f} s | Memoria: {mem_max/1024:.2f} KB\n"
                                     f"Nodos: {len(self.pasos)}")
        else:
            self.metricas_finales = (f"RESULTADOS: Jarras\n"
                                     f"Tiempo: {self.metricas_raw['tiempo']:.6f} s | Memoria: {self.metricas_raw['memoria']:.2f} KB\n"
                                     f"Pasos: {self.metricas_raw['pasos']}")
        
        self.escribir_metricas(self.metricas_finales)
        self.actualizar_vista()

    def toggle_autoplay(self):
        if not self.pasos: return
        self.reproduciendo = not self.reproduciendo
        if self.reproduciendo: self.ejecutar_paso()

    def ejecutar_paso(self):
        if self.reproduciendo and self.index_paso < len(self.pasos) - 1:
            self.index_paso += 1
            self.actualizar_vista()
            self.after(int(self.speed_scale.get()), self.ejecutar_paso)
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

    def dibujar_laberinto(self):
        n = self.dim_var.get()
        cs = self.cell_size
        offset = 2 
        for i in range(n):
            for j in range(n):
                color = "#2c3e50" if self.lab_data[i][j] == 1 else "white"
                if (i, j) == (0, 0): color = "#2ecc71"
                if (i, j) == (n-1, n-1): color = "#e74c3c"
                outline = "" if n >= 50 else "#ecf0f1"
                self.canvas.create_rectangle(offset + j*cs, offset + i*cs, offset + (j+1)*cs, offset + (i+1)*cs, fill=color, outline=outline)

        for k in range(1, self.index_paso + 1):
            tipo, pos = self.pasos[k]
            if pos:
                r, c = pos
                color = "#3498db" if tipo == 'v' else "#f1c40f"
                self.canvas.create_rectangle(offset + c*cs, offset + r*cs, offset + (c+1)*cs, offset + (r+1)*cs, fill=color, outline="")

    def dibujar_puzzle(self):
        estado = self.pasos[self.index_paso][1]
        cs = 500 // 3
        for idx, val in enumerate(estado):
            r, c = idx // 3, idx % 3
            x, y = c * cs, r * cs
            if val != 0:
                self.canvas.create_rectangle(x+4, y+4, x+cs-4, y+cs-4, fill="#3498db", outline="white", width=2)
                self.canvas.create_text(x+(cs/2), y+(cs/2), text=str(val), fill="white", font=("Segoe UI", 35, "bold"))
            else:
                self.canvas.create_rectangle(x, y, x+cs, y+cs, fill="#ecf0f1", outline="#bdc3c7")

    def dibujar_jarras(self):
        j1, j2 = self.pasos[self.index_paso][1]
        # Jarra 1 (Base 500px)
        self.canvas.create_rectangle(120, 150, 200, 400, outline="#2c3e50", width=3)
        h1 = (j1 / CAP1) * 250
        self.canvas.create_rectangle(123, 398 - h1, 197, 398, fill="#3498db", outline="")
        self.canvas.create_text(160, 430, text=f"4L: {j1}L", font=("Segoe UI", 10, "bold"))
        # Jarra 2
        self.canvas.create_rectangle(300, 212, 380, 400, outline="#2c3e50", width=3)
        h2 = (j2 / CAP2) * 188
        self.canvas.create_rectangle(303, 398 - h2, 377, 398, fill="#3498db", outline="")
        self.canvas.create_text(340, 430, text=f"3L: {j2}L", font=("Segoe UI", 10, "bold"))
        self.canvas.create_text(250, 80, text=f"Estado: ({j1}, {j2})", font=("Consolas", 14, "bold"))

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