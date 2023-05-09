#----------------------------------------------------
# Player implementation
#----------------------------------------------------

from .goat import Goat

class Player:
    '''
    An object in this class represents a player in the game Goat Race.
    '''
    def __init__(self, color) -> None:
        """Initialize the color and list of goat objects for each player"""
        self.color = color
        self.goats = []
    
    def add_goat(self, goat):
        """Add goats object in to each player list"""
        self.goats.append(goat)

    def remove_goat(self, goat):
        """Remove goats """
        self.goats.remove(goat)

    def check_color(self):
        """Check their color"""
        return self.color

    def check_goatsNumber(self):
        """Check how many goats does one player has?"""
        return len(self.goats)

    def __str__(self) -> str:
        """Return the string"""
        temp = ""
        temp += "{}\n{}:".format(self.color, "Goats")

        for i in self.goats:
            temp += "\n{} {}".format(self.color,  i)
        temp += "\n"

        return temp

