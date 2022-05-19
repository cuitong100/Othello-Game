"""
5001 MileStone1 Othello
Tong Cui
This is the class Player, which is one of the model of the whole program.
"""


class Player:
    """
    Class Player
    Attributes: color
    Methods: get_adversary, __str__, __eq__
    """
    def __init__(self, color):
        """
        Constructor -- creates new instances of Player
        Parameters:
           self -- the current object
           color -- a string, the color of this Player, black or white
        A ValueError would be raised if color is something except a string "black"
        or "white"
        """
        if color != "black" and color != "white":
            raise ValueError("color should be black or white")
        self.color = color

    def get_adversary(self):
        """
        Method -- get the adversary of the current player
        :return: a Player object
        """
        if self.color == 'white':
            return Player('black')
        else:
            return Player('white')

    def __str__(self):
        """
        Method -- get the string of the current player
        :return: str1, a string
        """
        str1 = f"{self.color}'s turn"
        return str1

    def __eq__(self, other):
        """
        Method -- equal, to tell whether two objects are equal
        :param other: an other Player object
        :return: a boolean, True or False
        """
        if not isinstance(other, Player):
            raise ValueError("other should be a Player object")
        if self.color == other.color:
            return True
        return False

