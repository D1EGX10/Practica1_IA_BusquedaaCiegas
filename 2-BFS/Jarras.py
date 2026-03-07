import time
import tracemalloc
#Jarras-Capacidad
CAP1 = 4
CAP2 = 3
estado_inicial = (0, 0)
OBJETIVO = 2
def obtener_vecinos(estado):
    x, y = estado
    vecinos = []

    # llenar1
    vecinos.append((CAP1, y))

    # llenar2
    vecinos.append((x, CAP2))

    # vaciar1
    vecinos.append((0, y))

    # vaciar2
    vecinos.append((x, 0))

    # verter1 en j2
    transferencia = min(x, CAP2 - y)
    vecinos.append((x - transferencia, y + transferencia))

    # verter2 en j1
    transferencia = min(y, CAP1 - x)
    vecinos.append((x + transferencia, y - transferencia))

    return vecinos

from collections import deque


def bfs_jarras():

    cola = deque([estado_inicial])
    visitados = set()
    camino = {estado_inicial: None}

    while cola:

        estado = cola.popleft()

        if estado not in visitados:
            visitados.add(estado)

            x, y = estado

            if x == OBJETIVO or y == OBJETIVO:
                return camino, estado, len(visitados), len(cola)

            for vecino in obtener_vecinos(estado):

                if vecino not in visitados:

                    cola.append(vecino)

                    if vecino not in camino:
                        camino[vecino] = estado

    return None, None, len(visitados), len(cola)