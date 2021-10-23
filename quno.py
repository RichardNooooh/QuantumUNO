import os
import platform

# Main Game Logic

class Game:

    def __init__(self, numPlayers):
        self.turnOrder = 1
        self.players = []

    # TODO game loop


def start_game():
    pass


def clear_console():
    os_name = platform.system
    if platform.system() == "Windows":
        os.system("cls")   # Windows
    else:
        os.system("clear") # Linux/Mac

if __name__ == "__main__":
    print("````````````````````````````````````````````````````````````````````````````````")
    print("|                                                                              |")
    print("|                  ██████╗ ██╗   ██╗███╗   ██╗ ██████╗                         |")
    print("|                 ██╔═══██╗██║   ██║████╗  ██║██╔═══██╗                        |")
    print("|                 ██║   ██║██║   ██║██╔██╗ ██║██║   ██║                        |")
    print("|                 ██║▄▄ ██║██║   ██║██║╚██╗██║██║   ██║                        |")
    print("|                 ╚██████╔╝╚██████╔╝██║ ╚████║╚██████╔╝                        |")
    print("|                  ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝                         |")
    print("|                                                                              |")
    print("````````````````````````````````````````````````````````````````````````````````")
    print("Welcome to QUNO - A Quantum-based UNO Console Game")
    print("     Developed by Abdullah Assaf, Emily Padilla, and Richard Noh")
    print("     For TODO...")
    print("")
    playerTotal = input("To start the game, please enter in the number of players for this game of QUNO: ")
    print("Before the game starts, please decide amongst yourselves who will be player\n1, 2, and etc.")
    input("Once you have decided, please press Enter:")

    # TODO write help documentation and help() function
    # TODO console input

    clear_console()
    

