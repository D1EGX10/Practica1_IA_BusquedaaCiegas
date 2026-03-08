import time
import tracemalloc
from collections import deque

CAP1 = 4
CAP2 = 3
estado_inicial = (0, 0)
OBJETIVO = 2

def obtener_vecinos(estado):
    x, y = estado
    vecinos = []

    # Llenar jarras
    vecinos.append((CAP1, y))
    vecinos.append((x, CAP2))
    
    # Vaciar jarras
    vecinos.append((0, y))
    vecinos.append((x, 0))

    # Transferir de jarra 1 a jarra 2
    transferencia = min(x, CAP2 - y)
    vecinos.append((x - transferencia, y + transferencia))

    # Transferir de jarra 2 a jarra 1
    transferencia = min(y, CAP1 - x)
    vecinos.append((x + transferencia, y - transferencia))

    return list(set(vecinos)) # Evitar duplicados inmediatos

def bfs_jarras():
    cola = deque([estado_inicial])
    visitados = set()
    camino = {estado_inicial: None}
    nodos_explorados = 0

    while cola:
        estado = cola.popleft()
        if estado in visitados:
            continue
            
        visitados.add(estado)
        nodos_explorados += 1
        x, y = estado

        if x == OBJETIVO or y == OBJETIVO:
            return camino, estado, nodos_explorados, len(cola)

        for vecino in obtener_vecinos(estado):
            if vecino not in visitados and vecino not in camino:
                cola.append(vecino)
                camino[vecino] = estado

    return None, None, nodos_explorados, len(cola)

def reconstruir_camino_jarras(camino, estado_final):
    ruta = []
    estado = estado_final
    while estado is not None:
        ruta.append(estado)
        estado = camino[estado]
    ruta.reverse()
    return ruta

def resolver_jarras_completo():
    tracemalloc.start()
    t0 = time.perf_counter()
    
    camino_dict, estado_final, explorados, en_cola = bfs_jarras()
    
    t1 = time.perf_counter()
    _, mem_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    ruta = reconstruir_camino_jarras(camino_dict, estado_final) if estado_final else []
    
    return {
        "camino": ruta,
        "tiempo": t1 - t0,
        "memoria": mem_max / 1024,
        "pasos": len(ruta),
        "explorados": explorados
    }