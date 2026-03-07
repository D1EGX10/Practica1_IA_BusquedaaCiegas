import tkinter as tk
import random
import time
from collections import deque

# estado objetivo
objetivo = (1,2,3,
            4,5,6,
            7,8,0)

# -----------------------------
# movimientos posibles
# -----------------------------

def vecinos(estado):

    lista = []

    i = estado.index(0)

    fila = i // 3
    col = i % 3

    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx,dy in dirs:

        nf = fila + dx
        nc = col + dy

        if 0 <= nf < 3 and 0 <= nc < 3:

            j = nf*3 + nc

            nuevo = list(estado)

            nuevo[i],nuevo[j] = nuevo[j],nuevo[i]

            lista.append(tuple(nuevo))

    return lista


# -----------------------------
# BFS
# -----------------------------

def bfs(inicio):

    cola = deque([inicio])
    visitados = set([inicio])
    padre = {}

    while cola:

        estado = cola.popleft()

        if estado == objetivo:
            break

        for v in vecinos(estado):

            if v not in visitados:

                cola.append(v)
                visitados.add(v)
                padre[v] = estado

    camino = []

    nodo = objetivo

    while nodo != inicio:

        camino.append(nodo)
        nodo = padre[nodo]

    camino.append(inicio)

    camino.reverse()

    return camino


# -----------------------------
# interfaz gráfica
# -----------------------------

class PuzzleApp:

    def __init__(self,root):

        self.root = root

        self.root.title("8 Puzzle BFS")

        self.estado = objetivo

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.botones = []

        for i in range(9):

            b = tk.Button(self.frame,
                          width=4,
                          height=2,
                          font=("Arial",24))

            b.grid(row=i//3,column=i%3)

            self.botones.append(b)

        panel = tk.Frame(root)
        panel.pack(pady=10)

        tk.Button(panel,
                  text="Mezclar Puzzle",
                  command=self.mezclar).pack(side=tk.LEFT,padx=10)

        tk.Button(panel,
                  text="Resolver BFS",
                  command=self.resolver).pack(side=tk.LEFT,padx=10)

        self.actualizar()


    def actualizar(self):

        for i in range(9):

            valor = self.estado[i]

            if valor == 0:
                self.botones[i]["text"] = ""
            else:
                self.botones[i]["text"] = str(valor)


    def mezclar(self):

        estado = list(objetivo)

        for _ in range(30):

            i = estado.index(0)

            fila = i // 3
            col = i % 3

            movimientos = []

            if fila > 0: movimientos.append(-3)
            if fila < 2: movimientos.append(3)
            if col > 0: movimientos.append(-1)
            if col < 2: movimientos.append(1)

            j = i + random.choice(movimientos)

            estado[i],estado[j] = estado[j],estado[i]

        self.estado = tuple(estado)

        self.actualizar()


    def resolver(self):

        camino = bfs(self.estado)

        for estado in camino:

            self.estado = estado

            self.actualizar()

            self.root.update()

            time.sleep(0.5)


# -----------------------------
# ejecutar programa
# -----------------------------

root = tk.Tk()

app = PuzzleApp(root)

root.mainloop()