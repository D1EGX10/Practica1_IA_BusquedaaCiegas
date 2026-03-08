import tracemalloc
import random
import time
from collections import deque
import tkinter as tk

MAX_SIZE = 700  # Tamaño máximo del canvas

# -----------------------------
# Generar laberinto con solución
# -----------------------------
def generar_laberinto(n):
    lab = [[1 for _ in range(n)] for _ in range(n)]
    x, y = 0, 0
    camino = [(0, 0)]

    while (x, y) != (n - 1, n - 1):
        if random.random() < 0.5 and x < n - 1:
            x += 1
        elif y < n - 1:
            y += 1
        elif x < n - 1:
            x += 1
        camino.append((x, y))

    for i, j in camino:
        lab[i][j] = 0

    for i in range(n):
        for j in range(n):
            if (i, j) not in camino and random.random() < 0.3:
                lab[i][j] = 1
            else:
                lab[i][j] = 0

    lab[0][0] = 0
    lab[n - 1][n - 1] = 0
    return lab

# -----------------------------
# BFS
# -----------------------------
def bfs_laberinto(lab):
    n = len(lab)
    inicio, meta = (0, 0), (n - 1, n - 1)
    cola = deque([inicio])
    visitados = set([inicio])
    padre = {}
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while cola:
        x, y = cola.popleft()
        if (x, y) == meta:
            break
        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and lab[nx][ny] == 0 and (nx, ny) not in visitados:
                cola.append((nx, ny))
                visitados.add((nx, ny))
                padre[(nx, ny)] = (x, y)

    # Reconstruir camino
    camino = []
    nodo = meta
    while nodo != inicio:
        camino.append(nodo)
        nodo = padre[nodo]
    camino.append(inicio)
    camino.reverse()
    return visitados, camino

# -----------------------------
# Resolver con medición
# -----------------------------
def resolver_laberinto(n):
    lab = generar_laberinto(n)
    tracemalloc.start()
    t0 = time.perf_counter()
    visitados, camino = bfs_laberinto(lab)
    t1 = time.perf_counter()
    mem_actual, mem_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "laberinto": lab,
        "visitados": visitados,
        "camino": camino,
        "tiempo": t1 - t0,
        "memoria": mem_max / 1024,  # KB
        "nodos_explorados": len(visitados)
    }