# -----------------------------
# DFS
# -----------------------------

def dfs(inicio):

    # Se inicializa con el estado inicial del puzzle
    pila = [inicio]

    # Conjunto que guarda los estados visitados
    visitados = set([inicio])

    # Diccionario que guarda el padre de cada estado
    padre = {}

    # Mientras la pila tenga estados por explorar
    while pila:

        # Extrae el último estado de la pila (LIFO)
        estado = pila.pop()

        # Si el estado actual es el objetivo se detiene la búsqueda
        if estado == objetivo:
            break

        # Genera todos los estados vecinos posibles
        for v in vecinos(estado):

            # Verifica que no haya sido visitado
            if v not in visitados:

                # Se agrega el estado a la pila
                pila.append(v)

                # Se marca como visitado
                visitados.add(v)

                # Guarda el padre para reconstruir el camino
                padre[v] = estado

    # Lista donde se guardará el camino solución
    camino = []

    # Se empieza desde el estado objetivo
    nodo = objetivo

    # Reconstrucción del camino
    while nodo != inicio:

        camino.append(nodo)
        nodo = padre[nodo]

    # Se agrega el inicio
    camino.append(inicio)

    # Se invierte para que vaya de inicio a objetivo
    camino.reverse()

    return camino, visitados