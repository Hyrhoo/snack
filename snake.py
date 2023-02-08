from kandinsky import draw_string, fill_rect, get_pixel, set_pixel, color, display
from time import sleep, monotonic
from random import randint
from pygame.key import get_pressed; from pygame.constants import *

# variabls
speed = 0.15 # le temps entre chaque déplacement du serpent
extend = 5 # la taille en plus que donne une pomme en la mangant 
apple_score = 15 # le score que donne une pomme
nbr_apple = 1 # nombre de pommes qui aparesse à chaque fois qu'une pomme doit apparêtre
mod = 1 # 1 = standard, 2 = vitesse accelère et taille augmente au cour du temps
wall = 2 # 1 = solide, 2 = téléport

# colors
c_board = (248, 252, 248) # du fond
c_snake = (0, 252, 120) # couleur du sepent (tige pomme)
c_bord = (16, 128, 24) # couleur des bords du sepent (tige pomme, yeux serpent)
c_apple = (248,0,0) # couleur des pommes (yeux du sepent, mort)

class Snake:

    def __init__(self, length=5, position=[10,7], direction=[1,0]) -> None:
        self.length = length
        self.pos = position
        self.snake = [self.pos.copy()]
        self.direc = direction

    def fill_head(self):
        x,y = (self.pos[0]*10) - (self.direc[0] if len(self.snake)>1 and self.direc[0] else -1), (22+self.pos[1]*10) - (self.direc[1] if len(self.snake)>1 and self.direc[1] else -1)
        width,height = 10 if self.direc[0] and len(self.snake)>1 else 8, 10 if self.direc[1] and len(self.snake)>1 else 8
        fill_rect(x,y,width,height,c_snake)

    def draw_face(self):
        x,y = 2+self.pos[0]*10, 24+self.pos[1]*10
        if self.direc == [1,0]:
            fill_rect(x+3,y,1,6,c_bord)
            fill_rect(x+4,y+1,1,4,c_apple)
            fill_rect(x+3,y+2,2,2,c_snake)
        if self.direc == [-1,0]:
            fill_rect(x+2,y,1,6,c_bord)
            fill_rect(x+1,y+1,1,4,c_apple)
            fill_rect(x+1,y+2,2,2,c_snake)
        if self.direc == [0,1]:
            fill_rect(x,y+3,6,1,c_bord)
            fill_rect(x+1,y+4,4,1,c_apple)
            fill_rect(x+2,y+3,2,2,c_snake)
        if self.direc == [0,-1]:
            fill_rect(x,y+2,6,1,c_bord)
            fill_rect(x+1,y+1,4,1,c_apple)
            fill_rect(x+2,y+1,2,2,c_snake)

    def head_contour(self):
        x,y = self.pos[0]*10, 22+self.pos[1]*10
        fill_rect(x,y,10,10,c_bord)

    def delete_old_head(self):
        pos = self.snake[-2]
        x,y = pos[0]*10, 22+pos[1]*10
        fill_rect(x+1,y+1,8,8,c_snake)

    def draw_head(self):
        self.head_contour()
        self.fill_head()
        self.draw_face()
        if len(self.snake)>1: self.delete_old_head()

    def delete_old_queue(self):
        pos = self.snake[0].copy()
        teste = [(-1,0,10,0), (1,0,-1,0), (0,-1,0,10), (0,1,0,-1)]
        for i in teste:
            pos_teste = [pos[0]+i[0], pos[1]+i[1]]
            self.correct_pos(pos_teste)
            if pos_teste[0] in range(32) and pos_teste[1] in range(20) and pos_teste not in self.snake:
                x,y = pos_teste[0]*10, 22+pos_teste[1]*10
                if get_pixel(x,y) == c_bord:
                    fill_rect(x,y,10,10,c_board)
                    width,height = 1+9*abs(i[1]), 1+9*abs(i[0])
                    fill_rect(x+i[2],y+i[3],width,height,c_bord)
                    break

    def affichage(self):
        self.draw_head()
        self.delete_old_queue()

    def correct_pos(self, tab):
        if tab[0] > 31: tab[0] = 0
        elif tab[0] < 0: tab[0] = 31
        if tab[1] > 19: tab[1] = 0
        elif tab[1] < 0: tab[1] = 19

    def move(self):
        old_pos = self.pos.copy()
        self.pos = [self.pos[0]+self.direc[0], self.pos[1]+ self.direc[1]]
        if wall == 2: self.correct_pos(self.pos)
        self.snake.append(self.pos.copy())
        while len(self.snake)>self.length: del self.snake[0]
        return old_pos

    def rotat(self, new_dir):
        if new_dir[0] and not self.direc[0]: self.direc = new_dir.copy()
        if new_dir[1] and not self.direc[1]: self.direc = new_dir.copy()

    def update(self, new_dir):
        self.rotat(new_dir)
        old = self.move()
        heat = self.heat()
        if mod == 2: self.length += 0.2
        loos = self.loos()
        if not loos: self.affichage()
        else: self.delete_old_head(),self.delete_old_queue(),fill_rect(1+old[0]*10,23+old[1]*10,8,8,c_apple)
        return loos,heat

    def heat(self):
        x,y = 4+self.pos[0]*10, 26+self.pos[1]*10
        heat = get_pixel(x,y) == c_apple
        if heat:
            self.length += extend
            for _ in range(nbr_apple):
                new_apple()
        return heat

    def loos(self):
        return ((not -1 < self.pos[0] < 32 or not -1 < self.pos[1] < 20) and wall == 1) or get_pixel(self.pos[0]*10,22+self.pos[1]*10) == c_bord

def new_apple():
    rx,ry = randint(0,31)*10, 22+randint(0,19)*10
    while get_pixel(rx,ry) == c_bord:
        rx,ry = randint(0,31)*10, 22+randint(0,19)*10
    fill_rect(rx,ry+4,10,4,c_apple)
    fill_rect(rx+2,ry+2,6,8,c_apple)
    fill_rect(rx+1,ry+3,8,6,c_apple)
    fill_rect(rx+2,ry,3,1,c_bord)
    fill_rect(rx+1,ry+1,5,1,c_bord)
    fill_rect(rx+2,ry+1,2,1,c_snake)
    fill_rect(rx+3,ry+2,3,1,c_snake)

def game_loop(speed):
    fill_rect(0,0,320,222,c_board)
    fill_rect(0,21,320,1,(0,0,0))
    draw_string("SNAKE",135,2)
    loos = heat = False
    score = 0
    direct = [1,0]
    time = monotonic()
    snake = Snake()
    snake.affichage()
    for _ in range(nbr_apple): new_apple()
    while not loos:
        fill_rect(0,21,320,1,(0,0,0))
        if get_pressed()[K_UP]: direct = [0,-1]
        if get_pressed()[K_DOWN]: direct = [0,1]
        if get_pressed()[K_LEFT]: direct = [-1,0]
        if get_pressed()[K_RIGHT]: direct = [1,0]
        if time + speed < monotonic():
            loos,heat = snake.update(direct)
            time = monotonic()
            score += 0.5 - speed
            if heat: score += apple_score
            if mod == 2 and speed < 0.3: speed *= 0.99
        draw_string(str(int(score)), 300-10*len(str(int(score))), 2)
        display(True)

game_loop(speed)

display()
