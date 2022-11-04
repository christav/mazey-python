# Base definitions for maze data structure

from directions import Directions


class Cell:
    """
    Class represnting a single cell in a maze
    """
    def __init__(self, maze, row, col):
        self._maze = maze
        self._row = row
        self._col = col
        self._doors = 0
        self.mark = 0

    @property
    def row(self):
        """ What row this cell is in """
        return self._row

    @property
    def col(self):
        """ What column this cell is in """
        return self._col

    @property
    def is_in_maze(self):
        """ Is this cell in the maze? """
        return self._maze.is_in_maze(self.row, self.col)

    def can_go(self, direction):
        """ Is there an open door from this cell in the given direction? """
        if direction == Directions.STATIONARY:
            return self
        return self._doors & direction.value.mask != 0

    def go(self, direction):
        """ Get the cell in the given direction """
        return self._maze.cell(self.row + direction.value.dy, self.col + direction.value.dx)

    @property
    def is_entrance(self):
        return self == self._maze.get_entrance()

    @property 
    def is_exit(self):
        return self == self._maze.get_exit()

    def open_door(self, direction):
        """ Open the door from the cell in the given direction """
        neighbor = self.go(direction)
        if neighbor != None:
            self._doors = self._doors | direction.value.mask
            neighbor._doors = neighbor._doors | Directions.opposite(direction).value.mask
    
    def set_entrance(self):
        """ This cell is now the maze entrance """
        self._doors = self._doors | Directions.LEFT.value.mask

    def set_exit(self):
        """ This cell is now the maze exit """
        self._doors = self._doors | Directions.RIGHT.value.mask

    def neighbors(self):
        """ All the neighbors accessible from this cell through open doors """
        for d in Directions.all():
            if self.can_go(d) and self.go(d) != None:
                yield self.go(d)


class Maze:
    """
    A 2d maze, stored as a 2d array of Cells
    """
    
    def __init__(self, rows, cols):
        """ Create the maze with all doors closed """
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(self, row, col) for col in range(cols)] for row in range(rows)]

    def all_cells(self):
        """ Gives access to all cells in the maze """
        for row in self.cells:
            for cell in row:
                yield cell

    def all_rows(self):
        """ Deliver all the rows of the maze one by one """
        return self.cells

    def row(self, row):
        """ Get all the cells in a single row """
        return self.cells[row]

    def all_cols(self):
        """ Give access to all the columns of the maze """
        for col in range(self.cols):
            yield [self.cells[row][col] for row in range(self.rows)]

    def col(self, col):
        """ Get all the cells in a single column """
        return [self.cells[row][col] for row in range(self.rows)]

    def cell(self, row, col):
        """ Get a single cell """
        if self.is_in_maze(row, col):
            return self.cells[row][col]
        return None

    def is_in_maze(self, row, col):
        """ Is the given coordinate in the maze? """
        return (
            row >= 0 and row < self.rows and
            col >=0 and col < self.cols
        )
    
    def get_entrance(self):
        """ Get the entrance cell """
        return [cell for cell in self.col(0) if cell.can_go(Directions.LEFT)][0]

    def get_exit(self):
        """ Get the exit cell """
        return [cell for cell in self.col(self.cols - 1) if cell.can_go(Directions.RIGHT)][0]

