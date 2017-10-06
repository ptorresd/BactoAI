from NeuralNetwork import *
import random


def calcularTiempo(self, origen, objetivo):
    vel = origen.tipo.velocidad
    dis = origen.dis(objetivo)
    return (dis / vel)

class IA:

    def __init__(self, network, nombre, campo, aps, delta):
        self.network=network
        self.campo=campo
        self.nombre=nombre
        self.aps=aps
        self.delta=delta
        self.contador_jugada=0.0
        self.contador_indice=0
        self.jugadas=[]
        self.estados=[]
        self.indicador=[]
        self.evaluacion=[]
        self.gama_p=math.pow(0.1,delta/1000)
        self.gama_a=math.pow(0.1,delta/300)


    def jugar(self, dt):

        self.contador_indice+=dt
        self.contador_jugada+=dt
        while self.contador_indice>=self.delta:
            self.indicador+=[self.campo.indicador(self.nombre)]
            self.contador_indice-=self.delta


        while self.contador_jugada>=1000/self.aps:
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
            self.contador_jugada-=1000/self.aps

    def evaluar_jugadas(self):
        instantes=len(self.indicador)
        delta_a=[0.0]
        for i in range(1,instantes):
            delta_a+=[self.indicador[i]-self.indicador[i-1]+delta_a[i-1]*self.gama_a]
        delta_p=[0.0]

        for i in range(instantes-2,-1,-1):
            delta_p=[self.gama_p*(self.indicador[i+1]-self.indicador[i]+delta_p[0])]+delta_p

        print(self.indicador)
        print(delta_a)
        print(delta_p)


        for i in range(len(self.jugadas)):
            t=min(int((4+i/self.aps)*1000/self.delta),instantes-1)
            self.evaluacion+=[delta_a[t]+delta_p[t]]



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

    def cambiar_sentido(self, input, x, y):
        new_input=[]
        for i in range(50):
            if i%5==0:
                new_input+=[(x*input[i]+(1-x)/2)]
            elif i%5==1:
                new_input+=[(y*input[i]+(1-y)/2)]
            else:
                new_input+=[input[i]]
        return np.array(new_input)

    def entrenar_greedy(self, jugadas, epochs, learning_rate):
        for k in range(epochs):
            for j in jugadas:
                input=self.cambiar_sentido(j[0],-1,-1)
                output=j[1]
                self.network.train(input,output,learning_rate)

    def entrenar_jugadas(self, epochs, div):
        for k in range(epochs):
            print("epoch: "+str(k))
            for i in range(len(self.jugadas)):
                input=np.array(self.estados[i])
                output=self.jugadas[i]
                learning_rate=self.evaluacion[i]/div
                self.network.train(input,output,learning_rate)

    def parse_output(self, raw_output):
        print(raw_output)
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



