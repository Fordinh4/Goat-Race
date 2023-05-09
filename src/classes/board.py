#----------------------------------------------------
# Board implementation
#----------------------------------------------------
from .stack import Stack
from .goat import Goat


class Board:
    '''
    An object in this class represents a board configuration in the game Goat Race.
    '''
    def __init__(self, width, height, obstacle_positions) -> None:
        """This method initializes the board. It takes three arguments, the width and height of the board, and a list that contains tuples indicating the position of obstacles, that is, (row, column)."""
        board = []
        for item in range(height):
            row = []
            for col in range(width):
                row.append(Stack())
            board.append(row)

        self.width = width
        self.height = height
        self.obstacle_positions = obstacle_positions
        self.board = board
    
    def check_row(self, row):
        """Checks if the given value for the row is valid (should be a number between 1 and height), and, if this is not the case, it raises an Exception."""

        if not (0 < row <= self.height):
            raise

    def check_column(self, column):
        """Checks if the given value for the column is valid (should be a valid character), and, if this is not the case, it raises an Exception."""
        
        if column not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
            raise

    def check_obstacle_positions(self, obstacle_positions):
        """Checks that the given list of obstacles has valid rows and columns for each obstacle."""
        for obstacle in obstacle_positions:
            self.check_row(obstacle[0])
            self.check_column(obstacle[1])

    def get_width(self):
        """This method returns the width of the board. It takes no arguments and returns an integer."""
        return self.width

    def get_height(self):
        """This method returns the height of the board. It takes no arguments and returns an integer."""
        return self.height

    def get_board(self):
        """This method returns the 2D list representing the board. It takes no arguments and returns a 2D list of Stack objects."""
        return self.board

    def __str__(self) -> str:
        """This method returns a string representation of the board. It takes no arguments and returns a string."""
        temp_str = "  "
        grid = self.board
        column = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        horizontal_barrier = "\n{0:>3}+{1}\n".format(" " ,"---+" * len(column))

        for letter in column:
            temp_str += "{0:>4s}".format(letter) # This is the first row of the board (the alphabet)

        for row in range(self.height):
            temp_str += horizontal_barrier
            temp_str += "{0:^3}|".format(row+1) # This is for the index of the row (The vertical numbers)
            
            for col in range(self.width):

                try:
                    location = grid[row][col].peek().color[0].upper()
                    # It will access in the 2D list by indexing in nested list (grid[row][col]) using double for loops and check that location for any goat color at the top of stack using peek() and .color and I slice the first letter of that color by using [0] and uppercase it in case it's not using upper()

                except:
                    # If there is nothing in the stack in that location, it will raise an exception -> empty space
                    location = " " 

                finally:
                    # If there is an obstacle in the position -> capital X
                    for obstacle in self.obstacle_positions:
                        obstacle_row, obstacle_col = obstacle
                        if (row,column[col]) == (obstacle_row - 1, obstacle_col):
                            location = 'X'

                temp_str += "{0:^3}|".format(location) # Vertical Barrier |
            
        temp_str += horizontal_barrier # The last line of horizontal barrier 
        return temp_str