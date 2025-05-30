""" Importing Python Modules """
from os import system, name


def clear_screen() -> None:
    """ A function for clearing the screen
    """

    if name == "nt":
        _ = system("cls")

    else:
        _ = system("clear")
