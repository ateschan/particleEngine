import pygame, sys, math, os, subprocess
from random import randint
import random
pygame.init()
clock = pygame.time.Clock()
WINDOW_SIZEX = 1200; WINDOW_SIZEY = 700; rendx = 390; rendy = 240
displaySize = (rendx, rendy)
screen = pygame.display.set_mode((WINDOW_SIZEX, WINDOW_SIZEY), pygame.RESIZABLE)
display = pygame.Surface((rendx, rendy))
colorHue = [0, 5, 180]; vortexVel = .4
p1 = True; p2 = False; p3 = False
shiftUpr = True; shiftUpg = True; shiftUpb = True
rotateLeft = False; rotateRight = False; rotateUp = False; rotateDown = False
collisons = False; generate = False; vortex = False; colorShift = False; 
pcount = 0
multiplierH = 1; multiplierV = 1; bounce = .1
particles1 = []
confetti = []


def redrawGameWindow():
    screen.blit(pygame.transform.scale(display, (WINDOW_SIZEX, WINDOW_SIZEY)), (0, 0))
    pygame.display.update()
    clock.tick(60)
    
def circle_surf(radius, color):
    radius = abs(radius)
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

def rect_surf(width, height, color):
    surf = pygame.Surface(width, height)
    pygame.draw.rect(surf, color, pygame.Rect(width * 2, height * 2, width, height))
    surf.set_colorkey((0, 0, 0))
    return surf

def explode():
    for x in range(100):
        particles1.append([[mouse[0], mouse[1]],[(random.randint(2, 15) / 10 - 1) * random.randint(0, 30), -random.randint(0, 10)], random.randint(2, 6)])
        particles1.append([[mouse[0], mouse[1]],[(random.randint(2, 15) / 10 - 1) * random.randint(0, 30), random.randint(0, 10)], random.randint(2, 6)])

def particleRender():
    if colorShift == True:
        pygame.draw.circle(display, (colorHue[0], colorHue[1], colorHue[2]), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        radius = particle[2] * 1.3
        display.blit(circle_surf(radius, (colorHue[0], colorHue[1], colorHue[2])), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=pygame.BLEND_RGB_ADD)
    else:
        pygame.draw.circle(display, (220, 100, 100), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        radius = particle[2] * 1.3
        display.blit(circle_surf(radius, (60, 20, 30)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=pygame.BLEND_RGB_ADD)
        


while True:
    
    pygame.mouse.set_visible(False)
    mouse1 = pygame.mouse.get_pos()
    mouse = [mouse1[0],mouse1[1]]
    display.fill((60, 25, 60))
    
    #Cursor
    pygame.draw.line(display, (255,255,255), (mouse[0], mouse[1]), (mouse[0] - 2, mouse[1] - 2), 1)
    pygame.draw.line(display, (255,255,255), (mouse[0], mouse[1]), (mouse[0] - 2, mouse[1]), 1)
    pygame.draw.line(display, (255,255,255), (mouse[0]-2, mouse[1]-2), (mouse[0]-2, mouse[1]), 1)
    
    #borderRect = ((0,0), (rendx,rendy))
    #pygame.draw.rect(display, (40,10,40), borderRect,1)
   
    if generate == True:
        particles1.append([[mouse[0], mouse[1]], [random.randint(0, 20) / 10 - 1 * multiplierH, -1], random.randint(4, 10)])
    
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()
            
        if ev.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(ev.size, pygame.RESIZABLE)
                    

        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
                explode()
        
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_1:
                if vortex == False:
                    vortex = True
                else:
                    vortex = False
            
            if ev.key == pygame.K_2:
                if colorShift == False:
                    colorShift = True
                else:
                    colorShift = False
		
            if ev.key == pygame.K_SPACE:
                if generate == False:
                    generate = True
                else:
                    generate = False
        
            if ev.key == pygame.K_LEFT:
                rotateLeft = True
            if ev.key == pygame.K_RIGHT:
                rotateRight = True
            if ev.key == pygame.K_UP:
                rotateUp = True
            if ev.key == pygame.K_DOWN:
                rotateDown = True
            if ev.key == pygame.K_c:
                if collisons == False:
                    collisons = True
                else: collisons = False
        
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_LEFT:
                rotateLeft = False
            if ev.key == pygame.K_RIGHT:
                rotateRight = False
            if ev.key == pygame.K_UP:
               rotateUp = False
            if ev.key == pygame.K_DOWN:
                rotateDown = False
             
            
    if rotateRight == True:
        multiplierH -= .05
    if rotateLeft == True:
        multiplierH += .05
    if rotateUp == True:
        multiplierV -= .05
    if rotateDown == True:
        multiplierV += .05
            

    #Particle 1
    if vortex == False:
        for particle in particles1:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.08
            particle[1][1] += 0.15 * multiplierV
            if collisons == True:
                if particle[0][0] <= 0.0:
                    particle[1][0] *= -1 - bounce
                if particle[0][0] >= rendx:
                    particle[1][0] *= -1 + bounce
                if particle[0][1] <= 0.0:
                    particle[1][1] *= -1 - bounce
                if particle[0][1] >= rendy:
                    particle[1][1] *= -1 + bounce
                    
            particleRender()
            if particle[2] <= 0:
                particles1.remove(particle)
    
    if vortex == True:
        for particle in particles1:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            if particle[0][0] < mouse[0]:
                particle[1][0] += vortexVel
            if particle[0][0] > mouse[0]:
                particle[1][0] -= vortexVel
            if particle[0][1] < mouse[1]:
                particle[1][1] += vortexVel
            if particle[0][1] > mouse[1]:
                particle[1][1] -= vortexVel
            particle[2] -= 0.1
            particle[1][1] += 0.15 * multiplierV
            if collisons == True:
                if particle[0][0] <= 0.0:
                    particle[1][0] *= -1 - bounce
                if particle[0][0] >= rendx:
                    particle[1][0] *= -1 + bounce
                if particle[0][1] <= 0.0:
                    particle[1][1] *= -1 - bounce
                if particle[0][1] >= rendy:
                    particle[1][1] *= -1 + bounce

            particleRender()
            if particle[2] <= 0:
                particles1.remove(particle)
        


    if colorShift == True:
        if shiftUpr == True:
            if colorHue[0] == 255:
                shiftUpr = False
            else:
                colorHue[0] += .5
        else:
            if colorHue[0] == 0:
                shiftUpr = True
            else:
                colorHue[0] -= 5
        
        if shiftUpg == True:
            if colorHue[1] == 255:
                shiftUpg = False
            else:
                colorHue[1] += 1
        else:
            if colorHue[1] == 0:
                shiftUpg = True
            else:
                colorHue[1] -= 3
        
        if shiftUpb == True:
            if colorHue[2] == 255:
                shiftUpb = False
            else:
                colorHue[2] += 1.5
        else:
            if colorHue[2] == 0:
                shiftUpb = True
            else:
                colorHue[2] -= 17

    #print(colorHue[0],colorHue[1], colorHue[2])
    #print(shiftUpr, shiftUpg, shiftUpb)
    redrawGameWindow()
