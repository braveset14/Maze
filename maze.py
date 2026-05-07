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
  # Dead ends 
dead_ends = []
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
    """Draws walls based on north_wall and east_wall arrays"""
    glColor3f(1.0, 1.0, 1.0)  # White color for walls
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

 # Function to generate maze
def generate_maze():
    """Generates a perfect maze using DFS algorithm with a stack"""
    
    # Choose random start cell
    global start_r, start_c
    start_r = random.randint(0, ROWS - 1)
    start_c = random.randint(0, COLS - 1)
    visited[start_r][start_c] = True
    
    # Stack stores cells we can backtrack to
    stack = [(start_r, start_c)]
    
    while stack:
        r, c = stack[-1]
        
        # Find all UNVISITED neighbors
        neighbors = []
        
        if r > 0 and not visited[r-1][c]:
            neighbors.append(('up', r-1, c))
        if r < ROWS-1 and not visited[r+1][c]:
            neighbors.append(('down', r+1, c))
        if c > 0 and not visited[r][c-1]:
            neighbors.append(('left', r, c-1))
        if c < COLS-1 and not visited[r][c+1]:
            neighbors.append(('right', r, c+1))
        
        if neighbors:
            # Pick random neighbor and eat the wall
            direction, nr, nc = random.choice(neighbors)
            
            if direction == 'up':
                north_wall[r][c] = 0
            elif direction == 'down':
                north_wall[nr][nc] = 0
            elif direction == 'left':
                east_wall[r][c-1] = 0
            elif direction == 'right':
                east_wall[r][c] = 0
            
            # Move to neighbor
            visited[nr][nc] = True
            stack.append((nr, nc))
            
            # Animate
            glClear(GL_COLOR_BUFFER_BIT)
            draw_walls()
            draw_start_end()
            pygame.display.flip()
            pygame.time.wait(30)
        else:
            # Backtrack
            stack.pop()
            if stack:
                br, bc = stack[-1]
                glClear(GL_COLOR_BUFFER_BIT)
                draw_walls()
                draw_start_end()
                pygame.display.flip()
                pygame.time.wait(20)

def solve_maze():
    """Solves the maze using backtracking algorithm"""
    global solved_path
    
    # Reset solver tracking arrays
    solver_visited = [[False for c in range(COLS)] for r in range(ROWS)]
    path_stack = []
    
    # Find start cell on LEFT edge
    start_r = None
    for r in range(ROWS):
        if left_open[r]:
            start_r = r
            break
    
    # Find end cell on RIGHT edge
    end_r = None
    for r in range(ROWS):
        if right_open[r]:
            end_r = r
            break
    
    if start_r is None or end_r is None:
        print("Error: Could not find start/end openings!")
        return False
    
    # Start at left edge
    current_r = start_r
    current_c = 0
    solver_visited[current_r][current_c] = True
    path_stack.append((current_r, current_c))
    
    while path_stack:
        r, c = path_stack[-1]
        
        # Draw current state
        glClear(GL_COLOR_BUFFER_BIT)
        draw_walls()
        draw_start_end()
        
        # Draw current path
        for i, (pr, pc) in enumerate(path_stack):
            if i == len(path_stack) - 1:
                draw_cell(pr, pc, (1.0, 0.0, 0.0))  # Bright red for current
            else:
                draw_cell(pr, pc, (0.8, 0.2, 0.2))  # Darker red for path
        for (dr, dc) in dead_ends:
            draw_cell(dr, dc, (0.0, 0.0, 1.0))
        pygame.display.flip()
        pygame.time.wait(50)
        
        # Check if reached end
        if r == end_r and c == COLS - 1:
            print("PATH FOUND! 🎉")
            
            # Save the solved path
            solved_path = list(path_stack)
            
            # Flash celebration
            for _ in range(5):
                glClear(GL_COLOR_BUFFER_BIT)
                draw_walls()
                draw_start_end()
                for (pr, pc) in solved_path:
                    draw_cell(pr, pc, (0.8, 0.2, 0.2))
                draw_cell(r, c, (1.0, 1.0, 0.0))
                pygame.display.flip()
                pygame.time.wait(100)
                glClear(GL_COLOR_BUFFER_BIT)
                draw_walls()
                draw_start_end()
                for (pr, pc) in solved_path:
                    draw_cell(pr, pc, (0.8, 0.2, 0.2))
                draw_cell(r, c, (1.0, 0.0, 0.0))
                pygame.display.flip()
                pygame.time.wait(100)
            
            return True
        
        # Find unvisited neighbors with no walls
        neighbors = []
        
        # Check UP
        if r > 0 and north_wall[r][c] == 0 and not solver_visited[r-1][c]:
            neighbors.append(('up', r-1, c))
        
        # Check DOWN
        if r < ROWS-1 and north_wall[r+1][c] == 0 and not solver_visited[r+1][c]:
            neighbors.append(('down', r+1, c))
        
        # Check LEFT
        if c > 0 and east_wall[r][c-1] == 0 and not solver_visited[r][c-1]:
            neighbors.append(('left', r, c-1))
        
        # Check RIGHT
        if c < COLS-1 and east_wall[r][c] == 0 and not solver_visited[r][c+1]:
            neighbors.append(('right', r, c+1))
        
        if neighbors:
            # Move to first valid neighbor
            direction, nr, nc = neighbors[0]



            solver_visited[nr][nc] = True
            path_stack.append((nr, nc))
        else:
            # Dead end - mark blue and backtrack

            dead_r, dead_c = path_stack.pop()
            dead_ends.append((dead_r, dead_c)) 
            glClear(GL_COLOR_BUFFER_BIT)
            draw_walls()
            draw_start_end()
            for pr, pc in path_stack:
                draw_cell(pr, pc, (0.8, 0.2, 0.2))
            for (dr,dc) in dead_ends:
                draw_cell(dr, dc, (0.0, 0.0, 1.0))  # Blue for dead end
            pygame.display.flip()
            pygame.time.wait(40)
    
    print("No path found!")
    return False