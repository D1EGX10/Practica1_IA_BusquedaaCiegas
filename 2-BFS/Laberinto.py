import tkinter as tk #Sirve para la interfaz grafica 
import tracemalloc #Mide la memoria utilizada
import random #Genera numeros aleatorios
import time #Mide el tiempo
from collections import deque #Cola

MAX_SIZE = 700 #Tamaño maximo del laberinto, cada celda mide 70px


# -----------------------------
# Generar laberinto con solución
# -----------------------------

def generar_laberinto(n):


    lab = [[1 for _ in range(n)] for _ in range(n)] #Estamos ingresando el tamaño que queeremos en nuestro caso, 10*10,20*10 y 50*50

    x,y = 0,0  #Posición inicial, en este caso "x" son las filas y "y" son las columnas 
    camino = [(0,0)] #Guardamos el camino hacia la meta

    while (x,y) != (n-1,n-1):  #Recorremmos todo hasta llegar a la meta

        if random.random() < 0.5 and x < n-1:  
            x += 1
        elif y < n-1: #Avanza a la derecha y se detiene hasta que llega a la meta.
            y += 1
        elif x < n-1: #Avanza de manera izquierda y sse detiene hasta que llega a la meta
            x += 1

        camino.append((x,y))  #Se guarda la solución

    for i,j in camino: # Se recorre el laberinto y se marca con un 0, para encontrar la solución
        lab[i][j] = 0

    for i in range(n):  #Recorre todo el laberinto
        for j in range(n):

            if (i,j) not in camino and random.random() < 0.3: #Si no hay camino se marca con un 1 , que significa que es una pared
                lab[i][j] = 1
            else:
                lab[i][j] = 0 #Si se marca como un 0, es porque hay un camino para la meta

    lab[0][0] = 0  #Asegura que siempre haya unna solución para el laberinto
    lab[n-1][n-1] = 0

    return lab


# -----------------------------
# BFS
# -----------------------------

def bfs(lab): #Definición por medio de BFS

    n = len(lab) #Obtiene el tamaño del laberinto

    inicio = (0,0)  #Inicio
    meta = (n-1,n-1) #Meta, n-1 ees porque el array se inicializa en 0,0

    cola = deque([inicio]) 
    visitados = set([inicio]) #Conjunto de nodos ya visitados
    padre = {} #Diccionario que guarda de qué nodo venimos para reconstruir el camino

    movimientos = [(0,1),(1,0),(0,-1),(-1,0)] #Posibles movimientos, izquierda, derecha, arriba y abajo

    while cola: 

        x,y = cola.popleft() #Toma el primer nodo de la cola

        if (x,y) == meta: #Verifica si la posición actual es la meta
            break

        for dx,dy in movimientos: #Calculo de la nueva posción, derecha , izquierda , arriba o abajo

            nx = x + dx
            ny = y + dy

            if 0 <= nx < n and 0 <= ny < n:  #Evita que se salga de las dimensiones del laberinto

                if lab[nx][ny] == 0 and (nx,ny) not in visitados: #Verifica que sea un camino al cual pueda llegar a la meta

                    cola.append((nx,ny)) #Agrega los nodos vecionos a la cola
                    visitados.add((nx,ny)) #Guarda los vecinos visitados, para ya no visitarlos nuevamente
                    padre[(nx,ny)] = (x,y) #Guarda el padre y la posiciones

    camino = []
    nodo = meta

    while nodo != inicio:

        camino.append(nodo) #Se agrega el camino
        nodo = padre[nodo] #Vamos retrocediendo hasta llegar a la meta

    camino.append(inicio) #Agregamos el inicio
    camino.reverse() #Invierte el camino para que vaya desde el inicio hasta la meta

    return visitados,camino 


# -----------------------------
# Interfaz
# -----------------------------

class LaberintoApp:

    def __init__(self,root):

        self.root = root
        self.root.title("Laberinto BFS")

        self.size = 20
        self.cell = MAX_SIZE // self.size

        self.canvas = tk.Canvas(root,
                                width=self.size*self.cell,
                                height=self.size*self.cell)

        self.canvas.pack()

        panel = tk.Frame(root)
        panel.pack(pady=10)

        tk.Button(panel,text="10x10",
                  command=lambda:self.cambiar(10)).pack(side=tk.LEFT,padx=5)

        tk.Button(panel,text="20x20",
                  command=lambda:self.cambiar(20)).pack(side=tk.LEFT,padx=5)

        tk.Button(panel,text="50x50",
                  command=lambda:self.cambiar(50)).pack(side=tk.LEFT,padx=5)

        tk.Button(panel,text="Nuevo Laberinto",
                  command=self.generar).pack(side=tk.LEFT,padx=5)

        tk.Button(panel,text="Resolver BFS",
                  command=self.resolver).pack(side=tk.LEFT,padx=5)


        # Barra de información
        self.info = tk.Label(root,
                             text="Tiempo: - | Memoria: -",
                             font=("Arial",12),
                             bg="#eeeeee",
                             width=60,
                             height=2)

        self.info.pack(pady=5)


        self.laberinto = generar_laberinto(self.size)

        self.dibujar()


    def cambiar(self,n):

        self.size = n
        self.cell = MAX_SIZE // n

        self.canvas.config(width=n*self.cell,
                           height=n*self.cell)

        self.laberinto = generar_laberinto(n)

        self.dibujar()

        self.info.config(text="Tiempo: - | Memoria: - ")


    def generar(self):

        self.laberinto = generar_laberinto(self.size)

        self.dibujar()

        self.info.config(text="Tiempo: - | Memoria: - ")


    def dibujar(self):

        self.canvas.delete("all")

        for i in range(self.size):
            for j in range(self.size):

                color = "white"

                if self.laberinto[i][j] == 1:
                    color = "black"

                self.canvas.create_rectangle(
                    j*self.cell,
                    i*self.cell,
                    (j+1)*self.cell,
                    (i+1)*self.cell,
                    fill=color,
                    outline="gray"
                )

        self.canvas.create_rectangle(0,0,self.cell,self.cell,fill="green")

        self.canvas.create_rectangle((self.size-1)*self.cell,
                                     (self.size-1)*self.cell,
                                     self.size*self.cell,
                                     self.size*self.cell,
                                     fill="red")


# -----------------------------
# Resolver con medición
# -----------------------------

    def resolver(self):

        tracemalloc.start()

        inicio = time.perf_counter()

        visitados,camino = bfs(self.laberinto)

        fin = time.perf_counter()

        memoria_actual, memoria_pico = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        tiempo = fin - inicio
        memoria_mb = memoria_pico / 10**6
        nodos = len(visitados)


        # mostrar en interfaz
        self.info.config(
            text=f"Tiempo de ejecución: {tiempo:.6f} s | Memoria pico: {memoria_mb:.3f}MB"
        )


        for x,y in visitados:

            self.canvas.create_rectangle(
                y*self.cell,
                x*self.cell,
                (y+1)*self.cell,
                (x+1)*self.cell,
                fill="blue"
            )

            self.root.update()
            time.sleep(0.001)


        for x,y in camino:

            self.canvas.create_rectangle(
                y*self.cell,
                x*self.cell,
                (y+1)*self.cell,
                (x+1)*self.cell,
                fill="yellow"
            )

            self.root.update()
            time.sleep(0.02)


# -----------------------------
# Ejecutar
# -----------------------------

root = tk.Tk()

app = LaberintoApp(root)

root.mainloop()