from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from enum import Enum, auto


class Color(Enum):
    """ Represents the color of the card
    """
    RED     = 0
    BLUE    = 1
    YELLOW  = 2
    GREEN   = 3


class Type(Enum):
    """ Represents the type of the card
    """

    # Normal UNO (May or may not use these types)
    NUMBER      = 0
    SKIP        = 1
    REVERSE     = 2
    DRAW_2      = 3
    WILD_DRAW_4 = 4
    WILD        = 5

    # Special Quantum Cards
    # SUPERPOSITION   = 6     # We can represent this card type with self.knownType[]
    MAKE_ENTANGLED  = 6
    ENTANGLED       = 7
    INTERFERENCE    = 8
    # all other card type numbers 9-15 are invalid (for now?)


class Card:
    """ Represents a card in the game

    Attributes
    ----------------
    qColorRegister : QuantumRegister
        A 2-qubit register that represents the color of the card.
    qTypeRegister : QuantumRegister
        A 4-qubit register taht represents the type of the card.
    cColorRegister : ClassicalRegister
        A 2-bit register that measures the color of the card.
    cTypeRegister : ClassicalRegister
        A 4-bit register that measures the type of the card.
    qc : QuantumCircuit
        The 6-qubit circuit that represents the underlying color and type of the
        card.
    
    wasMeasured : bool
        A boolean that simply checks if this Card object was measured before
        running self.action().

    knownColor : Color[]
        A list that represents the color(s) of the card that the Player knows.
        If the length of knownColor is 0, the type must be Type.ENTANGLED.
        If the length of knownColor is 1, this card is a single-colored card.
        If the length of knownColor is greater than 1, this card is in a superposition
            of the known colors.
        knownColor should directly reflect the internal state of the quantum 
        circuit (qc).
    knownType : Type[]
        A list that represents the type(s) of the card that the Player knows.
        The length of knownType MUST be greater than 0.
        If the length of knownType is 1, this card is a single-typed card.
        If the length of knownType is greater than 1, this card is in a superposition
            of the known colors.
    """

    def initialize_qc(self):
        """ Initializes the internal quantum circuit to the knownColors/knownTypes

        This method will add the appropriate gates to obtain the correct colors/types
        """
        
        pass


    def __init__(self, colors, types):
        # Parameter checks
        assert type(colors) is list and type(colors[0]) is Color, \
              "ERROR in Card.__init__() - The type of 'colors' is wrong: " \
              + str(type(colors[0])) + " instead of Color."
        assert type(types) is list and type(types[0]) is Type, \
              "ERROR in Card.__init__() - The type of 'types' is wrong: " \
              + str(type(types[0])) + " instead of Type."
        assert len(types) > 0, \
              "ERROR in Card.__init__() - The length of 'types' must be greater than 0."
        if len(colors) == 0:
            assert len(types) == 1 and types[0] == Type.ENTANGLED, \
                  "ERROR in card.__init__() - Type must be ENTANGLED if the length of colors == 0."
        
        # Quantum properties
        self.qColorRegister = QuantumRegister(2, name="Color")
        self.qTypeRegister = QuantumRegister(4, name="Type")
        self.cColorRegister = ClassicalRegister(2, name="Color")
        self.cTypeRegister = ClassicalRegister(4, name="Type")
        self.qc = QuantumCircuit(self.qColorRegister,
                                 self.qTypeRegister,
                                 self.cColorRegister,
                                 self.cTypeRegister)
        self.wasMeasured = False

        # Known properties
        self.knownColor = []
        self.knownType = []

        self.initialize_qc()

    def measure(self):
        """ Determines the actual color and type of this card
        
        Since a card's true state is represented by a quantum circuit,
        we need to measure the entire quantum system to determine the true
        color and type.

        Whenever a measurement is done, we will get an array of hits corresponding
        to each bitstring. The first two bits is the color register, while the
        last four bits are the type register. Interpreting these bits in
        decimal will give us the color/type, after mapping the numbers to
        the Color and Type enums.

        If there are multiple nontrivial measurement results, pick the one that
        had the most number of hits. The exact implementation details is up
        to you.

        Before this method returns:
            Returns a tuple (Color, Type) of the result,
            Sets the knownCard and knownType fields to the result, and
            Sets wasMeasured to True.
        """
        pass

    def action(self, nextPlayer, game):
        """ Plays the action of the current card

        Based on the knownType of the card, this method will do something
        to nextPlayer's cards or the game as a whole (like turnOrder).

        """
        # State checks
        assert self.wasMeasured == True, \
              "ERROR in Card.action() - This card has not been measured yet."
        assert len(self.knownCard) == 1 and len(self.knownType) == 1, \
              "ERROR in Card.action() - Card.measure() has not set the known " \
              + "card and type fields correctly."
        # Parameter checks
        assert type(nextPlayer) is Player, \
              "ERROR in Card.action() - nextPlayer parameter is not a Player."
        assert type(game) is Game, \
              "ERROR in Card.action() - game parameter is not a Game."
        
        pass

    def show_card(self):
        """ Prints out a representation of the current card to the console
        
        """
        pass # TODO

