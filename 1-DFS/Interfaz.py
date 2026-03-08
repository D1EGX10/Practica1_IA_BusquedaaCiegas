import tkinter as tk
from tkinter import ttk
import time
import tracemalloc

# Importar tus algoritmos originales
from Laberinto import resolver_laberinto_dfs
from Puzzle import resolver_puzzle_dfs
from Jarras import resolver_jarras_dfs

# Colores para mejorar la visualización
COLORS = {
    'fondo': '#f0f0f0',
    'boton': '#4CAF50',
    'boton_hover': '#45a049',
    'texto': '#333333',
    'canvas_bg': 'white',
    'explorado': '#4FC3F7',
    'camino': '#FFD700',
    'inicio': '#4CAF50',
    'fin': '#f44336',
    'muro': '#2c3e50',
    'agua1': '#3498db',
    'agua2': '#e74c3c',
    'nodo_normal': '#ffffff',
    'nodo_visitado': '#90CAF9',
    'arista': '#95a5a6'
}

class AppDFS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DFS - Visualizador de Algoritmos de Búsqueda")
        self.geometry("900x950")
        self.configure(bg=COLORS['fondo'])
        self.resizable(True, True)
        
        # Variables de control
        self.problema = tk.StringVar(value="Laberinto")
        self.size = tk.StringVar(value="10")
        self.velocidad = tk.StringVar(value="Normal")
        self.animacion_activa = False
        self.animacion_id = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Título
        titulo = tk.Label(self, text="DFS - Visualizador de Algoritmos de Búsqueda",
                         font=("Arial", 16, "bold"), bg=COLORS['fondo'],
                         fg=COLORS['texto'])
        titulo.pack(pady=10)
        
        # Frame de controles
        control_frame = tk.Frame(self, bg=COLORS['fondo'])
        control_frame.pack(pady=10)
        
        # Problema
        tk.Label(control_frame, text="Problema:", font=("Arial", 11),
                bg=COLORS['fondo']).pack(side=tk.LEFT, padx=5)
        
        self.problema_combo = ttk.Combobox(control_frame, textvariable=self.problema,
                                      values=["Laberinto", "8-Puzzle", "Jarras", "DFS-Grafo"],
                                      state="readonly", width=12)
        self.problema_combo.pack(side=tk.LEFT, padx=5)
        self.problema_combo.bind('<<ComboboxSelected>>', self.on_problema_change)
        
        # Tamaño (solo para laberinto)
        tk.Label(control_frame, text="Tamaño:", font=("Arial", 11),
                bg=COLORS['fondo']).pack(side=tk.LEFT, padx=5)
        
        self.size_combo = ttk.Combobox(control_frame, textvariable=self.size,
                                       values=["8", "10", "12", "15", "20"],
                                       state="readonly", width=8)
        self.size_combo.pack(side=tk.LEFT, padx=5)
        
        # Velocidad
        tk.Label(control_frame, text="Velocidad:", font=("Arial", 11),
                bg=COLORS['fondo']).pack(side=tk.LEFT, padx=5)
        
        velocidad_combo = ttk.Combobox(control_frame, textvariable=self.velocidad,
                                       values=["Lenta", "Normal", "Rápida", "Muy Rápida"],
                                       state="readonly", width=10)
        velocidad_combo.pack(side=tk.LEFT, padx=5)
        
        # Botones
        botones_frame = tk.Frame(self, bg=COLORS['fondo'])
        botones_frame.pack(pady=10)
        
        self.btn_iniciar = tk.Button(botones_frame, text="Iniciar", command=self.iniciar,
                                     bg=COLORS['boton'], fg='white', font=("Arial", 10),
                                     padx=15, pady=5, cursor='hand2')
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)
        
        self.btn_reiniciar = tk.Button(botones_frame, text="Reiniciar", command=self.reiniciar,
                                       bg=COLORS['boton'], fg='white', font=("Arial", 10),
                                       padx=15, pady=5, cursor='hand2', state=tk.DISABLED)
        self.btn_reiniciar.pack(side=tk.LEFT, padx=5)
        
        # Label de información de progreso
        self.info_label = tk.Label(self, text="", font=("Arial", 11, "bold"),
                                  bg=COLORS['fondo'], fg=COLORS['texto'])
        self.info_label.pack(pady=5)
        
        # Frame para el contenido (canvas o widgets específicos)
        self.content_frame = tk.Frame(self, bg=COLORS['fondo'], width=800, height=600)
        self.content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        self.content_frame.pack_propagate(False)
        
        # Canvas para visualización general
        self.canvas = tk.Canvas(self.content_frame, bg=COLORS['canvas_bg'],
                               highlightthickness=1, highlightbackground=COLORS['texto'])
        
        # Frame para métricas (siempre visible)
        self.metricas_frame = tk.Frame(self, bg=COLORS['fondo'], relief=tk.RAISED, bd=2)
        self.metricas_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.metricas_label = tk.Label(self.metricas_frame, text="", font=("Courier", 10),
                                       bg=COLORS['fondo'], fg=COLORS['texto'],
                                       justify=tk.LEFT, wraplength=850)
        self.metricas_label.pack(padx=10, pady=10)
        
        # Variables de estado
        self.pasos = []
        self.index = 0
        self.metricas = None
        
    def get_delay(self):
        velocidades = {
            "Lenta": 400,
            "Normal": 200,
            "Rápida": 80,
            "Muy Rápida": 20
        }
        return velocidades.get(self.velocidad.get(), 200)
    
    def on_problema_change(self, event=None):
        # Habilitar/deshabilitar combo de tamaño según el problema
        if self.problema.get() == "Laberinto":
            self.size_combo.config(state="readonly")
        else:
            self.size_combo.config(state="disabled")
        
        self.limpiar()
    
    def limpiar(self):
        # Cancelar animación si está activa
        if hasattr(self, 'animacion_id') and self.animacion_id:
            self.after_cancel(self.animacion_id)
            self.animacion_activa = False
        
        # Limpiar content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Restaurar canvas
        self.canvas = tk.Canvas(self.content_frame, bg=COLORS['canvas_bg'],
                               highlightthickness=1, highlightbackground=COLORS['texto'])
        
        self.pasos = []
        self.index = 0
        self.metricas = None
        self.metricas_label.config(text="")
        self.info_label.config(text="")
        self.btn_reiniciar.config(state=tk.DISABLED)
    
    def iniciar(self):
        self.limpiar()
        problema = self.problema.get()
        
        if problema == "Laberinto":
            self.iniciar_laberinto()
        elif problema == "8-Puzzle":
            self.iniciar_puzzle()
        elif problema == "Jarras":
            self.iniciar_jarras()
        elif problema == "DFS-Grafo":
            self.iniciar_grafo()
    
    def reiniciar(self):
        self.index = 0
        self.animacion_activa = False
        if hasattr(self, 'animacion_id') and self.animacion_id:
            self.after_cancel(self.animacion_id)
        self.actualizar_vista()
        self.animacion_activa = True
        self.animar()
    
    def actualizar_vista(self):
        problema = self.problema.get()
        
        if problema == "Laberinto":
            self.dibujar_laberinto()
        elif problema == "8-Puzzle":
            self.dibujar_puzzle()
        elif problema == "Jarras":
            self.dibujar_jarras()
        elif problema == "DFS-Grafo":
            self.dibujar_grafo()
    
    # ---------------------------------------------------
    # LABERINTO (AJUSTADO PARA NO VERSE CORTADO)
    # ---------------------------------------------------
    
    def iniciar_laberinto(self):
        size = int(self.size.get())
        
        # Usar tu algoritmo original
        resultado = resolver_laberinto_dfs(size)
        
        self.lab = resultado["laberinto"]
        self.visitados = resultado["visitados"]
        self.camino_set = set(resultado["camino"])  # Para búsqueda rápida
        self.camino = resultado["camino"]
        self.metricas = resultado
        
        # Calcular tamaño de celda para que quepa perfectamente (más pequeño)
        canvas_size = min(500, self.content_frame.winfo_width() - 40)
        if canvas_size < 100:
            canvas_size = 450
        
        self.cell = canvas_size // size
        self.size_lab = size
        
        # Configurar canvas con tamaño fijo
        self.canvas = tk.Canvas(self.content_frame, width=size*self.cell, 
                               height=size*self.cell, bg='white')
        self.canvas.pack(expand=True)
        
        # Crear pasos para animación (visitados primero)
        self.pasos = self.visitados.copy()
        
        self.index = 0
        self.animacion_activa = True
        self.btn_reiniciar.config(state=tk.NORMAL)
        
        self.animar()
    
    def dibujar_laberinto(self):
        self.canvas.delete("all")
        
        # Dibujar cuadrícula
        for i in range(self.size_lab):
            for j in range(self.size_lab):
                x1 = j * self.cell
                y1 = i * self.cell
                x2 = (j+1) * self.cell
                y2 = (i+1) * self.cell
                
                # Color base (muro o espacio)
                if self.lab[i][j] == 1:
                    color = COLORS['muro']
                else:
                    color = 'white'
                
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                           fill=color, outline='gray', width=1)
        
        # Dibujar celdas exploradas hasta el índice actual
        for idx in range(self.index):
            if idx < len(self.pasos):
                i, j = self.pasos[idx]
                
                x1 = j * self.cell
                y1 = i * self.cell
                x2 = (j+1) * self.cell
                y2 = (i+1) * self.cell
                
                # Color según si es parte del camino solución
                if (i, j) in self.camino_set:
                    color = COLORS['camino']
                else:
                    color = COLORS['explorado']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
        
        # Marcar inicio y fin
        # Inicio (verde)
        self.canvas.create_rectangle(0, 0, self.cell, self.cell,
                                    fill=COLORS['inicio'], outline='gray')
        self.canvas.create_text(self.cell//2, self.cell//2, text="S", 
                               font=("Arial", int(self.cell//3), "bold"), fill="white")
        
        # Fin (rojo)
        x_fin = (self.size_lab-1) * self.cell
        y_fin = (self.size_lab-1) * self.cell
        self.canvas.create_rectangle(x_fin, y_fin, x_fin+self.cell, y_fin+self.cell,
                                    fill=COLORS['fin'], outline='gray')
        self.canvas.create_text(x_fin + self.cell//2, y_fin + self.cell//2, text="F",
                               font=("Arial", int(self.cell//3), "bold"), fill="white")
    
    # ---------------------------------------------------
    # PUZZLE (CON MÉTRICAS)
    # ---------------------------------------------------
    
    def iniciar_puzzle(self):
        # Usar tu algoritmo original
        resultado = resolver_puzzle_dfs()
        
        self.pasos = resultado["camino"]
        self.metricas = resultado
        
        # Crear frame para los botones del puzzle
        self.puzzle_frame = tk.Frame(self.content_frame, bg=COLORS['fondo'])
        self.puzzle_frame.pack(expand=True)
        
        # Crear botones (3x3) más grandes
        self.botones = []
        for i in range(9):
            b = tk.Button(self.puzzle_frame, width=5, height=2, 
                         font=("Arial", 28), bg='white', relief='raised')
            b.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.botones.append(b)
        
        self.index = 0
        self.animacion_activa = True
        self.btn_reiniciar.config(state=tk.NORMAL)
        
        self.animar()
    
    def dibujar_puzzle(self):
        if self.index >= len(self.pasos):
            return
        
        estado = self.pasos[self.index]
        
        for i in range(9):
            val = estado[i]
            if val == 0:
                self.botones[i].config(text="", bg='white')
            else:
                # Colores diferentes según el número
                colors = ['#FFB6C1', '#87CEEB', '#98FB98', '#FFD700', 
                         '#DDA0DD', '#F0E68C', '#FFA07A', '#20B2AA']
                self.botones[i].config(text=str(val), bg=colors[val-1])
    
    # ---------------------------------------------------
    # JARRAS (MÁS ESPACIADAS)
    # ---------------------------------------------------
    
    def iniciar_jarras(self):
        # Usar tu algoritmo original
        resultado = resolver_jarras_dfs()
        
        self.pasos = resultado["camino"]
        self.metricas = resultado
        self.capacidades = (4, 3)  # Fijo como en tu algoritmo
        
        # Frame para jarras
        self.jarras_frame = tk.Frame(self.content_frame, bg=COLORS['fondo'])
        self.jarras_frame.pack(expand=True, fill=tk.BOTH)
        
        # Título del estado actual
        self.estado_label = tk.Label(self.jarras_frame, text="", 
                                     font=("Arial", 28, "bold"),
                                     bg=COLORS['fondo'])
        self.estado_label.pack(pady=30)
        
        # Frame para las jarras (horizontal)
        jarras_container = tk.Frame(self.jarras_frame, bg=COLORS['fondo'])
        jarras_container.pack(expand=True, pady=30)
        
        # Jarra 1
        jarra1_frame = tk.Frame(jarras_container, bg=COLORS['fondo'])
        jarra1_frame.pack(side=tk.LEFT, padx=60)
        
        tk.Label(jarra1_frame, text="Jarra 1", font=("Arial", 16, "bold"),
                bg=COLORS['fondo']).pack()
        
        self.jarra1_canvas = tk.Canvas(jarra1_frame, width=180, height=300,
                                       bg='white', highlightthickness=2,
                                       highlightbackground='black')
        self.jarra1_canvas.pack(pady=10)
        
        self.jarra1_texto = tk.Label(jarra1_frame, text="0/4 L", font=("Arial", 14),
                                     bg=COLORS['fondo'])
        self.jarra1_texto.pack()
        
        # Jarra 2
        jarra2_frame = tk.Frame(jarras_container, bg=COLORS['fondo'])
        jarra2_frame.pack(side=tk.LEFT, padx=60)
        
        tk.Label(jarra2_frame, text="Jarra 2", font=("Arial", 16, "bold"),
                bg=COLORS['fondo']).pack()
        
        self.jarra2_canvas = tk.Canvas(jarra2_frame, width=180, height=300,
                                       bg='white', highlightthickness=2,
                                       highlightbackground='black')
        self.jarra2_canvas.pack(pady=10)
        
        self.jarra2_texto = tk.Label(jarra2_frame, text="0/3 L", font=("Arial", 14),
                                     bg=COLORS['fondo'])
        self.jarra2_texto.pack()
        
        self.index = 0
        self.animacion_activa = True
        self.btn_reiniciar.config(state=tk.NORMAL)
        
        self.animar()
    
    def dibujar_jarras(self):
        if self.index >= len(self.pasos):
            return
        
        jarra1, jarra2 = self.pasos[self.index]
        cap1, cap2 = self.capacidades
        
        # Actualizar label
        self.estado_label.config(text=f"{jarra1} L  |  {jarra2} L")
        
        # Limpiar canvases
        self.jarra1_canvas.delete("all")
        self.jarra2_canvas.delete("all")
        
        # Dibujar contorno de jarras
        for canvas in [self.jarra1_canvas, self.jarra2_canvas]:
            canvas.create_rectangle(30, 50, 150, 250, outline='black', width=3)
            # Marcas de nivel
            for i in range(1, 5):
                y = 250 - (i * 50)
                canvas.create_line(20, y, 30, y, fill='gray', width=2)
                canvas.create_text(45, y-5, text=f"{i}L", font=("Arial", 9))
        
        # Dibujar agua jarra 1
        if jarra1 > 0:
            altura1 = (jarra1 / cap1) * 200
            self.jarra1_canvas.create_rectangle(30, 250-altura1, 150, 250,
                                               fill=COLORS['agua1'], outline='')
        
        # Dibujar agua jarra 2
        if jarra2 > 0:
            altura2 = (jarra2 / cap2) * 200
            self.jarra2_canvas.create_rectangle(30, 250-altura2, 150, 250,
                                               fill=COLORS['agua2'], outline='')
        
        # Actualizar textos
        self.jarra1_texto.config(text=f"{jarra1}/{cap1} L")
        self.jarra2_texto.config(text=f"{jarra2}/{cap2} L")
    
    # ---------------------------------------------------
    # GRAFO DFS (CON SOLUCIÓN CORREGIDA)
    # ---------------------------------------------------
    
    def iniciar_grafo(self):
        # Usar tu algoritmo de grafo original
        self.grafo = {
            "A": ["B", "C"],
            "B": ["D", "E"],
            "C": ["F"],
            "D": [],
            "E": ["F"],
            "F": []
        }
        inicio = "A"
        objetivo = "F"
        
        # Ejecutar DFS con tu algoritmo original
        tracemalloc.start()
        tiempo_inicio = time.perf_counter()
        
        # Algoritmo DFS original
        pila = [inicio]
        visitados = set()
        padre = {inicio: None}
        self.orden_visita = []
        
        while pila:
            nodo = pila.pop()
            
            if nodo not in visitados:
                visitados.add(nodo)
                self.orden_visita.append(nodo)
                
                if nodo == objetivo:
                    break
                
                # Agregar vecinos (sin revertir para mantener orden natural)
                for vecino in self.grafo[nodo]:
                    if vecino not in visitados and vecino not in padre:
                        pila.append(vecino)
                        if vecino not in padre:
                            padre[vecino] = nodo
        
        # Reconstruir camino usando tu función reconstruir_camino
        self.camino_final = []
        if objetivo in padre:
            nodo = objetivo
            while nodo is not None:
                self.camino_final.append(nodo)
                nodo = padre.get(nodo)
            self.camino_final.reverse()
        
        tiempo_total = time.perf_counter() - tiempo_inicio
        memoria = tracemalloc.get_traced_memory()[1] / 1024
        tracemalloc.stop()
        
        self.metricas = {
            'tiempo': tiempo_total,
            'memoria': memoria,
            'visitados': len(visitados),
            'camino': self.camino_final
        }
        
        # Crear canvas para el grafo (más grande)
        self.canvas = tk.Canvas(self.content_frame, width=700, height=500,
                               bg='white', highlightthickness=2,
                               highlightbackground='black')
        self.canvas.pack(expand=True)
        
        # Posiciones de los nodos (bien distribuidas)
        self.posiciones = {
            'A': (350, 70),
            'B': (150, 200),
            'C': (550, 200),
            'D': (70, 380),
            'E': (300, 380),
            'F': (630, 380)
        }
        
        self.pasos = self.orden_visita
        self.index = 0
        self.animacion_activa = True
        self.btn_reiniciar.config(state=tk.NORMAL)
        
        self.animar()
    
    def dibujar_grafo(self):
        self.canvas.delete("all")
        
        # Dibujar aristas
        for nodo, vecinos in self.grafo.items():
            x1, y1 = self.posiciones[nodo]
            for vecino in vecinos:
                x2, y2 = self.posiciones[vecino]
                self.canvas.create_line(x1, y1, x2, y2, fill=COLORS['arista'], width=2)
        
        # Determinar nodos visitados hasta ahora
        visitados_actuales = set(self.pasos[:self.index])
        
        # Dibujar nodos
        for nodo, (x, y) in self.posiciones.items():
            radio = 35
            
            # Determinar color
            if nodo == 'A':
                color = COLORS['inicio']  # Verde para inicio
            elif nodo == 'F':
                color = COLORS['fin']  # Rojo para objetivo
            elif nodo in self.camino_final and self.index == len(self.pasos):
                color = COLORS['camino']  # Amarillo para el camino solución
            elif nodo in visitados_actuales:
                color = COLORS['explorado']  # Azul para visitados
            else:
                color = 'white'
            
            # Sombra
            self.canvas.create_oval(x-radio+3, y-radio+3, x+radio+3, y+radio+3,
                                   fill='gray', outline='')
            # Nodo
            self.canvas.create_oval(x-radio, y-radio, x+radio, y+radio,
                                   fill=color, outline='black', width=2)
            # Etiqueta
            self.canvas.create_text(x, y, text=nodo, font=("Arial", 20, "bold"))
            
            # Mostrar orden de visita
            if nodo in visitados_actuales:
                orden = self.orden_visita.index(nodo) + 1
                self.canvas.create_text(x, y-radio-10, text=f"#{orden}",
                                       font=("Arial", 12), fill='#555')
        
        # Si la animación terminó, mostrar el camino solución
        if self.index == len(self.pasos) and self.camino_final:
            # Dibujar el camino solución con líneas punteadas
            for i in range(len(self.camino_final)-1):
                nodo1 = self.camino_final[i]
                nodo2 = self.camino_final[i+1]
                if nodo2 in self.grafo[nodo1]:
                    x1, y1 = self.posiciones[nodo1]
                    x2, y2 = self.posiciones[nodo2]
                    self.canvas.create_line(x1, y1, x2, y2, 
                                           fill=COLORS['camino'], width=4, dash=(5, 3))
    
    # ---------------------------------------------------
    # ANIMACIÓN Y MÉTRICAS
    # ---------------------------------------------------
    
    def animar(self):
        if not self.animacion_activa or self.index >= len(self.pasos):
            if self.index >= len(self.pasos):
                self.mostrar_metricas()
                self.info_label.config(text="¡Animación completada!")
                # Para el grafo, asegurar que se muestra el camino
                if self.problema.get() == "DFS-Grafo":
                    self.actualizar_vista()
            return
        
        self.actualizar_vista()
        
        # Actualizar información
        progreso = int((self.index / len(self.pasos)) * 100) if len(self.pasos) > 0 else 0
        self.info_label.config(text=f"Paso: {self.index}/{len(self.pasos)} | Progreso: {progreso}%")
        
        self.index += 1
        
        # Programar siguiente paso
        delay = self.get_delay()
        self.animacion_id = self.after(delay, self.animar)
    
    def mostrar_metricas(self):
        if not self.metricas:
            return
        
        texto = f"⏱️ Tiempo: {self.metricas['tiempo']:.6f}s | "
        texto += f"💾 Memoria: {self.metricas['memoria']:.2f} KB | "
        
        if self.problema.get() == "Laberinto":
            texto += f"📍 Nodos explorados: {self.metricas['nodos_explorados']}"
            if 'camino' in self.metricas:
                texto += f"\n📌 Longitud del camino: {len(self.metricas['camino'])}"
        
        elif self.problema.get() == "8-Puzzle":
            texto += f"📍 Estados explorados: {self.metricas['visitados']}"
            texto += f"\n📌 Pasos solución: {len(self.metricas['camino'])}"
        
        elif self.problema.get() == "Jarras":
            texto += f"📍 Estados explorados: {self.metricas['visitados']}"
            texto += f"\n📌 Pasos solución: {len(self.metricas['camino'])}"
        
        elif self.problema.get() == "DFS-Grafo":
            texto += f"📍 Nodos explorados: {self.metricas['visitados']}"
            texto += f"\n📌 Orden DFS: {' → '.join(self.orden_visita)}"
            if self.camino_final:
                texto += f"\n📌 Camino solución: {' → '.join(self.camino_final)}"
        
        self.metricas_label.config(text=texto)

if __name__ == "__main__":
    app = AppDFS()
    app.mainloop()