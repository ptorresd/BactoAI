import random
import math


################################################### Tipo ##############################################################

class TipoBacteria:
    def __init__(self, velocidad, ataque, defensa, reproduccion, nombre, sprites):
        self.nombre = nombre
        self.velocidad = velocidad
        self.ataque = ataque
        self.defensa = defensa
        self.reproduccion = reproduccion
        self.sprites = sprites

    #las siguientes funciones hacen que el movimiento de las bacterias sea unico segun cada clase

    def dx(self,t):                                       #componente de la velocidad tangencial a la direccion
        if self.nombre=="Rojo":
            t=(1000*t)%1500
            if t<=750:
                return 2.5
            else:
                return -0.5
        if self.nombre=="Verde":
            t=(1000*t)%500
            if t<=250:
                return 1.5
            else:
                return 0.5
        if self.nombre=="Violeta":
            t=(1000*t)%500
            if t<=400:
                return 1.15
            else:
                return 0.4
        return 1


    def dy(self,t):                                     #componente de la velocidad perpendicular a la direccion
        if self.nombre=="Violeta":
            t=(1000*t)%1000
            if t<=400:
                return 0.25
            if t<=500:
                return -1
            if t<=900:
                return -0.25
            return 1
        if self.nombre=="Azul":
            return 1.25*math.sin(5*t)-0.1
        return 0


rojo = TipoBacteria(40, 5, 5, 2.5, "Rojo", 6)
azul = TipoBacteria(70, 3, 3, 3, "Azul", 6)
violeta = TipoBacteria(130, 3.5, 1.5, 3, "Violeta", 6)
verde = TipoBacteria(70, 2, 2, 5  , "Verde", 6)

training_1 = TipoBacteria(70, 3, 3, 3, "T1", 6)
training_2 = TipoBacteria(70, 3, 3, 3, "T2", 6)


##################################################### Campo ###########################################################


class Campo:


    def __init__(self):
        self.colonias=[]
        self.ataques=[]

    def set_amenaza(self):
        for c in self.colonias:
            c.amenaza=0.0
        for a in self.ataques:
            a.objetivo.amenaza+=a.cantidad
        for c in self.colonias:
            c.amenaza=min(c.amenaza/(c.bacterias+30),1.0)

    def get_input(self, nombre):
        input=[]
        self.set_amenaza()
        for c in self.colonias:
            mismo_tipo=0
            if c.tipo.nombre==nombre:
                mismo_tipo=1
            input+=[c.x/640, c.y/480,min(c.bacterias/100,1),mismo_tipo, c.amenaza]
        return input


    def indicador(self, nombre):
        ind=0
        for c in self.colonias:
            if c.tipo.nombre==nombre:
                ind+=50+c.bacterias
            else:
                ind-=50+c.bacterias
        for a in self.ataques:
            if a.tipo.nombre==nombre:
                ind+=a.cantidad
            else:
                ind-=a.cantidad
        return ind

    def rellenar(self,tipo1,tipo2):
        neutral=TipoBacteria(0,0,1,0,"neutral",1)
        n=10#int(random.random()*5+10)
        base1=Colonia(60,60,20,tipo1,45)
        self.addColonia(base1)
        base2=Colonia(580,420,20,tipo2,45)
        self.addColonia(base2)
        for i in range(n-2):
            while True:
                cNeutral=self.generarColoniaRandom(neutral)
                if self.cabe(cNeutral):
                    self.addColonia(cNeutral)
                    break

    def revisarDerrota(self,nombre):
        for c in self.colonias:
            if c.tipo.nombre==nombre:
                return False
        return True


    def cabe(self,colonia):
        for c in self.colonias:
            if c.choque(colonia):
                return False

        return True

    def generarColoniaRandom(self,tipo):
        n=int(random.random()*4+1)
        r=17
        x=int(random.random()*(640-2*r)+r)
        y = int(random.random() * (480 - 2 * r) + r)
        return Colonia(x,y,n,tipo,r)


    def addColonia(self,colonia):
        self.colonias+=[colonia]
        colonia.campo=self

    def addAtaque(self, ataque):
        self.ataques += [ataque]

    def actualizar(self,dt):
        for c in self.colonias:
            c.actualizar(dt)

        for a in self.ataques:
            a.actualizar(dt)

    def eliminarAtaque(self,ataque):
        aux=[]
        for a in self.ataques:
            if ataque!=a:
                aux+=[a]
        self.ataques=aux

##################################################### Colonia #########################################################

class Colonia:

    def __init__(self,x,y,nBacterias,tipo,radio):
        self.amenaza=0.0
        self.radioMin=radio*1.0
        self.radioMax=radio+34
        self.campo=[]
        self.tipo=tipo
        self.x=x
        self.y=y
        self.bacterias=nBacterias
        self.sprite=0
        self.actualizar(0)

    def dis(self,otraColonia):
        return ((self.x - otraColonia.x) ** 2 + (self.y - otraColonia.y) ** 2) ** (1 / 2)

    def choque(self,colonia):
        return ((self.x-colonia.x)**2+(self.y-colonia.y)**2)**(1/2)<self.radio+colonia.radio+75

    def atacar(self, objetivo):
        ataque=Ataque(self,objetivo,self.campo)
        self.campo.addAtaque(ataque)

    def actualizar(self,dt):
        self.bacterias+=self.tipo.reproduccion*dt
        self.sprite+=dt
        if self.bacterias>100.5:
            self.bacterias-=10*dt

        self.radio=self.radioMin+min(34.0,self.bacterias/3)

############################################################### Ataque #################################################


def distanciaRectaPunto(A,B,C,x,y):
    return (A*x+B*y+C)/(A**2+B**2)**(1/2)

def estaEnElRango(xi,yi,xf,yf,colonia):
    r=colonia.radioMax-3
    enX=(xi<colonia.x+r and colonia.x-r<xf) or (xi>colonia.x-r and colonia.x+r>xf)
    enY=(yi<colonia.y+r and colonia.y-r<yf) or (yi>colonia.y-r and colonia.y+r>yf)
    fueraDelInicioX=(xi<colonia.x-r and xf<colonia.x+r) or (xi>colonia.x+r or xf>colonia.x-r)
    fueraDelInicioY=(yi<colonia.y-r and xf<colonia.y+r) or (yi>colonia.y+r or yf>colonia.y-r)
    return enX and enY and fueraDelInicioX and fueraDelInicioY

def signo(x):
    if x==0:
        return 1
    return int(x*1.0/abs(x))


class Ataque:

    def __init__(self,origen, objetivo,campo):
        self.campo=campo
        self.origen=origen
        self.x=origen.x
        self.y=origen.y
        self.tipo=origen.tipo
        self.baneados=[origen,objetivo]
        self.objetivo=objetivo
        self.cantidad=(origen.bacterias+1)//2
        origen.bacterias=origen.bacterias-self.cantidad
        self.trayectoria=self.calcularTrayectoria()
        self.t=0

    def hayColision(self,xi,yi,xf,yf):              #despues de muchos parches estas funciones son un caos, pero funcionan, la mayoria de las veces...
        A=(yf-yi)
        B=(xi-xf)
        C=-A*xi-B*yi
        for colonia in self.campo.colonias:
            if estaEnElRango(xi,yi,xf,yf,colonia) and colonia not in self.baneados:
                self.baneados+=[colonia]
                dis=distanciaRectaPunto(A,B,C,colonia.x,colonia.y)
                if abs(dis)<colonia.radioMax:
                    dx=A/(A**2+B**2)**(1/2)
                    dy=B/(A**2+B**2)**(1/2)
                    x=colonia.x-signo(dis)*colonia.radioMax*dx*1.05
                    y=colonia.y-signo(dis)*colonia.radioMax*dy*1.05
                    if abs(x-xi)>1 and abs(y-yi)>1 and abs(x-xf)>1 and abs(y-yf)>1:
                        return [x,y]
        return [xf,yf]

    def calcularTrayectoria(self):
        xi=self.origen.x
        yi=self.origen.y
        xf=self.objetivo.x
        yf=self.objetivo.y
        return self.calcularTrayectoriaRecursivo(xi,yi,xf,yf,1)

    def calcularTrayectoriaRecursivo(self,xi,yi,xf,yf,nivel):
        if abs(xi-xf)<1 and abs(yi-yf)<1 or nivel>7:
            return [[xf,yf]]
        x,y=self.hayColision(xi,yi,xf,yf)
        if abs(x-xf)<1 and abs(y-yf)<1:
            return [[xf,yf]]
        return self.calcularTrayectoriaRecursivo(xi,yi,x,y,nivel+1)+self.calcularTrayectoriaRecursivo(x,y,xf,yf,nivel+1)

    def actualizar(self,dt):
        self.t+=dt
        dis=((self.trayectoria[0][0]*1.0-self.x*1.0)**2+(self.trayectoria[0][1]*1.0-self.y*1.0)**2)**(1/2)
        if dis<self.objetivo.radio:
            self.trayectoria.pop(0)
            if len(self.trayectoria) == 0:
                self.atacar()
                self.objetivo.campo.eliminarAtaque(self)
            return
        compx=dt*(self.trayectoria[0][0]-self.x)*self.tipo.velocidad/dis
        compy=  dt * (self.trayectoria[0][1] - self.y) * self.tipo.velocidad/dis
        self.x+=(compx*self.tipo.dx(self.t)-compy*self.tipo.dy(self.t))
        self.y+=(compy*self.tipo.dx(self.t)+compx*self.tipo.dy(self.t))
        if self.x==self.trayectoria[0][0]:
            self.trayectoria.pop(0)
            if len(self.trayectoria)==0:
                self.atacar()
                self.objetivo.campo.eliminarAtaque(self)


    def atacar(self):
        if self.objetivo.tipo.nombre!=self.tipo.nombre:
            bajas = self.cantidad*self.tipo.ataque/self.objetivo.tipo.defensa
            if bajas>self.objetivo.bacterias:
                self.objetivo.bacterias=self.cantidad-(self.objetivo.bacterias*self.objetivo.tipo.defensa)/self.tipo.ataque
                self.objetivo.tipo=self.tipo
                self.objetivo.sprite=0
            else:
                self.objetivo.bacterias=self.objetivo.bacterias-bajas
        else:
            self.objetivo.bacterias=self.objetivo.bacterias+self.cantidad

        self.objetivo.campo.eliminarAtaque(self)


