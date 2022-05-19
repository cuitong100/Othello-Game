"""
5001 MileStone1 Othello
Tong Cui
This is the class Board, which is the view of the whole program.
"""

from player import *
import turtle

SQUARE = 50
RADIUS = 20
SIDE_NUM = 4


class Board:
    """
    Class Board
    Attributes: size, an even int that is larger than 2
    Methods: setup, set_click_handler, draw_board, draw_circle,
    update_view, print_winner, draw_lines, move, print_turn, __eq__
    """

    def __init__(self, size):
        """
        Constructor -- creates new instances of Board
        Parameters:
           self -- the current object
           size -- an even integer larger than 2, the size of the board
        """
        if not isinstance(size, int) and size % 2 == 0 and size >= 4:
            raise ValueError("size should be an even integer larger than 2.")
        self.size = size

    def setup(self):
        """
        Method -- setup the initial screen, including drawing the board and setting chess
        on the middle of the board
        :return: nothing
        """
        # draw the board_list
        self.draw_board()
        # draw the pieces
        self.update_view(Player("white"), self.size / 2 - 1, self.size / 2 - 1)
        self.update_view(Player("white"), self.size / 2, self.size / 2)
        self.update_view(Player("black"), self.size / 2 - 1, self.size / 2)
        self.update_view(Player("black"), self.size / 2, self.size / 2 - 1)
        turtle.goto(-1 * SQUARE, (1/2 * self.size) * SQUARE)
        turtle.write("black's turn", font=("lemon", 20, "normal"))

    def set_click_handler(self, handler):
        """
        Method -- get user's click on the screen
        :param handler: a function that can catch the coordinate of user's click
        :return: nothing
        """
        screen = turtle.Screen()
        screen.onclick(handler)

    def draw_board(self):
        """
        Method -- draw an nxn board_list with a green background
        :return: nothing
        """
        turtle.setup(self.size * SQUARE + SQUARE, self.size * SQUARE + SQUARE)
        turtle.screensize(self.size * SQUARE, self.size * SQUARE)
        turtle.bgcolor('white')
        turtle.title("Welcome to Othello")
        turtle.tracer(0)

        # Create the turtle to draw the board_list
        othello = turtle.Turtle()
        othello.penup()
        othello.speed(0)
        othello.hideturtle()

        # Line color is black, fill color is green
        othello.color("black", "forest green")
        # Move the turtle to the upper left corner
        corner = -self.size * SQUARE / 2
        othello.setposition(corner, corner)

        # Draw the green background

        othello.begin_fill()
        for i in range(SIDE_NUM):
            othello.pendown()
            othello.forward(SQUARE * self.size)
            othello.left(90)
        othello.end_fill()

        # Draw the horizontal lines
        for i in range(self.size + 1):
            othello.setposition(corner, SQUARE * i + corner)
            self.draw_lines(othello, self.size)

        # Draw the vertical lines
        othello.left(90)
        for i in range(self.size + 1):
            othello.setposition(SQUARE * i + corner, corner)
            self.draw_lines(othello, self.size)

    def draw_circle(self, color):
        """
        Method -- draw a circle in a certain color
        :param color: the color of the circle
        :return: nothing
        """
        turtle.pendown()
        turtle.hideturtle()
        turtle.color(color, color)
        turtle.setheading(270)
        turtle.begin_fill()
        turtle.circle(RADIUS)
        turtle.end_fill()
        turtle.penup()

    def draw_lines(self, turt, size):
        """
        Method -- draw lines
        :param turt: a turtle object
        :param size: the size of board
        :return: nothing
        """
        turt.pendown()
        turt.forward(SQUARE * size)
        turt.penup()

    def move(self, x_idx, y_idx):
        """
        Method -- move the turtle to new location
        :param x_idx: the new x_idx index location
        :param y_idx: the new y_idx index location
        :return: nothing
        """
        turtle.penup()
        x = SQUARE * (y_idx - self.size / 2) + (SQUARE - 2 * RADIUS) / 2
        y = (self.size / 2 - x_idx - 0.5) * SQUARE
        turtle.goto(x, y)
        turtle.pendown()

    def print_winner(self, result):
        """
        Method -- print the result on the board
        :param result: a string, the information about game result got from othello
        :return: nothing
        """
        turtle.goto(-3 / 2 * SQUARE, 0)
        turtle.color("red")
        turtle.write(result, font=("lemon", 20, "normal"))

    def print_turn(self, player):
        """
        Method -- print the turn on the board
        :param player: a Player object
        :return: nothing
        """
        turtle.goto(-1 * SQUARE, (1/2 * self.size) * SQUARE)
        turtle.color("white")
        turtle.write(player.get_adversary(), font=("lemon", 20, "normal"))
        turtle.color("black")
        turtle.write(player, font=("lemon", 20, "normal"))
        print(player)

    def update_view(self, player, x_idx, y_idx):
        """
        Method -- update the view on the board
        :param player: a Player object
        :param x_idx: the new x_idx location
        :param y_idx: the new y_idx location
        :return: nothing
        """
        self.move(x_idx, y_idx)
        self.draw_circle(player.color)

    def __eq__(self, other):
        """
        Method -- equal, to tell whether two object are equal
        :param other: an other Board object
        :return: a boolean, True or False
        """
        if not isinstance(other, Board):
            raise ValueError("other should be a Board object")
        if self.size == other.size:
            return True
        return False
