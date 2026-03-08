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

    vecinos.append((CAP1, y))
    vecinos.append((x, CAP2))
    vecinos.append((0, y))
    vecinos.append((x, 0))

    transferencia = min(x, CAP2 - y)
    vecinos.append((x - transferencia, y + transferencia))

    transferencia = min(y, CAP1 - x)
    vecinos.append((x + transferencia, y - transferencia))

    return vecinos


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


def reconstruir_camino(camino, estado_final):

    ruta = []
    estado = estado_final

    while estado is not None:
        ruta.append(estado)
        estado = camino[estado]

    ruta.reverse()
    return ruta