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
    
    def initialize_hand(self): #TODO add card sorting criteria based on color/number/type
        initialHandSize = 5
        for _ in range(initialHandSize):
            knownColor, knownType, isMakeEntangled = self.deck.newCard()
            self.cards.append(card.Card(knownColor, knownType))
    

    def __str__(self): #TODO make it so that the print outs consider showing the Entangled cards
        print("Here are your " + str(len(self.cards)) + " cards:")
        #TODO make this pretty
        returnString = ""
        for i in range(len(self.cards)):
            returnString += str(i) + ":\n " + str(self.cards[i]) + "\n"
        
        return returnString