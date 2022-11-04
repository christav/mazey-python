"""
Create a new maze
"""
import random
from maze import Maze
from directions import Directions

def make_maze(rows, cols):
    m = Maze(rows, cols)
    start_row = random.randrange(0, rows)
    start_col = random.randrange(0, cols)

    open_cells(m.cell(start_row, start_col))

    entrance_cell = m.cell(random.randrange(0, rows), 0)
    entrance_cell.set_entrance()
    exit_cell = m.cell(random.randrange(0, rows), cols - 1)
    exit_cell.set_exit()
    return m

def open_cells(cell):
    cell.mark = 1

    available_neighbors = [(c, d) for (c, d) in [(cell.go(d), d) for d in Directions.all()] if c != None]
    random.shuffle(available_neighbors)

    for (neighbor, direction) in available_neighbors:
        if neighbor.mark == 0:
            cell.open_door(direction)
            open_cells(neighbor)
