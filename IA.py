from NeuralNetwork import *
import random


def calcularTiempo(self, origen, objetivo):
    vel = origen.tipo.velocidad
    dis = origen.dis(objetivo)
    return (dis / vel)

class IA:

    def __init__(self, network, nombre, campo, aps):
        self.network=network
        self.campo=campo
        self.nombre=nombre
        self.aps=aps
        self.contador=0.0
        self.jugadas=[]
        self.estados=[]
        self.indicador=[]
        self.evaluacion=[]
        self.gama_p=math.pow(0.1,1/(10*self.aps))
        self.gama_a=math.pow(0.1,1/(3*self.aps))


    def jugar(self, dt):

        self.contador+=dt
        while self.contador>=1000/self.aps:
            input=self.campo.get_input(self.nombre)
            self.network.feed(np.array(input))
            raw_output=self.network.get_output()
            output=self.parse_output(raw_output)
            objetivo=0
            for i in range(10,20):
                if output[i]==1:
                    objetivo=i
            for i in range(10):
                if output[i]==1:
                    self.campo.colonias[i].atacar(self.campo.colonias[objetivo-10])

            self.estados+=[input]
            self.jugadas+=[output]
            self.indicador+=[self.campo.indicador(self.nombre)]
            self.contador-=1000/self.aps

    def evaluar_jugadas(self):
        instantes=len(self.indicador)
        delta_a=[0.0]
        for i in range(1,instantes):
            delta_a+=[self.indicador[i]-self.indicador[i-1]+delta_a[i-1]*self.gama_a]
        delta_p=[0.0]
        for i in range(instantes-2,-1,-1):
            delta_p=[self.gama_p*(self.indicador[i+1]-self.indicador[i]+delta_p[0])]+delta_p
        for i in range(instantes):
            self.evaluacion+=[delta_a[i]+delta_p[i]]

    def escribir_jugadas(self,direc):
        file=open(direc,"a")
        for i in range(len(self.jugadas)):
            for n in self.estados[i]:
                file.write(str(n)+" ")
            file.write("\n")
            for n in self.jugadas[i]:
                file.write(str(n)+" ")
            file.write("\n")
            file.write(str(self.evaluacion[i])+"\n")
        file.close()

    def reiniciar_estadisticas(self):
        self.contador=0.0
        self.jugadas=[]
        self.estados=[]
        self.indicador=[]
        self.evaluacion=[]

    def entrenar_jugadas(self, epochs):
        for k in range(epochs):
            print("epoch: "+str(k))
            for i in range(len(self.jugadas)):
                input=np.array(self.estados[i])
                output=self.jugadas[i]
                learning_rate=self.evaluacion[i]
                self.network.train(input,output,learning_rate)

    def parse_output(self, raw_output):
        maxi=0
        val_max=0
        agregado=False
        output=[]
        for i in range(10):
            c=self.campo.colonias[i]
            if c.tipo.nombre==self.nombre:
                if raw_output[i]>0.5:
                    output+=[1]
                    agregado=True
                else:
                    output+=[0]
                    if raw_output[i]>val_max:
                        val_max=raw_output[i]
                        maxi=i
            else:
                output+=[0]
        if not agregado:
            output[maxi]=1
        maxi=10
        val_max=0
        for i in range(10,20):
            output+=[0]
            if raw_output[i]>val_max:
                val_max=raw_output[i]
                maxi=i
        output[maxi]=1
        return output



