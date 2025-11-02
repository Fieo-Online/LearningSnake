import pygame
import random as random
from pygame import Surface
from pygame.key import ScancodeWrapper

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
X = 720
Y = 720
SNAKE_WIDTH = X/20
SNAKE_HEIGHT = X/20
lock = [False, False, False, False] #Only one True at a time allowed, gives the current active direction(w s a d)
old_current = lock
running = True
fruit = False

pygame.init()
screen = pygame.display.set_mode([X,Y])
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")
dt = 1

pygame.key.set_repeat(10)
player_pos = [pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)]
fruit_pos = None
#locks and switches movement direction for the player
def move_lock(current:[bool]):
    if lock.count(True) == 1:
        if old_current != current:
            print(current)
            direction = lock.index(True) # Give current direction
            opp = -1
            #Opposite direction is not optional -> Gets ignored
            if direction == 0:
                current[1] = False
                opp = 1
            elif direction == 1:
                current[0] = False
                opp = 0
            elif direction == 2:
                current[3] = False
                opp = 3
            elif direction == 3:
                current[2] = False
                opp = 2
            count = current.count(True)
            if count == 0:
                return 0
            if count == 1:
                if current.index(True) == direction:
                    return 0
                else:
                    lock[current.index(True)] = True
                    lock[direction] = False
            if count == 2:
                #First scenario: One of the inputs is already active in lock
                first = current.index(True)
                second = current.index(True, first+1)
                if current[direction]:
                    if first == direction:
                        lock[first] = False
                        lock[second] = True
                    else:
                        lock[second] = False
                        lock[first] = True
                else:
                #second scenario: Both inputs are inactive in lock
                    lock[random.choice([first, second])] = True
            if count == 3:
                temp = [0, 1, 2, 3]
                temp.remove(direction)
                temp.remove(opp)
                lock[direction] = False
                lock[random.choice(temp)] = True
    else:
        #initial direction
        if current.count(True) != 0:
            temp = [0, 1, 2, 3]
            for j in range(len(current)):
                if not current[j]:
                    temp.remove(j)
            lock[random.choice(temp)] = True
    return 1

while running:
    #Backround creation
    for i in range(20):
        for x in range (20):
            if i % 2 == 1 and x % 2 == 0:
                pygame.draw.rect(screen, (0,0,255), (SNAKE_WIDTH*i, SNAKE_HEIGHT*x, SNAKE_WIDTH, SNAKE_HEIGHT))
            elif i % 2 == 0 and x % 2 == 1:
                pygame.draw.rect(screen, (0,0,255), (SNAKE_WIDTH*i, SNAKE_HEIGHT*x, SNAKE_WIDTH, SNAKE_HEIGHT))
            elif i % 2 == 0 and x % 2 == 0:
                pygame.draw.rect(screen, (0,0,125), (SNAKE_WIDTH*i, SNAKE_HEIGHT*x, SNAKE_WIDTH, SNAKE_HEIGHT))
            elif i % 2 == 1 and x % 2 == 1:
                pygame.draw.rect(screen, (0,0,125), (SNAKE_WIDTH*i, SNAKE_HEIGHT*x, SNAKE_WIDTH, SNAKE_HEIGHT))

    if fruit:
        pygame.draw.rect(screen, RED, (fruit_pos.x, fruit_pos.y, SNAKE_WIDTH, SNAKE_HEIGHT))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Player Movement
    snake = pygame.draw.rect(screen, GREEN, (player_pos[0].x - SNAKE_WIDTH, player_pos[0].y - SNAKE_HEIGHT, SNAKE_WIDTH, SNAKE_HEIGHT)) #Player

    keys = pygame.key.get_pressed()
    move_lock([keys[pygame.K_w],keys[pygame.K_s],keys[pygame.K_a],keys[pygame.K_d]])
    old_current = [keys[pygame.K_w],keys[pygame.K_s],keys[pygame.K_a],keys[pygame.K_d]]

    for n in range(1,720000):
        if lock[0] and (player_pos[0].y >= 0 + SNAKE_HEIGHT):
            player_pos[0].y -= 0.00005
        if lock[1] and (player_pos[0].y <= Y):
            player_pos[0].y += 0.00005
        if lock[2] and (player_pos[0].x >= 0 + SNAKE_WIDTH):
            player_pos[0].x -= 0.00005
        if lock[3] and (player_pos[0].x <= X):
            player_pos[0].x += 0.00005

    #Spawning fruits
    if not fruit:
        x_fruit = random.randint(0,19)
        y_fruit = random.randint(0,19)
        if not pygame.Vector2(x_fruit*SNAKE_WIDTH, y_fruit*SNAKE_HEIGHT) in player_pos:
            pygame.draw.rect(screen, RED, (x_fruit*20, y_fruit*20, SNAKE_WIDTH, SNAKE_HEIGHT))
            fruit_pos = pygame.Vector2(x_fruit*20, y_fruit*20)
            fruit = True

    pygame.display.flip()
    dt = clock.tick(60) / 1000


