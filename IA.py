from NeuralNetwork import *
import random
class IA:

    def __init__(self, network, nombre, campo, aps):
        self.network=network
        self.campo=campo
        self.nombre=nombre
        self.aps=aps
        self.contador=0

    def jugar(self, dt):

        self.contador+=random.random()*self.aps*dt/1000
        while self.contador*1.0>1.0:
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
            self.contador-=1


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



