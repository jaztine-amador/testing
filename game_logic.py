""" Importing Python Modules """
import random
import time
from termcolor import cprint, colored
from dataclasses import dataclass
from enum import Enum

""" Importing Function from Local Files """
from utilities import clear_screen


""" ==================================================================== """
"""                          MAIN GAME FUNCTIONS                         """


@dataclass
class GameLevel(Enum):
    Apprentice = 20
    Scholar = 15
    Sorcerer = 10
    Master = 5
    Elder = 3


class WorderlyMap:

    def __init__(self, list_of_words: list[str], lives: int) -> None:

        self.grid_puzzle, self.main_word, self.all_valid_guess = grid_puzzle_generator(list_of_words)
        self.all_revealed_cells = initialize_empty_set()
        self.main_diagonal_cells = ((2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17))

        self.letters = self.shuffle_letters(self.main_word)

        self.lives = lives
        self.points = 0
        self.last_guess = None

        super().__init__()


    def hide_words(self):
        """ A method for hiding / concealing the words in the
            puzzle grid.
        """

        for i in range(15):
            for j in range(25):
                if self.grid_puzzle[i][j] != ".":
                    self.grid_puzzle[i][j] = "#"

    def shuffle_letters(self, letters):
        """ A method for shuffling the letters of the main word.
            This feature allows the player to have an aide in
            making guesses given the set of letters.
        """

        res = []

        for i in range(3):
            res.extend([letters[i], letters[i+3]])

        return "".join(res)


    def not_all_revealed(self):
        """ A method for determining whether there are still
            hidden word/s in the puzzle grid. This is utilized to
            determine whether the game will continue or not.
        """

        for row in self.grid_puzzle:
            if "#" in row:
                return True

        return False



    def display_game_state(self):
        """ A method for displaying the latest game state, showing the
            updated puzzle grid, letters, lives left, points, and the
            last guess that the player have made.
        """

        cprint( "="*55, "white" )
        cprint( "Welcome to Wizards of Worderly Place!".center(55, " "), "yellow")
        cprint( "="*55, "white")
        cprint( "")

        for row in self.grid_puzzle:
            print( " ".join(row).center(55, " ").replace(".", " ") )

        cprint( "")
        cprint( "="*55, "white")

        print( colored("    🔤 Letters:", "blue"), " ".join(self.letters.upper()))
        print( colored("    💚 Lives Left:", "green"), self.lives)
        print( colored("    🌟 Points:", "yellow"), self.points)
        print( colored("    ❓ Last Guess:", "red"), self.last_guess)

        cprint( "="*55, "white")


    def has_valid_guess(self, guess):
        """ A function for determining whether the player's guess is
            valid, that is it belongs to the set of all valid guess.
            This functions returns a boolean.
        """

        if guess in self.all_valid_guess:

            position_orientation_pairs = self.all_valid_guess[guess]
            len_word = len(guess)
            cells_of_word = cells_containing_word(position_orientation_pairs, len_word)

            return len(cells_of_word - self.all_revealed_cells) > 0

        return False


    def update_points(self, cells_of_word):
        """ A function for determining the points earned by the player
            by guessing a certain word. It utilizes set operation,
            specifically set difference between the set of ( i, j )
            pairs that denote the cells occupied by the word on the
            puzzle grid and the set of all revealed cells.
        """

        self.points += len(cells_of_word - self.all_revealed_cells)


    def update_grid_puzzle(self, position_orientation_pairs, word_guess):
        """ A function that updates the puzzle grid, revealing the
            placement of the guess word, assuming it is valid. The
            position_orientation_pairs is a list of pairs containing
            the pair (i, j), denoting where the first letter of the word
            is located on the puzzle grid, and a string ( "H" or "V" ),
            denoting the orientation of the word on the puzzle grid with
            "H" denoting horizontal orientation and "V" denoting the
            vetical orientation.
        """

        new_grid_puzzle = list(self.grid_puzzle)

        for ( ( i, j ) , orientation ) in position_orientation_pairs:

            if orientation == "D":

                cells = self.main_diagonal_cells

                for ( ch, ( x, y ) ) in zip(word_guess, cells):

                    if new_grid_puzzle[x][y] == "#":
                        new_grid_puzzle[x][y] = ch.upper()

            if orientation == "V":

                cells = vertical_cells(i, j, len(word_guess))

                for ( ch, ( x, y ) ) in zip(word_guess, cells):

                    if at_main_diagonal(x, y):
                        new_grid_puzzle[x][y] = ch.upper()

                    elif new_grid_puzzle[x][y] == "#":
                        new_grid_puzzle[x][y] = ch.lower()

            if orientation == "H":

                cells = horizontal_cells(i, j, len(word_guess))

                for ( ch, ( x, y ) ) in zip(word_guess, cells):

                    if at_main_diagonal(x, y):
                        new_grid_puzzle[x][y] = ch.upper()

                    elif new_grid_puzzle[x][y] == "#":
                        new_grid_puzzle[x][y] = ch.lower()

        self.grid_puzzle = list(new_grid_puzzle)































def is_the_main_word(guess: str, main_word: str) -> bool:
    """ A function for determining whether the player's guess is
        the main word of the game, placed symmetrically in the
        main diagonal.
    """

    return guess.strip().lower() == main_word.strip().lower()


def at_main_diagonal(i: int, j: int) -> bool:
    """ A function for determining whether an ( i , j ) pair
        is located at the main diagonal, meaning the letter
        located in it belongs to the main word.
    """

    return (i, j) in ((2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17))


def vertical_cells(i: int, j: int, len_word: int) -> list[tuple[int]]:
    """ A function for collecting all the ( i, j ) pairs
        that denote the location of the letters of a certain
        word on the puzzle grid. This function specifically
        handles words that are oriented vertically.
    """

    vertical_cells: list[tuple[int]] = []

    for x in range(i, i + len_word):
        vertical_cells.append((x, j))

    return vertical_cells


def horizontal_cells(i: int, j: int, len_word: int) -> list[tuple[int]]:
    """ A function for collecting all the ( i, j ) pairs
        that denote the location of the letters of a certain
        word on the puzzle grid. This function specifically
        handles words that are oriented horizontally.
    """

    horizontal_cells: list[tuple[int]] = []

    for y in range(j, j + len_word):
        horizontal_cells.append((i, y))

    return horizontal_cells


def cells_containing_word(position_orientation_pairs: list[tuple[tuple[int], str]], len_word: int) -> set[tuple[int]]:
    """ A function for collecting all the ( i, j ) pairs
        that denote the location of a certain word on the
        puzzle grid. This function handles both horizontal
        and vertical orientation.
    """

    main_diagonal_cells: tuple[tuple[int]] = ((2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17))
    cells_of_word: list[tuple[int]] = []

    for ( ( i, j ) , orientation ) in position_orientation_pairs:

        if orientation == "D":  # Diagonal Orientation ( Main Word )

            cells_of_word.extend(main_diagonal_cells)

        if orientation == "V":  # Vertical Orientation

            cells_of_word.extend( vertical_cells(i, j, len_word) )

        if orientation == "H":  # Horizontal Orientation

            cells_of_word.extend( horizontal_cells(i, j, len_word) )

    return set( cells_of_word )


def play_game(game_map: WorderlyMap) -> int:
    """ A function for the main loop of the game. In order to
        play, the game requires a valid puzzle grid, a main word,
        all the valid guess a player can make, and the number of
        lives given to the player.
    """

    while game_map.all_valid_guess and game_map.lives and game_map.not_all_revealed():
        """ The game will continue if it satisifies the following conditions:
                - There are still hidden words in the puzze grid.
                - The player still has number of lives greater than zero (0).
        """

        game_map.display_game_state()

        cprint( "🔀 [ SHUFFLE ] - Type [S]".rjust(53, " "), "blue")
        cprint( "❌ [ EXIT ] - Type [E]".rjust(53, " "), "red")
        cprint( "="*55, "white")
        cprint( "")
        print(game_map.all_valid_guess.keys())
        guess: str = input( colored( "Guess / Command: ", "cyan" ) ).lower().strip()

        if guess == "e":
            """ If the player has entered "E" or "e", this means
                that the player has decided to exit the game level.
                This will break the main game loop and the game
                will recognize this as a failed attempt to solve
                the puzzle grid.
            """

            print("")
            cprint( "The wizard has surrendered...".center(55, " "), "red")
            time.sleep(1)

            clear_screen()
            break

        elif guess == "s":
            """ If the player has entered "S" or "s", this means
                that the player wants to shufle the letters.
                This will have no effect on the puzzle grid, lives,
                points, and the last guess in the game.
            """

            game_map.letters = game_map.shuffle_letters(game_map.letters)

            print("")
            cprint( "The Elder is shuffling the word...".center(55, " "), "yellow")
            time.sleep(1)

            clear_screen()

        elif game_map.has_valid_guess(guess):
            """ If the guess made by the player is a valid guess,
                the puzzle grid, points, and last guess will be
                updated. On the other hand, the lives left will
                stay the same since the guess is valid.
            """

            position_orientation_pairs: list[tuple[tuple[int], str]] = game_map.all_valid_guess[guess]
            len_word: int = len(guess)
            cells_of_word: set[tuple[int]] = cells_containing_word(position_orientation_pairs, len_word)

            game_map.update_grid_puzzle(position_orientation_pairs, guess)
            game_map.update_points(cells_of_word)
            game_map.last_guess: str = guess

            game_map.all_revealed_cells |= cells_of_word
            del game_map.all_valid_guess[guess]


            print("")
            cprint( "Magical Guess!".center(55, " "), "yellow")
            time.sleep(1)

            clear_screen()

        else:
            """ If the player does not want to exit nor shuffle, and
                the guess made is not valid, a life will be deducted
                and the last guess will be updated. On the other hand,
                the puzzle grid, letters, and points will stay the
                same since the guess is invalid.
            """

            try:
                del game_map.all_valid_guess[guess]

            except:
                pass

            game_map.lives -= 1
            game_map.last_guess: str = guess

            print("")
            cprint( "Wrong Guess! You have taken damage!".center(55, " "), "red")
            time.sleep(1)

            clear_screen()


    """ Two messages of two kinds will be shown when the game ends.
        The game will end under two conditions, whether the player
        has successfully unveiled all the hidden words or the player
        has consumed all their life.

            --> Winning Messages ( All Hidden Words Unconvered )
                - "CONGRATULATIONS!"
                - "You managed to uveil all the hidden words!
                   Magnificent!"

            --> Losing Messages ( Lives Exhausted / Player Surrendered )
                - "GAME OVER"
                - "Nice Try, Wizard!"
    """
    message1: str = "GAME OVER" if game_map.not_all_revealed() else "CONGRATULATIONS!"
    message2: str = "Nice Try, Wizard!" if (message1 == "GAME OVER") else "You managed to uveil all the hidden words! Magnificent!"
    message3: str = "EXIT" if (message1 == "GAME OVER") else "CONTINUE"

    game_map.display_game_state()
    """ This will display the final state of the game showing the final
        puzzle grid, letters, lives, points, and last guess.
    """

    cprint( message1.center(55, " "), "red" if message1 == "GAME OVER" else "yellow")
    cprint( message2.center(55, " "), "white")
    cprint( "="*55, "white")
    cprint( f"-- Press ENTER to {message3} --".center(55, " "), "white")


    exit_prompt: str = input()
    """ Waits for the prompt of the player before closing the
        game level and navigating back to the game level menu.
    """

    if message1 == "GAME OVER":
        game_map.points = 0

    cprint( "Warping Out of the Game Level....".center(55, " "), "yellow")
    time.sleep(1)
    clear_screen()
    return game_map.points


def play_game_loop(list_of_words: list[str], lives: int) -> None:

    grid_puzzle_streak: int = 0
    total_streak_score: int = 0

    while True:
        game_map: WorderlyMap = WorderlyMap(list_of_words, lives)
        game_map.hide_words()

        earned_map_points: int = play_game(game_map)

        if not earned_map_points:
            break

        total_streak_score += earned_map_points
        grid_puzzle_streak += 1

    while True:

        cprint( "="*55, "white" )
        cprint( "Welcome to Wizards of Worderly Place!".center(55, " "), "yellow")
        cprint( "="*55, "white")
        cprint( "")
        cprint( "Game Summary".center(55, " "), "green")
        cprint( "")

        print( f"{colored("                 🔤 Puzzles Solved:", "blue")} {grid_puzzle_streak}")
        print( f"{colored("                 🌟 Total Points:", "yellow")} {total_streak_score}")

        cprint( "")
        cprint( "="*55, "white")
        cprint( "-- Enter short one-word player name --".center(55, " "), "red")
        player_name: str = input(colored("Enter Player Name: ", "cyan")).strip().split()

        if len(player_name) == 1 and len(player_name[0]) <= 15:
            break

        print("")
        cprint( "Invalid Name!".center(55, " "), "yellow")
        time.sleep(1)
        clear_screen()


    with open("leaderboard.txt", "r") as leaderboard:
        header: str = leaderboard.readline()
        contents: list[str] = [row for row in leaderboard if row]

    ranking: list[list[str]] = []

    for row in contents:
        ranking.append(row.split())

    ranking.append([player_name[0], str(grid_puzzle_streak), str(total_streak_score)])
    ranking.sort(key=lambda x: (int(x[1]), int(x[2])))

    new_ranking: list[str] = [" ".join((
            str(x).center(17, " "),
            str(y).center(17, " "),
            str(z).center(17, " ")
            ))
        for (x, y, z) in reversed(ranking)
        ]

    with open("leaderboard.txt", "w") as leaderboard:
        leaderboard.write(header)

        for row in new_ranking:
            leaderboard.write(f" {row} \n")

    from main_menu_display import display_levels

    print("")
    cprint( "Warping to the Worderly Place....".center(55, " "), "yellow")
    time.sleep(1)
    clear_screen()
    display_levels()





""" ==================================================================== """
"""                         MAP GENERATOR FUNCTIONS                      """
def initialize_empty_set() -> set:
    """ A function for initializing an empty set
    """

    return set()


def is_valid_word(main_word: str, word: str) -> bool:
    """ A funtion for determining whether a word is
        a valid word, that is it is a permutation of
        a subsequence of the main word
    """

    for ch in set(word):
        if word.count(ch) > main_word.count(ch):
            return False

    return main_word != word


def get_all_valid_words(main_word: str, list_of_words: list[str]) -> list[str]:
    """ A function for collecting all the valid words
        from a list of words given the main word
    """

    valid_words: list[str] = []

    for word in list_of_words:
        if ( 3 <= len(word) <= 6 ) and ( is_valid_word(main_word, word) ):
            valid_words.append(word.strip().lower())

    return valid_words


def select_main_word(list_of_words: list[str]) -> str:
    """ A function for selecting the main word randomly
        in the given list of words
    """

    while True:

        i: int = random.randint(0, len(list_of_words)-1)
        main_word: str = list_of_words[i]

        if len(main_word.strip()) == 6:
            return main_word


def is_valid_grid(all_valid_guess: dict[str, list[tuple[tuple[int], str]]]) -> bool:
    """ A function for determining whether the puzzle grid
        is valid based on the number of unique words that
        it contains which corresponds to the number
        of valid guesses.
    """

    return len(all_valid_guess) >= 21


def main_and_valid_words(list_of_words: list[str]) -> tuple[str, list[str]]:
    """ A function for selecting a random 6-letter main word
        and all the valid words that can be constructed using
        the letter available in the main word.
    """

    while True:

        main_word: str = select_main_word(list_of_words)
        valid_words: list[str] = get_all_valid_words(main_word, list_of_words)

        if len(valid_words) >= 20:
            return main_word, valid_words


def can_intersect_horizontal(grid_puzzle: list[list[str]], word:str, i: int, j: int, occupied_horizontal_cells: list[tuple[int]], occupied_vertical_cells: list[tuple[int]], starting_cells: list[tuple[int]], ending_cells: list[tuple[int]]) -> bool:
    """ A function for determining whether a word can properly intersect
        other word/s in the puzzle grid, given a starting cell ( i, j )
        and a horizontal orientation.
    """

    main_diagonal_cells: tuple[tuple[int]] = ((2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17))
    cells: list[tuple[int]] = horizontal_cells(i, j, len(word))

    intersects: bool = False
    has_buffer: bool = valid_intersection_buffers_horizontal(cells, occupied_horizontal_cells, occupied_vertical_cells, starting_cells, ending_cells)

    for ( (x, y), ch ) in zip(cells, word):

        does_not_match: bool = grid_puzzle[x][y] not in ( ch, "." )   # The cells must either be empty or contains a character matching with the character of the word.
        is_occupied: bool = (x, y) in occupied_horizontal_cells       # A word cannot intersect horizontally with other horizontally oriented words.

        if does_not_match or is_occupied:
            return False

        if grid_puzzle[x][y] == ch:     # An intersection is valid if and only if it intersects with at least one other word.
            intersects: bool = True

    return intersects and has_buffer


def can_intersect_vertical(grid_puzzle: list[list[str]], word: str, i: int, j: int, occupied_horizontal_cells: list[tuple[int]], occupied_vertical_cells: list[tuple[int]], starting_cells: list[tuple[int]], ending_cells: list[tuple[int]]) -> bool:
    """ A function for determining whether a word can properly intersect
        other word/s in the puzzle grid, given a starting cell ( i, j )
        and a vertical orientation.
    """

    main_diagonal_cells: tuple[tuple[int]] = ((2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17))
    cells: list[tuple[int]] = vertical_cells(i, j, len(word))

    intersects: bool = False
    has_buffer: bool = valid_intersection_buffers_vertical(cells, occupied_horizontal_cells, occupied_vertical_cells, starting_cells, ending_cells)

    for ( (x, y), ch ) in zip(cells, word):

        does_not_match: bool = grid_puzzle[x][y] not in ( ch, "." )   # The cells must either be empty or contains a character matching with the character of the word.
        is_occupied: bool = (x, y) in occupied_vertical_cells         # A word cannot intersect vertically with other vertically oriented words.

        if does_not_match or is_occupied:
            return False

        if grid_puzzle[x][y] == ch:     # An intersection is valid if and only if it intersects with at least one other word.
            intersects: bool = True

    return intersects and has_buffer


def valid_intersection_buffers_horizontal(cells: list[tuple[int]], occupied_horizontal_cells: list[tuple[int]], occupied_vertical_cells: list[tuple[int]], starting_cells: list[tuple[int]], ending_cells: list[tuple[int]]) -> bool:
    """ A function for determining whether a word has a valid horizontal buffer
        around it, given a starting cell ( i, j ).
    """

    main_diagonal_cells: tuple[tuple[int]] = ((2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17))

    for (n, (i, j)) in enumerate(cells):

        if n == 0 and (i, j-1) in (*occupied_horizontal_cells, *occupied_vertical_cells, *main_diagonal_cells):
            return False        # The cell on the left of the starting cell must not be occupied.

        elif n == len(cells)-1 and (i, j+1) in (*occupied_horizontal_cells, *occupied_vertical_cells, *main_diagonal_cells):
            return False        # The cell on the right of the ending cell must not be occupied.

        invalid_top_buffer: bool = (i-1, j) in (*occupied_horizontal_cells, *main_diagonal_cells, *ending_cells)
        """ The cell above the cell ( i, j ) which corresponds to
            a character of the word must not be occupied by another
            horizontally oriented word, the main diagonal word, and
            a vertically oriented word that ends at it.
        """

        invalid_bottom_buffer: bool = (i+1, j) in (*occupied_horizontal_cells, *main_diagonal_cells, *starting_cells)
        """ The cell bellow the cell ( i, j ) which corresponds to
            a character of the word must not be occupied by another
            horizontally oriented word, the main diagonal word, and
            a vertically oriented word that starts at it.
        """

        if invalid_top_buffer or invalid_bottom_buffer:
            return False

    return True


def valid_intersection_buffers_vertical(cells: list[tuple[int]], occupied_horizontal_cells: list[tuple[int]], occupied_vertical_cells: list[tuple[int]], starting_cells: list[tuple[int]], ending_cells: list[tuple[int]]) -> bool:
    """ A function for determining whether a word has a valid vertical buffer
        around it, given a starting cell ( i, j ).
    """

    main_diagonal_cells: tuple[tuple[int]] = ((2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17))

    for (n, (i, j)) in enumerate(cells):

        if n == 0 and (i-1, j) in (*occupied_horizontal_cells, *occupied_vertical_cells, *main_diagonal_cells):
            return False    # The cell on above the starting cell must not be occupied.

        elif n == len(cells)-1 and (i+1, j) in (*occupied_horizontal_cells, *occupied_vertical_cells, *main_diagonal_cells):
            return False    # The cell on below the starting cell must not be occupied.

        invalid_left_buffer: bool = (i, j-1) in (*occupied_vertical_cells, *main_diagonal_cells, *ending_cells)
        """ The cell at the left of the cell ( i, j ) which corresponds
            to a character of the word must not be occupied by another
            vertically oriented word, the main diagonal word, and
            a horizontally oriented word that ends at it.
        """

        invalid_right_buffer: bool = (i, j+1) in (*occupied_vertical_cells, *main_diagonal_cells, *starting_cells)
        """ The cell at the right of the cell ( i, j ) which corresponds
            to a character of the word must not be occupied by another
            vertically oriented word, the main diagonal word, and
            a horizontally oriented word that starts at it.
        """

        if invalid_left_buffer or invalid_right_buffer:
            return False

    return True


def grid_puzzle_word_placer(grid_puzzle: list[list[str]], i: int, j: int, orientation: str, word: str, len_word: int) -> list[list[str]]:
    """ A function for placing a word on the grid given the starting
        cell ( i, j ), word length, and orientation.
    """

    new_grid_puzzle: list[list[str]] = list(grid_puzzle)

    if orientation == "H":

        cells: list[tuple[int]] = horizontal_cells(i, j, len_word)

        for ( (x, y), ch ) in zip(cells, word):

            if grid_puzzle[x][y] == ".":

                grid_puzzle[x][y]: str = ch.lower()

    if orientation == "V":

        cells: list[tuple[int]] = vertical_cells(i, j, len_word)

        for ( (x, y), ch ) in zip(cells, word):

            if grid_puzzle[x][y] == ".":

                grid_puzzle[x][y]: str = ch.lower()

    return list(new_grid_puzzle)


def base_grid_builder(main_word: str) -> list[list[str]]:
    """ A function for building the base puzzle grid. The
        base puzzle grid consists only of the main word
        placed diagonally at the center.
    """

    main_diagonal_cells: tuple[tuple[int]] = ((2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17))

    grid_puzzle: list[list[str]] = [ ["." for j in range(25)] for i in range(15) ]

    for ( (i, j), ch ) in zip(main_diagonal_cells, main_word):
        grid_puzzle[i][j]: str = ch.lower()

    return grid_puzzle





def all_cells(len_word: int) -> tuple[tuple[int]]:
    """ A function for determining all the cells ( i, j )
        where a word can be placed both vertically and
        horizontally starting from cell ( i, j ), given
        the length of the word.
    """

    return tuple( (i, j)
        for i in range(15-len_word+1)
        for j in range(25-len_word+1)
        )


def cells_for_main_diagonal(i: int, j: int, len_word: int) -> tuple[tuple[int, int, str]]:
    """ A function for determining all the cells ( x, y )
        where a word can be placed and its orientation
        ( vertical or horizontal ), given the length of
        word, such that placing the start of the word
        on cell ( x, y ) guarantees that it will intersect
        with the main diagonal cell ( i, j )
    """

    return tuple( (i, y, "H")
        for y in range(max(0, j-len_word+1), min(j+1, 25-len_word+1))
        )+ tuple( (x, j, "V")
        for x in range(max(0, i-len_word+1), min(i+1, 15-len_word+1))
        )


def grid_puzzle_builder(main_word: str, valid_words: list[str]) -> tuple[list[list[str]], dict[str, list[tuple[tuple[int], str]]]]:
    """ A function for building a puzzle grid, not necessarily a valid
        puzzle grid, given a main word and the list of all valid words.
    """

    valid_words: list[str] = list(reversed(sorted(list(valid_words))))
    """ The valid words are sorted based on decreasing length
        to maximize the number of valid intersection points.
    """

    # Variables
    starting_cells: list[tuple[int]] = []     # The cells (i,j) where the first character of words in the puzzle grid are located.
    ending_cells: list[tuple[int]] = []       # the cells (i,j) where the last character of the words in the puzzle grid are located.
    main_diagonal_cells: tuple[tuple[int]] = ((2, 7), (4, 9), (6, 11), (8, 13), (10, 15), (12, 17))     # The cells of the main word
    occupied_horizontal_cells: list[tuple[int]] = []      # The cells (i,j) occupied by a horizontally oriented word in the puzzle grid
    occupied_vertical_cells: list[tuple[int]] = []        # The cells (i,j) occupied by a vertically oriented words in the puzzle grid

    grid_puzzle: list[list[str]] = base_grid_builder(main_word)  # The puzzle grid

    all_valid_guess: dict[str, list[tuple[tuple[int], str]]] = {main_word: [((2, 7), "D")],}
    """ The valid words in the grid, and their position orientation
        pairs denoting their starting cell ( i , j ) and their
        orientation in the puzzle grid.
    """

    for (x, y) in main_diagonal_cells:
        """ The loop for placing 6 initial words in the grid
            that would each intersect with exactly one of the
            main diagonal cells. This is guaranteed given that
            the valid words consists of characters from the
            main word.
        """

        main_diagonal_cell_filled: bool = False
        # Tracks whether a word has intersected with the main diagonal cell ( x, y )

        for word in valid_words:

            for (i, j, orientation) in cells_for_main_diagonal(x, y, len(word)):

                if orientation == "H" and can_intersect_horizontal(grid_puzzle, word, i, j, occupied_horizontal_cells, occupied_vertical_cells, starting_cells, ending_cells):
                    """ If the word has a valid horizontal intersection given its
                        starting cell ( i, j ), then it is placed on the puzzle grid.
                        The corresponding list of cells are updated and the main
                        diagonal cell ( x, y ) is marked as filled.
                    """

                    covered_horizontal_cells: list[tuple[int]] = horizontal_cells(i, j, len(word))

                    grid_puzzle: list[list[str]] = grid_puzzle_word_placer(grid_puzzle, i, j, "H", word, len(word))
                    occupied_horizontal_cells.extend(covered_horizontal_cells)
                    all_valid_guess[word]: list[tuple[tuple[int], str]] = [((i, j), "H")]

                    starting_cells.append(( i, j ))
                    ending_cells.append(( i, j+len(word)-1))
                    main_diagonal_cell_filled = True
                    valid_words.remove(word)
                    break

                elif orientation == "V" and can_intersect_vertical(grid_puzzle, word, i, j, occupied_horizontal_cells, occupied_vertical_cells, starting_cells, ending_cells):
                    """ If the word has a valid vertical intersection given its
                        starting cell ( i, j ), then it is placed on the puzzle grid.
                        The corresponding list of cells are updated and the main
                        diagonal cell ( x, y ) is marked as filled.
                    """

                    covered_vertical_cells: list[tuple[int]] = vertical_cells(i, j, len(word))

                    grid_puzzle: list[list[str]] = grid_puzzle_word_placer(grid_puzzle, i, j, "V", word, len(word))
                    occupied_vertical_cells.extend(covered_vertical_cells)
                    all_valid_guess[word]: list[tuple[tuple[int], str]] = [((i, j), "V")]

                    starting_cells.append(( i, j ))
                    ending_cells.append(( i+len(word)-1, j ))
                    main_diagonal_cell_filled = True
                    valid_words.remove(word)
                    break

            if main_diagonal_cell_filled:
                """ The loop for the main digonal cell ( x, y ) is terminated
                    once a word has intersected with it.
                """
                break


    for word in valid_words:
        """ The loop for placing the remaining valid words in the puzzle grid.
        """

        for (i, j) in all_cells(len(word)):

            if can_intersect_horizontal(grid_puzzle, word, i, j, occupied_horizontal_cells, occupied_vertical_cells, starting_cells, ending_cells):
                """ If the word has a valid horizontal intersection given its
                    starting cell ( i, j ), then it is placed on the puzzle grid.
                    The corresponding list of cells are updated.
                """

                covered_horizontal_cells: list[tuple[int]] = horizontal_cells(i, j, len(word))

                grid_puzzle: list[list[str]] = grid_puzzle_word_placer(grid_puzzle, i, j, "H", word, len(word))
                occupied_horizontal_cells.extend(covered_horizontal_cells)
                all_valid_guess[word]: list[tuple[tuple[int], str]] = [((i, j), "H")]

                starting_cells.append(( i, j ))
                ending_cells.append(( i, j+len(word)-1))
                break
                """ The loop for a word is terminated once it is intersected with
                    other words in the puzzle grid
                """

            elif can_intersect_vertical(grid_puzzle, word, i, j, occupied_horizontal_cells, occupied_vertical_cells, starting_cells, ending_cells):
                """ If the word has a valid vertical intersection given its
                    starting cell ( i, j ), then it is placed on the puzzle grid.
                    The corresponding list of cells are updated.
                """

                covered_vertical_cells: list[tuple[int]] = vertical_cells(i, j, len(word))

                grid_puzzle: list[list[str]] = grid_puzzle_word_placer(grid_puzzle, i, j, "V", word, len(word))
                occupied_vertical_cells.extend(covered_vertical_cells)
                all_valid_guess[word]: list[tuple[tuple[int], str]] = [((i, j), "V")]

                starting_cells.append(( i, j ))
                ending_cells.append(( i+len(word)-1, j ))
                break
                """ The loop for a word is terminated once it is intersected with
                    other words in the puzzle grid
                """

        if is_valid_grid(all_valid_guess):
            # The loop is terminated once the puzzle grid is valid.
            break

    return grid_puzzle, all_valid_guess


def grid_puzzle_generator(list_of_words: list[str]) -> tuple[list[list[str]], str, dict[str, list[tuple[tuple[int], str]]]]:
    """ A function for generating puzzle grid until a valid grid
        puzzle is generated.
    """

    while True:

        main_word, valid_words = main_and_valid_words(list_of_words)
        grid_puzzle, all_valid_guess = grid_puzzle_builder(main_word, valid_words)

        if is_valid_grid(all_valid_guess):
            return grid_puzzle, main_word, all_valid_guess




