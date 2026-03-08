import random
import time
import tracemalloc

def generar_laberinto(n):
    lab = [[1 for _ in range(n)] for _ in range(n)]
    x, y = 0, 0
    camino_seguro = [(0, 0)]
    while (x, y) != (n - 1, n - 1):
        if x < n - 1 and (y == n - 1 or random.random() < 0.5): x += 1
        elif y < n - 1: y += 1
        camino_seguro.append((x, y))
    for i, j in camino_seguro: lab[i][j] = 0
    for i in range(n):
        for j in range(n):
            if (i, j) not in camino_seguro:
                lab[i][j] = 1 if random.random() < 0.28 else 0
    lab[0][0], lab[n-1][n-1] = 0, 0
    return lab

def resolver_laberinto_dfs(n):
    lab = generar_laberinto(n)
    tracemalloc.start()
    t0 = time.perf_counter()

    pila = [(0, 0)]
    visitados_orden = []
    visitados_set = {(0, 0)}
    padre = {(0, 0): None}
    
    while pila:
        curr = pila.pop()
        visitados_orden.append(curr)
        if curr == (n-1, n-1): break

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = curr[0] + dx, curr[1] + dy
            if 0 <= nx < n and 0 <= ny < n and lab[nx][ny] == 0 and (nx, ny) not in visitados_set:
                visitados_set.add((nx, ny))
                padre[(nx, ny)] = curr
                pila.append((nx, ny))
    
    camino = []
    curr = (n-1, n-1)
    if curr in padre:
        while curr is not None:
            camino.append(curr)
            curr = padre[curr]
    
    t1 = time.perf_counter()
    _, m_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "laberinto": lab,
        "visitados": visitados_orden,
        "camino": camino[::-1],
        "tiempo": t1 - t0,
        "memoria": m_max / 1024,
        "nodos_explorados": len(visitados_orden)
    }