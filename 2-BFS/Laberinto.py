import tracemalloc
import random
import time
from collections import deque

def generar_laberinto(n):

    lab = [[0 if random.random() > 0.3 else 1 for _ in range(n)] for _ in range(n)]

    lab[0][0] = 0
    lab[n-1][n-1] = 0

    return lab


def bfs_laberinto(lab):

    n = len(lab)

    inicio = (0,0)
    meta = (n-1,n-1)

    cola = deque([inicio])
    visitados = {inicio}

    padre = {}

    pasos_exploracion = []

    movimientos = [(0,1),(1,0),(0,-1),(-1,0)]

    while cola:

        x,y = cola.popleft()

        pasos_exploracion.append((x,y))

        if (x,y) == meta:
            break

        for dx,dy in movimientos:

            nx,ny = x+dx,y+dy

            if 0<=nx<n and 0<=ny<n and lab[nx][ny]==0 and (nx,ny) not in visitados:

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

    return pasos_exploracion, camino


def resolver_laberinto(n):

    lab = generar_laberinto(n)

    tracemalloc.start()

    t0 = time.perf_counter()

    exploracion, camino = bfs_laberinto(lab)

    t1 = time.perf_counter()

    mem = tracemalloc.get_traced_memory()[1]

    tracemalloc.stop()

    return {
        "laberinto": lab,
        "exploracion": exploracion,
        "camino": camino,
        "tiempo": t1 - t0,
        "memoria": mem/1024,
        "nodos_explorados": len(exploracion)
    }