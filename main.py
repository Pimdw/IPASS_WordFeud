import random
import algorithm, application
import csv

def play_game():
    # Run this once to make it.
    # algorithm.make_and_save_DAWG_reversed_DAWG()

    root, reversed_root = algorithm.load_DAWG_reversed_DAWG()
    # Create empty board
    board = application.initialize_game_board()

    # Create a tile_bag that has all the tiles with their respective amount
    tile_bag = application.initialize_game_tile_bag()

    # square_multiplier used for terminal colouring
    letter_point, square_multiplier = application.game_scores()

    # Assign 7 random tiles to a player's rack and remove them from the tile_bag
    rack_player1, rack_player2, tile_bag = application.initialize_game_rack(tile_bag)

    helper = int(input("Want to autoplay (0) the game or on helper (1) function? "))
    if helper:
        start_player_or_not = int(input("Are you the start player, yes(1), no(2): "))
        vs_other_player = int(input("Versus other player?: yes(1), no(0): "))

    selected_algorithm = str(input("Type 'greedy' or 'random'"))
    # selected_algorithm = 'greedy'

    current_player = 1

    current_rack = rack_player1
    
    player1_total_score = 0
    player2_total_score = 0

    player1_list_of_moves = []
    player2_list_of_moves = []

    # Main game loop
    game_is_on = True
    no_moves_found = 0
    while game_is_on:
        print(f"Player {current_player}'s turn.")
        print("Remaining tiles in bag:", len(tile_bag))
        print("Current rack:", current_rack)

        all_moves = application.move_generation(board, root, reversed_root, current_rack)

        if all_moves:
            no_moves_found = 0
            # Loops through all the moves, assigns a score to the word played by the move and adds them all to all_scores
            all_scores = application.moves_score_is_transposed(all_moves)

            # Different condition to get certain configurations
            if helper and current_player == start_player_or_not:
                best_move, best_move_word, best_move_score, best_move_side, best_move_is_transposed = application.helper(board, square_multiplier, selected_algorithm, all_scores)

            if helper and vs_other_player and current_player != start_player_or_not:
                best_move, best_move_word, best_move_score, best_move_side, best_move_is_transposed = application.manual_input(board, square_multiplier, all_scores)

            if not helper or (helper and current_player != start_player_or_not and not vs_other_player):
                best_move, best_move_word, best_move_score, best_move_side, best_move_is_transposed = application.computer(selected_algorithm, all_scores)


            board, tile_bag, player1_total_score, player1_list_of_moves, player2_total_score, player2_list_of_moves, current_rack, current_player = application.place_move_print_board_player_management(board, best_move_is_transposed, best_move, best_move_word, square_multiplier, best_move_score, best_move_side, tile_bag, player1_total_score, player1_list_of_moves, player2_total_score, player2_list_of_moves, rack_player1, rack_player2, current_rack, current_player)
        else:
            no_moves_found += 1
            if no_moves_found == 2:
                game_is_on = False
                print("No moves found")

    print(f"Player1 words played: {player1_list_of_moves}")
    print(f"Player2 words played: {player2_list_of_moves}")

    if player1_total_score > player2_total_score:
        winner = 'Player1'
        print(f"Player1 wins!")
    elif player1_total_score == player2_total_score:
        winner = 'Draw'
        print(f"It's a draw!")
    else:
        winner = 'Player2'
        print(f"Player2 wins!")
    
    return player1_total_score, player1_list_of_moves, player2_total_score, player2_list_of_moves, winner


if __name__ == '__main__':

    player1_total_score, player1_list_of_moves, player2_total_score, player2_list_of_moves, winner = play_game()
