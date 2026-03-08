import time
import tracemalloc

CAP1, CAP2, OBJ = 4, 3, 2

def resolver_jarras_dfs():
    tracemalloc.start()
    t0 = time.perf_counter()

    pila = [(0, 0)]
    visitados = {(0, 0)}
    padre = {(0, 0): None}
    final = None
    
    while pila:
        x, y = pila.pop()
        if x == OBJ or y == OBJ:
            final = (x, y)
            break
            
        sucesores = [
            (CAP1, y), (x, CAP2), (0, y), (x, 0),
            (x - min(x, CAP2 - y), y + min(x, CAP2 - y)),
            (x + min(y, CAP1 - x), y - min(y, CAP1 - x))
        ]
        
        for s in sucesores:
            if s not in visitados:
                visitados.add(s)
                padre[s] = (x, y)
                pila.append(s)
                
    camino = []
    curr = final
    while curr is not None:
        camino.append(curr)
        curr = padre[curr]

    t1 = time.perf_counter()
    _, m_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "camino": camino[::-1],
        "tiempo": t1 - t0,
        "memoria": m_max / 1024,
        "visitados": len(visitados)
    }
print("")
