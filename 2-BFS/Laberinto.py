import tracemalloc
import random
import time
from collections import deque

def generar_laberinto(n):
    # Crear laberinto lleno de paredes (1)
    lab = [[1 for _ in range(n)] for _ in range(n)]
    x, y = 0, 0
    camino_garantizado = [(0, 0)]

    # Crear un camino aleatorio hacia la meta para asegurar solución
    while (x, y) != (n - 1, n - 1):
        if x < n - 1 and (y == n - 1 or random.random() < 0.5):
            x += 1
        elif y < n - 1:
            y += 1
        camino_garantizado.append((x, y))

    # Convertir camino garantizado en pasillos (0)
    for i, j in camino_garantizado:
        lab[i][j] = 0

    # Llenar el resto aleatoriamente
    for i in range(n):
        for j in range(n):
            if (i, j) not in camino_garantizado:
                # 30% de probabilidad de ser pared
                lab[i][j] = 1 if random.random() < 0.3 else 0

    # Asegurar extremos libres
    lab[0][0] = 0
    lab[n - 1][n - 1] = 0
    return lab

def bfs_laberinto(lab):
    n = len(lab)
    inicio, meta = (0, 0), (n - 1, n - 1)
    cola = deque([inicio])
    visitados_orden = [] # Para animar en orden de exploración
    visitados_set = {inicio}
    padre = {}
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while cola:
        curr = cola.popleft()
        visitados_orden.append(curr)
        
        if curr == meta:
            break

        for dx, dy in movimientos:
            nx, ny = curr[0] + dx, curr[1] + dy
            if 0 <= nx < n and 0 <= ny < n and lab[nx][ny] == 0 and (nx, ny) not in visitados_set:
                cola.append((nx, ny))
                visitados_set.add((nx, ny))
                padre[(nx, ny)] = curr

    # Reconstruir camino
    camino_final = []
    if meta in padre or meta == inicio:
        nodo = meta
        while nodo != inicio:
            camino_final.append(nodo)
            nodo = padre[nodo]
        camino_final.append(inicio)
        camino_final.reverse()
        
    return visitados_orden, camino_final

def resolver_laberinto(n):
    lab = generar_laberinto(n)
    tracemalloc.start()
    t0 = time.perf_counter()
    visitados, camino = bfs_laberinto(lab)
    t1 = time.perf_counter()
    _, mem_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "laberinto": lab,
        "visitados": visitados,
        "camino": camino,
        "tiempo": t1 - t0,
        "memoria": mem_max / 1024,
        "nodos_explorados": len(visitados)
    }