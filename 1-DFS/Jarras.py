from collections import deque
import time
import tracemalloc


class ProblemaJarras:

    def __init__(self, capacidad1, capacidad2, objetivo):
        self.cap1 = capacidad1
        self.cap2 = capacidad2
        self.objetivo = objetivo

    def es_objetivo(self, estado):
        return estado[0] == self.objetivo or estado[1] == self.objetivo

    def sucesores(self, estado):

        x, y = estado
        sucesores = []

        # llenar jarra 1
        sucesores.append((self.cap1, y))

        # llenar jarra 2
        sucesores.append((x, self.cap2))

        # vaciar jarra 1
        sucesores.append((0, y))

        # vaciar jarra 2
        sucesores.append((x, 0))

        # verter jarra1 -> jarra2
        transfer = min(x, self.cap2 - y)
        sucesores.append((x - transfer, y + transfer))

        # verter jarra2 -> jarra1
        transfer = min(y, self.cap1 - x)
        sucesores.append((x + transfer, y - transfer))

        return sucesores

    def resolver(self):

        tracemalloc.start()
        inicio = time.perf_counter()

        inicial = (0, 0)

        cola = deque()
        cola.append((inicial, [inicial]))

        visitados = set()

        while cola:

            estado, camino = cola.popleft()

            if estado in visitados:
                continue

            visitados.add(estado)

            if self.es_objetivo(estado):

                tiempo = time.perf_counter() - inicio
                memoria = tracemalloc.get_traced_memory()[1] / 1024
                tracemalloc.stop()

                return camino, tiempo, memoria, len(visitados)

            for suc in self.sucesores(estado):

                if suc not in visitados:
                    cola.append((suc, camino + [suc]))

        tiempo = time.perf_counter() - inicio
        memoria = tracemalloc.get_traced_memory()[1] / 1024
        tracemalloc.stop()

        return None, tiempo, memoria, len(visitados)


# ------------------------------------------------
# FUNCIÓN QUE USA LA INTERFAZ
# ------------------------------------------------

def resolver_jarras_dfs():

    capacidad1 = 4
    capacidad2 = 3
    objetivo = 2

    problema = ProblemaJarras(capacidad1, capacidad2, objetivo)

    camino, tiempo, memoria, visitados = problema.resolver()

    return {
        "camino": camino,
        "visitados": visitados,
        "tiempo": tiempo,
        "memoria": memoria
    }