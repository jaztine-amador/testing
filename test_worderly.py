""" Importing Functions from Local Files """
from game_logic import grid_puzzle_generator
from game_logic import main_and_valid_words
from game_logic import select_main_word
from game_logic import get_all_valid_words
from game_logic import is_valid_word
from game_logic import grid_puzzle_builder
from game_logic import base_grid_builder
from game_logic import cells_for_main_diagonal
from game_logic import can_intersect_horizontal
from game_logic import horizontal_cells
from game_logic import valid_intersection_buffers_horizontal
from game_logic import can_intersect_vertical
from game_logic import vertical_cells
from game_logic import valid_intersection_buffers_vertical
from game_logic import is_valid_grid
from game_logic import all_cells
from game_logic import hide_words
from game_logic import is_valid_guess
from game_logic import cells_containing_word
from game_logic import points_updater
from game_logic import is_the_main_word
from game_logic import at_main_diagonal

""" Importing Python Modules """
import random

# As a valid parameter, we use STREAK which is given in the Project Specs.
main_word = "streak"

# List of possible main words with "streak" included.
another_list_of_words = ["streak", "dog", "cat", "everything", "zebra"]

# Below are all valid words of the main word: "streak".
valid_words = [
    'are', 'ark', 'arks', 'art', 'arts', 'ask', 'aster', 'ate', 'ear', 'ears',
    'east', 'eat', 'eats', 'era', 'eras', 'erst', 'est', 'eta', 'karst', 'rake',
    'rakes', 'rat', 'rate', 'rates', 'rats', 'rest', 'sake', 'sat', 'sea', 'sear',
    'seat', 'set', 'skate', 'skater', 'stake', 'star', 'stare', 'stark', 'steak',
    'take', 'taker', 'takers', 'takes', 'tar', 'tares', 'tars', 'task', 'tea', 'teak',
    'tear', 'tears', 'teas', 'trek', 'treks']

# Proper initial grid with only the main horizontal word "streak".
initial_grid = [
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', 's', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', 't', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'r', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'e', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', 'a', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', 'k', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
'.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]

# Main diagonal cells where the main word will be placed.
main_diagonal_cells = [ (2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17) ]


def open_list_of_words():
    """ A function that gives us a copy of list of words.
    """
    with open("ac-permanent-lexicon.txt", encoding='utf-8') as game_levels_lexicon:
        list_of_words = game_levels_lexicon.read().split()

    # List of words from "ac-permanent-lexicon.txt".
    return list_of_words


list_of_words = open_list_of_words()

""" Note:
    This unit test handles only the specific word: "streak".
    We use the function: print(grid_puzzle_builder("streak", valid_words)[1]) for reference.
    We use the output value of this function to determine the valid guess as well as their cells.
    Result may vary if a different main word is used since this unit test is defined only for "streak".
"""


""" Unit Test for generating the puzzle's grid """


def test_grid_puzzle_generator():
    """ Function should return arguments (grid_puzzle, main_word, all_valid_guess) of length 3.
    """
    assert len(grid_puzzle_generator(list_of_words)) == 3


def test_main_and_valid_words():
    """ Function should return arguments (main_word, valid_words) of length 2.
    """
    assert len(main_and_valid_words(list_of_words)) == 2
    assert len(main_and_valid_words(list_of_words)[1]) >= 20


def test_select_main_word():
    """ Here, we use the parameter "streak".
        In a limited list of possible main words, we should return the word "streak".
        Given that it's the only valid main word out of all.
    """
    assert select_main_word(another_list_of_words) == "streak"
    assert select_main_word(another_list_of_words) != "dog"


def test_get_all_valid_words():
    """ Function that returns all valid words from the list of words.
        We use the main word: streak.
    """
    assert get_all_valid_words("streak", list_of_words) == valid_words


def test_is_valid_word():
    """ Function that tests if a selected word from list of words is a valid word.
    """
    i = random.randint(0, len(valid_words) - 1)
    assert is_valid_word("streak", valid_words[i]) == True
    assert is_valid_word("streak", "dog") == False
    assert is_valid_word("streak", "stream") == False


def test_grid_puzzle_builder():
    """ Function that checks if the grid puzzle and all valid guesses are returned.
        There should be at least 20 valid guesses.
        The grid's length shouldbe 15, meaning it has 15 rows (for it to become a valid grid).
    """

    # Test Case 1: The output should be of length 2: grid puzzle and all valid guess
    assert len(grid_puzzle_builder("streak", valid_words)) == 2

    # Test Case 2: All valid guess should have length greater than 20.
    assert len(grid_puzzle_builder("streak", valid_words)[1]) >= 20

    # Test Case 3: The grid puzzle should have length equal to 15 for it to become a valid grid.
    assert len(grid_puzzle_builder("streak", valid_words)[0]) == 15


def test_base_grid_builder():
    """ Function that tests if the initial grid with only the main word is properly made.
        We use a pre-made initial grid with only the horizontal main word for comparison.
    """

    """ Test Case: We check if the word "streak" is placed properly in the grid.
        The initial grid is pre-made sincee the horizontal word is fixed in a single position.
    """
    assert base_grid_builder("streak") == initial_grid


def test_cells_for_main_diagonal():
    """ Function that tests if a proper list of (coordinate, orientation) is returned.
    """

    """ We test for possible length of words in range(3, 7)
        As well as the main diagonal cells [ (2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17) ]
    """

    # Test Case A: We use increasing length of 3rd parameter [range(3, 7)].

        # Test Case 1: len(word) = 3
    assert len(cells_for_main_diagonal(2, 7, 3)) == 6

        # Test Case 2: len(word) = 4
    assert len(cells_for_main_diagonal(2, 7, 4)) == 7

        # Test Case 3: len(word) = 5
    assert len(cells_for_main_diagonal(2, 7, 5)) == 8

        # Test Case 4: len(word) = 6
    assert len(cells_for_main_diagonal(2, 7, 6)) == 9

    # Test Case B: We use different (i, j) pairs but same len(word). The length of cells should be the same.

        # Test Case 1: len(word) = 3 >> (2, 7) == (4, 9) == (6, 11) == (8, 13) == (10, 15) == (12, 17)
        # Every (i, j) pairs should yield the same length of cells.
    assert (len(cells_for_main_diagonal(2, 7, 3)) == len(cells_for_main_diagonal(4, 9, 3)) ==
            len(cells_for_main_diagonal(6, 11, 3)) == len(cells_for_main_diagonal(8, 13, 3)) ==
            len(cells_for_main_diagonal(10, 15, 3)) == len(cells_for_main_diagonal(12, 17, 3)))

        # Test Case 1: len(word) = 4
            # (2, 7) == (12, 17)
            # (4, 9) == (10, 15)
            # (6, 11) == (8, 13)
    assert (len(cells_for_main_diagonal(2, 7, 4)) == len(cells_for_main_diagonal(12, 17, 4)))
    assert (len(cells_for_main_diagonal(4, 9, 4)) == len(cells_for_main_diagonal(10, 15, 4)))
    assert (len(cells_for_main_diagonal(6, 11, 4)) == len(cells_for_main_diagonal(8, 13, 4)))

        # Test Case 1: len(word) = 5
            # (2, 7) == (12, 17)
            # (4, 9) == (10, 15)
            # (6, 11) == (8, 13)
    assert (len(cells_for_main_diagonal(2, 7, 5)) == len(cells_for_main_diagonal(12, 17, 5)))
    assert (len(cells_for_main_diagonal(4, 9, 5)) == len(cells_for_main_diagonal(10, 15, 5)))
    assert (len(cells_for_main_diagonal(6, 11, 5)) == len(cells_for_main_diagonal(8, 13, 5)))

        # Test Case 1: len(word) = 6
            # (2, 7) == (12, 17)
            # (4, 9) == (10, 15)
            # (6, 11) == (8, 13)
    assert (len(cells_for_main_diagonal(2, 7, 6)) == len(cells_for_main_diagonal(12, 17, 6)))
    assert (len(cells_for_main_diagonal(4, 9, 6)) == len(cells_for_main_diagonal(10, 15, 6)))
    assert (len(cells_for_main_diagonal(6, 11, 6)) == len(cells_for_main_diagonal(8, 13, 6)))


def test_can_intersect_horizontal():
    """ Function that tests if a given word can intersect horizontally to the grid.
    """

    """ We check for the word: "treks" if it can intersect horizontally in the initial grid.
        Initially, there is no other word placed in the grid except the main horizontal word.
    """
    # Test Case 1: It is True since the word fits in the grid and fits the main word horizontally.
    assert can_intersect_horizontal(initial_grid, "treks", 2, 3, [], [], main_diagonal_cells, [], []) == True
    # Test Case 2: False cases. Even though some are valid cells, it cannot fit the main word horizontally.
    assert can_intersect_horizontal(initial_grid, "treks", 2, 4, [], [], main_diagonal_cells, [], []) == False
    assert can_intersect_horizontal(initial_grid, "treks", 2, 5, [], [], main_diagonal_cells, [], []) == False
    assert can_intersect_horizontal(initial_grid, "treks", 2, 6, [], [], main_diagonal_cells, [], []) == False
    assert can_intersect_horizontal(initial_grid, "treks", 2, 7, [], [], main_diagonal_cells, [], []) == False


def test_horizontal_cells():
    """ Function that tests if a given input (i, j, len(word)) yields
        a list of tuples with length = len(word)
    """

    # Test Case 1: We test if it yields the correct (i, j) pairs.
    assert horizontal_cells(2, 3, 5) == [(2, 3), (2, 4), (2, 5), (2, 6), (2, 7)]

    # Test Case 2: Given an input of len(word), the output should have the same length as len(word).
    assert len(horizontal_cells(2, 3, 5)) == 5
    assert len(horizontal_cells(2, 2, 6)) == 6
    assert len(horizontal_cells(2, 4, 3)) == 3


def test_valid_intersection_buffers_horizontal():
    """ Function that checks if there's a buffer before placing a word horizontally.
    """

    # Test Case 1: (i, j, len(word)) = (2, 3, 5) and the grid is empty except the main horizontal.
    cells = horizontal_cells(2, 3, 5)
    assert valid_intersection_buffers_horizontal(cells, [], [], main_diagonal_cells, [], []) == True


def test_can_intersect_vertical():
    """ Function that tests if a given word can intersect vertically to the grid.
    """

    """ We check for the word: "treks" if it can intersect vertically in the initial grid.
        Initially, there is no other word placed in the grid except the main horizontal word.
    """
    # Test Case 1: It is True since the word fits in the grid and fits the main word vertically.
    assert can_intersect_vertical(initial_grid, "treks", 4, 9, [], [], main_diagonal_cells, [], []) == True

    # Test Case 2: False cases. Even though the (i, j) pairs are valid cells, it cannot fit the main word vertically.
    assert can_intersect_vertical(initial_grid, "treks", 0, 7, [], [], main_diagonal_cells, [], []) == False
    assert can_intersect_vertical(initial_grid, "treks", 1, 7, [], [], main_diagonal_cells, [], []) == False
    assert can_intersect_vertical(initial_grid, "treks", 2, 7, [], [], main_diagonal_cells, [], []) == False
    assert can_intersect_vertical(initial_grid, "treks", 2, 5, [], [], main_diagonal_cells, [], []) == False


def test_vertical_cells():
    """ Function that tests if a given input (i, j, len(word)) yields
        a list of tuples with length = len(word)
    """

    # Test Case 1: We test if it yields the correct (i, j) pairs.
    assert vertical_cells(0, 7, 5) == [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7)]

    # Test Case 2: Given an input of len(word), the output should have the same length as len(word).
    assert len(vertical_cells(0, 7, 5)) == 5
    assert len(vertical_cells(1, 7, 6)) == 6
    assert len(vertical_cells(2, 7, 3)) == 3


def test_valid_intersection_buffers_vertical():
    """ Function that checks if there's a buffer before placing a word vertically.
    """

    # Test Case 1: (i, j, len(word)) = (4, 9, 5) and the grid is empty except the main horizontal.
    cells = horizontal_cells(4, 9, 5)
    assert valid_intersection_buffers_horizontal(cells, [], [], main_diagonal_cells, [], []) == True


def test_is_valid_grid():
    """ Function that checks if the grid puzzle built by the function: grid_puzzle_builder
        is a valid grid.
        A valid grid implies that there are at least 20 words placed properly in the grid.
    """

    assert is_valid_grid(grid_puzzle_builder("streak", valid_words)[1]) == True


def test_all_cells():
    """ Function that checks if a proper tuple is returned when called.
        Each input of len(word) has a specific returned value (length of tuple returned).
    """

    assert len(all_cells(6)) == 200
    assert len(all_cells(5)) == 231
    assert len(all_cells(4)) == 264
    assert len(all_cells(3)) == 299
    

def test_hide_words():
    """ Function that checks if the words in the grid are hidden before playing.
    """

    i = random.randint(0, 14)
    j = random.randint(0, 5)
    ch = "streak"

    # Test Case 1: "#" should be present in every main diagonal row.
    assert ("#" in (hide_words(grid_puzzle_builder("streak", valid_words)[0]))[2])
    assert ("#" in (hide_words(grid_puzzle_builder("streak", valid_words)[0]))[4])
    assert ("#" in (hide_words(grid_puzzle_builder("streak", valid_words)[0]))[6])
    assert ("#" in (hide_words(grid_puzzle_builder("streak", valid_words)[0]))[8])
    assert ("#" in (hide_words(grid_puzzle_builder("streak", valid_words)[0]))[10])
    assert ("#" in (hide_words(grid_puzzle_builder("streak", valid_words)[0]))[12])

    # Test Case 2: The characters of the word "streak" should not be in the grid (should be replaced by "#").
    assert (ch[j] not in (hide_words(grid_puzzle_builder("streak", valid_words)[0]))[i])
    

def test_is_valid_guess():
    """ Function that checks if a guess is a valid guess.
    """
    assert is_valid_guess("dog", grid_puzzle_builder("streak", valid_words)[1], set(), main_diagonal_cells) == False
    assert is_valid_guess("treks", grid_puzzle_builder("streak", valid_words)[1], set(), main_diagonal_cells) == True
    assert is_valid_guess("trek", grid_puzzle_builder("streak", valid_words)[1], set(), main_diagonal_cells) == True


def test_cells_containing_word():
    """ Function that checks if the cells of a valid grid is returned correctly.
        It should be a set with len = len(guess).
    """

    """ Each cells containing word should have the length = len(guess).
        This is because it reveals the coordinate where each letter is placed.
    """

    assert len(cells_containing_word(grid_puzzle_builder("streak", valid_words)[1]["treks"], 5, main_diagonal_cells)) == 5
    assert len(cells_containing_word(grid_puzzle_builder("streak", valid_words)[1]["trek"], 4, main_diagonal_cells)) == 4


def test_points_updater():
    """ Function that checks if the points are updated correctly every valid guess.
    """

    # Test Case 1: First guess (No cells are revealed yet).
    assert points_updater(cells_containing_word(grid_puzzle_builder("streak", valid_words)[1]["treks"], 5, main_diagonal_cells), set()) == 5

    # Test Case 2: "treks" is already revealed. "tares" should overlap it vertically.
    first_guess = cells_containing_word(grid_puzzle_builder("streak", valid_words)[1]["treks"], 5, main_diagonal_cells)
    assert points_updater(cells_containing_word(grid_puzzle_builder("streak", valid_words)[1]["tares"], 5, main_diagonal_cells), first_guess) == 4


def test_is_the_main_word():
    """ Function that checks if the main word guess is handled correctly.
    """

    """ Take note that our main word is "streaks".
        If guess is the same, it should return True, else False.
    """
    assert is_the_main_word("streak", main_word) == True
    assert is_the_main_word("strek", main_word) == False
    assert is_the_main_word("str3ak", main_word) == False
    assert is_the_main_word("streaks", main_word) == False


def test_at_main_diagonal():
    """ Function that checks if the (i, j) of a character is in the main_diagonal.
    """

    # Test Case 1: The character "s" of "treks" should be at the main diagonal.
    assert at_main_diagonal(2, 7, main_diagonal_cells) == True

    # Test Case 2: The character "k" of "treks" is not at the main diagonal.
    assert at_main_diagonal(2, 6, main_diagonal_cells) == False
