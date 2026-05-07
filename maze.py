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
 
 # Function to  draw the walls.
def draw_walls():
    #Draws walls based on north_wall and east_wall arrays
    glColor3f(1.0, 1.0, 1.0)  
    glLineWidth(3.0)
    
    # Draw NORTH walls
    for r in range(ROWS):
        for c in range(COLS):
            if north_wall[r][c] == 1:
                x = c * CELL_SIZE
                y = r * CELL_SIZE
                glBegin(GL_LINES)
                glVertex2f(x, y)
                glVertex2f(x + CELL_SIZE, y)
                glEnd()
    
    # Draw EAST walls
    for r in range(ROWS):
        for c in range(COLS):
            if east_wall[r][c] == 1:
                x = (c + 1) * CELL_SIZE
                y = r * CELL_SIZE
                glBegin(GL_LINES)
                glVertex2f(x, y)
                glVertex2f(x, y + CELL_SIZE)
                glEnd()
    
    # Draw LEFT boundary with openings
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(3.0)
    for r in range(ROWS):
        y = r * CELL_SIZE
        if not left_open[r]:
            glBegin(GL_LINES)
            glVertex2f(0, y)
            glVertex2f(0, y + CELL_SIZE)
            glEnd()
    
    # Draw RIGHT boundary with openings
    for r in range(ROWS):
        y = r * CELL_SIZE
        x = WIDTH
        if not right_open[r]:
            glBegin(GL_LINES)
            glVertex2f(x, y)
            glVertex2f(x, y + CELL_SIZE)
            glEnd()
    
    # Draw BOTTOM boundary
    glBegin(GL_LINES)
    glVertex2f(0, HEIGHT)
    glVertex2f(WIDTH, HEIGHT)
    glEnd()

 # Function to draw left and right markers.
def draw_start_end():
    """Draws special markers for start (left edge) and end (right edge)"""
    
    # Find and draw start cell on left edge
    for r in range(ROWS):
        if left_open[r]:
            x = 5
            y = r * CELL_SIZE + CELL_SIZE // 2
            glColor3f(0.0, 1.0, 0.0)  # Green
            glPointSize(8.0)
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()
            
            # Draw "S"
            glLineWidth(2.0)
            glBegin(GL_LINE_STRIP)
            glVertex2f(x + 2, y - 8)
            glVertex2f(x + 2, y + 8)
            glVertex2f(x + 10, y + 8)
            glVertex2f(x + 10, y)
            glVertex2f(x + 2, y)
            glEnd()
            break
    
    # Find and draw end cell on right edge
    for r in range(ROWS):
        if right_open[r]:
            x = WIDTH - 15
            y = r * CELL_SIZE + CELL_SIZE // 2
            glColor3f(1.0, 0.0, 0.0)  # Red
            glPointSize(8.0)
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()
            
            # Draw "E"
            glLineWidth(2.0)
            glBegin(GL_LINE_STRIP)
            glVertex2f(x - 10, y - 8)
            glVertex2f(x - 2, y - 8)
            glVertex2f(x - 2, y + 8)
            glVertex2f(x - 10, y + 8)
            glEnd()
            glBegin(GL_LINES)
            glVertex2f(x - 10, y)
            glVertex2f(x - 2, y)
            glEnd()
            break