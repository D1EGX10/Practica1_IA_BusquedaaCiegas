def dfs(grafo, inicio, objetivo):
    pila = [inicio]
    visitados = set()
    camino = {inicio: None}

    while pila:
        nodo = pila.pop()

        if nodo not in visitados:
            visitados.add(nodo)

            if nodo == objetivo:
                return camino

            for vecino in grafo[nodo]:
                if vecino not in visitados:
                    pila.append(vecino)

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


if __name__ == "__main__":

    # Grafo de prueba
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

    resultado = dfs(grafo, inicio, objetivo)

    if resultado:
        ruta = reconstruir_camino(resultado, inicio, objetivo)
        print("Camino encontrado:", ruta)
    else:
        print("No se encontró camino")