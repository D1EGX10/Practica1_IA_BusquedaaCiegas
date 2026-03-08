from collections import deque
import tracemalloc
import time

# Estado objetivo
OBJETIVO = (1, 2, 3,
            4, 5, 6,
            7, 8, 0)


# -----------------------------
# Generar vecinos
# -----------------------------
def vecinos(estado):

    lista = []

    i = estado.index(0)
    fila, col = i // 3, i % 3

    direcciones = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx, dy in direcciones:

        nf, nc = fila + dx, col + dy

        if 0 <= nf < 3 and 0 <= nc < 3:

            j = nf * 3 + nc

            nuevo = list(estado)

            nuevo[i], nuevo[j] = nuevo[j], nuevo[i]

            lista.append(tuple(nuevo))

    return lista


# -----------------------------
# BFS
# -----------------------------
def bfs_puzzle(inicio):

    cola = deque([inicio])

    visitados = set([inicio])

    padre = {}

    while cola:

        estado = cola.popleft()

        if estado == OBJETIVO:
            break

        for v in vecinos(estado):

            if v not in visitados:

                cola.append(v)

                visitados.add(v)

                padre[v] = estado

    # reconstruir camino
    camino = []

    nodo = OBJETIVO

    while nodo != inicio:

        camino.append(nodo)

        nodo = padre[nodo]

    camino.append(inicio)

    camino.reverse()

    return camino


# -----------------------------
# Resolver puzzle con métricas
# -----------------------------
def resolver_puzzle(inicio):

    tracemalloc.start()

    inicio_tiempo = time.perf_counter()

    camino = bfs_puzzle(inicio)

    fin_tiempo = time.perf_counter()

    memoria_actual, memoria_max = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    return {
        "camino": camino,
        "tiempo": fin_tiempo - inicio_tiempo,
        "memoria": memoria_max / 1024,
        "pasos": len(camino)
    }