import time
import tracemalloc

OBJETIVO = (1,2,3,4,5,6,7,8,0)


def resolver_puzzle_dfs(estado_inicial):

    tracemalloc.start()
    t0 = time.perf_counter()

    camino, visitados = dfs(estado_inicial)

    t1 = time.perf_counter()
    mem_actual, mem_max = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "camino": camino,
        "visitados": visitados,
        "tiempo": t1 - t0,
        "memoria": mem_max / 1024
    }