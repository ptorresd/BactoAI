import Vista
import pygame
import Modelo as mdl
from pygame.locals import *
import random
import Jugador
import time
import Greedy
from IA import *

snd_intro = 0
snd_cursor = 0
tipoJugador = 0
jugador=0
campo=0
ia=0
ia2=0
tiempo=0

def escogerTipoIA():
    tipos=[mdl.rojo,mdl.verde,mdl.violeta,mdl.azul]
    aux=[]
    for t in tipos:
        if t!=tipoJugador:
            aux+=[t]
    i=random.randint(0,2)
    return aux[i]



def estadoIntro(vista):
    snd_intro.play(-1 )
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    snd_cursor.play(0)
                    pygame.time.wait(400)
                    return "menu"
        vista.dibujarIntro()
        pygame.display.flip()

def estadoMenu(vista):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONUP:
                if Vista.seleccionado!=0:
                    snd_cursor.play(0)
                    pygame.time.wait(400)
                    snd_intro.stop()
                    global tipoJugador
                    tipoJugador = Vista.seleccionado
                    preparaJuego(vista)
                    return "juego"

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    snd_intro.stop()
                    return "entrenamiento"
        vista.dibujarMenu()
        pygame.display.flip()

def preparaJuego(vista):
    global campo
    global jugador
    global ia
    global ia2
    campo = mdl.Campo()
    tipoIA=escogerTipoIA()
    campo.rellenar(tipoJugador, tipoIA)
    jugador=Jugador.Jugador(campo,tipoJugador)
    vista.setCampo(campo)
    vista.setJugador(jugador)
    ia2=Greedy.IA(tipoIA.nombre, campo, 0.8)
    network=import_network("IA_java6.txt")
    ia = IA(network,tipoIA.nombre, campo, 1.5)

def estadoJuego(vista):
    snd_main = pygame.mixer.Sound('res/MainTheme.wav')
    snd_main.play(-1)
    clock = pygame.time.Clock()
    click=False
    seleccionado=False
    holding=False
    tClick=0

    while True:

        dt=clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                x,y=event.pos
                holding=True
                seleccionado=jugador.agregarColonia(x,y)
                tClick=time.time()
            if event.type ==MOUSEBUTTONUP:
                x,y=event.pos
                holding=False
                if (time.time()-tClick)*1.0>0.15:
                    jugador.atacarColonia(x,y)
                    click=False
                elif not click and seleccionado:
                    click=True
                else:
                    jugador.atacarColonia(x,y)
                    click=False
            if event.type == KEYDOWN:
                if event.key== K_m:
                    snd_cursor.play(0)
                    pygame.time.wait(400)
                    snd_main.stop()
                    snd_intro.play(-1)
                    return "menu"
                if event.key== K_ESCAPE:
                    snd_cursor.play(0)
                    pygame.time.wait(200)
                    snd_main.stop()
                    return "pausa"




        if holding:
            x,y=pygame.mouse.get_pos()
            jugador.agregarColonia(x,y)

        campo.actualizar(dt/1000)
        vista.dibujarCampo()
        pygame.display.flip()
        if campo.revisarDerrota(jugador.nombre):
            snd_main.stop()
            return "derrota"
        elif campo.revisarDerrota(ia.nombre):
            snd_main.stop()
            return "victoria"
        ia.jugar(dt)
        #ia2.jugar(dt)             #para ver a las IAs jugar entre si, descomentar esta linea

def estadoEntrenamiento(vista):
    global campo
    clock = pygame.time.Clock()
    network=import_network("IA_java6.txt")
    #network = Network(50, [300, 100, 20])
    seguir=True
    greedy=0
    nn=0
    while seguir:
        campo = mdl.Campo()
        campo.rellenar(mdl.training_1,mdl.training_2)
        ia_greedy=Greedy.IA("T2", campo, 0.5)
        ia_nn = IA(network,"T1", campo, 0.5)
        vista.setCampo(campo)
        vista.setJugador(jugador)
        termino=False
        while True:
            dt=200
            #dt=clock.tick(60)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key== K_SPACE:
                        seguir=False

            campo.actualizar(dt / 1000)

            ver=False
            if ver:
                vista.dibujarCampoEntrenamiento()
                pygame.display.flip()

            if campo.revisarDerrota("T1"):
                #ia_greedy.escribir_jugadas("jugadas.txt")
                greedy+=1
                termino=True
            elif campo.revisarDerrota("T2"):
                #ia_nn.escribir_jugadas("jugadas.txt")
                nn+=1
                termino=True

            if termino:
                break

            ia_greedy.jugar(dt)
            ia_nn.jugar(dt)
        #jugadas=ia_greedy.get_jugadas()
        #ia_nn.escribir_jugadas("jugadas.txt")
        #ia_nn.entrenar_greedy(jugadas,10,0.0002)
        #ia_nn.entrenar_jugadas(10,200000)

    #network.export_network("IA_java2.txt")
    print("greedy: "+str(greedy))
    print("nn: " + str(nn))
    return "menu"



def estadoPausa(vista):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key== K_ESCAPE:
                    snd_cursor.play(0)
                    pygame.time.wait(200)
                    return "juego"
        vista.dibujarPausa()
        pygame.display.flip()


def estadoVictoria(vista):
    snd_fanfare = pygame.mixer.Sound('res/Fanfare.wav')
    snd_fanfare.play(0)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key== K_SPACE:
                    snd_fanfare.stop()
                    snd_cursor.play(0)
                    pygame.time.wait(400)
                    snd_intro.play(-1)
                    return "menu"
        vista.dibujarVictoria()
        pygame.display.flip()

def estadoDerrota(vista):

    snd_defeat = pygame.mixer.Sound('res/Defeat.wav')
    snd_defeat.play(0)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key== K_SPACE:
                    snd_defeat.stop()
                    snd_cursor.play(0)
                    pygame.time.wait(400)
                    snd_intro.play(-1)
                    return "menu"
        vista.dibujarDerrota()
        pygame.display.flip()






def main():
    pygame.init()
    global snd_intro
    snd_intro = pygame.mixer.Sound('res/Intro.wav')
    global snd_cursor
    snd_cursor = pygame.mixer.Sound('res/cursor.wav')
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Bacto')
    vista=Vista.Vista(screen)
    col=mdl.Colonia(420,257,5,mdl.rojo,17)
    a=mdl.estaEnElRango(580,420,390,151,col)
    estado="intro"
    while True:
        if estado=="menu":
            estado=estadoMenu(vista)
        if estado=="intro":
            estado=estadoIntro(vista)
        if estado=="juego":
            estado=estadoJuego(vista)
        if estado=="victoria":
            estado=estadoVictoria(vista)
        if estado == "derrota":
            estado = estadoDerrota(vista)
        if estado == "pausa":
            estado = estadoPausa(vista)
        if estado=="entrenamiento":
            estado = estadoEntrenamiento(vista)



if __name__ == '__main__':
    main()