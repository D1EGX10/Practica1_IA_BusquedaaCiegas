import time
import tracemalloc
from collections import deque


def bfs(grafo, inicio, objetivo):

    cola = deque([inicio])
    visitados = set()
    camino = {inicio: None}

    while cola:

        nodo = cola.popleft()

        if nodo not in visitados:

            visitados.add(nodo)

            if nodo == objetivo:
                return camino

            for vecino in grafo[nodo]:

                if vecino not in visitados:

                    cola.append(vecino)

                    if vecino not in camino:
                        camino[vecino] = nodo

    return None


def reconstruir_camino(camino, inicio, objetivo):

    ruta = []
    nodo = objetivo

    while nodo is not None:

        ruta.append(nodo)

        nodo = camino[nodo]

    ruta.reverse()

    return ruta


# Prueba
grafo = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["F"],
    "F": []
}

inicio = "A"
objetivo = "F"


# Medición de memoria
tracemalloc.start()

# Medición de tiempo
inicio_tiempo = time.perf_counter()

resultado = bfs(grafo, inicio, objetivo)

fin_tiempo = time.perf_counter()

memoria_actual, memoria_maxima = tracemalloc.get_traced_memory()
tracemalloc.stop()


# Resultado
if resultado:

    ruta = reconstruir_camino(resultado, inicio, objetivo)

    print("Camino encontrado:", ruta)

else:

    print("No se encontró camino")


print("\n--- Métricas de ejecución ---")

print("Tiempo de ejecución:", fin_tiempo - inicio_tiempo, "segundos")

print("Memoria máxima usada:", memoria_maxima / 1024, "KB")