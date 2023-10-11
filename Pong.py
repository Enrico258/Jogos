#Pong 
import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((700,400))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()
p1 = 0
p2 = 0

fundo = pygame.Surface((100,200))

font = pygame.font.SysFont(None, 48)
multiB = font.render('multiplayer', True, (255,255,255))
multiV = font.render('multiplayer', True, (255,0,0))

singoB = font.render('singleplayer', True, (255,255,255))
singoV = font.render('singleplayer', True, (255,0,0))

fontP = pygame.font.SysFont(None, 60)

class Button():
    def __init__(self,x,y,image,press):
        self.image = image
        self.pressed = press
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            screen.blit(self.pressed, (self.rect.x, self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

singo = Button(80, 150, singoB, singoV)
multi = Button(420, 150, multiB, multiV)




def menu():
    screen.fill((0,0,0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if singo.draw() == True:
            return 0

        if multi.draw() == True:
            return 1

        pygame.display.update()

def single():
    raquete = Rect(650, 60, 15, 50)
    bolita = Rect(350, 180, 10, 10)
    sinalx = 1
    sinaly = 0
    contador = 1
    
    while True:
        keys = pygame.key.get_pressed()
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
        #posição raquete
        if keys[pygame.K_w]:
            raquete.y -= 2
        if keys[pygame.K_s]:
            raquete.y += 2
        if raquete.y < -50:
            raquete.y = 390
        if raquete.y > 400:
            raquete.y = -50

        #posição bolinha
        if bolita.x <= 0:
            sinalx = 1
        if raquete.colliderect(bolita) == 1:
            sinalx = -1
        if bolita.x >= 700:
            print("Perdeu")
            pygame.quit()
            exit()
        if bolita.midright[1] < raquete.midleft[1] + 2 and raquete.colliderect(bolita) == 1:
            sinaly = -1
            contador += 0.2
        if bolita.midright[1] > raquete.midleft[1] + 2 and raquete.colliderect(bolita) == 1:
            sinaly = 1
            contador += 0.2
        if bolita.midtop[1] <= 0:
            sinaly = 1
        if bolita.midbottom[1] >= 400:
            sinaly = -1
    
        bolita.x += 2*sinalx*contador
        bolita.y += 2*sinaly*contador
    
        pygame.draw.rect(screen, (255,255,255), raquete)
        pygame.draw.rect(screen, (255,255,255), bolita)
        #print(bolita.midright[1])
        #print(raquete.midleft[1])

        pygame.display.update()
        clock.tick(60)

def multiplayer(placar, vez):
    raquete1 = Rect(50, 60, 15, 50)
    raquete2 = Rect(650, 60, 15, 50)
    bolita = Rect(350, 180, 10, 10)
    sinalx = vez
    sinaly = 0
    contador = 1
    while True:
        keys = pygame.key.get_pressed()
        screen.fill((0,0,0))
        screen.blit(placar, (330, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        #posição raquete 1
        if keys[pygame.K_w]:
            raquete1.y -= 2
        if keys[pygame.K_s]:
            raquete1.y += 2
        if raquete1.y < -50:
            raquete1.y = 390
        if raquete1.y > 400:
            raquete1.y = -50

        #posição raquete 2
        if keys[pygame.K_UP]:
            raquete2.y -= 2
        if keys[pygame.K_DOWN]:
            raquete2.y += 2
        if raquete2.y < -50:
            raquete2.y = 390
        if raquete2.y > 400:
            raquete2.y = -50

        #posição bolinha
        if raquete1.colliderect(bolita) == 1:
            sinalx = 1
        if raquete2.colliderect(bolita) == 1:
            sinalx = -1
        if bolita.x >= 700:
            return 1
        if bolita.x <= 0:
            return 2
        if bolita.midright[1] < raquete1.midleft[1] + 2 and raquete1.colliderect(bolita) == 1:
            sinaly = -1
            contador += 0.2
        if bolita.midright[1] > raquete1.midleft[1] + 2 and raquete1.colliderect(bolita) == 1:
            sinaly = 1
            contador += 0.2
        if bolita.midright[1] < raquete2.midleft[1] + 2 and raquete2.colliderect(bolita) == 1:
            sinaly = -1
        if bolita.midright[1] > raquete2.midleft[1] + 2 and raquete2.colliderect(bolita) == 1:
            sinaly = 1
        if bolita.midtop[1] <= 0:
            sinaly = 1
        if bolita.midbottom[1] >= 400:
            sinaly = -1
    
        
    
        bolita.x += 2*sinalx*contador
        bolita.y += 2*sinaly*contador
    
        pygame.draw.rect(screen, (255,255,255), raquete1)
        pygame.draw.rect(screen, (255,255,255), raquete2)
        pygame.draw.rect(screen, (255,255,255), bolita)
        #print(bolita.midright[1])
        #print(raquete.midleft[1])

        pygame.display.update()
        clock.tick(60)

modo = menu()
vez = -1
while modo == 0:
    single()
while modo == 1:
    placar = fontP.render(str(p1)+":"+str(p2), True, (255,255,255))
    if multiplayer(placar, vez) == 1:
        p1 += 1
        vez = -1
    else:
        p2 += 1
        vez = 1



