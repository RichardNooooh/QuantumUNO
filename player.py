from card import Card

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
        
        self.initialize_hand()
    
    def initialize_hand(self):
        """ Gives the Player their initial hand of random cards
        """
        pass

    def get_card(self):
        pass

    def play_card(self, index):
        pass
