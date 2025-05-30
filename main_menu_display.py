""" Importing Python Modules """
import sys
import time
from termcolor import cprint, colored


""" Importing Functions / Classes from Local Files """
from utilities import clear_screen

from game_logic import grid_puzzle_generator
from game_logic import play_game_loop
from game_logic import GameLevel


def display_levels() -> None:
    """ A function for displaying the level menu """

    while True:
        cprint( "="*55, "white" )
        cprint( "Welcome to Wizards of Worderly Place!".center(55, " "), "yellow")
        cprint( "="*55, "white")
        cprint( "")

        cprint( "🪄 [ LEVELS ] 🪄".center(55, " "))
        cprint( "")
        cprint( "Test your worderly magic!".center(55, " "))
        cprint( "Good luck, wizard!".center(55, " "))
        cprint( "")
        cprint( "Apprentice    [ 1 ]".center(55, " "), "yellow")
        cprint( "")
        cprint( "Scholar       [ 2 ]".center(55, " "), "cyan")
        cprint( "")
        cprint( "Sorcerer      [ 3 ]".center(55, " "), "green")
        cprint( "")
        cprint( "Master        [ 4 ]".center(55, " "), "blue")
        cprint( "")
        cprint( "Elder         [ 5 ]".center(55, " "), "magenta")
        cprint( "")

        cprint( "="*55, "white")
        cprint( "❌ [ EXIT ]  -  Type [E]".center(55, " "), "red")
        cprint( "="*55, "white")
        cprint( "")

        if (
            player_command := input(colored("Select Level / Exit: ", "cyan"))
            .upper()
            .strip()
        ) in {"1", "2", "3", "4", "5", "E"}:
            break

        """ The player will not be able to exit the game level menu
            until either the player enters a valid game level or
            the player exits the game level menu.
        """
        print("")
        cprint( "Invalid Input!".center(55, " "), "yellow")
        time.sleep(1)
        clear_screen()

    if player_command == "E":
        """ The game level menu closes and the player
            navigates back to the main menu.
        """

        print("")
        cprint( "Warping Back to the Worderly Menu....".center(55, " "), "yellow")
        time.sleep(1)
        clear_screen()
        main_menu()

    else:
        """ A game level will be initialized.
        """

        game_level: dict[str, GameLevel] = {
            "1": GameLevel.Apprentice,
            "2": GameLevel.Scholar,
            "3": GameLevel.Sorcerer,
            "4": GameLevel.Master,
            "5": GameLevel.Elder
            }

        if len(sys.argv) != 2:
            """ If an input lexicon file is not given, the
                permanent lexicon file will be used.
            """

            with open("ac-permanent-lexicon.txt", encoding='utf-8') as lexicon:
                list_of_words = lexicon.read().split()

        else:
            """ If an input file is given, it will be
                used as the lexicon file to load the game.
            """

            with open(sys.argv[1], encoding='utf-8') as lexicon:
                list_of_words = lexicon.read().split()

        print("")
        cprint( "Loading Level....".center(55, " "), "yellow")
        time.sleep(1)
        clear_screen()

        """ Generates a valid game level """
        play_game_loop(list_of_words, game_level[player_command].value)


def display_leaderboard() -> None:

    with open("leaderboard.txt", "r") as leaderboard:
        header: str = leaderboard.readline()
        ranking: list[str] = leaderboard.readlines()

    cprint( "="*55, "white" )
    cprint( "Welcome to Wizards of Worderly Place!".center(55, " "), "yellow")
    cprint( "="*55, "white")
    cprint( "")

    cprint( "🏅 [ LEADERBOARD ] ℹ️".center(55, " "), "white")
    cprint( "")

    cprint( header, "green")
    for row in ranking:
        print(row.strip("\n"))

    cprint( "")
    cprint( "="*55, "white")
    cprint( "-- Press ENTER to EXIT --".center(55, " "), "red")
    cprint( "="*55, "white")

    exit_prompt: str = input()
    """ Waits for the prompt of the player before closing the
        help menu and navigating back to the main menu.
    """

    cprint( "Warping Back to the Worderly Menu....".center(55, " "), "yellow")
    time.sleep(1)
    clear_screen()
    main_menu()


def display_help() -> None:
    """ A function for displaying the help menu """

    cprint( "="*55, "white" )
    cprint( "Welcome to Wizards of Worderly Place!".center(55, " "), "yellow")
    cprint( "="*55, "white")
    cprint( "")

    cprint( "ℹ️ [ WIZARD'S MANUAL ] ℹ️".center(55, " "), "white")
    cprint( "")

    cprint( "Magic Mechanics".center(55, " "), "green" )
    cprint( " -> Once the worderly game commence, 6 (six) unordered")
    cprint( "    letters are given.")
    cprint( " -> The puzzle shows the placement of the words in")
    cprint( "    the worderly map.")
    cprint( " -> You are tasked to guess a valid word of length at")
    cprint( "    least 3 (three) and at most 6 (six).")
    cprint( " -> A guess is valid if it corresponds to a word in")
    cprint( "    the puzzle that has not been revealed yet.")
    cprint( " -> A valid guess will reveal the placement of the")
    cprint( "    word in the puzzle and will earn its corresponding")
    cprint( "    magic merits.")
    cprint( " -> An invalid guess will consume 1 (one) life.")
    cprint( " -> The game will end once all lives are consumed or")
    cprint( "    all words in the puzzle are revealed.")
    cprint( "")

    cprint( "Magic Merits".center(55, " "), "blue" )
    cprint( " -> On each valid guess, a wizard will earn a point")
    cprint( "    for each new letter that is revealed on the puzzle.")
    cprint( " -> Depending on the guess, assuming it is valid, a")
    cprint( "    wizard can earn at least 1 (one) point and at most")
    cprint( "    6 (six) points.")
    cprint( "")

    cprint( "Magical Levels".center(55, " "), "magenta" )
    cprint( " -> Each level has different difficulties, with the")
    cprint( "    Apprentice Level being the easiest and the Elder")
    cprint( "    Level being the hardest.")
    cprint( " -> The difficulty of each level is based on the maximum")
    cprint( "    number of lives given to the player.")
    cprint( "       - Apprentice Level ( 20 Lives )")
    cprint( "       - Scholar Level ( 15 Lives )")
    cprint( "       - Sorcerer Level ( 10 Lives )")
    cprint( "       - Master Level ( 5 Lives )")
    cprint( "       - Elder Level ( 3 Lives )")

    cprint( "")
    cprint( "="*55, "white")
    cprint( "-- Press ENTER to EXIT --".center(55, " "), "red")
    cprint( "="*55, "white")

    exit_prompt: str = input()
    """ Waits for the prompt of the player before closing the
        help menu and navigating back to the main menu.
    """

    cprint( "Warping Back to the Worderly Menu....".center(55, " "), "yellow")
    time.sleep(1)
    clear_screen()
    main_menu()


def main_menu() -> None:
    """ A function for displaying the main menu """

    while True:
        cprint( "="*55, "white" )
        cprint( "Welcome to Wizards of Worderly Place!".center(55, " "), "yellow")
        cprint( "="*55, "white")
        cprint( "")
        cprint( "🪄 [ PLAY ]  -  Type [P]".center(55, " "), "green")
        cprint( "")
        cprint( "ℹ️ [ HELP ]  -  Type [H]".center(55, " "), "blue")
        cprint( "")
        cprint( "🏅 [ LEADERBOARD ]  -  Type [L]".center(55, " "), "magenta")
        cprint( "")
        cprint( "="*55, "white")
        cprint( "❌ [ EXIT ]  -  Type [E]".center(55, " "), "red")
        cprint( "="*55, "white")
        cprint( "")

        if (
            player_command := input(colored("Enter Command: ", "cyan")).upper().strip()
        ) in {"P", "H", "E", "L"}:
            break

        """ The player cannot leave the main menu until either
            the player exits the game or navigates to other menus.
        """
        print("")
        cprint( "Invalid Input!".center(55, " "), "yellow")
        time.sleep(1)
        clear_screen()

    if player_command == "P":
        """ Navigates to the game level menu. """

        print("")
        cprint( "Warping to the Worderly Place....".center(55, " "), "yellow")
        time.sleep(1)
        clear_screen()
        display_levels()

    if player_command == "L":
        """ Navigates to the leaderboard. """

        print("")
        cprint( "Warping to the Worderly Place....".center(55, " "), "yellow")
        time.sleep(1)
        clear_screen()
        display_leaderboard()

    if player_command == "H":
        """ Navigates to the help menu. """

        print("")
        cprint( "Calling the Wizards....".center(55, " "), "yellow")
        time.sleep(1)
        clear_screen()
        display_help()

    if player_command == "E":
        """ Closes the game. """

        print("")
        cprint( "Warping Out of the Worderly Place....".center(55, " "), "yellow")
        time.sleep(1)
        clear_screen()
        sys.exit()
