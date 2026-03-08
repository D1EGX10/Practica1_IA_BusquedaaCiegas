import time
import tracemalloc
import random

OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def vecinos(estado):
    res = []
    i = estado.index(0)
    r, c = i // 3, i % 3
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nuevo = list(estado)
            j = nr * 3 + nc
            nuevo[i], nuevo[j] = nuevo[j], nuevo[i]
            res.append(tuple(nuevo))
    return res

def resolver_puzzle_dfs(inicio):
    tracemalloc.start()
    t0 = time.perf_counter()

    pila = [inicio]
    visitados = {inicio}
    padre = {inicio: None}
    
    while pila:
        curr = pila.pop()
        if curr == OBJETIVO: break
        for v in vecinos(curr):
            if v not in visitados:
                visitados.add(v)
                padre[v] = curr
                pila.append(v)
    
    camino = []
    curr = OBJETIVO
    if curr in padre:
        while curr is not None:
            camino.append(curr)
            curr = padre[curr]
    
    t1 = time.perf_counter()
    _, m_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "camino": camino[::-1],
        "tiempo": t1 - t0,
        "memoria": m_max / 1024,
        "visitados": len(visitados)
    }