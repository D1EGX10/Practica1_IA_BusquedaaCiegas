import tkinter as tk
from tkinter import ttk
import random

# IMPORTACIÓN DE TUS MÓDULOS
from Laberinto import resolver_laberinto_dfs
from Puzzle import resolver_puzzle_dfs, OBJETIVO
from Jarras import resolver_jarras_dfs

COLORS = {
    'fondo': "#f0f2f5", 'pared': "#2c3e50", 'pasillo': "white",
    'visitado': "#8ab4f8", 'camino': "#f1c40f", 'inicio': "#2ecc71",
    'fin': "#e74c3c", 'agua': "#3498db"
}

class AppDFSSolver(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Solver - DFS Edition")
        self.geometry("800x820")
        self.configure(bg=COLORS['fondo'])
        self.pasos = []; self.index_paso = 0; self.reproduciendo = False
        self.setup_ui()

    def setup_ui(self):
        ctrl = tk.Frame(self, pady=10, bg=COLORS['fondo']); ctrl.pack()
        tk.Label(ctrl, text="Problema:", bg=COLORS['fondo'], font=("Arial", 10, "bold")).grid(row=0, column=0)
        self.prob_var = tk.StringVar(value="Laberinto")
        ttk.Combobox(ctrl, textvariable=self.prob_var, values=["Laberinto", "8-Puzzle", "Jarras"], state="readonly").grid(row=0, column=1, padx=5)
        
        tk.Label(ctrl, text="Dimensión:", bg=COLORS['fondo'], font=("Arial", 10, "bold")).grid(row=0, column=2)
        self.dim_var = tk.IntVar(value=10)
        ttk.Combobox(ctrl, textvariable=self.dim_var, values=[10, 20, 50], width=5).grid(row=0, column=3, padx=5)

        btns = tk.Frame(self, bg=COLORS['fondo']); btns.pack(pady=5)
        ttk.Button(btns, text="🚀 CALCULAR", command=self.resolver).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="⏯ PLAY", command=self.toggle).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="🔄 RESET", command=self.reset).pack(side=tk.LEFT, padx=5)

        self.speed = ttk.Scale(self, from_=500, to_=5, orient=tk.HORIZONTAL, length=200)
        self.speed.set(100); self.speed.pack()

        self.canvas = tk.Canvas(self, width=500, height=500, bg="white", bd=1, relief="solid")
        self.canvas.pack(pady=10)

        self.lbl_status = tk.Label(self, text="Paso: 0/0", font=("Consolas", 11), bg=COLORS['fondo']); self.lbl_status.pack()
        self.txt_metrics = tk.Text(self, height=5, width=70, state="disabled", font=("Consolas", 10)); self.txt_metrics.pack()

    def resolver(self):
        self.reproduciendo = False; self.index_paso = 0
        tipo = self.prob_var.get()
        if tipo == "Laberinto":
            res = resolver_laberinto_dfs(self.dim_var.get())
            self.lab_data = res["laberinto"]
            self.pasos = [('v', p) for p in res["visitados"]] + [('c', p) for p in res["camino"]]
            self.cell_size = 496 // self.dim_var.get()
        elif tipo == "8-Puzzle":
            inicio = list(OBJETIVO); random.shuffle(inicio)
            res = resolver_puzzle_dfs(tuple(inicio))
            self.pasos = [('p', e) for e in res["camino"]]
        else:
            res = resolver_jarras_dfs()
            self.pasos = [('j', e) for e in res["camino"]]
        
        self.escribir(f"--- MÉTRICAS DFS ---\nTiempo: {res['tiempo']:.6f} s\nMemoria: {res['memoria']:.2f} KB")
        self.dibujar()

    def toggle(self):
        self.reproduciendo = not self.reproduciendo
        if self.reproduciendo: self.animar()

    def animar(self):
        if self.reproduciendo and self.index_paso < len(self.pasos)-1:
            self.index_paso += 1; self.dibujar()
            self.after(int(self.speed.get()), self.animar)

    def dibujar(self):
        self.canvas.delete("all")
        tipo = self.prob_var.get(); off = 2
        if tipo == "Laberinto":
            cs = self.cell_size; n = self.dim_var.get()
            for i in range(n):
                for j in range(n):
                    c = COLORS['pared'] if self.lab_data[i][j] == 1 else COLORS['pasillo']
                    if (i,j) == (0,0): c = COLORS['inicio']
                    if (i,j) == (n-1,n-1): c = COLORS['fin']
                    self.canvas.create_rectangle(off+j*cs, off+i*cs, off+(j+1)*cs, off+(i+1)*cs, fill=c, outline="" if n>=50 else "#eee")
            for k in range(self.index_paso + 1):
                t, p = self.pasos[k]
                col = COLORS['visitado'] if t == 'v' else COLORS['camino']
                self.canvas.create_rectangle(off+p[1]*cs, off+p[0]*cs, off+(p[1]+1)*cs, off+(p[0]+1)*cs, fill=col, outline="")
        elif tipo == "8-Puzzle":
            estado = self.pasos[self.index_paso][1]; cs = 500 // 3
            for i, v in enumerate(estado):
                r, c = i//3, i%3
                if v != 0:
                    self.canvas.create_rectangle(c*cs+5, r*cs+5, (c+1)*cs-5, (r+1)*cs-5, fill=COLORS['agua'], outline="white")
                    self.canvas.create_text(c*cs+cs/2, r*cs+cs/2, text=str(v), fill="white", font=("Arial", 40, "bold"))
        elif tipo == "Jarras":
            j1, j2 = self.pasos[self.index_paso][1]
            self.canvas.create_rectangle(120, 150, 220, 400, outline=COLORS['pared'], width=3)
            self.canvas.create_rectangle(123, 398-(j1/4)*250, 217, 398, fill=COLORS['agua'], outline="")
            self.canvas.create_rectangle(300, 212, 380, 400, outline=COLORS['pared'], width=3)
            self.canvas.create_rectangle(303, 398-(j2/3)*188, 377, 398, fill=COLORS['agua'], outline="")
            self.canvas.create_text(250, 80, text=f"({j1}L, {j2}L)", font=("Consolas", 16, "bold"))
        self.lbl_status.config(text=f"Paso: {self.index_paso}/{len(self.pasos)-1}")

    def reset(self): self.reproduciendo = False; self.index_paso = 0; self.dibujar()
    def escribir(self, t):
        self.txt_metrics.config(state="normal"); self.txt_metrics.delete(1.0, tk.END)
        self.txt_metrics.insert(tk.END, t); self.txt_metrics.config(state="disabled")

if __name__ == "__main__": AppDFSSolver().mainloop()