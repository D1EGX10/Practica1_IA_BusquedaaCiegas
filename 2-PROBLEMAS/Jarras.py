def obtener_vecinos(estado, cap1, cap2):
    x, y = estado
    vecinos = []

    # llenar1
    vecinos.append((cap1, y))

    # llenar2
    vecinos.append((x, cap2))

    # vaciar1
    vecinos.append((0, y))

    # vaciar2
    vecinos.append((x, 0))

    # verter1 -> en2
    transferir = min(x, cap2 - y)
    vecinos.append((x - transferir, y + transferir))

    # verter2 -> en1
    transferir = min(y, cap1 - x)
    vecinos.append((x + transferir, y - transferir))

    return vecinos