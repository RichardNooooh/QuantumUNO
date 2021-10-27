import os
import platform
import player

# Main Game Logic

class Game:
    """ Manages the current state of the game

    This handles the main interface between the users and this program.
    """

    def __init__(self, numPlayers):
        self.turnOrder = 1
        self.playerIndex = 0
        self.players = []
        
        self.initialize_players(numPlayers)
    

    def initialize_players(self, numPlayers):
        for i in range(numPlayers):
            self.players.append(player.Player(i))

    def play_turn(self):
        print("Player " + str(self.playerIndex + 1) + ", it's your turn.")
        currentPlayer = self.players[self.playerIndex]
        print(currentPlayer)
        cardSelectionIndex = int(input("Select a Card! (0 - " + str(len(currentPlayer.cards) - 1) + "): "))
        playedCard = currentPlayer.cards[cardSelectionIndex]
        playedCard.measure()
        playedCard.action()

        # Check win condition
        if len(currentPlayer.cards) == 0:
            self.win()


        self.playerIndex = (self.playerIndex + 1) % len(self.players)
        
        # clear_console()
        currentPlayer.print_hand()
        input("Press enter...")

        self.next_turn()


    def next_turn(self):
        # clear_console()
        input("Please bring player " + str(self.playerIndex + 1) + " to the computer! Press enter once you do. :)")
        # clear_console()
        self.play_turn()

    def win(self):
        print("CONGRATULATIONS! YOU WON, PLAYER " + str(self.playerIndex + 1) + "!")

    def start_game(self):
        self.play_turn()

def clear_console():
    os_name = platform.system
    if os_name == "Windows":
        os.system("cls")   # Windows
    else:
        os.system("clear") # Linux/Mac

def validInput(outString, lowerLimit, upperLimit):
    isValid = False
    givenInput = ""
    while not isValid:
        givenInput = input(outString)
        if not givenInput.isnumeric():
            outString = " Please try again with a number: "
        elif not lowerLimit <= int(givenInput) < upperLimit:
            outString = " Please enter a number between " + str(lowerLimit) + " to " + str(upperLimit-1) + ": "
        else:
            isValid = True
    
    return givenInput

if __name__ == "__main__":
    clear_console()
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
    playerTotal = validInput("To start the game, please enter in the number of players for this game of QUNO: ", 3, 9)
    print("Before the game starts, please decide amongst yourselves who will be player\n1, 2, and etc.")
    input("Once you have decided, please press Enter:")

    # TODO write help documentation and help() function
    # TODO console input
    clear_console()

    game = Game(int(playerTotal))
    game.start_game()
