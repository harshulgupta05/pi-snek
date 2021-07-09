#importing libraries
from gpiozero import Button
import pygame
import time
import random

snake_speed = 10

# set window size
window_x = 1080
window_y = 720

# defining colours
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# set up buttons
button_up = Button(2)
button_down = Button(3)
button_left = Button(15)
button_right = Button(14)

# initialising pygame
pygame.init()

#initialise game window
pygame.display.set_caption('SNEK')
game_window = pygame.display.set_mode((window_x, window_y))

#fps controller
fps = pygame.time.Clock()

# snake default position
snake_pos = [100, 50]

# first four blocks of snake body
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# fruit position
fruit_pos = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
fruit_colour = pygame.Color(random.randrange(100, 255), random.randrange(100, 255), random.randrange(100,255))
fruit_spawn = True

# snek default direction
direction = 'RIGHT'
change_to = direction

#initialise score
score = 0

# score display function
def show_score(choice, color, font, size):
    #creating font object
    score_font = pygame.font.SysFont(font, size)
    
    #creating display surface object
    score_surface = score_font.render('Score: ' + str(score), True, color)
    
    # creating a rectangular object for the text surface object
    score_rect = score_surface.get_rect()
    
    # display text
    game_window.blit(score_surface, score_rect)
    
def game_over():
    #create font object
    my_font = pygame.font.SysFont('times new roman', 50)
    
    #create text surface
    game_over_surface = my_font.render('Your Score is: ' + str(score), True, red)
    
    # create rectangular object for text surface object
    game_over_rect = game_over_surface.get_rect()
    
    #set game over position of text
    game_over_rect.midtop = (window_x/2, window_y/4)
    
    # draw text onto screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    # sleep for 2 seconds
    time.sleep(2)
    
    # deactivate pygame library
    pygame.quit()
    
    # quit game
    quit()
    
while True:
    # handling button input
    if (button_up.is_pressed):
        change_to = 'UP'
    
    if (button_down.is_pressed):
        change_to = 'DOWN'

    if (button_left.is_pressed):
        change_to = 'LEFT'

    if (button_right.is_pressed):
        change_to = 'RIGHT'
    
    # avoid opposite direction conflict
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    
    #snek movement
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10
        
    #snake body growth and collisions
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == fruit_pos[0] and snake_pos[1] == fruit_pos[1]:
        score += 10
        
        #increase speed
        if (score >= 150):
            snake_speed = 15
            
        if (score >= 300):
            snake_speed = 20
        
        fruit_spawn = False
    else:
        snake_body.pop()
        
    if not fruit_spawn:
        fruit_pos = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
        fruit_colour = pygame.Color(random.randrange(100, 255), random.randrange(100, 255), random.randrange(100,255))
        
    fruit_spawn = True
    game_window.fill(black)
    
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    
    pygame.draw.rect(game_window, fruit_colour, pygame.Rect(fruit_pos[0], fruit_pos[1], 10, 10))
    
    # game over conditionals
    if snake_pos[0] < 0 or snake_pos[0] > window_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > window_y-10:
        game_over()
    
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
    
    show_score(1, white, 'times new roman', 20)
    
    pygame.display.update()
    
    fps.tick(snake_speed)