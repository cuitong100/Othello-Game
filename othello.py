"""
5001 MileStone1 Othello
Tong Cui
This is the class Othello, which is one of the model of the whole program.
"""


class Othello:
    """
    Class Othello
    Attributes: size
    Methods: is_game_end, is_legal_move, handle_click, get_winner, get_legal_move_list,
    in_south_range, in_north_range, in_east_range, in_west_range, in_northeast_range, in_southeast_range,
    in_northwest_range, in_southwest_range, load_score, save_score, __eq__
    """

    def __init__(self, size):
        """
        Constructor -- creates new instances of Othello
        Parameters:
           self -- the current object
           size -- the size of the board
        Instance variables:
            game -- None
            size -- an even integer larger than 2, the size of the board
            board_list -- a two-dimensional list to store the status of the piece
            num_black -- the number of black pieces
            num_white -- the number of white pieces
            score -- None
            winner -- None
        A ValueError would be raised if size is not an even integer larger than 2
        """
        self.name = None
        if not isinstance(size, int) or size % 2 != 0 or size < 4:
            raise ValueError("Size should be an even integer larger than 2.")
        self.game = None
        self.size = size
        self.board_list = [['E' for i in range(size)] for j in range(size)]
        self.board_list[int(size / 2 - 1)][int(size / 2 - 1)] = "white"
        self.board_list[int(size / 2)][int(size / 2)] = "white"
        self.board_list[int(size / 2)][int(size / 2 - 1)] = "black"
        self.board_list[int(size / 2 - 1)][int(size / 2)] = "black"
        self.num_black = 0
        self.num_white = 0
        self.score = None
        self.winner = None

    def is_game_end(self, player):
        """
        Method -- check whether the game is end and if so print the winner
        :param player: a Player object
        :return: boolean,True if the game is end, otherwise false
        """
        self.num_black = 0
        self.num_white = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board_list[i][j] == 'white':
                    self.num_white += 1
                elif self.board_list[i][j] == 'black':
                    self.num_black += 1
        if self.num_white + self.num_black == self.size ** 2:
            return True
        elif len(self.get_legal_move_list(player)) == 0 and len(self.get_legal_move_list(player.get_adversary())) == 0:
            return True
        else:
            return False

    def get_winner(self):
        """
        Method -- compare the number of pieces for black and white and get the winner
        :return: result, a string, the information about game result
        """
        self.num_black = 0
        self.num_white = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board_list[i][j] == 'white':
                    self.num_white += 1
                elif self.board_list[i][j] == 'black':
                    self.num_black += 1
        if self.num_white == self.num_black:
            self.score = self.num_black
            result = f"       It's a tie.\n Black: {self.num_black} White: {self.num_white}"
        elif self.num_white > self.num_black:
            self.score = self.num_white
            self.winner = 'white'
            result = f"       White wins!\n Black: {self.num_black} White: {self.num_white}"
        else:
            self.score = self.num_black
            self.winner = 'black'
            result = f"       Black wins!\n Black: {self.num_black} White: {self.num_white}"
        return result

    def is_legal_move(self, player, x_idx, y_idx):
        """
        Method -- Check whether a move is legal
        :param player: a player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: boolean, True if the move is valid
        A ValueError would be raised if x_idx and y_idx are not integers from 0 to size - 1
        """
        if (x_idx < 0 or x_idx >= self.size) or (y_idx < 0 or y_idx >= self.size) \
                or self.board_list[x_idx][y_idx] != 'E':
            return False
        if (x_idx, y_idx) in self.get_legal_move_list(player):
            return True
        else:
            return False

    def get_legal_move_list(self, player):
        """
        Method -- to get a list containing all the legal moves for the certain player
        :param player: a Player object
        :return: legal_move_list, a list containing all the coordination of legal move
        """
        legal_move_list = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board_list[i][j] == 'E':
                    if not self.in_north_range(player, i, j) \
                            and not self.in_south_range(player, i, j) \
                            and not self.in_east_range(player, i, j) \
                            and not self.in_west_range(player, i, j) \
                            and not self.in_northeast_range(player, i, j) \
                            and not self.in_southeast_range(player, i, j) \
                            and not self.in_southwest_range(player, i, j) \
                            and not self.in_northwest_range(player, i, j):
                        continue
                    legal_move_list.append((i, j))
        return legal_move_list

    def load_score(self):
        """
        Static Method -- load the score in a ".txt" file
        :return: score_list, a list containing the names and scores of the file,
        """
        try:
            filename = "scores.txt"
            score_list = []
            with open(filename, 'r') as scores:
                for score in scores:
                    name, score = score.rsplit(' ', 1)
                    score_list.append([name, int(score)])
            return score_list
        except PermissionError:
            print("You do not have permission to use that file")
        except OSError:
            return None

    def save_score(self):
        """
        Method -- save a new name and a new score in the file
        and list the highest score record on the top of the file.
        :return: nothing
        """
        try:
            filename = "scores.txt"
            score_list = self.load_score()
            if score_list is None:
                score_list = []
            score_list.append([self.name, self.score])
            score_list.sort(key=lambda x: x[1], reverse=True)
            with open(filename, 'w') as scores:
                for record in score_list:
                    scores.write(str(record[0]) + ' ' + str(record[1]) + "\n")
        except PermissionError:
            print("You do not have permission to use that file")
        except OSError:
            print("File 'grades.txt' not found, please create one first")

    def save_winner(self):
        self.name = input("Congratulations! You win! What's your name?")
        self.save_score()
        quit()

    def in_south_range(self, player, x_idx, y_idx):
        """
        Method -- to test if the coordinate is in the south range of
         at least one opponent's piece can be flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: a boolean, True or False
        """
        if x_idx == 0:
            return False
        i = x_idx - 1
        j = y_idx
        if self.board_list[i][j] == "E":
            return False
        elif self.board_list[i][j] == player.color:
            return False
        while self.board_list[i][j] != player.color and i > 0:
            i -= 1
            if self.board_list[i][j] == "E":
                return False
            elif self.board_list[i][j] == player.color:
                return True
        return False

    def in_north_range(self, player, x_idx, y_idx):
        """
         Method -- to test if the coordinate is in the north range of
         at least one opponent's piece can be flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: a boolean, True or False
        """
        if x_idx == self.size - 1:
            return False
        i = x_idx + 1
        j = y_idx
        if self.board_list[i][j] == "E":
            return False
        elif self.board_list[i][j] == player.color:
            return False
        while self.board_list[i][j] != player.color and i < self.size - 1:
            i += 1
            if self.board_list[i][j] == "E":
                return False
            elif self.board_list[i][j] == player.color:
                return True
        return False

    def in_west_range(self, player, x_idx, y_idx):
        """
         Method -- to test if the coordinate is in the west range of
         at least one opponent's piece can be flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: a boolean, True or False
        """
        if y_idx == self.size - 1:
            return False
        i = x_idx
        j = y_idx + 1
        if self.board_list[i][j] == "E":
            return False
        elif self.board_list[i][j] == player.color:
            return False
        while self.board_list[i][j] != player.color and j < self.size - 1:
            j += 1
            if self.board_list[i][j] == "E":
                return False
            elif self.board_list[i][j] == player.color:
                return True
        return False

    def in_east_range(self, player, x_idx, y_idx):
        """
        Method -- to test if the coordinate is in the east range of
         at least one opponent's piece can be flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: a boolean, True or False
        """
        if y_idx == 0:
            return False
        i = x_idx
        j = y_idx - 1
        if self.board_list[i][j] == "E":
            return False
        elif self.board_list[i][j] == player.color:
            return False
        while self.board_list[i][j] != player.color and j > 0:
            j -= 1
            if self.board_list[i][j] == "E":
                return False
            elif self.board_list[i][j] == player.color:
                return True
        return False

    def in_northeast_range(self, player, x_idx, y_idx):
        """
        Method -- to test if the coordinate is in the northeast range of
         at least one opponent's piece can be flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: a boolean, True or False
        """
        if y_idx == 0 or x_idx == self.size - 1:
            return False
        i = x_idx + 1
        j = y_idx - 1
        if self.board_list[i][j] == "E":
            return False
        elif self.board_list[i][j] == player.color:
            return False
        while self.board_list[i][j] != player.color and i < self.size - 1 and j > 0:
            i += 1
            j -= 1
            if self.board_list[i][j] == "E":
                return False
            elif self.board_list[i][j] == player.color:
                return True
        return False

    def in_southeast_range(self, player, x_idx, y_idx):
        """
        Method -- to test if the coordinate is in the southeast range of
         at least one opponent's piece can be flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: a boolean, True or False
        """
        if y_idx == 0 or x_idx == 0:
            return False
        i = x_idx - 1
        j = y_idx - 1
        if self.board_list[i][j] == "E":
            return False
        elif self.board_list[i][j] == player.color:
            return False
        while self.board_list[i][j] != player.color and i > 0 and j > 0:
            i -= 1
            j -= 1
            if self.board_list[i][j] == "E":
                return False
            elif self.board_list[i][j] == player.color:
                return True
        return False

    def in_northwest_range(self, player, x_idx, y_idx):
        """
        Method -- to test if the coordinate is in the northwest range of
         at least one opponent's piece can be flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: a boolean, True or False
        """
        if y_idx == self.size - 1 or x_idx == self.size - 1:
            return False
        i = x_idx + 1
        j = y_idx + 1
        if self.board_list[i][j] == "E":
            return False
        elif self.board_list[i][j] == player.color:
            return False
        while self.board_list[i][j] != player.color and i < self.size - 1 and j < self.size - 1:
            i += 1
            j += 1
            if self.board_list[i][j] == "E":
                return False
            elif self.board_list[i][j] == player.color:
                return True
        return False

    def in_southwest_range(self, player, x_idx, y_idx):
        """
        Method -- to test if the coordinate is in the southwest range of
         at least one opponent's piece can be flipped.
        :param player: a Player object
        :param x_idx: an int, the x index coordinate of the move, [0, size-1]
        :param y_idx: an int, the y index coordinate of the move, [0, size-1]
        :return: a boolean, True or False
        """
        if y_idx == self.size - 1 or x_idx == 0:
            return False
        i = x_idx - 1
        j = y_idx + 1
        if self.board_list[i][j] == "E":
            return False
        elif self.board_list[i][j] == player.color:
            return False
        while self.board_list[i][j] != player.color and i > 0 and j < self.size - 1:
            i -= 1
            j += 1
            if self.board_list[i][j] == "E":
                return False
            elif self.board_list[i][j] == player.color:
                return True
        return False

    def test_write_to_file(self, file_name, expected):
        """
        function: test write to file
        :param file_name: a string, the name of a ".txt" file
        :param expected: a string, the expected content of the file
        :return: a boolean, True or False
        """
        try:
            with open(file_name, 'r', encoding="utf-8-sig") as f:
                content = f.read()
                return content == expected
        except PermissionError:
            print("You don't have permission to use the file:", file_name)
        except OSError:
            print("Something happened while writing to the file:", file_name)
        except UnboundLocalError:
            print("Local variable referenced before assignment")

    def __eq__(self, other):
        """
        Method -- equal, to tell whether two object are equal
        :param other: an other Othello object
        :return: a boolean, True or False
        """
        if not isinstance(other, Othello):
            raise ValueError("other should be an Othello object")
        if self.size == other.size:
            return True
        return False
