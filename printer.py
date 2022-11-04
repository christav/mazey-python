""" Class that prints a maze """

import sys
from directions import Directions
from solver import is_solution_cell

class CharSet:
    def __init__(self, corners, solution_chars):
        self.corners = corners
        self.solution_chars = solution_chars


unicode_char_set = CharSet(
    corners = " ╹╺┗╻┃┏┣╸┛━┻┓┫┳╋",
    solution_chars = [
        "   ", "   ", "   ", " ╰┄",
        "   ", " ┆ ", " ╭┄", "   ",
        "   ", "┄╯ ", "┄┄┄", "   ",
        "┄╮ ", "   ", "   ", "   "
    ]
)

ascii_char_set = CharSet(
    corners = " ++++|++++-+++++",
    solution_chars = [
        "   ", "   ", "   ", " XX",
        "   ", " X ", " XX", "   ",
        "   ", "XX ", "XXX", "   ",
        "XX ", "   ", "   ", "   "
    ]
)

class MazePrinter:
    def __init__(self, out = sys.stdout, char_set = unicode_char_set):
        self.out = out
        self.char_set = char_set
        self.horizontal_bar = self.char_set.corners[10] * 3

    def print_maze(self, maze):
        for row in maze.all_rows():
            self.print_row_separator(row)
            self.print_row(row)
        self.print_maze_bottom(maze)

    def print_row_separator(self, row):
        for cell in row:
            self.out.write(self.corner_char(cell))
            if cell.can_go(Directions.UP):
                if is_solution_cell(cell) and is_solution_cell(cell.go(Directions.UP)):
                    self.out.write(self.char_set.solution_chars[5])
                else:
                    self.out.write("   ")
            else:
                self.out.write(self.horizontal_bar)
        self.out.write(self.row_separator_end(row))
        self.out.write("\n")

    def print_row(self, row):
        for cell in row:
            if cell.is_entrance:
                if is_solution_cell(cell):
                    self.out.write(self.char_set.solution_chars[10][1])
                else:
                    self.out.write(" ")
            elif cell.can_go(Directions.LEFT):
                if is_solution_cell(cell) and is_solution_cell(cell.go(Directions.LEFT)):
                    self.out.write(self.char_set.solution_chars[10][1])
                else:
                    self.out.write(" ")
            else:
                self.out.write(self.char_set.corners[5])

            self.out.write(self.cell_contents(cell))

        lastCell = row[-1]
        if lastCell.is_exit:
            if is_solution_cell(lastCell):
                self.out.write(self.char_set.solution_chars[10][1])
            else:
                self.out.write(" ")
        else:
            self.out.write(self.char_set.corners[5])

        self.out.write("\n")

    def print_maze_bottom(self, maze):
        for cell in maze.all_rows()[-1]:
            index = 0xa | (0 if cell.can_go(Directions.LEFT) else 1)
            if cell.col == 0:
                index &= 0x7

            self.out.write(self.char_set.corners[index])
            self.out.write(self.horizontal_bar)

        last_cell = maze.all_rows()[-1][-1]
        index = 0x8 | (0 if last_cell.can_go(Directions.RIGHT) else 1)
        self.out.write(self.char_set.corners[index])
        self.out.write("\n")

    def corner_char(self, cell):
        neighbors = [cell.go(d) for d in [Directions.UP, Directions.LEFT]]

        index = 0
        index |= 0 if neighbors[0] != None and (neighbors[0].is_entrance or neighbors[0].can_go(Directions.LEFT)) else 1
        index |= 0 if cell.can_go(Directions.UP) else 2
        index |= 0 if cell.is_entrance or cell.can_go(Directions.LEFT) else 4
        index |= 0 if neighbors[1] != None and neighbors[1].can_go(Directions.UP) else 8

        if cell.row == 0:
            index &= 0xe

        if cell.col == 0:
            index &= 0x7

        return self.char_set.corners[index]

    def row_separator_end(self, row):
        cell = row[-1]
        up_cell = cell.go(Directions.UP)
        index = 0
        index |= 0 if up_cell != None and up_cell.is_exit else 1
        index |= 0 if cell.is_exit else 4
        index |= 0 if cell.can_go(Directions.UP) else 8

        if cell.row == 0:
            index &= 0xe

        return self.char_set.corners[index]

    def cell_contents(self, cell):
        if not is_solution_cell(cell):
            return "   "

        index = 0
        index |= 1 if (cell.can_go(Directions.UP) and is_solution_cell(cell.go(Directions.UP))) else 0
        index |= 2 if (cell.is_exit or cell.can_go(Directions.RIGHT) and is_solution_cell(cell.go(Directions.RIGHT))) else 0
        index |= 4 if (cell.can_go(Directions.DOWN) and is_solution_cell(cell.go(Directions.DOWN))) else 0
        index |= 8 if (cell.is_entrance or cell.can_go(Directions.LEFT) and is_solution_cell(cell.go(Directions.LEFT))) else 0
        return self.char_set.solution_chars[index]
