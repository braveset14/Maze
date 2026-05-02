# Maze 
## Overview
  This project generates perfect mazes where every cell is connected by a unique path to every other cell and finds a path from the left edge to the right edge. 
  The program uses a stack-based Depth-First Search (DFS) algorithm where a "mouse" eats through walls to create the maze, then uses backtracking to solve it.

## How the Maze Generator Works

### The "Mouse" Algorithm (Stack-based DFS)

The maze generation process follows these steps:

1. **Initialization**: All walls are intact (complete grid of cells). The mouse starts in a randomly chosen cell.

2. **Wall Eating Process**: The mouse looks at its four neighboring cells (up, down, left, right). For each neighbor that hasn't been visited yet (all four walls still intact), it adds that neighbor as a candidate.

3. **Random Selection**: The mouse randomly chooses one candidate neighbor and "eats" through the connecting wall, removing it. The remaining unvisited neighbors are pushed onto a **stack** for later exploration.

4. **Backtracking**: When the mouse reaches a dead end (no unvisited neighbors), it pops a cell from the stack and continues from there. This is the key property of DFS - we always explore one path fully before backtracking.

5. **Termination**: The process repeats until the stack is empty, meaning all cells have been visited. The result is a perfect maze where all cells are connected.

### Why Stack vs Queue?  

- **Stack (LIFO)**: Creates long, winding paths that go deep before branching. This produces mazes with long corridors and fewer cycles.
- **Queue (FIFO)**: Would create more branching patterns, similar to a BFS. This would result in wider, tree-like structures with shorter paths.

For this implementation, a stack is used because it naturally creates the "tortuous paths" described in the assignment, where the mouse explores deeply before backtracking.

## Maze Solver

The solver uses a backtracking algorithm:

1. **Red Dot**: Marks the mouse's current position while traversing the maze.
2. **Blue Dot**: Marks dead ends that have been explored and lead nowhere.
3. **Stack Usage**: The mouse pushes its position onto a stack when moving forward, and pops to backtrack when hitting a dead end

This ensures the algorithm always finds a path from start to end without repetition.

## Edge Openings

Start and end points are randomly placed on the left and right edges respectively. The program creates openings at these edges to allow entry and exit from the maze.

## Installation & Requirements

```bash
pip install pygame PyOpenGL PyOpenGL_accelerate