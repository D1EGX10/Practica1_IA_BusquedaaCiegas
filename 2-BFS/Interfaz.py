import tkinter as tk
from tkinter import ttk
import time

from Jarras import bfs_jarras, reconstruir_camino
from Laberinto import resolver_laberinto
from Puzzle import resolver_puzzle

PROBLEMAS = {
    "Jarras":"jarras",
    "Laberinto":"laberinto",
    "8-Puzzle":"puzzle"
}

class AppBFSSelector(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("BFS Problemas")

        self.geometry("700x700")

        tk.Label(self,text="Selecciona problema").pack()

        self.var=tk.StringVar(value="Jarras")

        ttk.Combobox(self,textvariable=self.var,values=list(PROBLEMAS.keys())).pack()

        tk.Button(self,text="Iniciar",command=self.iniciar).pack()

        nav=tk.Frame(self)

        nav.pack()

        self.btn_ant=tk.Button(nav,text="Anterior",command=self.anterior)

        self.btn_ant.pack(side="left")

        self.btn_sig=tk.Button(nav,text="Siguiente",command=self.siguiente)

        self.btn_sig.pack(side="left")

        self.canvas=tk.Canvas(self,width=600,height=600)

        self.canvas.pack()

        self.pasos=[]
        self.index=0

    def iniciar(self):

        p=PROBLEMAS[self.var.get()]

        if p=="jarras":
            self.jarras()

        if p=="laberinto":
            self.laberinto()

        if p=="puzzle":
            self.puzzle()

    # -------------------
    # JARRAS MANUAL
    # -------------------

    def jarras(self):

        camino,estado,_,_=bfs_jarras()

        self.pasos=reconstruir_camino(camino,estado)

        self.index=0

        self.mostrar_jarras()

    def mostrar_jarras(self):

        estado=self.pasos[self.index]

        self.canvas.delete("all")

        x,y=estado

        h1=x*40
        h2=y*60

        self.canvas.create_rectangle(100,200,160,400)
        self.canvas.create_rectangle(100,400-h1,160,400,fill="blue")

        self.canvas.create_rectangle(300,200,360,400)
        self.canvas.create_rectangle(300,400-h2,360,400,fill="blue")

    def siguiente(self):

        if self.index<len(self.pasos)-1:

            self.index+=1

            self.mostrar_jarras()

    def anterior(self):

        if self.index>0:

            self.index-=1

            self.mostrar_jarras()

    # -------------------
    # LABERINTO AUTOMATICO
    # -------------------

    def laberinto(self):

        r=resolver_laberinto(15)

        self.lab=r["laberinto"]
        self.expl=r["exploracion"]
        self.cam=r["camino"]

        self.i=0

        self.animar_laberinto()

    def animar_laberinto(self):

        if self.i<len(self.expl):

            x,y=self.expl[self.i]

            s=30

            self.canvas.create_rectangle(
                y*s,x*s,y*s+s,x*s+s,
                fill="blue"
            )

            self.i+=1

            self.after(50,self.animar_laberinto)

        else:

            self.animar_camino(0)

    def animar_camino(self,i):

        if i<len(self.cam):

            x,y=self.cam[i]

            s=30

            self.canvas.create_rectangle(
                y*s,x*s+s,y*s+s,x*s+s,
                fill="yellow"
            )

            self.after(80,lambda:self.animar_camino(i+1))

    # -------------------
    # PUZZLE AUTOMATICO
    # -------------------

    def puzzle(self):

        inicio=(1,2,3,4,5,6,0,7,8)

        r=resolver_puzzle(inicio)

        self.cam=r["camino"]

        self.i=0

        self.animar_puzzle()

    def animar_puzzle(self):

        if self.i<len(self.cam):

            estado=self.cam[self.i]

            self.canvas.delete("all")

            for i in range(9):

                x=(i%3)*100
                y=(i//3)*100

                v=estado[i]

                self.canvas.create_rectangle(x,y,x+100,y+100)

                if v!=0:
                    self.canvas.create_text(x+50,y+50,text=str(v),font=("Arial",20))

            self.i+=1

            self.after(500,self.animar_puzzle)


if __name__=="__main__":

    app=AppBFSSelector()

    app.mainloop()