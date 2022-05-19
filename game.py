"""
5001 MileStone1 Othello
Tong Cui
This is the class Game, which is the controller of the whole program.
"""

from board import *
from player import *
from othello import *
import time


class Game:
    """
    Class Game
    Attributes: size
    Methods: handler_human, handler_AI, handle_click, handle_AI_click, handle_human_click_with_AI,
    update_view, print_winner, get_total_flip, get_south_flip, get_north_flip, get_west_flip, get_east_flip,
    get_southwest_flip, get_southeast_flip, get_northeast_flip, get_northwest_flip, get_flip, get_north_flip_num,
    get_flip, get_south_flip_num, get_east_flip_num, get_west_flip_num, get_northeast_flip_num, get_northwest_flip_num,
    get_southwest_flip_num, get_southeast_flip_num, in_corner, on_edge, get_AI_move, __eq__
    """

    def __init__(self, size, mode='H'):
        """
        Constructor -- creates new instances of Game
        Parameters:
           self -- the current Game
           size -- an even integer larger than 2, the size of the board
           mode -- A string, 'H' or 'AI', to decide who does the user play with
        Instance variables:
            board -- new instances of Board
            othello -- new instance of Othello
            player1 -- new instance of Player, with color black
            player2 -- new instance of Player, with color white
            who_plays -- set the turn for player1 at the beginning
            northwest_flip_num -- an int, the number of pieces would get flipped in this direction
            southwest_flip_num -- an int, the number of pieces would get flipped in this direction
            southeast_flip_num -- an int, the number of pieces would get flipped in this direction
            northeast_flip_num -- an int, the number of pieces would get flipped in this direction
            north_flip_num -- an int, the number of pieces would get flipped in this direction
            east_flip_num -- an int, the number of pieces would get flipped in this direction
            west_flip_num -- an int, the number of pieces would get flipped in this direction
            south_flip_num -- an int, the number of pieces would get flipped in this direction
            best_move_x -- None, the x-coordination of AI's move
            best_move_y -- None, the y-coordination of AI's move
        A ValueError would be raised if size is not an even integer larger than 2
        """
        self.northwest_flip_num = 0
        self.southwest_flip_num = 0
        self.southeast_flip_num = 0
        self.northeast_flip_num = 0
        self.north_flip_num = 0
        self.east_flip_num = 0
        self.west_flip_num = 0
        self.south_flip_num = 0
        self.best_move_x = None
        self.best_move_y = None
        if not isinstance(size, int) or size % 2 != 0 or size < 4:
            raise ValueError("size should be an even integer larger than 2.")
        if mode != 'H' and mode != 'AI':
            raise ValueError("Mode only can be 'H'(means human) or 'AI'")
        self.board = Board(size)
        self.board.setup()
        self.othello = Othello(size)
        self.othello.game = self
        self.player_1 = Player("black")
        self.player_2 = Player("white")
        self.who_plays = self.player_1
        self.size = size
        self.mode = mode
        if self.mode == 'H':
            self.board.set_click_handler(self.handler_human)
        elif self.mode == 'AI':
            self.board.set_click_handler(self.handler_AI)

    def handler_human(self, x, y):
        """
        Method -- handler catches the coordinate of user's click and ask handle_click to deal with it
        :param x: a float, the x-coordinate of user's click
        :param y: a float, the y-coordinate of user's click
        :return: nothing
        A ValueError would be raised if x and y are not floats
        """
        if not isinstance(x, float):
            raise ValueError("x should be a float")
        if not isinstance(y, float):
            raise ValueError("y should be a float")
        if self.who_plays == self.player_1:
            self.handle_click(self.player_1, x, y)
        else:
            self.handle_click(self.player_2, x, y)

    def handler_AI(self, x, y):
        """
        Method -- handler_AI catches the coordinate of user's click and ask handle_click to deal with it,
        and then get the AI's move and ask handle_AI_click to deal with it
        :param x: a float, the x-coordinate of user's click
        :param y: a float, the y-coordinate of user's click
        :return: nothing
        A ValueError would be raised if x and y are not floats
        """
        if not isinstance(x, float):
            raise ValueError("x should be a float")
        if not isinstance(y, float):
            raise ValueError("y should be a float")
        x_idx = int(-y // SQUARE + self.size / 2)
        y_idx = int(x // SQUARE + self.size / 2)
        if self.othello.get_legal_move_list(self.player_1):
            if self.othello.is_legal_move(self.player_1, x_idx, y_idx):
                self.handle_human_click_with_AI(self.player_1, x, y)
                time.sleep(1.5)
                self.handle_AI_click()
        else:
            self.switch_player()
            self.print_turn(self.player_2)
            time.sleep(1.5)
            self.handle_AI_click()

    def handle_click(self, player, x, y):
        """
        Method -- transfer the coordination of user click (x, y)
        to index coordination (x_idx, y_idx), if the move is legal, place a piece on the board
        if the game is end, the winner would be printed on the screen,
        and the name and score would be saved in a file
        :param player: a Player object
        :param x: a float, the x coordinate of the move
        :param y: a float, the y coordinate of the move
        :return: nothing
        A ValueError would be raised if x and y are not floats
        """
        if not isinstance(x, float):
            raise ValueError("x should be a float")
        if not isinstance(y, float):
            raise ValueError("y should be a float")
        x_idx = int(-y // SQUARE + self.size / 2)
        y_idx = int(x // SQUARE + self.size / 2)
        # print("{} at ({}, {})".format(player.name, x_idx, y_idx))
        if not self.othello.is_game_end(player):
            if self.othello.get_legal_move_list(player):
                if self.othello.is_legal_move(player, x_idx, y_idx):
                    self.set_piece(player, x_idx, y_idx)
                    self.switch_player()
                    self.print_turn(player.get_adversary())
            else:
                self.switch_player()
                self.print_turn(player.get_adversary())
        if self.othello.is_game_end(player.get_adversary()):
            result = self.othello.get_winner()
            self.print_winner(result)
            if 'tie' not in result:
                if self.mode != 'AI' or self.othello.winner != 'white':
                    self.othello.save_winner()

    def handle_human_click_with_AI(self, player, x, y):
        """
        Method -- transfer the coordination of user click (x, y)
        to index coordination (x_idx, y_idx), if the move is legal, place a piece on the board
        if the game is end, the winner would be printed on the screen,
        and the name and score would be saved in a file
        :param player: a Player object
        :param x: a float, the x coordinate of the move
        :param y: a float, the y coordinate of the move
        :return: nothing
        A ValueError would be raised if x and y are not floats
        """
        if not isinstance(x, float):
            raise ValueError("x should be a float")
        if not isinstance(y, float):
            raise ValueError("y should be a float")
        x_idx = int(-y // SQUARE + self.size / 2)
        y_idx = int(x // SQUARE + self.size / 2)
        # print("{} at ({}, {})".format(player.name, x_idx, y_idx))
        if not self.othello.is_game_end(player):
            self.set_piece(player, x_idx, y_idx)
            self.switch_player()
            self.print_turn(player.get_adversary())
        if self.othello.is_game_end(player.get_adversary()):
            result = self.othello.get_winner()
            self.print_winner(result)
            if 'tie' not in result:
                if self.mode != 'AI' or self.othello.winner != 'white':
                    self.othello.save_winner()

    def handle_AI_click(self):
        """
        Method -- get a move from AI, if the move is legal, place a piece on the board
        if the game is end, the winner would be printed on the screen,
        and if user wins, the name and score would be saved in a file
        :return: nothing
        """
        if not self.othello.is_game_end(self.player_2):
            if self.othello.get_legal_move_list(self.player_2):
                x_idx, y_idx = self.get_AI_move()
                self.set_piece(self.player_2, x_idx, y_idx)
                self.print_turn(self.player_1)
            else:
                self.print_turn(self.player_1)
        if self.othello.is_game_end(self.player_1):
            result = self.othello.get_winner()
            self.print_winner(result)
            if 'tie' not in result and self.othello.winner == 'black':
                self.othello.save_winner()

    def get_AI_move(self):
        """
        Method -- get the AI move. If legal move list contain the move in corners or on edges,
        method would return the best coordination in corners or on edges. Otherwise, it would
        return a move which can flip the most opponents' pieces.
        :return: best_move_x, best_move_y, two ints
        """
        list1 = self.othello.get_legal_move_list(self.player_2)
        if list1 != []:
            max_flip = 1
            for corr in list1:
                x_idx = corr[0]
                y_idx = corr[1]
                if self.in_corner(x_idx, y_idx):
                    self.best_move_x = x_idx
                    self.best_move_y = y_idx
                    break
                elif self.on_edge(x_idx, y_idx):
                    self.best_move_x = x_idx
                    self.best_move_y = y_idx
                    break
                else:
                    total_flip = self.get_total_flip(x_idx, y_idx)
                    if total_flip >= max_flip:
                        self.best_move_x = x_idx
                        self.best_move_y = y_idx
                        max_flip = total_flip
        return self.best_move_x, self.best_move_y

    def switch_player(self):
        """
        Method -- switch_player would switch the turn between player1 and player2
        :return: nothing
        """
        if self.who_plays == self.player_1:
            self.who_plays = self.player_2
        else:
            self.who_plays = self.player_1

    def get_total_flip(self, x_idx, y_idx):
        """
        Method -- get the number of the opponent's pieces which would be flipped,
        assuming the AI player places a piece in the input coordination
        :param x_idx: the x-coordination of AI's move
        :param y_idx: the y-coordination of AI's move
        :return: total_flip, an int
        """
        south_flip_num = self.get_south_flip_num(self.player_2, x_idx, y_idx)
        north_flip_num = self.get_north_flip_num(self.player_2, x_idx, y_idx)
        east_flip_num = self.get_east_flip_num(self.player_2, x_idx, y_idx)
        west_flip_num = self.get_west_flip_num(self.player_2, x_idx, y_idx)
        northwest_flip_num = self.get_northwest_flip_num(self.player_2, x_idx, y_idx)
        southwest_flip_num = self.get_southwest_flip_num(self.player_2, x_idx, y_idx)
        southeast_flip_num = self.get_southeast_flip_num(self.player_2, x_idx, y_idx)
        northeast_flip_num = self.get_northeast_flip_num(self.player_2, x_idx, y_idx)
        total_flip = south_flip_num + north_flip_num + east_flip_num + west_flip_num \
                     + northwest_flip_num + southeast_flip_num + southwest_flip_num \
                     + northeast_flip_num
        return total_flip

    def in_corner(self, x_idx, y_idx):
        """
        Method -- to decide if the move is in corners
        :param x_idx: the x-coordination of AI's move
        :param y_idx: the y-coordination of AI's move
        :return: a boolean, True or False
        """
        if x_idx in [0, self.size - 1] and y_idx in [0, self.size - 1]:
            return True
        return False

    def on_edge(self, x_idx, y_idx):
        """
        Method -- to decide if the move is on edges
        :param x_idx: the x-coordination of AI's move
        :param y_idx: the y-coordination of AI's move
        :return: a boolean, True or False
        """
        if x_idx in [0, self.size - 1] or y_idx in [0, self.size - 1]:
            return True
        return False

    def update_view(self, player, x_idx, y_idx):
        """
        Method -- update_view would call the board variable to update the board
        :param player: an instance of Player
        :param x_idx: the corresponding row of user_click
        :param y_idx: the corresponding col of user_click
        :return: nothing
        A ValueError would be raised if x_idx and y_idx are not integers from 0 to size - 1
        """
        if not isinstance(player, Player):
            raise ValueError("player should be a Player object")
        if not isinstance(x_idx, int) or x_idx < 0 or x_idx > self.size - 1:
            raise ValueError("x_idx should be an int from 0 to size - 1")
        if not isinstance(y_idx, int) or y_idx < 0 or y_idx > self.size - 1:
            raise ValueError("y_idx should be an int from 0 to size - 1")
        self.board.update_view(player, x_idx, y_idx)

    def print_winner(self, result):
        """
        Method -- ask the board variable to print the winner
        :param result: a string, the information about game result got from othello
        :return: nothing
        """
        self.board.print_winner(result)

    def print_turn(self, player):
        """
        Method -- ask the board variable to print the turn
        :param player: a player object
        :return: nothing
        """
        self.board.print_turn(player)

    def set_piece(self, player, x_idx, y_idx):
        """
        Method -- set a piece for the current player
        :param player: a player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: nothing
        """
        self.othello.board_list[x_idx][y_idx] = player.color
        self.update_view(player, x_idx, y_idx)
        self.get_flip(player, x_idx, y_idx)

    def get_south_flip(self, player, x_idx, y_idx):
        """
        Method -- if the player is in the south range of the opponent,
        this method would get the opponent's pieces flip.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: nothing
        """
        if self.othello.in_south_range(player, x_idx, y_idx):
            i = x_idx - 1
            j = y_idx
            while self.othello.board_list[i][j] != player.color and i > 0:
                self.othello.board_list[i][j] = player.color
                self.update_view(player, i, j)
                i -= 1

    def get_north_flip(self, player, x_idx, y_idx):
        """
        Method -- if the player is in the north range of the opponent,
        this method would get the opponent's pieces flip.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: nothing
        """
        if self.othello.in_north_range(player, x_idx, y_idx):
            i = x_idx + 1
            j = y_idx
            while self.othello.board_list[i][j] != player.color and i < self.size - 1:
                self.othello.board_list[i][j] = player.color
                self.update_view(player, i, j)
                i += 1

    def get_west_flip(self, player, x_idx, y_idx):
        """
        Method -- if the player is in the west range of the opponent,
        this method would get the opponent's pieces flip.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: nothing
        """
        if self.othello.in_west_range(player, x_idx, y_idx):
            i = x_idx
            j = y_idx + 1
            while self.othello.board_list[i][j] != player.color and j < self.size - 1:
                self.othello.board_list[i][j] = player.color
                self.update_view(player, i, j)
                j += 1

    def get_east_flip(self, player, x_idx, y_idx):
        """
        Method -- if the player is in the east range of the opponent,
        this method would get the opponent's pieces flip.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: nothing
        """
        if self.othello.in_east_range(player, x_idx, y_idx):
            i = x_idx
            j = y_idx - 1
            while self.othello.board_list[i][j] != player.color and j > 0:
                self.othello.board_list[i][j] = player.color
                self.update_view(player, i, j)
                j -= 1

    def get_northeast_flip(self, player, x_idx, y_idx):
        """
        Method -- if the player is in the northeast range of the opponent,
        this method would get the opponent's pieces flip.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: nothing
        """
        if self.othello.in_northeast_range(player, x_idx, y_idx):
            i = x_idx + 1
            j = y_idx - 1
            while self.othello.board_list[i][j] != player.color and j > 0 and i < self.size - 1:
                self.othello.board_list[i][j] = player.color
                self.update_view(player, i, j)
                i += 1
                j -= 1

    def get_southeast_flip(self, player, x_idx, y_idx):
        """
        Method -- if the player is in the southeast range of the opponent,
        this method would get the opponent's pieces flip.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: nothing
        """
        if self.othello.in_southeast_range(player, x_idx, y_idx):
            i = x_idx - 1
            j = y_idx - 1
            while self.othello.board_list[i][j] != player.color and j > 0 and i > 0:
                self.othello.board_list[i][j] = player.color
                self.update_view(player, i, j)
                i -= 1
                j -= 1

    def get_northwest_flip(self, player, x_idx, y_idx):
        """
        Method -- if the player is in the northwest range of the opponent,
        this method would get the opponent's pieces flip.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: nothing
        """
        if self.othello.in_northwest_range(player, x_idx, y_idx):
            i = x_idx + 1
            j = y_idx + 1
            while self.othello.board_list[i][j] != player.color and j < self.size - 1 and i < self.size - 1:
                self.othello.board_list[i][j] = player.color
                self.update_view(player, i, j)
                i += 1
                j += 1

    def get_southwest_flip(self, player, x_idx, y_idx):
        """
        Method -- if the player is in the southwest range of the opponent,
        this method would get the opponent's pieces flip.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: nothing
        """
        if self.othello.in_southwest_range(player, x_idx, y_idx):
            i = x_idx - 1
            j = y_idx + 1
            while self.othello.board_list[i][j] != player.color and j < self.size - 1 and i > 0:
                self.othello.board_list[i][j] = player.color
                self.update_view(player, i, j)
                i -= 1
                j += 1

    def get_flip(self, player, x_idx, y_idx):
        """
        Method -- get all the opponent's pieces flip if they are available
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: nothing
        """
        self.get_north_flip(player, x_idx, y_idx)
        self.get_south_flip(player, x_idx, y_idx)
        self.get_west_flip(player, x_idx, y_idx)
        self.get_east_flip(player, x_idx, y_idx)
        self.get_northeast_flip(player, x_idx, y_idx)
        self.get_southeast_flip(player, x_idx, y_idx)
        self.get_northwest_flip(player, x_idx, y_idx)
        self.get_southwest_flip(player, x_idx, y_idx)

    def get_south_flip_num(self, player, x_idx, y_idx):
        """
        Method -- assuming the player places a piece in the certain index coordination
        in the south range of the opponent, this method would count how many opponent's pieces would get flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: self.south_flip_num, an int, the number of opponent's pieces which would be flipped
        """
        self.south_flip_num = 0
        if self.othello.in_south_range(player, x_idx, y_idx):
            i = x_idx - 1
            j = y_idx
            while self.othello.board_list[i][j] != player.color and i > 0:
                i -= 1
                self.south_flip_num += 1
        return self.south_flip_num

    def get_west_flip_num(self, player, x_idx, y_idx):
        """
        Method -- assuming the player places a piece in the certain index coordination
        in the west range of the opponent, this method would count how many opponent's pieces would get flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: self.west_flip_num, an int, the number of opponent's pieces which would be flipped
        """
        self.west_flip_num = 0
        if self.othello.in_west_range(player, x_idx, y_idx):
            i = x_idx
            j = y_idx + 1
            while self.othello.board_list[i][j] != player.color and j < self.size - 1:
                j += 1
                self.west_flip_num += 1
        return self.west_flip_num

    def get_east_flip_num(self, player, x_idx, y_idx):
        """
        Method -- assuming the player places a piece in the certain index coordination
        in the east range of the opponent, this method would count how many opponent's pieces would get flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: self.east_flip_num, an int, the number of opponent's pieces which would be flipped
        """
        self.east_flip_num = 0
        if self.othello.in_east_range(player, x_idx, y_idx):
            i = x_idx
            j = y_idx - 1
            while self.othello.board_list[i][j] != player.color and j > 0:
                j -= 1
                self.east_flip_num += 1
        return self.east_flip_num

    def get_north_flip_num(self, player, x_idx, y_idx):
        """
        Method -- assuming the player places a piece in the certain index coordination
        in the north range of the opponent, this method would count how many opponent's pieces would get flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: self.north_flip_num, an int, the number of opponent's pieces which would be flipped
        """
        self.north_flip_num = 0
        if self.othello.in_north_range(player, x_idx, y_idx):
            i = x_idx + 1
            j = y_idx
            while self.othello.board_list[i][j] != player.color and i < self.size - 1:
                i += 1
                self.north_flip_num += 1
        return self.north_flip_num

    def get_northeast_flip_num(self, player, x_idx, y_idx):
        """
        Method -- assuming the player places a piece in the certain index coordination
        in the northeast range of the opponent, this method would count how many opponent's pieces would get flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: self.northeast_flip_num, an int, the number of opponent's pieces which would be flipped
        """
        self.northeast_flip_num = 0
        if self.othello.in_northeast_range(player, x_idx, y_idx):
            i = x_idx + 1
            j = y_idx - 1
            while self.othello.board_list[i][j] != player.color and j > 0 and i < self.size - 1:
                i += 1
                j -= 1
                self.northeast_flip_num += 1
        return self.northeast_flip_num

    def get_southeast_flip_num(self, player, x_idx, y_idx):
        """
        Method -- assuming the player places a piece in the certain index coordination
        in the southeast range of the opponent, this method would count how many opponent's pieces would get flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: self.southeast_flip_num, an int, the number of opponent's pieces which would be flipped
        """
        self.southeast_flip_num = 0
        if self.othello.in_southeast_range(player, x_idx, y_idx):
            i = x_idx - 1
            j = y_idx - 1
            while self.othello.board_list[i][j] != player.color and j > 0 and i > 0:
                i -= 1
                j -= 1
                self.southeast_flip_num += 1
        return self.southeast_flip_num

    def get_northwest_flip_num(self, player, x_idx, y_idx):
        """
        Method -- assuming the player places a piece in the certain index coordination
        in the northwest range of the opponent, this method would count how many opponent's pieces would get flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: self.northwest_flip_num, an int, the number of opponent's pieces which would be flipped
        """
        self.northwest_flip_num = 0
        if self.othello.in_northwest_range(player, x_idx, y_idx):
            i = x_idx + 1
            j = y_idx + 1
            while self.othello.board_list[i][j] != player.color and j < self.size - 1 and i < self.size - 1:
                i += 1
                j += 1
                self.northwest_flip_num += 1
        return self.northwest_flip_num

    def get_southwest_flip_num(self, player, x_idx, y_idx):
        """
        Method -- assuming the player places a piece in the certain index coordination
        in the southwest range of the opponent, this method would count how many opponent's pieces would get flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: self.southwest_flip_num, an int, the number of opponent's pieces which would be flipped
        """
        self.southwest_flip_num = 0
        if self.othello.in_southwest_range(player, x_idx, y_idx):
            i = x_idx - 1
            j = y_idx + 1
            while self.othello.board_list[i][j] != player.color and j < self.size - 1 and i > 0:
                i -= 1
                j += 1
                self.southwest_flip_num += 1
        return self.southwest_flip_num

    def __eq__(self, other):
        """
        Method -- equal, to tell whether two objects are equal
        :param other: an other game object
        :return: a boolean, True or False
        """
        if not isinstance(other, Game):
            raise ValueError("other should be a Game object")
        if self.size == other.size and self.mode == other.mode:
            return True
        return False
