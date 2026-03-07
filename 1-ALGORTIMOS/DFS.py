def dfs(grafo, inicio, objetivo):
    pila = [inicio]
    visitados = set()
    camino = {inicio: None}
def dfs(grafo, inicio, objetivo):
    pila = [inicio]
    visitados = set()
    camino = {inicio: None}

    while pila:
        nodo = pila.pop()

        if nodo not in visitados:
            visitados.add(nodo)