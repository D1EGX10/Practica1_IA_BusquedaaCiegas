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

def reconstruir_camino(camino, estado_final):

    ruta = []
    estado = estado_final

    while estado is not None:
        ruta.append(estado)
        estado = camino[estado]

    ruta.reverse()
    return ruta

if __name__ == "__main__":

    tracemalloc.start()

    inicio = time.perf_counter()

    camino, estado_final, estados_visitados, tamaño_cola = bfs_jarras()

    fin = time.perf_counter()

    memoria_actual, memoria_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if estado_final:

        ruta = reconstruir_camino(camino, estado_final)

        print("Solución encontrada:\n")

        for paso in ruta:
            print(paso)

    else:
        print("No se encontró solución")

    print("\n--- Métricas de rendimiento ---")
    print("Tiempo de ejecución:", fin - inicio, "segundos")
    print("Estados explorados:", estados_visitados)
    print("Tamaño final de la cola:", tamaño_cola)
    print("Memoria máxima usada:", memoria_max / 1024, "KB")