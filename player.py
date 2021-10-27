import deck

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

    def __init__(self, turn_number):
        self.turnNumber = turn_number
        self.cards = []
        self.hasUNO = False
        
        self.initialize_hand()
    
    def initialize_hand(self): #TODO add card sorting criteria based on color/number/type
        initialHandSize = 5
        for _ in range(initialHandSize):
            self.cards.append(deck.Deck.newCard())
        

    def get_card(self):
        pass

    def play_card(self, index):
        pass

    def __str__(self):
        print("Here are your " + str(len(self.cards)) + " cards:")
        #TODO make this pretty
        returnString = ""
        for i in range(len(self.cards)):
            returnString += str(i) + ":\n " + str(self.cards[i]) + "\n"
        
        return returnString