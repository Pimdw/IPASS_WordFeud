import random
import colorama
colorama.init(autoreset=True)
from colorama import Fore, Back, Style
import algorithm

def transpose_board_counterclockwise(board):
    """
    Transposes a 2D board array counterclockwise.

    Parameters:
    - board (list of lists): A 2D list representing a board where each sublist is a row.

    Returns:
    - list of lists: The transposed board after rotating it counterclockwise.
    """
    transposed_board = [[board[j][i] for j in range(len(board))] for i in range(len(board[0])-1, -1, -1)]
    return transposed_board

def transpose_board_clockwise(board):
    """
    Transposes a 2D board array clockwise.

    Parameters:
    - board (list of lists): A 2D list representing a board where each sublist is a row.

    Returns:
    - list of lists: The transposed board after rotating it clockwise.
    """
    transposed_board = [[board[j][i] for j in range(len(board)-1, -1, -1)] for i in range(len(board[0]))]
    return transposed_board

def game_scores():
    """
    Defines the point values for each letter used in the game and the score multipliers for specific board positions.

    Returns:
    - tuple:
        - letter_point (dict): Dictionary where keys are letters (str) and values are their corresponding point values (int).
        - square_multiplier (dict): Dictionary mapping board positions (tuple of (row, col)) to score multipliers (str),
          indicating special scoring tiles on the board ('2L' for double letter score, '3L' for triple letter score, 
          '2W' for double word score, and '3W' for triple word score).
    """
    letter_point = {
                    "A": 1, "B": 4, "C": 5, "D": 2,
                    "E": 1, "F": 4, "G": 3, "H": 4,
                    "I": 2, "J": 4, "K": 3, "L": 3,
                    "M": 3, "N": 1, "O": 1, "P": 4,
                    "Q": 10, "R": 2, "S": 2, "T": 2,
                    "U": 2, "V": 4, "W": 5, "X": 8,
                    "Y": 8, "Z": 5
                }
    
    square_multiplier = { 
                    (0, 0): '3L', (0, 1): '', (0, 2): '', (0, 3): '', (0, 4): '3W', (0, 5): '', (0, 6): '', (0, 7): '2L', (0, 8): '', (0, 9): '', (0, 10): '3W', (0, 11): '', (0, 12): '', (0, 13): '', (0, 14): '3L', 
                    (1, 0): '', (1, 1): '2L', (1, 2): '', (1, 3): '', (1, 4): '', (1, 5): '3L', (1, 6): '', (1, 7): '', (1, 8): '', (1, 9): '3L', (1, 10): '', (1, 11): '', (1, 12): '', (1, 13): '2L', (1, 14): '', 
                    (2, 0): '', (2, 1): '', (2, 2): '2W', (2, 3): '', (2, 4): '', (2, 5): '', (2, 6): '2L', (2, 7): '', (2, 8): '2L', (2, 9): '', (2, 10): '', (2, 11): '', (2, 12): '2W', (2, 13): '', (2, 14): '', 
                    (3, 0): '', (3, 1): '', (3, 2): '', (3, 3): '3L', (3, 4): '', (3, 5): '', (3, 6): '', (3, 7): '2W', (3, 8): '', (3, 9): '', (3, 10): '', (3, 11): '3L', (3, 12): '', (3, 13): '', (3, 14): '', 
                    (4, 0): '3W', (4, 1): '', (4, 2): '', (4, 3): '', (4, 4): '2W', (4, 5): '', (4, 6): '2L', (4, 7): '', (4, 8): '2L', (4, 9): '', (4, 10): '2W', (4, 11): '', (4, 12): '', (4, 13): '', (4, 14): '3W', 
                    (5, 0): '', (5, 1): '3L', (5, 2): '', (5, 3): '', (5, 4): '', (5, 5): '3L', (5, 6): '', (5, 7): '', (5, 8): '', (5, 9): '3L', (5, 10): '', (5, 11): '', (5, 12): '', (5, 13): '3L', (5, 14): '', 
                    (6, 0): '', (6, 1): '', (6, 2): '2L', (6, 3): '', (6, 4): '2L', (6, 5): '', (6, 6): '', (6, 7): '', (6, 8): '', (6, 9): '', (6, 10): '2L', (6, 11): '', (6, 12): '2L', (6, 13): '', (6, 14): '', 
                    (7, 0): '2L', (7, 1): '', (7, 2): '', (7, 3): '2W', (7, 4): '', (7, 5): '', (7, 6): '', (7, 7): '', (7, 8): '', (7, 9): '', (7, 10): '', (7, 11): '2W', (7, 12): '', (7, 13): '', (7, 14): '2L', 
                    (8, 0): '', (8, 1): '', (8, 2): '2L', (8, 3): '', (8, 4): '2L', (8, 5): '', (8, 6): '', (8, 7): '', (8, 8): '', (8, 9): '', (8, 10): '2L', (8, 11): '', (8, 12): '2L', (8, 13): '', (8, 14): '', 
                    (9, 0): '', (9, 1): '3L', (9, 2): '', (9, 3): '', (9, 4): '', (9, 5): '3L', (9, 6): '', (9, 7): '', (9, 8): '', (9, 9): '3L', (9, 10): '', (9, 11): '', (9, 12): '', (9, 13): '3L', (9, 14): '', 
                    (10, 0): '3W', (10, 1): '', (10, 2): '', (10, 3): '', (10, 4): '2W', (10, 5): '', (10, 6): '2L', (10, 7): '', (10, 8): '2L', (10, 9): '', (10, 10): '2W', (10, 11): '', (10, 12): '', (10, 13): '', (10, 14): '3W', 
                    (11, 0): '', (11, 1): '', (11, 2): '', (11, 3): '3L', (11, 4): '', (11, 5): '', (11, 6): '', (11, 7): '2W', (11, 8): '', (11, 9): '', (11, 10): '', (11, 11): '3L', (11, 12): '', (11, 13): '', (11, 14): '', 
                    (12, 0): '', (12, 1): '', (12, 2): '2W', (12, 3): '', (12, 4): '', (12, 5): '', (12, 6): '2L', (12, 7): '', (12, 8): '2L', (12, 9): '', (12, 10): '', (12, 11): '', (12, 12): '2W', (12, 13): '', (12, 14): '', 
                    (13, 0): '', (13, 1): '2L', (13, 2): '', (13, 3): '', (13, 4): '', (13, 5): '3L', (13, 6): '', (13, 7): '', (13, 8): '', (13, 9): '3L', (13, 10): '', (13, 11): '', (13, 12): '', (13, 13): '2L', (13, 14): '', 
                    (14, 0): '3L', (14, 1): '', (14, 2): '', (14, 3): '', (14, 4): '3W', (14, 5): '', (14, 6): '', (14, 7): '2L', (14, 8): '', (14, 9): '', (14, 10): '3W', (14, 11): '', (14, 12): '', (14, 13): '', (14, 14): '3L' 
                    }
    
    return letter_point, square_multiplier

def get_color(multiplier):
    if multiplier == '3L':
        return Back.BLUE + Fore.BLACK  # Blue background with white text for triple letter
    elif multiplier == '2L':
        return Back.CYAN + Fore.BLACK  # Light blue/cyan background for double letter
    elif multiplier == '3W':
        return Back.RED + Fore.BLACK  # Red background for triple word
    elif multiplier == '2W':
        return Back.MAGENTA + Fore.BLACK  # Yellow background for double word
    else:
        return Back.WHITE + Fore.BLACK

def print_board_with_colors(board, square_multiplier):
    for i in range(len(board)):
        for j in range(len(board[i])):
            multiplier = square_multiplier.get((i, j), '')
            color = get_color(multiplier)
            tile = f" {board[i][j]} " if board[i][j] != ' ' else ' . '
            print(color + f"{tile:^3}", end='')
        print()

def give_scores(move):
    """
    Calculates the total score for a move based on the letters used, their positions, and the multipliers applicable to those positions.

    Parameters:
    - move (tuple): A tuple representing a move, structured as (initial_part, extended_part, word, anchor, side).
                    Here, 'word' is the complete word formed, 'anchor' is the starting position (tuple of row and col),
                    and 'side' indicates the direction ('left' or 'right').

    Returns:
    - tuple: A tuple containing the original move and its calculated total score (int).
    """
    initial_part, extended_part, word, anchor, side = move
    letter_point, square_multiplier = game_scores()

    word_score = 0
    multiplier_letter_score = 0
    multiplier_word_score = 0

    start_row, start_col = anchor
    
    # Give points for letters in word
    for char in word:
        score = letter_point.get(char)
        word_score += score

    # Give points for multipliers
    if side == 'left':
        for i in range(len(extended_part)):
            col = start_col - i
            multiplier = square_multiplier.get((start_row, col))
            for char in extended_part[len(extended_part) - i - 1]:
                if multiplier == '2L':
                    score = letter_point.get(char)
                    multiplier_letter_score += score
                elif multiplier == '3L':
                    score = letter_point.get(char)
                    multiplier_word_score += score * 2
                elif multiplier == '2W':
                    multiplier_word_score += word_score
                elif multiplier == '3W':
                    multiplier_word_score += word_score * 2

    if side == 'right':
        for i in range(len(extended_part)):
            col = start_col + i
            multiplier = square_multiplier.get((start_row, col))
            for char in extended_part[i]:
                if multiplier == '2L':
                    score = letter_point.get(char)
                    multiplier_letter_score += score
                elif multiplier == '3L':
                    score = letter_point.get(char)
                    multiplier_word_score += score * 2
                elif multiplier == '2W':
                    multiplier_word_score += word_score
                elif multiplier == '3W':
                    multiplier_word_score += word_score * 2

    total_score = word_score + multiplier_letter_score + multiplier_word_score

    # Bonus points for using all rack letters
    if len(extended_part) == 7:
        total_score += 40

    return move, total_score

def get_best_move(all_scores, amount_of_best_moves):
    """
    Selects the best move from a list of scored moves, potentially picking randomly among ties for the highest score.

    Parameters:
    - all_scores (list of tuples): A list where each tuple contains a move's details and its score. 
      The structure is ((move_details, score), is_transposed).

    Returns:
    - tuple: The best move tuple containing the move's details and whether the board was transposed for this move.
    """
    # (move, score), is_transposed = all_scores
    # best_move_initial_part, best_move_extended_part, best_move_word, best_move_anchor, best_move_side = move
    if not all_scores:
        return []

    unique_moves = []
    seen_words = set()

    # Determine the highest score from all evaluated moves
    sorted_moves = sorted(all_scores, key=lambda score: score[0][1], reverse=True)
    # Needed to determine unique moves to retun as possible moves. Since all moves get added to all_scores which are transposed etc or not.
    if amount_of_best_moves > 1 and amount_of_best_moves < len(sorted_moves):
        for move in sorted_moves:
            best_move_word = move[0][0][2]
            best_move_side = move[0][0][4]
            if best_move_side == 'left':
                best_move_word = ''.join(reversed(best_move_word))
            if best_move_word not in seen_words:
                seen_words.add(best_move_word)
                unique_moves.append(move)
                if len(unique_moves) == amount_of_best_moves:
                    break
        return unique_moves
    else:
        best_move = sorted_moves

    return best_move

def update_board_with_best_move(board, best_move):
    """
    Updates the board with letters from the best move determined by game logic.

    Parameters:
    - board (list of lists): The board represented as a 15x15 grid of characters.
    - best_move (tuple): A tuple representing the best move, structured as (initial_part, extended_part, word, anchor, side),
                         where 'anchor' is the (row, col) starting position and 'side' indicates the direction of the word ('left' or 'right').

    Returns:
    - list of lists: The updated board with the new word added.
    """
    initial_part, extended_part, word, anchor, side = best_move

    start_row, start_col = anchor

    extended_index = 0

    # Place letters on the board depending on the direction of the move
    if side == 'left':
        # If placing leftwards, reverse the extended part to match the board's orientation
        distance_to_edge_left = start_col
        extended_part = ''.join(reversed(extended_part))
        for i in range(distance_to_edge_left):
            col = start_col - i
            # Ensure no overwriting of existing letters
            if board[start_row][col] == ' ' and extended_index < len(extended_part):
                board[start_row][col] = extended_part[extended_index]
                extended_index += 1
    else:
        distance_to_edge_right = 15 - start_col
        for i in range(distance_to_edge_right):
            col = start_col + i
            # Ensure no overwriting of existing letters
            if board[start_row][col] == ' ' and extended_index < len(extended_part):
                board[start_row][col] = extended_part[extended_index]
                extended_index += 1

    return board

def initialize_game_board():
    # Create an empty board
    board = [[' ' for _ in range(15)] for _ in range(15)]

    return board

def initialize_game_tile_bag():
    # Create a tile_bag that has all the tiles with their respective amount
    tile_bag = ["A"] * 7 + ["B"] * 2 + ["C"] * 2 + ["D"] * 5 + ["E"] * 18 + ["F"] * 2 + ["G"] * 3 + \
                ["H"] * 2 + ["I"] * 4 + ["J"] * 2 + ["K"] * 3 + ["L"] * 3 + ["M"] * 3 + ["N"] * 11 + \
                ["O"] * 6 + ["P"] * 2 + ["Q"] * 1 + ["R"] * 5 + ["S"] * 5 + ["T"] * 5 + ["U"] * 2 + \
                ["V"] * 2 + ["W"] * 2 + ["X"] * 1 + ["Y"] * 1 + ["Z"] * 2

    return tile_bag

def initialize_game_rack(tile_bag):
    # Assign 7 random tiles to a player's rack and remove them from the tile_bag
    rack_player1 = random.sample(tile_bag, 7)
    for letter in rack_player1:
        tile_bag.remove(letter)
    rack_player2 = random.sample(tile_bag, 7)
    for letter in rack_player2:
        tile_bag.remove(letter)

    return rack_player1, rack_player2, tile_bag

def move_generation(board, root, reversed_root, current_rack):
    # non transposed and transposed state
    board_states = [(board, False), (transpose_board_counterclockwise(board), True)]

    # Loops through the board states and adds all possible moves to the all_moves list
    all_moves = []
    for current_board, is_transposed in board_states:
        anchor_positions = algorithm.find_anchor_positions(current_board)
        cross_checks = algorithm.precompute_cross_checks(root, current_board)
        for anchor in anchor_positions:
            moves_right = algorithm.generate_word_right(anchor, current_rack, current_board, cross_checks, root)
            moves_left = algorithm.generate_word_left(anchor, current_rack, current_board, cross_checks, reversed_root)
            all_moves.extend([(move, is_transposed) for move in moves_right])
            all_moves.extend([(move, is_transposed) for move in moves_left]) 

    return all_moves

def moves_score_is_transposed(all_moves):
    all_scores = []
    for move, is_transposed in all_moves:
        move_with_total_score = give_scores(move)
        all_scores.append((move_with_total_score, is_transposed))
    return all_scores

def helper(board, square_multiplier, selected_algorithm, all_scores):
    print_board_with_colors(board, square_multiplier)
    amount_of_best_moves = int(input("How many best moves should it give: "))
    if selected_algorithm == 'greedy':
        best_scoring_move = get_best_move(all_scores, amount_of_best_moves) # Use this for the greedy algorithm
    if selected_algorithm == 'random':
        best_scoring_move = random.sample(all_scores, amount_of_best_moves) # Use this for random algorithm
    print(best_scoring_move)
    moves_range = min(amount_of_best_moves, len(best_scoring_move))
    
    for i in range(moves_range):
        # Unpack the best move for further use and statistics
        (best_move, best_move_score), best_move_is_transposed = best_scoring_move[i]
        best_move_initial_part, best_move_extended_part, best_move_word, best_move_anchor, best_move_side = best_move
        # Reverse the word from the reversed dawg for better readability
        if best_move_side == 'left':
            best_move_word = ''.join(reversed(best_move_word))
        print(f"All best scoring moves are: {i}, {best_move_word}, {best_move_score}")
    which_to_choose = int(input("Which word do you want to place: "))
    best_scoring_move = best_scoring_move[which_to_choose]
    # Unpack the best move for further use and statistics
    (best_move, best_move_score), best_move_is_transposed = best_scoring_move
    best_move_initial_part, best_move_extended_part, best_move_word, best_move_anchor, best_move_side = best_move

    return best_move, best_move_word, best_move_score, best_move_side, best_move_is_transposed

def manual_input(board, square_multiplier, all_scores):
    print_board_with_colors(board, square_multiplier)
    input_valid_word = True
    while input_valid_word:
    # all scores = [(((inital_part, extended part, word, anchor, side) score) is_transposed)]
        which_word_to_input = str(input("Which word to input: "))
        for score in all_scores:
            side = score[0][0][4]
            word = score[0][0][2]
            if side == 'left':
                word = ''.join(reversed(word))
            if which_word_to_input == word:
                input_valid_word = False
                best_scoring_move = score
        if input_valid_word:
            print("Input a valid word")
    (best_move, best_move_score), best_move_is_transposed = best_scoring_move
    best_move_initial_part, best_move_extended_part, best_move_word, best_move_anchor, best_move_side = best_move

    return best_move, best_move_word, best_move_score, best_move_side, best_move_is_transposed

def computer(selected_algorithm, all_scores):
    amount_of_best_moves = 1
    if selected_algorithm == 'greedy':
        best_scoring_move = get_best_move(all_scores, amount_of_best_moves)[0] # Use this for the greedy algorithm
    if selected_algorithm == 'random':      
        best_scoring_move = random.choice(all_scores) # Use this for random algorithm
    print(f"Best scoring move: {best_scoring_move}")

    # Unpack the best move for further use and statistics
    (best_move, best_move_score), best_move_is_transposed = best_scoring_move
    best_move_initial_part, best_move_extended_part, best_move_word, best_move_anchor, best_move_side = best_move

    return best_move, best_move_word, best_move_score, best_move_side, best_move_is_transposed

def place_move_print_board_player_management(board, best_move_is_transposed, best_move, best_move_word, square_multiplier, best_move_score, best_move_side, tile_bag, player1_total_score, player1_list_of_moves, player2_total_score, player2_list_of_moves, rack_player1, rack_player2, current_rack, current_player):    
    # Places a transposed move on the board
    if best_move_is_transposed:
        transposed_board = transpose_board_counterclockwise(board)
        transposed_board = update_board_with_best_move(transposed_board, best_move)
        board = transpose_board_clockwise(transposed_board)

    else:
        board = update_board_with_best_move(board, best_move)

    print_board_with_colors(board, square_multiplier)

    # Reverse the word from the reversed dawg for better readability
    if best_move_side == 'left':
        best_move_word = ''.join(reversed(best_move_word))
        
    if current_player == 1:
        player1_total_score += best_move_score
        player1_list_of_moves.append(best_move_word)
        print(f"Player1 score: {best_move_score}")
        print(f"Player1 total score: {player1_total_score}")
        print(f"Player1 word played: {best_move_word}")
        rack_player1 = algorithm.rack_manager(rack_player1, tile_bag, best_move)
        current_player = 2
        current_rack = rack_player2
    else:
        player2_total_score += best_move_score
        player2_list_of_moves.append(best_move_word)
        print(f"Player2 score: {best_move_score}")
        print(f"Player2 total score: {player2_total_score}")
        print(f"Player2 word played: {best_move_word}")
        rack_player2 = algorithm.rack_manager(rack_player2, tile_bag, best_move)
        current_player = 1
        current_rack = rack_player1
    print('---------------------------------------------')

    return board, tile_bag, player1_total_score, player1_list_of_moves, player2_total_score, player2_list_of_moves, current_rack, current_player