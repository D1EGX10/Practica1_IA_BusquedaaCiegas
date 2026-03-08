import time
import tracemalloc

OBJETIVO = (1,2,3,4,5,6,7,8,0)


def vecinos(estado):

    i = estado.index(0)

    movimientos = []

    fila = i // 3
    col = i % 3

    if fila > 0:
        movimientos.append(i-3)

    if fila < 2:
        movimientos.append(i+3)

    if col > 0:
        movimientos.append(i-1)

    if col < 2:
        movimientos.append(i+1)

    estados = []

    for j in movimientos:

        nuevo = list(estado)

        nuevo[i], nuevo[j] = nuevo[j], nuevo[i]

        estados.append(tuple(nuevo))

    return estados


def dfs(inicial):

    pila = [inicial]

    visitados = set()

    padre = {inicial:None}

    while pila:

        estado = pila.pop()

        if estado == OBJETIVO:
            break

        visitados.add(estado)

        for v in vecinos(estado):

            if v not in visitados and v not in padre:

                padre[v] = estado
                pila.append(v)

    camino = []

    nodo = OBJETIVO

    while nodo:

        camino.append(nodo)
        nodo = padre.get(nodo)

    camino.reverse()

    return camino, len(visitados)


def resolver_puzzle_dfs(estado_inicial):

    tracemalloc.start()
    t0 = time.perf_counter()

    camino, visitados = dfs(estado_inicial)

    t1 = time.perf_counter()

    mem_actual, mem_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "camino": camino,
        "visitados": visitados,
        "tiempo": t1-t0,
        "memoria": mem_max/1024
    }