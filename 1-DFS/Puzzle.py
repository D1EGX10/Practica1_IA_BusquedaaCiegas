import time
import tracemalloc
import random

OBJETIVO = (1,2,3,4,5,6,7,8,0)


def vecinos(estado):

    i = estado.index(0)

    fila = i // 3
    col = i % 3

    movimientos = []

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
    padre = {inicial: None}

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

    while nodo is not None:

        camino.append(nodo)
        nodo = padre.get(nodo)

    camino.reverse()

    return camino, len(visitados)


def generar_puzzle():

    estado = list(OBJETIVO)

    for _ in range(40):

        i = estado.index(0)

        movimientos = [-3,3,-1,1]

        j = i + random.choice(movimientos)

        if 0 <= j < 9:
            estado[i],estado[j] = estado[j],estado[i]

    return tuple(estado)


def resolver_puzzle_dfs():

    estado_inicial = generar_puzzle()

    tracemalloc.start()
    inicio_t = time.perf_counter()

    camino, visitados = dfs(estado_inicial)

    fin_t = time.perf_counter()

    memoria_actual, memoria_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "camino": camino,
        "visitados": visitados,
        "tiempo": fin_t - inicio_t,
        "memoria": memoria_max / 1024
    }