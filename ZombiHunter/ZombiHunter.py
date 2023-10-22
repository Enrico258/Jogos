#Pong 
import pygame
from pygame.locals import *
from sys import exit
from pygame import mixer
import random
from math import asin, acos, degrees, pi, cos, sin, radians, atan2

pygame.init()
screen = pygame.display.set_mode((1400,800))
pygame.display.set_caption('ZombieHunters')
clock = pygame.time.Clock()

#imagens personagens
jax = pygame.image.load('designs/jogador/jax.png')
jax = pygame.transform.scale(jax, (180, 260))
jay = pygame.image.load('designs/jogador/jay.png')
jay = pygame.transform.scale(jay, (180, 260))
jerry = pygame.image.load('designs/jogador/jerry.png')
jerry = pygame.transform.scale(jerry, (180, 260))
jaxAD = pygame.image.load('designs/jogador/jaxAD.png')
jaxAD = pygame.transform.scale(jaxAD, (180, 260))
jayAD = pygame.image.load('designs/jogador/jayAD.png')
jayAD = pygame.transform.scale(jayAD, (180, 260))
jerryAD = pygame.image.load('designs/jogador/jerryAD.png')
jerryAD = pygame.transform.scale(jerryAD, (180, 260))
jaxAE = pygame.image.load('designs/jogador/jaxAE.png')
jaxAE = pygame.transform.scale(jaxAE, (180, 260))
jayAE = pygame.image.load('designs/jogador/jayAE.png')
jayAE = pygame.transform.scale(jayAE, (180, 260))
jerryAE = pygame.image.load('designs/jogador/jerryAE.png')
jerryAE = pygame.transform.scale(jerryAE, (180, 260))

#inimigos
fantasma = pygame.image.load('designs/mobs/fantasma.png')
fantasma = pygame.transform.scale(fantasma, (36, 52))


personagens = [[jax, jaxAD, jaxAE], [jay, jayAD, jayAE], [jerry, jerryAD, jerryAE]]


player = jax.get_rect()

setaD = pygame.image.load('designs/setaD.png')
setaD = pygame.transform.scale(setaD, (50, 50))
setaE = pygame.image.load('designs/setaE.png')
setaE = pygame.transform.scale(setaE, (50, 50))
dR = setaD.get_rect()
eR = setaE.get_rect()
dR.x = 900
dR.y = 300
eR.x = 450
eR.y = 300


texto = pygame.font.Font(None, 30)
textoB = pygame.font.Font(None, 100)

jogarW = textoB.render('JOGAR', False, 'White')
jogarV = textoB.render('JOGAR', False, 'Red')
escolherB = textoB.render('ESCOLHER', False, 'BLACK')
escolherV = textoB.render('ESCOLHER', False, 'Red')


no = pygame.font.Font(None, 100)
nome = no.render('Zombie Hunters', False, 'White')
sub = texto.render('The infinite monsters shooter', False, 'White')

fundo = pygame.image.load('mapa/mapa.png')
fundo = pygame.transform.scale(fundo, (9600, 6400))

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


jogarB = Button(600, 400, jogarW, jogarV)
escolherB = Button(530, 500, escolherB, escolherV)

class Square:
    def __init__(self, color, x, y, width, height, speed):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = color
        self.speed = speed

    def collided(self, other_rect):
        #Return True if self collided with other_rect
        return self.rect.colliderect(other_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

#classe tiro
class Bullet(Square):
    def __init__(self, color, x, y, width, height, speed, targetx,targety):
        super().__init__(color, x, y, width, height, speed)
        angle = atan2(targety-y, targetx-x) 
        #print('Angle in degrees:', int(angle*180/pi))
        self.dx = cos(angle)*speed
        self.dy = sin(angle)*speed
        self.x = x
        self.y = y
    
    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

#classe inimigo
class MobVisu:
    def __init__(self, skin, x, y, speed):
        self.skin = skin
        self.rect = self.skin.get_rect()
        self.speed = speed

    def collided(self, other_rect):
        #Return True if self collided with other_rect
        return self.rect.colliderect(other_rect)

    def draw(self):
        screen.blit(self.skin, (self.rect))
        
class Mobs(MobVisu):
    def __init__(self, skin, x, y, speed, targetx, targety):
        super().__init__(skin, x, y, speed)
        angle = atan2(targety-y, targetx-x) 
        #print('Angle in degrees:', int(angle*180/pi))
        self.dx = cos(angle)*speed
        self.dy = sin(angle)*speed
        self.x = x
        self.y = y
        self.xa = x
        self.ya = y
    
    def move(self, vx, vy):
        
        self.x += self.dx + vx
        self.y += self.dy + vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        

pente = []
inimigos = []

def personagem():
    screen.fill("Black")
    co = 0
    boneco = personagens[0][0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        pos = pygame.mouse.get_pos()
        screen.fill("GRAY")
        
        if pygame.mouse.get_pressed()[0] == 1 and eR.collidepoint(pos) == 1:
            co -= 1
            boneco = personagens[co%3][0]
            
        if pygame.mouse.get_pressed()[0] == 1 and dR.collidepoint(pos) == 1:
            co += 1
            boneco = personagens[co%3][0]
            
        screen.blit(boneco, (620, 200))
        screen.blit(setaD, (dR.x, dR.y))
        screen.blit(setaE, (eR.x, eR.y))
        
        if escolherB.draw() == True:
            return personagens[co%3][1], personagens[co%3][2]
            

        pygame.display.update()

def menu():
    screen.fill("Black")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        
        screen.fill("BLACK")
        screen.blit(nome, (60,0))
        screen.blit(sub, (100,60))
        if jogarB.draw() == True:
            return 1
            

        pygame.display.update()


def jogo(persoD, persoE):
    pos = pygame.mouse.get_pos()    
    lado = 0
    fontP = pygame.font.SysFont(None, 60)
    persoD = pygame.transform.scale(persoD, (36, 52))
    persoE = pygame.transform.scale(persoE, (36, 52))
    player = pygame.transform.scale(persoD, (36, 52))
    playerP = player.get_rect()
    fundoP = fundo.get_rect()
    fundoP.x = -2915
    fundoP.y = -3360
    playerP.x = 700
    playerP.y = 350
    fantasmaP = fantasma.get_rect()
    pontos = 0
    while True:
        vx = 0
        vy = 0
        boost = 1
        placar = fontP.render(str(pontos), True, (255,0,0))
        keys = pygame.key.get_pressed()
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                #print(x,y)
                b = Bullet((0,0,0), 720, 370, 5, 5, 20, x,y)
                pente.append(b)
                
        
        
        #controlar jogador
        if keys[pygame.K_LSHIFT]:
            boost = 2
        if keys[pygame.K_w]:
            vy = 4*boost
            fundoP.y += vy
        if keys[pygame.K_s]:
            vy = -4*boost
            fundoP.y += vy
        if keys[pygame.K_a]:
            vx = 4*boost
            fundoP.x += vx
            player = persoE
        if keys[pygame.K_d]:
            vx = -4*boost
            fundoP.x += vx
            player = persoD

        for b in pente:
            b.move()
        for e in inimigos:
            e.move(vx, vy)
            
        #gera inimigo
        if random.randint(5,45) == 15: 
            x = random.randint(-100,1500)
            y = random.randint(-100,900)
            x = 750
            y = 900
            velo = 3
            if x < 0 or x > 1400 or y < 0 or y > 800:
                e = Mobs(fantasma, x, y, velo,700, 350)
                inimigos.append(e)
        
        #inimigos
        nX = random.randint(0, 1400)
        ny = random.randint(0, 800)
        
        for i in reversed(range(len(pente))):
            for j in reversed(range(len(inimigos))):
                if pente[i].collided(inimigos[j].rect):
                    pontos += 10
                    del inimigos[j]
                    del pente[i]
                    break
                
        for k in reversed(range(len(inimigos))):
            if inimigos[k].collided(playerP):
                return
            
        screen.blit(fundo, (fundoP.x, fundoP.y))
        screen.blit(player, (700, 350))
        screen.blit(placar, (0, 0))
        
        for b in pente:
            b.draw(screen)
        for e in inimigos:
            e.draw()
            
        pygame.display.flip()
        clock.tick(60)
        
final = no.render('VOCÊ PERDEU', False, 'RED')

def fim():
    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.blit(final, (500, 350))
        pygame.display.flip()
        clock.tick(60)
        
if (menu() == True):
    persoD, persoE = personagem()
    jogo(persoD, persoE)
    fim()



