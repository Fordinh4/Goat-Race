#----------------------------------------------------
# Goat implementation
#----------------------------------------------------

class Goat:
    '''
    An object in this class represents a goat in the game Goat Race.
    '''
    def __init__(self, color) -> None:
        if color not in ['WHITE', 'BLACK', 'RED', 'ORANGE', 'GREEN']:
            raise

        self.color = color
        self.column = None
        self.row = None

    def color(self):
        return self.color

    def check_location(self):
        if (self.column and self.row) == None:
            return -1
        return self.row, self.column

    def set_row(self, Row):
        if 0 >= Row - 1 >= 6:
            raise
        else: 
            self.row = Row - 1

    def set_column(self, Column):
        if type(Column) == str:
            col =['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
            newColumn = col.index(Column)

        else:
            newColumn = Column
            
        if 0 > newColumn > 9:
            raise
        else: 
            self.column = newColumn

    def __str__(self) -> str:
        col =['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        return f"{col[self.column]}{self.row + 1}"