""" Importing Python Modules """
import sys

""" Importing Functions from Local Files """
from main_menu_display import main_menu

from game_logic import grid_puzzle_generator
from game_logic import play_game_loop
from game_logic import GameLevel
from utilities import clear_screen


def main() -> None:
    """ This is the main function of the game.
        Handles command line arguments.
    """

    if len(sys.argv) != 2:
        """ If there is no given input file, the game will
            initialize the main menu where the player can explore
            other features such as a user manual, and can also
            play the game using a permanent lexicon file.
        """

        main_menu()

    else:
        """ If there is an input file, the game will initialize
            the game using the input file as the lexicon file.
        """

        with open(sys.argv[1], encoding='utf-8') as lexicon:

            list_of_words: list[str] = lexicon.readlines()

        play_game_loop(list_of_words, 5)


if __name__ == "__main__":
    """ Once the main file is ran, the terminal
        will be cleared and the main function will be initialized
    """

    clear_screen()
    main()
