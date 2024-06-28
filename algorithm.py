import pickle

def create_node(id_counter=[0]):
    """
    Creates a new node in a trie or Directed Acyclic Word Graph (DAWG) structure.

    Parameters:
    - id_counter (list of int, default=[0]): A list containing a single integer that acts as a unique identifier for each node created. This counter is incremented every time a new node is created.

    Returns:
    - dict: A new node represented as a dictionary with three keys:
        - 'children' (dict): An empty dictionary to hold child nodes.
        - 'is_terminal' (bool): A boolean flag indicating whether the node represents the end of a valid word in the trie.
        - 'id' (int): A unique identifier for the node.
    """
    id_counter[0] += 1
    return {
        'children': {},
        'is_terminal': False,
        'id': id_counter[0]
    }

def insert(root, word):
    """
    Inserts a word into the trie or DAWG rooted at the given node.

    Parameters:
    - root (dict): The root node of the trie or DAWG where the word will be inserted.
    - word (str): The word to be inserted into the trie.

    Returns:
    - None: This function modifies the trie in place by adding nodes for each character of the word if they do not already exist.
    """
    node = root
    for char in word:
        if char not in node['children']:
            node['children'][char] = create_node()
        node = node['children'][char]
    node['is_terminal'] = True

def minimize(node, nodes=None):
    """
    Minimizes a trie into a DAWG by merging equivalent nodes, which are nodes having the same children and terminal status.

    Parameters:
    - node (dict): The node from which to start the minimization process.
    - nodes (dict, optional): A dictionary used to keep track of nodes that have already been processed to facilitate node merging. If not provided, an empty dictionary is initialized.

    Returns:
    - tuple: A unique identifier for the node, used to check and manage node equivalency during the minimization process.
    """
    if nodes is None:
        nodes = {}
    if not node['children']:
        node_id = (node['is_terminal'],)
    else:
        child_tuples = []
        for char, next_node in sorted(node['children'].items()):
            minimized_child_id = minimize(next_node, nodes)
            child_tuples.append((char, minimized_child_id))
        node_id = (node['is_terminal'],) + tuple(child_tuples)

    if node_id in nodes:
        existing_node = nodes[node_id]
        node['children'] = existing_node['children']
        node['is_terminal'] = existing_node['is_terminal']
        node['id'] = existing_node['id']
    else:
        nodes[node_id] = node
    return node_id

def search_terminal_word(root, word):
    """
    Searches for a word in a trie and checks if it is a terminal word (i.e., a complete and valid word).

    Parameters:
    - root (dict): The root node of the trie.
    - word (str): The word to search for in the trie.

    Returns:
    - bool: True if the word exists in the trie and is marked as terminal, False otherwise.
    """
    node = root
    for char in word:
        if char in node['children']:
            node = node['children'][char]
        else:
            return False
    return node['is_terminal']

def find_anchor_positions(board):
    """
    Identifies and returns anchor positions. Anchor positions are empty spaces (' ')
    that are adjacent to any non-empty tile, which are potential starting points for placing new words.

    Parameters:
    - board (list of lists): A 2D list representing the board where each element is either a space (' ')
      indicating an empty tile or a character representing a letter tile.

    Returns:
    - list of tuples: A list containing the (row, col) coordinates of each anchor position on the board.
      If no anchors are found, it returns the center of the board (7, 7) as the default anchor position.
    """
    anchors = []
    for row in range(15):
        for col in range(15):
            if board[row][col] == ' ':
                if (row > 0 and board[row-1][col] != ' ') or \
                    (row < 14 and board[row+1][col] != ' ') or \
                    (col > 0 and board[row][col-1] != ' ') or \
                    (col < 14 and board[row][col+1] != ' '):
                    anchors.append((row, col))
    # Used when it's the start of the game
    if not anchors:
        return [(7, 7)]
    return anchors

def precompute_cross_checks(root, board):
    """
    Computes valid letters for each empty cell on the board that can potentially form valid words vertically.

    Parameters:
    - board (list of lists): A 15x15 grid representing the board, where each cell contains a letter or a space.

    Returns:
    - dict: A dictionary mapping (row, col) tuples of empty cells to a list of valid letters that can be placed there 
      based on vertical word formation.
    """
    cross_checks = {}
    for row in range(15):
        for col in range(15):
            if board[row][col] == ' ':
                valid_letters = set()
                for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    if is_cross_check_valid(root, letter, (row, col), board):
                        valid_letters.add(letter)
                cross_checks[(row, col)] = sorted(valid_letters)
    return cross_checks

def is_cross_check_valid(root, letter, anchor, board):
    """
    Checks if placing a letter at a specific board position is valid based on existing vertical words.

    Parameters:
    - letter (str): The letter to be placed on the board.
    - anchor (tuple): The (row, col) position on the board where the letter is to be placed.
    - board (list of lists): The board.

    Returns:
    - bool: True if placing the letter does not violate the rules by forming invalid vertical words, False otherwise.
    """
    row, col = anchor
    board[row][col] = letter
    valid = True
    if row > 0 and board[row - 1][col] != ' ':
        valid = valid and search_terminal_word(root, collect_vertical_word((row - 1, col), board))
    if row < 14 and board[row + 1][col] != ' ':
        valid = valid and search_terminal_word(root, collect_vertical_word((row + 1, col), board))
    board[row][col] = ' '
    return valid

def collect_vertical_word(anchor, board):
    """
    Collects a vertical word from the board starting from a given position and moving upwards and downwards 
    from that point until reaching a space.

    Parameters:
    - anchor (tuple): The starting (row, col) position on the board from which to collect the vertical word.
    - board (list of lists): The board.

    Returns:
    - str: The word collected vertically from the board around the specified anchor position.
    """
    row, col = anchor
    word = ""
    while row > 0 and board[row - 1][col] != ' ':
        row -= 1
    while row < 15 and board[row][col] != ' ':
        word += board[row][col]
        row += 1
    return word

def generate_word_left(anchor, rack, board, cross_checks, reversed_root):
    """
    Generates all possible leftward word extensions from a given anchor point using the letters in the player's rack.

    Parameters:
    - anchor (tuple): The (row, col) position on the board from which to extend words leftward.
    - rack (list of str): List of characters available to the player to form words.
    - board (list of lists): The board represented as a 15x15 grid of characters.
    - cross_checks (dict): Dictionary containing valid letters for each board position, precomputed for vertical words.

    Returns:
    - list of tuples: Each tuple contains details of a valid move including parts of the word before and after the anchor,
      the complete word formed, the original anchor, and the direction ('left').
    """
    moves = []  # Initialize a list to hold all valid moves
    right_part = collect_right_part_from_board(anchor, board)  # Collect contiguous letters to the right of the anchor
    start_node = reversed_root  # Starting point in the DAWG
    right_part = ''.join(reversed(right_part))
    if right_part:
        # Traverse the DAWG to the node matching the end of the right_part
        # print(right_part_start_node)
        for char in right_part:
            if char in start_node['children']:
                start_node = start_node['children'][char]
    # Call extend_left to recursively try building words to the left from the current node
    extend_left(reversed_root, right_part, right_part, "", start_node, anchor, anchor, rack, board, moves, cross_checks)
    return moves

def collect_right_part_from_board(anchor, board):
    """
    Collects contiguous letters to the right of a specified anchor point on the board until an empty space is encountered.

    Parameters:
    - anchor (tuple): The (row, col) position on the board from which to start collecting letters.
    - board (list of lists): The board represented as a 15x15 grid of characters.

    Returns:
    - str: A string composed of all consecutive letters to the right of the anchor point up to the first empty space.
    """
    row, col = anchor
    right_part = ""
    # Collect all contiguous letters to the right until an empty space
    while col + 1 < 15 and board[row][col + 1] != ' ':
        right_part += board[row][col + 1]
        col += 1
    return right_part

def extend_left(reversed_root, partial_word, initial_right_part, left_part, node, anchor, initial_anchor, rack, board, moves, cross_checks, used_from_rack=False):
    """
    Recursively extends a word to the left from a specified anchor point, using available letters in the rack, considering
    cross-check constraints for forming valid vertical words.

    Parameters:
    - partial_word (str): The word formed so far during recursion.
    - initial_right_part (str): The initial letters collected to the right of the anchor point.
    - left_part (str): The letters collected to the left of the anchor point during recursion.
    - node (dict): Current node in the DAWG representing the last letter of the left_part.
    - anchor (tuple): Current (row, col) position during recursion.
    - initial_anchor (tuple): Original (row, col) position from which leftward extension started.
    - rack (list of str): Remaining letters in the player's rack.
    - board (list of lists): The board.
    - moves (list of tuples): Accumulates valid moves found during recursion.
    - cross_checks (dict): Contains valid letters for each position for vertical compatibility.
    - used_from_rack (bool): Indicates if at least one letter from the rack has been used, ensuring move validity.

    Returns:
    - None: Modifies the moves list in-place by appending valid moves as they are found.
    """
    row, col = anchor

    # Return early if the column index goes out of board's left edge
    if col < 0:
        return

    if board[row][col] == ' ':
        # Check if a valid word is formed at the terminal node and add it to moves if it's not seen before
        if node['is_terminal'] and used_from_rack and search_terminal_word(reversed_root, partial_word):
            initial_right_part = ''.join(reversed(initial_right_part))
            moves.append((initial_right_part, left_part, partial_word, initial_anchor, 'left'))

        # Explore extending the word to the left using each letter in the rack
        for i, letter in enumerate(rack):
            if letter in node['children'] and letter in cross_checks[(row, col)]:
                new_rack = rack[:i] + rack[i+1:] # Create a new rack without the current letter
                new_left_part = letter + left_part # Add the current letter to the left part of the word
                # Recursive call to try extending further to the left
                extend_left(reversed_root, partial_word + letter, initial_right_part, new_left_part, node['children'][letter], (row, col - 1), initial_anchor, new_rack, board, moves, cross_checks, True)

def generate_word_right(anchor, rack, board, cross_checks, root):
    """
    Generates all possible rightward word extensions from a given anchor point using the letters in the player's rack.

    Parameters:
    - anchor (tuple): The (row, col) position on the board from which to extend words rightward.
    - rack (list of str): List of characters available to the player to form words.
    - board (list of lists): The board represented as a 15x15 grid of characters.
    - cross_checks (dict): Dictionary containing valid letters for each board position, precomputed for vertical words.

    Returns:
    - list of tuples: Each tuple contains details of a valid move including parts of the word before and after the anchor,
      the complete word formed, the original anchor, and the direction ('right').
    """
    moves = [] # Initialize a list to hold all valid moves
    left_part = collect_left_part_from_board(anchor, board) # Collect contiguous letters to the left of the anchor
    start_node = root # Starting point in the DAWG
    if left_part:
        # Traverse the trie to the node matching the end of the left_part
        for char in left_part:
            if char in start_node['children']:
                start_node = start_node['children'][char]
    # Call extend_right to recursively try building words to the right from the current node
    extend_right(root, left_part, left_part, "", start_node, anchor, anchor, rack, board, moves, cross_checks)
    return moves

def collect_left_part_from_board(anchor, board):
    """
    Collects contiguous letters to the left of a specified anchor point on the board until an empty space is encountered.

    Parameters:
    - anchor (tuple): The (row, col) position on the board from which to start collecting letters.
    - board (list of lists): The board represented as a 15x15 grid of characters.

    Returns:
    - str: A string composed of all consecutive letters to the left of the anchor point up to the first empty space.
    """
    row, col = anchor
    left_part = ""
    # Collect all contiguous letters to the left until an empty space
    while col > 0 and board[row][col - 1] != ' ':
        col -= 1
        left_part = board[row][col] + left_part
    return left_part

def extend_right(root, partial_word, initial_left_part, right_part, node, anchor, initial_anchor, rack, board, moves, cross_checks, used_from_rack=False):
    """
    Recursively extends a word to the right from a specified anchor point, using available letters in the rack, considering
    cross-check constraints for forming valid vertical words.

    Parameters:
    - partial_word (str): The word formed so far during recursion.
    - initial_left_part (str): The initial letters collected to the left of the anchor point.
    - right_part (str): The letters collected to the right of the anchor point during recursion.
    - node (dict): Current node in the trie representing the last letter of the right_part.
    - anchor (tuple): Current (row, col) position during recursion.
    - initial_anchor (tuple): Original (row, col) position from which rightward extension started.
    - rack (list of str): Remaining letters in the player's rack.
    - board (list of lists): The board.
    - moves (list of tuples): Accumulates valid moves found during recursion.
    - cross_checks (dict): Contains valid letters for each position for vertical compatibility.
    - used_from_rack (bool): Indicates if at least one letter from the rack has been used, ensuring move validity.

    Returns:
    - None: Modifies the moves list in-place by appending valid moves as they are found.
    """
    row, col = anchor

    # Return early if the column index goes out of board's right edge
    if col >= 15:
        return

    if board[row][col] == ' ':
        # Check if a valid word is formed at the terminal node and add it to moves
        if node['is_terminal'] and used_from_rack and search_terminal_word(root, partial_word):
            moves.append((initial_left_part, right_part, partial_word, initial_anchor, 'right'))

        for i, letter in enumerate(rack):
            if letter in node['children'] and letter in cross_checks[(row, col)]:
                new_rack = rack[:i] + rack[i+1:]
                new_right_part = right_part + letter
                extend_right(root, partial_word + letter, initial_left_part, new_right_part, node['children'][letter], (row, col + 1), initial_anchor, new_rack, board, moves, cross_checks, True)

def rack_manager(rack, tile_bag, best_move):
    """
    Manages the player's rack by removing letters used in the best move and replenishing it from the tile bag.

    Parameters:
    - rack (list of str): The current set of letters available to the player.
    - tile_bag (list of str): The remaining pool of letters available to draw from.
    - best_move (tuple): The best move made, containing details about the move including the letters used.

    Returns:
    - list of str: The updated rack after the move has been made and new letters (if any) have been drawn.
    """
    initial_part, extended_part, word, anchor, side = best_move

    # Remove letters used in the move from the rack
    for letter in extended_part:
        if letter in rack:
            rack.remove(letter)

    # Determine the number of new tiles needed and if tiles are available in the bag
    add_to_rack = len(extended_part)
    if add_to_rack > 0 and len(tile_bag) > 0:
        if len(tile_bag) >= add_to_rack:
            # new_tiles = random.sample(tile_bag, add_to_rack) # For normal program
            new_tiles = tile_bag[:add_to_rack] # for test case, removing the randomness
        else:
            new_tiles = tile_bag[:]

        # Add new tiles to the rack and remove them from the tile bag
        rack.extend(new_tiles)
        for tile in new_tiles:
            tile_bag.remove(tile)

    return rack

def save_dawg(dawg, filename):
    """
    Saves a Directed Acyclic Word Graph (DAWG) to a file using Python's pickle module.

    Parameters:
    - dawg (object): The DAWG object.
    - filename (str): The path and name of the file where the DAWG should be saved.

    Returns:
    - None: This function performs file I/O and does not return a value.
    """
    with open(filename, 'wb') as f:
        pickle.dump(dawg, f)

def load_dawg(filename):
    """
    Loads a Directed Acyclic Word Graph (DAWG) from a file using Python's pickle module.

    Parameters:
    - filename (str): The path and name of the file from which the DAWG should be loaded.

    Returns:
    - object: The deserialized DAWG object loaded from the specified file.
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)
    
def make_and_save_DAWG_reversed_DAWG():
    # Initialize roots
    root = create_node()
    reversed_root = create_node()

    # Read lexicon file
    with open("lexicon/Collins Scrabble Words (2019).txt", "r") as file:
        list_to_add_to_DAWG = file.readlines()

    # Insert words and their reversed versions into DAWGs
    for word in list_to_add_to_DAWG:
        if len(word) <= 9:
            word = word.strip("\n")
            word = word.upper()
            insert(root, word)
            reversed_word = reversed(word)
            insert(reversed_root, reversed_word)

    # Minimize the DAWGs to reduce redundancy and save memory
    minimize(root)
    minimize(reversed_root)

    # Save the DAWGs to files
    save_dawg(root, 'DAWG/root_dawg.pkl')
    save_dawg(reversed_root, 'DAWG/reversed_root_dawg.pkl')

    file.close()

def load_DAWG_reversed_DAWG():
    # # Load the root and reversed_root 
    root = load_dawg('DAWG/root_dawg.pkl')
    reversed_root = load_dawg('DAWG/reversed_root_dawg.pkl')

    return root, reversed_root