import os
import sys
import player
import deck

# Main Game Logic

class Game:
    """ Manages the current state of the game

    This handles the main interface between the users and this program.
    The text UI, primary game loop and win condition checks are all
    here.
    """

    def __init__(self, numPlayers):
        self.turnOrder = 1 # ! shouldn't need this
        self.playerIndex = 0
        self.players = []
        self.topOfPlayedPile = None

        self.deck = deck.Deck()
        
        self.initialize_players(numPlayers)
    

    def initialize_players(self, numPlayers):
        for i in range(numPlayers):
            self.players.append(player.Player(i, self.deck))


    def validPlayInput(self, currentPlayer, outString): # TODO make this return a tuple
        givenInput = ""
        while True:
            givenInput = input(outString)
            if givenInput.isnumeric() and 0 <= int(givenInput) < len(currentPlayer.cards):
                cardSelectionIndex = int(givenInput)
                playedCard = currentPlayer.cards[cardSelectionIndex]
                if playedCard.isPlayable(self.topOfPlayedPile): 
                    return (False, playedCard)
                else:
                    outString = "   Sorry! That card can not be played because the color/type does not match."
            elif givenInput.lower() == "d" or givenInput.lower() == "deck":
                # self.deck.addRYPhase()
                playedCard = self.deck.getTopCard()
                return (True, playedCard)
            outString = "   Please enter in a valid card id number to play a card from your hand,\n" \
                + "    or enter \"deck\"/\"d\" to retrieve the top deck card."

    
    def displayTurnUI(self):
        print("   The next card from the deck will be: ")
        if len(self.deck.deckColors) == 2:
            print("    A superposition of:")
            print("    " + str(self.deck.topOfDeckColor[0][0]) + " and " + str(self.deck.topOfDeckColor[0][1]))
            if len(self.deck.topOfDeckColor) == 2:
                print("    " + str(self.deck.topOfDeckColor[1][0]) + " and " + str(self.deck.topOfDeckColor[1][1]))
        else:
            print("     " + str(self.deck.topOfDeckColor[0][0]))
            if len(self.deck.topOfDeckColor) == 2:
                print("     " + str(self.deck.topOfDeckColor[1][0]))

        if self.topOfPlayedPile is not None:
            print("\nLast played card: " + str(self.topOfPlayedPile))



    def play_turn(self):
        # Display starting UI
        # TODO alert player if anyone has an UNO card
        # TODO display the top deck card
        clear_console()
        print("Welcome Player " + str(self.playerIndex + 1) + ".")
        self.displayTurnUI()
        currentPlayer = self.players[self.playerIndex]
        print(currentPlayer)

        # Receive input
        pulledDeck, playedCard = self.validPlayInput(currentPlayer, "Select a Card from 0 to " + str(len(currentPlayer.cards) - 1) \
            + ", or type \"d\" to draw the from the deck.")
        
        nextPlayerIndex = (self.playerIndex + 1) % len(self.players)
        if pulledDeck is False: 
            # Collapse superposition (if there was one)
            self.topOfPlayedPile = playedCard.measure()
            currentPlayer.cards.remove(playedCard)

            # Do the card's action
            playedCard.action(self.players[nextPlayerIndex], self)
        else:
            self.players[self.playerIndex].cards.append(playedCard)

        # Check win/UNO condition
        if len(currentPlayer.cards) == 0:
            self.win()
        elif len(currentPlayer.cards) == 1:
            currentPlayer.hasUNO = True
        else:
            currentPlayer.hasUNO = False
        
        # redisplay the table
        clear_console()
        self.displayTurnUI()
        print(currentPlayer)
        input("Press enter...")

        self.playerIndex = nextPlayerIndex
        self.next_turn()


    def next_turn(self):
        # clear_console()
        input("Please bring player " + str(self.playerIndex + 1) + " to the computer! Press enter once you do. :)")
        # clear_console()
        self.play_turn()

    def win(self):
        print("CONGRATULATIONS! YOU WON, PLAYER " + str(self.playerIndex + 1) + "!")
        sys.exit()

    def start_game(self):
        self.play_turn()

def clear_console():
    if os.name=='nt':
        os.system("cls")   # Windows
    else:
        os.system("clear") # Linux/Mac

    for _ in range(100):
        print("\n")

def validNumInput(outString, lowerLimit, upperLimit):
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
    playerTotal = validNumInput("To start the game, please enter in the number of players for this game of QUNO: ", 3, 9)
    print("Before the game starts, please decide amongst yourselves who will be player\n1, 2, and etc.")
    input("Once you have decided, please press Enter:")

    # TODO write help documentation and help() function
    # TODO console input
    clear_console()

    game = Game(int(playerTotal))
    game.start_game()
