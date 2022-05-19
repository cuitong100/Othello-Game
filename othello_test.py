"""
5001 MileStone1 Othello
Tong Cui
This is the test file for the class Othello, Game, Player.
"""

from game import *
from player import *
import unittest


class TestOthello(unittest.TestCase):
    def test_player_init_basic(self):
        player1 = Player("white")
        self.assertEqual(player1.color, "white")

    def test_player_other_color_raise_ValueError(self):
        with self.assertRaises(ValueError):
            Player("blue")

    def test_othello_init_basic(self):
        othello1 = Othello(8)
        self.assertEqual(othello1.size, 8)
        self.assertEqual(othello1.game, None)
        self.assertEqual(othello1.num_black, 0)
        self.assertEqual(othello1.num_white, 0)
        self.assertEqual(othello1.board_list[3][3], "white")
        self.assertEqual(othello1.board_list[4][4], "white")
        self.assertEqual(othello1.board_list[4][3], "black")
        self.assertEqual(othello1.board_list[3][4], "black")
        self.assertEqual(othello1.winner, None)
        self.assertEqual(othello1.score, None)
        self.assertEqual(othello1.game, None)

    def test_othello_with_wrong_size_raise_ValueError(self):
        with self.assertRaises(ValueError):
            Othello(-4)

    def test_othello_with_wrong_string__size_raise_ValueError(self):
        with self.assertRaises(ValueError):
            Othello('t')

    def test_othello_is_game_end_True(self):
        othello = Othello(4)
        for i in range(4):
            for j in range(4):
                if i % 2 == 0 and j % 2 == 0:
                    othello.board_list[i][j] = 'white'
                elif i % 2 != 0 and j % 2 != 0:
                    othello.board_list[i][j] = 'white'
                else:
                    othello.board_list[i][j] = 'black'
        player1 = Player('black')
        self.assertTrue(othello.is_game_end(player1))

    def test_othello_is_game_end_False(self):
        othello = Othello(4)
        for i in range(4):
            for j in range(4):
                if i % 2 == 0 and j % 2 == 0:
                    othello.board_list[i][j] = 'white'
                elif i % 2 != 0 and j % 2 != 0:
                    othello.board_list[i][j] = 'white'
                else:
                    othello.board_list[i][j] = 'black'
        othello.board_list[0][0] = 'E'
        player1 = Player('white')
        self.assertFalse(othello.is_game_end(player1))

    def test_othello_not_full_is_game_end_False(self):
        othello = Othello(4)
        for i in range(4):
            for j in range(4):
                if i % 2 == 0 and j % 2 == 0:
                    othello.board_list[i][j] = 'white'
                elif i % 2 != 0 and j % 2 != 0:
                    othello.board_list[i][j] = 'white'
                else:
                    othello.board_list[i][j] = 'black'
        othello.board_list[0][0] = 'E'
        othello.board_list[1][1] = 'black'
        player1 = Player('black')
        self.assertFalse(othello.is_game_end(player1))

    def test_othello_not_full_is_game_end_True(self):
        othello = Othello(4)
        for i in range(4):
            for j in range(4):
                othello.board_list[i][j] = 'white'
        othello.board_list[0][0] = 'E'
        player1 = Player('black')
        self.assertTrue(othello.is_game_end(player1))

    def test_othello_get_winner_black_win(self):
        othello = Othello(4)
        for i in range(4):
            for j in range(4):
                if i % 2 == 0 and j % 2 == 0:
                    othello.board_list[i][j] = 'white'
                elif i % 2 != 0 and j % 2 != 0:
                    othello.board_list[i][j] = 'white'
                else:
                    othello.board_list[i][j] = 'black'
        othello.board_list[0][0] = 'E'
        msg = f"       Black wins!\n Black: 8 White: 7"
        self.assertEqual(othello.get_winner(), msg)

    def test_othello_get_winner_white(self):
        othello = Othello(4)
        for i in range(4):
            for j in range(4):
                if i % 2 == 0 and j % 2 == 0:
                    othello.board_list[i][j] = 'black'
                elif i % 2 != 0 and j % 2 != 0:
                    othello.board_list[i][j] = 'black'
                else:
                    othello.board_list[i][j] = 'white'
        othello.board_list[0][0] = 'E'
        msg = f"       White wins!\n Black: 7 White: 8"
        self.assertEqual(othello.get_winner(), msg)

    def test_othello_get_winner_tie(self):
        othello = Othello(4)
        for i in range(4):
            for j in range(4):
                if i % 2 == 0 and j % 2 == 0:
                    othello.board_list[i][j] = 'black'
                elif i % 2 != 0 and j % 2 != 0:
                    othello.board_list[i][j] = 'black'
                else:
                    othello.board_list[i][j] = 'white'
        msg = f"       It's a tie.\n Black: 8 White: 8"
        self.assertEqual(othello.get_winner(), msg)

    def test_othello_is_legal_move_True(self):
        othello = Othello(8)
        player1 = Player('black')
        self.assertTrue(othello.is_legal_move(player1, 5, 4))

    def test_othello_is_legal_move_False(self):
        othello = Othello(8)
        player1 = Player('black')
        self.assertFalse(othello.is_legal_move(player1, 5, 5))

    def test_othello_get_legal_move_list_black(self):
        othello = Othello(8)
        player1 = Player('black')
        legal_move_list = [(2, 3), (3, 2), (4, 5), (5, 4)]
        self.assertEqual(othello.get_legal_move_list(player1), legal_move_list)

    def test_othello_get_legal_move_list_white(self):
        othello = Othello(8)
        player1 = Player('white')
        legal_move_list = [(2, 4), (3, 5), (4, 2), (5, 3)]
        self.assertEqual(othello.get_legal_move_list(player1), legal_move_list)

    def test_othello_in_south_range_True(self):
        othello = Othello(8)
        player1 = Player('white')
        self.assertTrue(othello.in_south_range(player1, 5, 3))

    def test_othello_in_south_range_False(self):
        othello = Othello(8)
        player1 = Player('white')
        self.assertFalse(othello.in_south_range(player1, 5, 4))

    def test_othello_in_north_range_True(self):
        othello = Othello(8)
        player1 = Player('white')
        self.assertTrue(othello.in_north_range(player1, 2, 4))

    def test_othello_in_north_range_False(self):
        othello = Othello(8)
        player1 = Player('white')
        self.assertFalse(othello.in_north_range(player1, 2, 3))

    def test_othello_in_east_range_True(self):
        othello = Othello(8)
        player1 = Player('white')
        self.assertTrue(othello.in_east_range(player1, 3, 5))

    def test_othello_in_east_range_False(self):
        othello = Othello(8)
        player1 = Player('white')
        self.assertFalse(othello.in_east_range(player1, 2, 4))

    def test_othello_in_west_range_True(self):
        othello = Othello(8)
        player1 = Player('white')
        self.assertTrue(othello.in_west_range(player1, 4, 2))

    def test_othello_in_west_range_False(self):
        othello = Othello(8)
        player1 = Player('white')
        self.assertFalse(othello.in_west_range(player1, 2, 4))

    def test_othello_in_northwest_range_True(self):
        othello = Othello(8)
        othello.board_list[3][3] = "black"
        player1 = Player('white')
        self.assertTrue(othello.in_northwest_range(player1, 2, 2))

    def test_othello_in_northwest_range_False(self):
        othello = Othello(8)
        othello.board_list[3][3] = "black"
        player1 = Player('black')
        self.assertFalse(othello.in_northwest_range(player1, 2, 2))

    def test_othello_in_northeast_range_True(self):
        othello = Othello(8)
        othello.board_list[4][3] = "white"
        player1 = Player('white')
        self.assertTrue(othello.in_northeast_range(player1, 2, 5))

    def test_othello_in_northeast_range_False(self):
        othello = Othello(8)
        othello.board_list[3][3] = "white"
        player1 = Player('black')
        self.assertFalse(othello.in_northeast_range(player1, 2, 5))

    def test_othello_in_southeast_range_True(self):
        othello = Othello(8)
        othello.board_list[4][4] = "black"
        player1 = Player('white')
        self.assertTrue(othello.in_southeast_range(player1, 5, 5))

    def test_othello_in_southeast_range_False(self):
        othello = Othello(8)
        othello.board_list[4][4] = "black"
        player1 = Player('black')
        self.assertFalse(othello.in_southeast_range(player1, 5, 5))

    def test_othello_in_southwest_range_True(self):
        othello = Othello(8)
        othello.board_list[3][4] = "white"
        player1 = Player('white')
        self.assertTrue(othello.in_southwest_range(player1, 5, 2))

    def test_othello_in_southwest_range_False(self):
        othello = Othello(8)
        othello.board_list[3][4] = "white"
        player1 = Player('black')
        self.assertFalse(othello.in_southwest_range(player1, 5, 2))

    def test_game_switch_player(self):
        game = Game(8)
        game.switch_player()
        self.assertEqual(game.who_plays, game.player_2)

    def test_game_get_north_flip(self):
        game = Game(8)
        player1 = Player('black')
        game.get_north_flip(player1, 2, 3)
        self.assertEqual(game.othello.board_list[3][3], 'black')

    def test_game_get_south_flip(self):
        game = Game(8)
        player1 = Player('black')
        game.get_south_flip(player1, 5, 4)
        self.assertEqual(game.othello.board_list[4][4], 'black')

    def test_game_get_east_flip(self):
        game = Game(8)
        player1 = Player('black')
        game.get_east_flip(player1, 4, 5)
        self.assertEqual(game.othello.board_list[4][4], 'black')

    def test_game_get_west_flip(self):
        game = Game(8)
        player1 = Player('black')
        game.get_west_flip(player1, 3, 2)
        self.assertEqual(game.othello.board_list[3][3], 'black')

    def test_game_get_northwest_flip(self):
        game = Game(8)
        player1 = Player('black')
        game.othello.board_list[4][4] = 'black'
        game.get_northwest_flip(player1, 2, 2)
        self.assertEqual(game.othello.board_list[3][3], 'black')

    def test_game_get_northeast_flip(self):
        game = Game(8)
        player1 = Player('black')
        game.othello.board_list[3][4] = 'white'
        game.get_northeast_flip(player1, 2, 5)
        self.assertEqual(game.othello.board_list[3][4], 'black')

    def test_game_get_southeast_flip(self):
        game = Game(8)
        player1 = Player('white')
        game.othello.board_list[4][4] = 'black'
        game.get_southeast_flip(player1, 5, 5)
        self.assertEqual(game.othello.board_list[4][4], 'white')

    def test_game_et_southwest_flip(self):
        game = Game(8)
        player1 = Player('white')
        game.othello.board_list[3][4] = 'white'
        game.get_southwest_flip(player1, 5, 2)
        self.assertEqual(game.othello.board_list[4][3], 'white')

    def test_game_init_basic(self):
        game = Game(8, 'AI')
        self.assertEqual(game.board, Board(8))
        self.assertEqual(game.othello.game, game)
        self.assertEqual(game.othello, Othello(8))
        self.assertEqual(game.player_1, Player("black"))
        self.assertEqual(game.player_2, Player("white"))
        self.assertEqual(game.who_plays, game.player_1)
        self.assertEqual(game.size, 8)
        self.assertEqual(game.best_move_x, None)
        self.assertEqual(game.best_move_y, None)
        self.assertEqual(game.mode, 'AI')
        self.assertEqual(game.northwest_flip_num, 0)
        self.assertEqual(game.southwest_flip_num, 0)
        self.assertEqual(game.northeast_flip_num, 0)
        self.assertEqual(game.southeast_flip_num, 0)
        self.assertEqual(game.north_flip_num, 0)
        self.assertEqual(game.west_flip_num, 0)
        self.assertEqual(game.south_flip_num, 0)
        self.assertEqual(game.east_flip_num, 0)

    def test_game_get_AI_move(self):
        game = Game(8)
        game.othello.board_list[2][4] = 'black'
        self.assertEqual(game.get_AI_move(), (1, 4))

    def test_in_corner_true(self):
        game = Game(8)
        x_idx = 0
        y_idx = 0
        self.assertTrue(game.in_corner(x_idx, y_idx))

    def test_in_corner_false(self):
        game = Game(8)
        x_idx = 0
        y_idx = 4
        self.assertFalse(game.in_corner(x_idx, y_idx))

    def test_on_edge_true(self):
        game = Game(8)
        x_idx = 0
        y_idx = 4
        self.assertTrue(game.on_edge(x_idx, y_idx))

    def test_on_edge_false(self):
        game = Game(8)
        x_idx = 4
        y_idx = 4
        self.assertFalse(game.on_edge(x_idx, y_idx))

    def test_game_get_south_flip_num(self):
        game = Game(8)
        x_idx = 5
        y_idx = 3
        self.assertEqual(game.get_south_flip_num(game.player_2, x_idx, y_idx), 1)

    def test_game_get_north_flip_num(self):
        game = Game(8)
        x_idx = 2
        y_idx = 4
        self.assertEqual(game.get_north_flip_num(game.player_2, x_idx, y_idx), 1)

    def test_game_get_east_flip_num(self):
        game = Game(8)
        x_idx = 3
        y_idx = 5
        self.assertEqual(game.get_east_flip_num(game.player_2, x_idx, y_idx), 1)

    def test_game_get_west_flip_num(self):
        game = Game(8)
        x_idx = 4
        y_idx = 2
        self.assertEqual(game.get_west_flip_num(game.player_2, x_idx, y_idx), 1)

    def test_game_get_northwest_flip_num(self):
        game = Game(8)
        game.othello.board_list[3][3] = 'black'
        game.othello.board_list[4][4] = 'black'
        game.othello.board_list[5][5] = 'white'
        x_idx = 2
        y_idx = 2
        self.assertEqual(game.get_northwest_flip_num(game.player_2, x_idx, y_idx), 2)

    def test_game_get_northeast_flip_num(self):
        game = Game(8)
        game.othello.board_list[5][2] = 'white'
        x_idx = 2
        y_idx = 5
        self.assertEqual(game.get_northeast_flip_num(game.player_2, x_idx, y_idx), 2)

    def test_game_get_southwest_flip_num(self):
        game = Game(8)
        game.othello.board_list[2][5] = 'white'
        x_idx = 5
        y_idx = 2
        self.assertEqual(game.get_southwest_flip_num(game.player_2, x_idx, y_idx), 2)

    def test_game_get_southeast_flip_num(self):
        game = Game(8)
        game.othello.board_list[3][3] = 'black'
        game.othello.board_list[4][4] = 'black'
        game.othello.board_list[2][2] = 'white'
        x_idx = 5
        y_idx = 5
        self.assertEqual(game.get_southeast_flip_num(game.player_2, x_idx, y_idx), 2)

    def test_othello_save_score(self):
        """
        Please notice that this test only work when there is no 'scores.txt' file or there is nothing in the
        'scores.txt' file. It would test whether the function of save_score() in Othello can work well when writing
        a record in the file.
        :return: nothing
        """
        othello1 = Othello(8)
        othello1.name = 'David'
        othello1.score = 4
        othello1.save_score()
        self.assertTrue(othello1.test_write_to_file('scores.txt', 'David 4\n'))


def main():
    unittest.main(verbosity = 3)


if __name__ == '__main__':
    main()
