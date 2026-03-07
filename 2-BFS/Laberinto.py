import tkinter as tk
import tracemalloc
import random
import time
from collections import deque

MAX_SIZE = 700


# -----------------------------
# Generar laberinto con solución
# -----------------------------

def generar_laberinto(n):

    lab = [[1 for _ in range(n)] for _ in range(n)]

    x,y = 0,0
    camino = [(0,0)]

    while (x,y) != (n-1,n-1):

        if random.random() < 0.5 and x < n-1:
            x += 1
        elif y < n-1:
            y += 1
        elif x < n-1:
            x += 1

        camino.append((x,y))

    for i,j in camino:
        lab[i][j] = 0

    for i in range(n):
        for j in range(n):

            if (i,j) not in camino and random.random() < 0.3:
                lab[i][j] = 1
            else:
                lab[i][j] = 0

    lab[0][0] = 0
    lab[n-1][n-1] = 0

    return lab


# -----------------------------
# BFS
# -----------------------------

def bfs(lab):

    n = len(lab)

    inicio = (0,0)
    meta = (n-1,n-1)

    cola = deque([inicio])
    visitados = set([inicio])
    padre = {}

    movimientos = [(0,1),(1,0),(0,-1),(-1,0)]

    while cola:

        x,y = cola.popleft()

        if (x,y) == meta:
            break

        for dx,dy in movimientos:

            nx = x + dx
            ny = y + dy

            if 0 <= nx < n and 0 <= ny < n:

                if lab[nx][ny] == 0 and (nx,ny) not in visitados:

                    cola.append((nx,ny))
                    visitados.add((nx,ny))
                    padre[(nx,ny)] = (x,y)

    camino = []
    nodo = meta

    while nodo != inicio:

        camino.append(nodo)
        nodo = padre[nodo]

    camino.append(inicio)
    camino.reverse()

    return visitados,camino


# -----------------------------
# Interfaz
# -----------------------------

class LaberintoApp:

    def __init__(self,root):

        self.root = root
        self.root.title("Laberinto BFS")

        self.size = 20
        self.cell = MAX_SIZE // self.size

        self.canvas = tk.Canvas(root,
                                width=self.size*self.cell,
                                height=self.size*self.cell)

        self.canvas.pack()

        panel = tk.Frame(root)
        panel.pack(pady=10)

        tk.Button(panel,text="10x10",
                  command=lambda:self.cambiar(10)).pack(side=tk.LEFT,padx=5)

        tk.Button(panel,text="20x20",
                  command=lambda:self.cambiar(20)).pack(side=tk.LEFT,padx=5)

        tk.Button(panel,text="50x50",
                  command=lambda:self.cambiar(50)).pack(side=tk.LEFT,padx=5)

        tk.Button(panel,text="Nuevo Laberinto",
                  command=self.generar).pack(side=tk.LEFT,padx=5)

        tk.Button(panel,text="Resolver BFS",
                  command=self.resolver).pack(side=tk.LEFT,padx=5)


        # Barra de información
        self.info = tk.Label(root,
                             text="Tiempo: - | Memoria: - | Nodos explorados: -",
                             font=("Arial",12),
                             bg="#eeeeee",
                             width=60,
                             height=2)

        self.info.pack(pady=5)


        self.laberinto = generar_laberinto(self.size)

        self.dibujar()


    def cambiar(self,n):

        self.size = n
        self.cell = MAX_SIZE // n

        self.canvas.config(width=n*self.cell,
                           height=n*self.cell)

        self.laberinto = generar_laberinto(n)

        self.dibujar()

        self.info.config(text="Tiempo: - | Memoria: - | Nodos explorados: -")


    def generar(self):

        self.laberinto = generar_laberinto(self.size)

        self.dibujar()

        self.info.config(text="Tiempo: - | Memoria: - | Nodos explorados: -")


    def dibujar(self):

        self.canvas.delete("all")

        for i in range(self.size):
            for j in range(self.size):

                color = "white"

                if self.laberinto[i][j] == 1:
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

        self.canvas.create_rectangle((self.size-1)*self.cell,
                                     (self.size-1)*self.cell,
                                     self.size*self.cell,
                                     self.size*self.cell,
                                     fill="red")


# -----------------------------
# Resolver con medición
# -----------------------------

    def resolver(self):

        tracemalloc.start()

        inicio = time.perf_counter()

        visitados,camino = bfs(self.laberinto)

        fin = time.perf_counter()

        memoria_actual, memoria_pico = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        tiempo = fin - inicio
        memoria_mb = memoria_pico / 10**6
        nodos = len(visitados)


        # mostrar en interfaz
        self.info.config(
            text=f"Tiempo de ejecución: {tiempo:.6f} s | Memoria pico: {memoria_mb:.3f}"
        )


        for x,y in visitados:

            self.canvas.create_rectangle(
                y*self.cell,
                x*self.cell,
                (y+1)*self.cell,
                (x+1)*self.cell,
                fill="blue"
            )

            self.root.update()
            time.sleep(0.001)


        for x,y in camino:

            self.canvas.create_rectangle(
                y*self.cell,
                x*self.cell,
                (y+1)*self.cell,
                (x+1)*self.cell,
                fill="yellow"
            )

            self.root.update()
            time.sleep(0.02)


# -----------------------------
# Ejecutar
# -----------------------------

root = tk.Tk()

app = LaberintoApp(root)

root.mainloop()