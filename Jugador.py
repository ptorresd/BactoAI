import pygame

class Jugador:

    def __init__(self,campo,tipoBacteria):
        self.campo=campo
        self.nombre=tipoBacteria.nombre
        self.coloniasSeleccionadas=[]

    def revisarSeleccion(self,x,y):
        for c in self.campo.colonias:
            if abs(x-c.x)<c.radio and abs(y-c.y)<c.radio:
                return c
        return 0
    def atacarColonia(self,x,y):
        a = self.revisarSeleccion(x, y)
        if a != 0:
            for c in self.coloniasSeleccionadas:
                c.atacar(a)
        self.coloniasSeleccionadas = []

    def agregarColonia(self,x,y):
        a = self.revisarSeleccion(x, y)
        if a != 0:
            if a.tipo.nombre==self.nombre:
                for c in self.coloniasSeleccionadas:
                    if c==a:
                        return True
                self.coloniasSeleccionadas+=[a]
                return True
            return False

    def mostrarSeleccion(self,pos,screen):
        for c in self.coloniasSeleccionadas:
            pygame.draw.line(screen,(0,0,0),(c.x,c.y),pos,3)



