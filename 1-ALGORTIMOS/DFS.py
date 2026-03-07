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