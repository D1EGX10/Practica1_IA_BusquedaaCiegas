import random
import time
import tracemalloc


def dfs(lab):

    n = len(lab)

    inicio = (0,0)
    meta = (n-1,n-1)

    pila = [inicio]

    visitados = []
    visitados_set = {inicio}

    padre = {}

    movimientos = [(0,1),(1,0),(0,-1),(-1,0)]

    while pila:

        x,y = pila.pop()

        visitados.append((x,y))

        if (x,y) == meta:
            break

        for dx,dy in movimientos:

            nx = x + dx
            ny = y + dy

            if 0 <= nx < n and 0 <= ny < n:

                if lab[nx][ny] == 0 and (nx,ny) not in visitados_set:

                    pila.append((nx,ny))
                    visitados_set.add((nx,ny))
                    padre[(nx,ny)] = (x,y)

    camino = []

    nodo = meta

    while nodo in padre:
        camino.append(nodo)
        nodo = padre[nodo]

    camino.append(inicio)
    camino.reverse()

    return visitados, camino


def generar_laberinto(n):

    lab = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):

            if (i,j) not in [(0,0),(n-1,n-1)]:

                if random.random() < 0.30:
                    lab[i][j] = 1

    return lab


def resolver_laberinto_dfs(size):

    lab = generar_laberinto(size)

    tracemalloc.start()
    t0 = time.perf_counter()

    visitados, camino = dfs(lab)

    t1 = time.perf_counter()

    mem_actual, mem_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "laberinto": lab,
        "visitados": visitados,
        "camino": camino,
        "tiempo": t1-t0,
        "nodos_explorados": len(visitados),
        "memoria": mem_max/1024
    }