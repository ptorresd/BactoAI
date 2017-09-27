import Modelo
import pygame

seleccionado=0

class Vista:
    def __init__(self,screen):
        self.screen=screen
        self.texColonia={}
        self.texAtaque={}
        self.font = pygame.font.Font('res/8bit.TTF', 16)
        self.ffont = pygame.font.Font('res/8bit.TTF', 32)
        self.Font = pygame.font.Font('res/8bit.TTF', 40)
        self.FONT = pygame.font.Font('res/8bit.TTF',90)

    def setCampo(self,campo):
        self.campo=campo

    def setJugador(self, jugador):
        self.jugador = jugador

    def dibujarVictoria(self):
        text = self.Font.render("Victory", 1, (0, 255, 0))
        self.blitCentrado(text,320,240)
        space = self.font.render("Press Space to continue", 1, (255, 255, 255))
        self.blitCentrado(space, 320, 380)

    def dibujarDerrota(self):
        text = self.Font.render("YOU DIED", 1, (255, 0, 0))
        self.blitCentrado(text,320,240)
        space = self.font.render("Press Space to continue", 1, (255, 255, 255))
        self.blitCentrado(space, 320, 380)

    def dibujarPausa(self):
        text = self.Font.render("PAUSE", 1, (255, 255, 255))
        self.blitCentrado(text,320,160)
        space = self.font.render("Press escape to resume the game", 1, (255, 255, 255))
        self.blitCentrado(space, 320, 300)

    def dibujarIntro(self):
        texFondo=pygame.image.load('res/menu.png')
        self.screen.blit(texFondo,(0,0))
        title = self.FONT.render("BACTO", 1, (255, 255, 255))
        self.blitCentrado(title, 320, 180)
        space = self.font.render("Press Space to continue", 1, (255, 255, 255))
        self.blitCentrado(space, 320, 380)

    def dibujarMenu(self):
        global seleccionado
        seleccionado = 0
        texFondo = pygame.image.load('res/menu.png')
        self.screen.blit(texFondo, (0, 0))
        self.mostrarBacteria(Modelo.rojo,120,200)
        self.mostrarBacteria(Modelo.azul, 260, 200)
        self.mostrarBacteria(Modelo.violeta, 400, 200)
        self.mostrarBacteria(Modelo.verde, 540, 200)
        space = self.Font.render("Choose your class", 1, (255, 255, 255))
        self.blitCentrado(space, 320, 80)

    def mostrarBacteria(self,tipo,posx,posy):
        tex = pygame.image.load('res/img'+tipo.nombre+'.png')
        tex =pygame.transform.scale(tex, (120, 120))
        self.blitCentrado(tex,posx,posy)
        x,y =pygame.mouse.get_pos()
        if abs(x-posx)<60 and abs(y-posy)<60:
            self.mostrarEstadisticas(tipo)
            global seleccionado
            seleccionado=tipo



    def mostrarEstadisticas(self,tipo):
        attack = self.font.render("Attack   ", 1, (255, 255, 255))
        attack2 = self.font.render(str(int(tipo.ataque//1)) + " i 5", 1, (255, 255, 255))
        self.screen.blit(attack,(80, 280))
        self.screen.blit(attack2,(460,280))
        defense = self.font.render("Defense  ", 1, (255, 255, 255))
        defense2 = self.font.render(str(int(tipo.defensa//1)) + " i 5", 1, (255, 255, 255))
        self.screen.blit(defense, (80, 320))
        self.screen.blit(defense2,(460,320))
        speed = self.font.render("Speed", 1, (255, 255, 255))
        speed2 = self.font.render(str(int(tipo.velocidad//1)) + " i 100", 1, (255, 255, 255))
        self.screen.blit(speed, (80, 360))
        self.screen.blit(speed2,(420,360))
        rep = self.font.render("Reproduction", 1, (255, 255, 255))
        rep2 = self.font.render(str(int(tipo.reproduccion//1)) + " i 5", 1, (255, 255, 255))
        self.screen.blit(rep, (80, 400))
        self.screen.blit(rep2, (460, 400))

    def dibujarCampo(self):
        texFondo=pygame.image.load('res/fondo2.png')
        self.screen.blit(texFondo,(0,0))
        self.jugador.mostrarSeleccion(pygame.mouse.get_pos(),self.screen)
        for c in self.campo.colonias:
            self.dibujarColonia(c)
        for a in self.campo.ataques:
            self.dibujarAtaque(a)

    def dibujarCampoEntrenamiento(self):
        texFondo=pygame.image.load('res/fondo2.png')
        self.screen.blit(texFondo,(0,0))
        for c in self.campo.colonias:
            self.dibujarColonia(c)
        for a in self.campo.ataques:
            self.dibujarAtaque(a)

    def dibujarColonia(self,colonia):
        pygame.init()
        nSprites=colonia.tipo.sprites
        sprite= colonia.tipo.nombre +str(int((colonia.sprite)*9)%nSprites+1)
        if not (sprite in self.texColonia):
            self.texColonia[sprite] = pygame.image.load('res/' +sprite + '.png')
        tex=self.texColonia[sprite]
        tex=pygame.transform.scale(tex, (int(2*colonia.radio), int(2*colonia.radio)))
        self.blitCentrado(tex,colonia.x,colonia.y)
        text = self.font.render(str(int(colonia.bacterias//1)), 1, (0, 0, 0))
        self.blitCentrado(text, colonia.x, colonia.y)

    def dibujarAtaque(self,ataque):
        pygame.init()
        if not(ataque.tipo.nombre in self.texAtaque):
            self.texAtaque[ataque.tipo.nombre]=pygame.image.load('res/ataque'+ataque.tipo.nombre+'.png')
        tex=self.texAtaque[ataque.tipo.nombre]
        self.blitCentrado(tex,ataque.x,ataque.y)

    def blitCentrado(self,tex,x,y):
        size=tex.get_size()
        self.screen.blit(tex,(x-size[0]/2,y-size[1]/2))