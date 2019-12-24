import pygame
import random
import time

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
snake_size = 20
food_size = 10

pygame.init()

quit = False
paused = False
size = [800, 600]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")

clock_spd = 5
snake_len = 1
snake_list = []
x_coord = size[0]/2
y_coord = size[1]/2
x_vel = 0
y_vel = 0
food_x = random.randint(20, size[0]-20)
food_y = random.randint(20, size[1]-20)
score = 0
fuel = 0

vel = snake_size
boost_vel = 2*snake_size


clock = pygame.time.Clock()

def message(msg, color):
    font = pygame.font.SysFont(None, 100)
    mes = font.render(msg, True, color)
    screen.blit(mes, [size[0]/2-200, size[1]/2])

def draw_snake(li):
    for x in li[:-1]:
        pygame.draw.rect(screen, red, [x[0], x[1], snake_size, snake_size])
    snake = pygame.draw.rect(screen, black, [li[-1][0], li[-1][1], snake_size, snake_size])
    return snake

def pause_mes():
    font = pygame.font.SysFont(None, 60)
    mes = font.render("Paused", True, red)
    screen.blit(mes, [size[0]/2-100, 20])
    font = pygame.font.SysFont(None, 40)
    mes = font.render("p - Pause", True, red)
    screen.blit(mes, [size[0]/2-70, 80])
    mes = font.render("SPACE - Boost", True, red)
    screen.blit(mes, [size[0]/2-70, 120])
    mes = font.render("q - Quit", True, red)
    screen.blit(mes, [size[0]/2-70, 200])

while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    temp_x = x_vel
                    temp_y = y_vel
                    x_vel = 0
                    y_vel = 0
                else:
                    x_vel = temp_x
                    y_vel = temp_y

            if paused: continue
            if event.key == pygame.K_LEFT:
                if x_vel == 0: 
                    x_vel = -1*vel
                    y_vel = 0
            if event.key == pygame.K_RIGHT:
                if x_vel == 0: 
                    x_vel = vel
                    y_vel = 0
            if event.key == pygame.K_UP:
                if y_vel == 0: 
                    y_vel = -1*vel
                    x_vel = 0
            if event.key == pygame.K_DOWN:
                if y_vel == 0: 
                    y_vel = vel
                    x_vel = 0
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_SPACE:
                if fuel > 0:
                    clock_spd *= 1.2-fuel
                    fuel -= 1
    
    x_coord = (x_coord+x_vel)%size[0]
    y_coord = (y_coord+y_vel)%size[1]
    head = [x_coord, y_coord]
    snake_list.append(head)
    if len(snake_list)>snake_len: snake_list = snake_list[1:]
    quit = quit or any(map( lambda x: x==head, snake_list[:-1]))
    
    screen.fill(white)
    font = pygame.font.SysFont(None, 30)
    mes = font.render("Fuel", True, black)
    screen.blit(mes, [size[0]-50, 20])
    pygame.draw.rect(screen, green, [size[0]-20, size[1]-40-(fuel*(size[1]-100)), 15, (fuel*(size[1]-100))])
    food = pygame.draw.rect(screen, green, [food_x, food_y, food_size, food_size])
    snake = draw_snake(snake_list)
    font = pygame.font.SysFont(None, 30)
    mes = font.render("You Score: " + str(score), True, black)
    screen.blit(mes, [10,10])
    if paused: pause_mes()

    if(snake.colliderect(food)):
        score += 10
        snake_len += 1
        fuel = min(1, fuel+0.1)
        clock_spd += (score/40)
        food_x = random.randint(20, size[0]-20)
        food_y = random.randint(20, size[1]-20)

    pygame.display.update()
    clock.tick(clock_spd)

message("Game over", red)
pygame.display.update()
time.sleep(2)

pygame.quit()
exit()
