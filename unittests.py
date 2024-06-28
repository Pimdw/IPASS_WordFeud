from algorithm import create_node, insert, minimize, search_terminal_word, find_anchor_positions, precompute_cross_checks, is_cross_check_valid, collect_vertical_word, generate_word_left, collect_right_part_from_board, extend_left, generate_word_right, collect_left_part_from_board, extend_right, rack_manager
from application import transpose_board_counterclockwise, transpose_board_clockwise, game_scores, give_scores, get_best_move, update_board_with_best_move
import unittest

class TestScrabbleGame(unittest.TestCase):
    def setUp(self):
        self.root = create_node()
        self.reversed_root = create_node()

        words = ["cat", "cats", "car", "cars", "do", "dog", "dogs", "done", "ear", "ears", "eat", "eats", "ercat"]
        for word in words:
            word = word.upper()
            word = ''.join(reversed(word))
            insert(self.reversed_root, word)
        minimize(self.reversed_root)
        for word in words:
            word = word.upper()
            insert(self.root, word)
        minimize(self.root)

        self.rack = ['C', 'A', 'T', 'S', 'R', 'E', 'N']
        self.tile_bag = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        
        self.board =   [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', 'A', 'T', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        
        self.cross_checks = precompute_cross_checks(self.root, self.board)

    def test_insert_and_search(self):
        self.assertTrue(search_terminal_word(self.root, 'DOGS'))
        self.assertTrue(search_terminal_word(self.root, 'EARS'))
        self.assertFalse(search_terminal_word(self.root, 'NONE'))
        self.assertTrue(search_terminal_word(self.reversed_root, 'SRAE'))
        self.assertTrue(search_terminal_word(self.reversed_root, 'SRAE'))
        self.assertFalse(search_terminal_word(self.reversed_root, 'NONE'))

    def test_find_anchor_positions(self):
        anchors = find_anchor_positions(self.board)
        expected_anchors = [(6, 7), (6, 8), (6, 9), (7, 6), (7, 10), (8, 7), (8, 8), (8, 9)]
        self.assertEqual(sorted(anchors), sorted(expected_anchors))

    def test_precompute_cross_checks(self):
        cross_checks = precompute_cross_checks(self.root, self.board)
        self.assertEqual(cross_checks[(6, 7)], [])
        self.assertEqual(cross_checks[(6, 8)], [])
        self.assertEqual(cross_checks[(6, 9)], [])
        self.assertEqual(cross_checks[(7, 6)], ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
        self.assertEqual(cross_checks[(7, 10)], ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
        self.assertEqual(cross_checks[(8, 7)], [])
        self.assertEqual(cross_checks[(8, 8)], [])
        self.assertEqual(cross_checks[(8, 9)], [])

    def test_transpose_board_counterclockwise(self):
        transposed = transpose_board_counterclockwise(self.board)
        expected =     [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'A', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(transposed, expected)

    def test_transpose_board_clockwise(self):
        transposed = transpose_board_clockwise(self.board)
        expected =     [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'A', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(transposed, expected)

    def test_rack_manager_normal_case(self):
        # Test case where sufficient tiles are available
        best_move = ('CAT', 'S', 'CATS', (7, 7), 'right')
        expected_rack = ['C', 'A', 'T', 'R', 'E', 'N', 'A']
        updated_rack = rack_manager(self.rack.copy(), self.tile_bag.copy(), best_move)
        self.assertEqual(sorted(updated_rack), sorted(expected_rack))

    def test_rack_manager_insufficient_tiles(self):
        # Test case where there are not enough tiles in the bag
        tile_bag_small = ['X', 'Y']
        best_move = ('CAT', 'S', 'CATS', (7, 7), 'right')
        expected_rack = ['C', 'A', 'T', 'R', 'E', 'N', 'X']
        updated_rack = rack_manager(self.rack.copy(), tile_bag_small.copy(), best_move)
        self.assertEqual(sorted(updated_rack), sorted(expected_rack))

    def test_rack_manager_no_tiles_left(self):
        # Test case with no tiles left to replenish the rack
        tile_bag_empty = []
        best_move = ('CAT', 'S', 'CATS', (7, 7), 'right')
        expected_rack = ['C', 'A', 'T', 'R', 'E', 'N']
        updated_rack = rack_manager(self.rack.copy(), tile_bag_empty.copy(), best_move)
        self.assertEqual(sorted(updated_rack), sorted(expected_rack))

    def test_rack_manager_no_letters_used(self):
        # Test case where no letters are used from the rack
        best_move = ('', '', '', (7, 7), 'right')
        updated_rack = rack_manager(self.rack.copy(), self.tile_bag.copy(), best_move)
        self.assertEqual(sorted(updated_rack), sorted(self.rack))

    def test_generate_word_left(self):
        anchor = (7, 6)
        move = generate_word_left(anchor, self.rack, self.board, self.cross_checks, self.reversed_root)
        expected_moves = [('CAT', 'ER', 'TACRE', (7, 6), 'left')]
        self.assertEqual(expected_moves, move)

    def test_generate_word_right(self):
        anchor = (7, 10)
        move = generate_word_right(anchor, self.rack, self.board, self.cross_checks, self.root)
        expected_moves = [('CAT', 'S', 'CATS', (7, 10), 'right')]
        self.assertEqual(expected_moves, move)

    def test_word_give_scores(self):
        move = ('CAT', 'S', 'CATS', (7, 10), 'right')
        score = give_scores(move)
        expected_score = (('CAT', 'S', 'CATS', (7, 10), 'right'), 10)
        self.assertEqual(expected_score, score)
        move = ('CAT', 'S', 'STAC', (7, 10), 'left')
        score = give_scores(move)
        expected_score = (('CAT', 'S', 'STAC', (7, 10), 'left'), 10)
        self.assertEqual(expected_score, score)
    
    def test_multiplier_give_scores(self):
        move = ('', 'CATS', 'CATS', (11, 10), 'right')
        score = give_scores(move)
        expected_score = (('', 'CATS', 'CATS', (11, 10), 'right'), 12)
        self.assertEqual(expected_score, score)
        move = ('', 'STAC', 'STAC', (11, 13), 'left')
        score = give_scores(move)
        expected_score = (('', 'STAC', 'STAC', (11, 13), 'left'), 14)
        self.assertEqual(expected_score, score)

    def test_update_board(self):
        # Place the full word. No left part found
        best_move = ('', 'CATS', 'CATS', (11, 10), 'right')
        expected_board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', 'A', 'T', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', 'A', 'T', 'S', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        updated_board = update_board_with_best_move(self.board, best_move)
        self.assertEqual(expected_board, updated_board)
        # Only place the S since that's the extra part. It expects the 'CAT' to already be there.
        best_move = ('CAT', 'ES', 'SCAT', (2, 3), 'left')
        expected_board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', 'E', 'S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', 'A', 'T', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', 'A', 'T', 'S', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        updated_board = update_board_with_best_move(self.board, best_move)
        self.assertEqual(expected_board, updated_board)
# python -m unittest xxxxxunittests.py

if __name__ == '__main__':
    unittest.main()