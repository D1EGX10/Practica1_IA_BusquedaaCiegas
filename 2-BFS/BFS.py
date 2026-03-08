import time
import tracemalloc
from collections import deque

def bfs(grafo, inicio, objetivo):
    if inicio == objetivo:
        return {inicio: None}

    cola = deque([inicio])
    # Marcamos como visitado al ENCOLAR
    visitados = {inicio}
    padre = {inicio: None}

    while cola:
        nodo = cola.popleft()

        if nodo == objetivo:
            return padre

        for vecino in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino) # Evita duplicados en la cola
                padre[vecino] = nodo
                cola.append(vecino)

    return None

def reconstruir_camino(padre_dict, objetivo):
    ruta = []
    nodo = objetivo
    while nodo is not None:
        ruta.append(nodo)
        nodo = padre_dict[nodo]
    return ruta[::-1] # Inversión más limpia

# --- PRUEBA Y MÉTRICAS ---
grafo = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["F"],
    "F": []
}

inicio, objetivo = "A", "F"

tracemalloc.start()
inicio_tiempo = time.perf_counter()

resultado_padres = bfs(grafo, inicio, objetivo)

fin_tiempo = time.perf_counter()
_, memoria_maxima = tracemalloc.get_traced_memory()
tracemalloc.stop()

if resultado_padres:
    ruta = reconstruir_camino(resultado_padres, objetivo)
    print(f"Camino encontrado: {ruta}")
else:
    print("No se encontró camino")

print("\n--- Métricas de ejecución ---")
print(f"Tiempo: {fin_tiempo - inicio_tiempo:.8f} segundos")
print(f"Memoria máxima: {memoria_maxima / 1024:.2f} KB")