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
 
  # My wall data structures
  
  # north_wall[r][c]= 1----> means  the cell (r,c) has a wall above it. 
  # north_wall[r][c]= 0----> means  the cell (r,c) doesn't have a wall above it.It is open.
north_wall = [[1 for c in range(COLS)] for r in range(ROWS)]
  # east_wall[r][c]= 1----> means  the cell (r,c) has a wall to the right of it. 
  # east_wall[r][c]= 0----> means  the cell (r,c) doesn't have a wall on the right.It is open.
east_wall = [[1 for c in range(COLS)] for r in range(ROWS)]
  # We check if a cell was visited by visited[r][c]== true or false.
visited = [[False for c in range(COLS)] for r in range(ROWS)]
  # An array to hpold solved path.
solved_path = [] 
  # Edge openings
left_open = [False for r in range(ROWS)]
right_open = [False for r in range(ROWS)]

 ## Function to draw each cell.
def draw_cell(r, c, color):
    # Draws a filled square at cell (r,c) with given color.
    x = c * CELL_SIZE
    y = r * CELL_SIZE
    padding = 8
    
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_QUADS)
    glVertex2f(x + padding, y + padding)
    glVertex2f(x + CELL_SIZE - padding, y + padding)
    glVertex2f(x + CELL_SIZE - padding, y + CELL_SIZE - padding)
    glVertex2f(x + padding, y + CELL_SIZE - padding)
    glEnd()

