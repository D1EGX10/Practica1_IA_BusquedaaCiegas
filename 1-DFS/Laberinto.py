# -----------------------------
# DFS
# -----------------------------

def dfs(lab):  # Definición por medio de DFS

    n = len(lab)  # Obtiene el tamaño del laberinto

    inicio = (0,0)   # Inicio
    meta = (n-1,n-1) # Meta

    pila = [inicio]  
    visitados = set([inicio])  # Conjunto de nodos visitados
    padre = {}  # Diccionario para reconstruir el camino

    movimientos = [(0,1),(1,0),(0,-1),(-1,0)]  # Posibles movimientos

    while pila:

        x,y = pila.pop()  # Toma el último nodo agregado (LIFO)

        if (x,y) == meta:  # Verifica si llegó a la meta
            break

        for dx,dy in movimientos:  # Calcula nuevas posiciones

            nx = x + dx
            ny = y + dy

            if 0 <= nx < n and 0 <= ny < n:  # Verifica límites

                if lab[nx][ny] == 0 and (nx,ny) not in visitados:  # Verifica si es camino válido

                    pila.append((nx,ny))  # Agrega a la pila
                    visitados.add((nx,ny))  # Marca como visitado
                    padre[(nx,ny)] = (x,y)  # Guarda el padre

    camino = []
    nodo = meta

    while nodo != inicio:

        camino.append(nodo)  # Agrega nodo al camino
        nodo = padre[nodo]   # Retrocede al nodo padre

    camino.append(inicio)
    camino.reverse()  # Invierte el camino

    return visitados, camino