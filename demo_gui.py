import pygame
import sys
import time

#initialize basic classes and modify general settings
pygame.init()
screen = pygame.display.set_mode([1270, 900])
#don't use set_mode to create other surfaces, they wont show up on the screen
background_surface = pygame.Surface([1270, 900])
stone_surface =      pygame.Surface([1270, 900])
#initial_screen = pygame.display.set_mode([1270, 900])

clock = pygame.time.Clock()
pygame.display.set_caption("Super krasses 4-gewinnt was dein Leben verändern wird")

def drop_stone(dest_pos_index):
    #use global keyword because i want to override y and current_stone here, otherwise this would result in an Unboundlocalerror
    #you have to explicitly type the global keyword to make clear which variable you want to use and that you don't want to create a new one in the function scope
    global y
    global current_stone
    y_copy = y
    acceleration = 1
    
    while y != (dest_pos_index * y_spacing_for_76 + y_copy):
        #dirty fix to make sure we reach the end of the loop, accelaration makes it comlicated
        if y >= (dest_pos_index * y_spacing_for_76 + y_copy):
            break
        
        acceleration = acceleration*1.09
        y += 1 + acceleration
        draw_screen_surface()

    #make stoneposition permanent, switch player and reset y (and maybe x in the future, so that the initial position is 4)
    y = dest_pos_index * y_spacing_for_76 + y_copy
    background_surface.blit(current_stone, (x,y))
    current_stone = switch_stone(current_stone)
    y = y_copy
        
def draw_screen_surface():    
    screen.blit(background_surface, (0, 0))
    screen.blit(current_stone,      (x, y))
    screen.blit(spielfeld,          (0, 180))
    #display our drawings
    pygame.display.update()

def draw_winning_surface():
    pass

def draw_initial_surface():
    pass

def switch_stone(current_stone):
    if current_stone == gelber_stein:
        current_stone = roter_stein
    else:
        current_stone = gelber_stein
    return current_stone

##definition stuff
#import graphics
spielfeld = pygame.image.load("re_Spielfeld.png")
initial_spielfeld = spielfeld.copy()
roter_stein = pygame.image.load("re_rot.png")
initial_roter_stein = roter_stein.copy()
gelber_stein = pygame.image.load("re_gelb.png")
first_field_coordinates = (-283, -34)

#color variables shortcuts
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

#some variables for moving elements around and keep track of the actual position of the current stone
x_spacing_for_76 = 95
y_spacing_for_76 = 87
x = 313 
y = 240 - y_spacing_for_76

#this will be player one or two - the right side is the default value aka player which makes the first move
current_stone = roter_stein

#static stuff - do that once instead of doing that every frame inside the loop
background_surface.fill(BLACK)


running = True
#counter is sometimes useful for fixing things
counter = 0
while running:
    #standard exit/break out the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
             
  
    pressed_button_vert = pygame.key.get_pressed()
    if pressed_button_vert[pygame.K_RIGHT]:
        x += x_spacing_for_76
        #sleep because otherwise a click is more than click and we don't want that #dirty fix
        time.sleep(0.07)
    if pressed_button_vert[pygame.K_LEFT]:
        x -= x_spacing_for_76
        time.sleep(0.07)
    if pressed_button_vert[pygame.K_RETURN]:
        drop_stone(6)
        
    #-----temporary code - maybe we will make it a feature for a special mode :D
    #-------------------------------------------------------------------#
    if pressed_button_vert[pygame.K_DOWN]:

        y += y_spacing_for_76
        time.sleep(0.07)

    if pressed_button_vert[pygame.K_UP]:
        y -= y_spacing_for_76
        time.sleep(0.07)
        
    #-------------------------------------------------------------------#

    draw_screen_surface()   
    #60 frames per second refresh rate
    clock.tick(60)
    counter += 1
    print(counter)
   
            
