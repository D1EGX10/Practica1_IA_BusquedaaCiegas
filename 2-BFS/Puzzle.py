import tkinter as tk #Sirve para la interfaz grafica 
import random #Genera numeros aleatorios
import time  #Mide el tiempo
import tracemalloc #Mide la memoria utilizada
from collections import deque  #Cola
 
# estado objetivo
objetivo = (1,2,3,
            4,5,6,
            7,8,0)


# movimientos posibles


def vecinos(estado): 

    lista = [] #Guarda los nuevos estados posibles.

    i = estado.index(0) #Busca dónde está el 0, posición dentro del puzzle.

    fila = i // 3 #Estas dos lineas de codigo indican las coordenas del tablero, para ubicar el 0
    col = i % 3

    dirs = [(-1,0),(1,0),(0,-1),(0,1)]  #Representa los posibles movimientos arriba,izquierda ,abajo y derecha    

    for dx,dy in dirs:  #intenta mover el espacio vacío en cada dirección.

        nf = fila + dx #Calcula la nueva posición del espacio vacío.
        nc = col + dy  #Calcula la nueva posición del espacio vacío.

        if 0 <= nf < 3 and 0 <= nc < 3:  #Evita que se salga del tablero

            j = nf*3 + nc #Convierte fila y columna nuevamente a posición del arreglo.

            nuevo = list(estado)   #Convierte la tupla en lista porque las tuplas no se pueden modificar.

            nuevo[i],nuevo[j] = nuevo[j],nuevo[i]  #mueve el espacio vacío.

            lista.append(tuple(nuevo)) #Convierte nuevamente a tupla y lo guarda.

    return lista


# -----------------------------
# BFS
# -----------------------------

def bfs(inicio):
   
    # Se inicializa con el estado inicial del puzzle
    cola = deque([inicio])

    # Conjunto que guarda los estados que ya fueron visitados, evita explorar el mismo estado más de una vez
    visitados = set([inicio])

    # Diccionario que guarda el "padre" de cada estado, sirve para reconstruir el camino desde el inicio hasta el objetivo
    padre = {}

    # Mientras la cola tenga estados por explorar
    while cola:

        # Extrae el primer estado de la cola (FIFO)
        estado = cola.popleft()

        # Si el estado actual es el estado objetivo, se detiene la búsqueda
        if estado == objetivo:
            break

        # Genera todos los estados vecinos posibles
        for v in vecinos(estado):

            # Verifica que el estado vecino no haya sido visitado
            if v not in visitados:

                # Se agrega el nuevo estado a la cola para explorarlo después
                cola.append(v)

                # Se marca el estado como visitado
                visitados.add(v)

                # Se guarda el estado actual como "padre" del nuevo estado, permite reconstruir el camino solución
                padre[v] = estado

    # Lista donde se guardará el camino solución
    camino = []

    # Se empieza desde el estado objetivo
    nodo = objetivo

    # Se reconstruye el camino retrocediendo usando el diccionario padre
    while nodo != inicio:

        # Se agrega el nodo actual al camino
        camino.append(nodo)

        # Se retrocede al estado padre
        nodo = padre[nodo]

    # Finalmente se agrega el estado inicial
    camino.append(inicio)

    # El camino se construyó desde objetivo -> inicio
    # Por eso se invierte para obtener inicio -> objetivo
    camino.reverse()

    # Retorna:
    # 1. El camino solución
    # 2. El conjunto de estados visitados durante la búsqueda
    return camino, visitados

# -----------------------------
# interfaz gráfica
# -----------------------------

class PuzzleApp:

    def __init__(self,root):

        self.root = root

        self.root.title("8 Puzzle BFS")

        self.estado = objetivo

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.botones = []

        for i in range(9):

            b = tk.Button(self.frame,
                          width=4,
                          height=2,
                          font=("Arial",24))

            b.grid(row=i//3,column=i%3)

            self.botones.append(b)

        panel = tk.Frame(root)
        panel.pack(pady=10)

        tk.Button(panel,
                  text="Mezclar Puzzle",
                  command=self.mezclar).pack(side=tk.LEFT,padx=10)

        tk.Button(panel,
                  text="Resolver BFS",
                  command=self.resolver).pack(side=tk.LEFT,padx=10)

        # Barra de información
        self.info = tk.Label(root,
                             text="Tiempo: - | Memoria: - ",
                             font=("Arial",12),
                             bg="#eeeeee",
                             width=45,
                             height=2)

        self.info.pack(pady=5)

        self.actualizar()


    def actualizar(self):

        for i in range(9):

            valor = self.estado[i]

            if valor == 0:
                self.botones[i]["text"] = ""
            else:
                self.botones[i]["text"] = str(valor)


    def mezclar(self):

        estado = list(objetivo)

        for _ in range(30):

            i = estado.index(0)

            fila = i // 3
            col = i % 3

            movimientos = []

            if fila > 0: movimientos.append(-3)
            if fila < 2: movimientos.append(3)
            if col > 0: movimientos.append(-1)
            if col < 2: movimientos.append(1)

            j = i + random.choice(movimientos)

            estado[i],estado[j] = estado[j],estado[i]

        self.estado = tuple(estado)

        self.actualizar()


    def resolver(self):

        # iniciar medición de memoria
        tracemalloc.start()

        # tiempo inicial
        inicio = time.perf_counter()

        camino, visitados = bfs(self.estado)

        # tiempo final
        fin = time.perf_counter()

        # obtener memoria usada
        memoria_actual, memoria_pico = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        tiempo = fin - inicio
        memoria_mb = memoria_pico / 10**6
        estados = len(visitados)

        # mostrar en la interfaz
        self.info.config(
            text=f"Tiempo: {tiempo:.6f} s | Memoria pico: {memoria_mb:.3f} MB "
        )

        # animación de la solución
        for estado in camino:

            self.estado = estado

            self.actualizar()

            self.root.update()

            time.sleep(0.5)


# -----------------------------
# ejecutar programa
# -----------------------------

root = tk.Tk()

app = PuzzleApp(root)

root.mainloop()