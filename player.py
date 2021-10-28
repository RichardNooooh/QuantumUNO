import deck
import card

class Player:
    """ Represents a player in the game
    
    Attributes
    --------------
    # ? not too sure if turnNumber is needed
    turnNumber : int
        Represents the player's turn order in the game.

    cards : Card[]
        Represents the hand of cards that the player holds.
    """

    def __init__(self, turn_number, deck):
        self.turnNumber = turn_number
        self.cards = []
        self.deck = deck
        self.hasUNO = False
        
        self.initialize_hand()
    

    # Creates the initial cards
    def initialize_hand(self):
        initialHandSize = 5
        for _ in range(initialHandSize):
            knownColor, knownType = self.deck.newCard()
            self.cards.append(card.Card(knownColor, knownType))
    

    # Prints out the cards
    def __str__(self):
        print("--------------------------------------------------------------------------")
        print("██    ██  ██████  ██    ██ ██████      ██   ██  █████  ███    ██ ██████  ")
        print(" ██  ██  ██    ██ ██    ██ ██   ██     ██   ██ ██   ██ ████   ██ ██   ██ ")
        print("  ████   ██    ██ ██    ██ ██████      ███████ ███████ ██ ██  ██ ██   ██ ")
        print("   ██    ██    ██ ██    ██ ██   ██     ██   ██ ██   ██ ██  ██ ██ ██   ██ ")
        print("   ██     ██████   ██████  ██   ██     ██   ██ ██   ██ ██   ████ ██████  ")
        print("--------------------------------------------------------------------------")
        returnString = ""
        for i in range(len(self.cards)):
            returnString += "Card #" + str(i) + ":\n" + str(self.cards[i]) + "\n"
        
        return returnString