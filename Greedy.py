import random
import numpy as np

def sacarMaximoBacterias(colonias):
    aux=[]
    maximo=colonias[0]
    for c in colonias:
        if c.bacterias>maximo.bacterias:
            maximo=c
    for c in colonias:
        if c!=maximo:
            aux+=[c]
    return [maximo,aux]

def minimoBacterias(colonias):
    aux=[]
    minimo=colonias[0]
    for c in colonias:
        if c.bacterias<minimo.bacterias:
            minimo=c
    return minimo

def maximoDistancia(colonias,objetivo):
    maximo=colonias[0]
    for c in colonias:
        if c.dis(objetivo)>maximo.dis(objetivo):
            maximo=c
    return maximo

class IA:

    def __init__(self, nombre, campo, dificultad):
        self.nombre=nombre
        self.campo=campo
        self.dificultad=dificultad
        self.contador=0
        self.jugadas=[]

    def getColonias(self):
        aliadas=[]
        noAliadas=[]
        for c in self.campo.colonias:
            if c.tipo.nombre==self.nombre:
                aliadas+=[c]
            else:
                noAliadas+=[c]
        return [aliadas,noAliadas]

    def calcularTiempo(self,origen,objetivo):
        vel=origen.tipo.velocidad
        dis=origen.dis(objetivo)
        return (dis/vel)

    def sirve(self,origen,objetivo):
        cantidad=(origen.bacterias+1)//2
        bactEnemigas=objetivo.bacterias+self.calcularTiempo(origen,objetivo)*objetivo.tipo.reproduccion
        return bactEnemigas*objetivo.tipo.defensa<cantidad*origen.tipo.ataque

    def sirven(self,colonias,objetivo):
        cantidad=0
        for origen in colonias:
            cantidad+=(origen.bacterias+1)//2
        tiempo=self.calcularTiempo(maximoDistancia(colonias,objetivo) ,objetivo)
        bactEnemigas=objetivo.bacterias+tiempo*objetivo.tipo.reproduccion
        return bactEnemigas*objetivo.tipo.defensa<cantidad*colonias[0].tipo.ataque

    def parse_output(self, colonias, obj):
        output=[]
        for i in range(10):
            c=self.campo.colonias[i]
            if c in colonias:
                output+=[1]
            else:
                output+=[0]
        for i in range(10):
            c=self.campo.colonias[i]
            if c == obj:
                output+=[1]
            else:
                output+=[0]
        return np.array(output)

    def jugadaSimple(self):
        colonias=self.getColonias()
        mejorOpcion=0
        disMin=1000000
        for ori in colonias[0]:
            for obj in colonias[1]:
                if self.sirve(ori,obj) and ori.dis(obj)<disMin:
                    alreadyAtacked=False
                    for a in self.campo.ataques:
                        if a.objetivo==obj and a.tipo.nombre==self.nombre:
                            alreadyAtacked=True
                    if not alreadyAtacked:
                        disMin=ori.dis(obj)
                        mejorOpcion=[ori,obj]
        return mejorOpcion


    def jugadaElaborada(self):
        aliadas,enemigas = self.getColonias()
        colonias=[]
        objetivo=minimoBacterias(enemigas)
        jugada=0
        while aliadas!=[]:
            maximo,aliadas=sacarMaximoBacterias(aliadas)
            colonias+=[maximo]
            if self.sirven(colonias,objetivo):
                alreadyAtacked = False
                for a in self.campo.ataques:
                    if a.objetivo == objetivo and a.tipo.nombre == self.nombre:
                        alreadyAtacked = True
                if not alreadyAtacked:
                    jugada=[colonias,objetivo]
                    break


        if jugada != 0:
            output = self.parse_output(jugada[0], jugada[1])
            input = np.array(self.campo.get_input(self.nombre))
            self.jugadas += [[input, output]]
            for c in jugada[0]:
                c.atacar(jugada[1])

    def jugadaNoTanElaborada(self):
        aliadas,enemigas = self.getColonias()
        objetivo=minimoBacterias(enemigas)
        maximo,basura=sacarMaximoBacterias(aliadas)
        maximo.atacar(objetivo)

    def get_jugadas(self):
        return self.jugadas

    def escribir_jugadas(self,direc):
        file=open(direc,"a")
        for j in self.jugadas:
            for n in j[0]:
                file.write(str(n)+" ")
            file.write("\n")
            for n in j[1]:
                file.write(str(n)+" ")
            file.write("\n")
        file.close()

    def jugar(self,dt):
        self.contador+=2*random.random()*self.dificultad*dt/1000
        while self.contador*1.0>1.0:
            jugada=self.jugadaSimple()
            if jugada!=0:
                jugada[0].atacar(jugada[1])
                output=self.parse_output([jugada[0]],jugada[1])
                input=np.array(self.campo.get_input(self.nombre))
                self.jugadas+=[[input,output]]

            else:
                self.jugadaElaborada()
            self.contador-=1

