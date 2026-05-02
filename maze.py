import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

## Defining constnts that don't change throuout the project.

ROWS=10
COLS=15
CELL_SIZE=40 # Each cell is 40 pixels
WIDTH=COLS * CELL_SIZE
HEIGHT=ROWS * CELL_SIZE

## Initialize pygame and opengl

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT),OPENGL)
 # Set the Window title
pygame.display.set_caption('Maze Generator')
 # Setup matrix 
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0,WIDTH,HEIGHT,0,-1,1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity() 
glClearColor(0.2, 0.2, 0.3, 1.0)