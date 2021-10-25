from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.visualization import plot_histogram, plot_state_qsphere, plot_bloch_multivector, plot_bloch_vector
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

    #TODO prints are just my notes when testing, lol. def delete later
    def initialize_qc(self):
        """ Initializes the internal quantum circuit to the knownColors/knownTypes
        This method will add the appropriate gates to obtain the correct colors/types
        """
        # TODO: I used hadamards for superposition, but we could use other gates
        # instead later? but hadamards might be simplest way to do superposition
        # (e.g. put both qubits 0 and 1 in superposition via hadamards... then measure
        # so that results could be 00, 01, 10, or 11)... basically using Noah's idea in
        # the piazza post

        if len(self.knownColor) > 1: 
          print("superposition here")
          self.qc.h(self.qColorRegister[0])
          self.qc.h(self.qColorRegister[1])
          
        elif len(self.knownColor) == 1:
          print("single colored card")
          if self.knownColor[0] == Color.BLUE:
            print("it's blue")
            self.qc.x(self.qColorRegister[0])
          elif self.knownColor[0] == Color.YELLOW:
            print("it's yellow")
            self.qc.x(self.qColorRegister[1])
          elif self.knownColor[0] == Color.GREEN:
            print("it's green")
            self.qc.x(self.qColorRegister[0])
            self.qc.x(self.qColorRegister[1])
          else:
            print("it's red")
        
        if len(self.knownType) == 1:
          print("single type card")
          if self.knownType[0] == Type.SKIP:
            print("it's skip")
            self.qc.x(self.qTypeRegister[0])
          elif self.knownType[0] == Type.REVERSE:
            print("it's reverse")
            self.qc.x(self.qTypeRegister[1])
          elif self.knownType[0] == Type.DRAW_2:
            print("it's draw 2")
            self.qc.x(self.qTypeRegister[0])
            self.qc.x(self.qTypeRegister[1])
          elif self.knownType[0] == Type.WILD_DRAW_4:
            print("it's wild draw 4")
            self.qc.x(self.qTypeRegister[2])
          elif self.knownType[0] == Type.WILD:
            print("it's wild")
            self.qc.x(self.qTypeRegister[0])
            self.qc.x(self.qTypeRegister[2])
          elif self.knownType[0] == Type.MAKE_ENTANGLED:
            print("it's make entangled")
            self.qc.x(self.qTypeRegister[1])
            self.qc.x(self.qTypeRegister[2])
          elif self.knownType[0] == Type.ENTANGLED:
            print("it's entangled")
            self.qc.x(self.qTypeRegiser[0])
            self.qc.x(self.qTypeRegister[1])
            self.qc.x(self.qTypeRegister[2])
          elif self.knownType[0] == Type.INTERFERENCE:
            print("it's interference")
            self.qc.x(self.qTypeRegister[3])
          else:
            print("it's number")
        else:
          print("superposition of colors") 
          # TODO: we really don't need to do anything here, no?

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
        self.qColorRegister = QuantumRegister(2)
        self.qTypeRegister = QuantumRegister(4)
        self.cColorRegister = ClassicalRegister(2)
        self.cTypeRegister = ClassicalRegister(4)
        self.qc = QuantumCircuit(self.qColorRegister,
                                 self.qTypeRegister,
                                 self.cColorRegister,
                                 self.cTypeRegister)
        self.wasMeasured = False

        # Known properties
        self.knownColor = colors
        self.knownType = types

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
        self.qc.measure(self.qColorRegister, self.cColorRegister)
        self.qc.measure(self.qTypeRegister, self.cTypeRegister)
        backend = Aer.get_backend('qasm_simulator')
        counts = execute(self.qc,backend, shots=1024).result().get_counts(self.qc)
        print(counts)
        plot_histogram(counts) #TODO: Nothing prints. not that this is a necessary thing, but i never really know why this doesn't happen
        #TODO: set arrays to counts
        lAnswer = [(k[::-1],v) for k,v in counts.items()]
        lAnswer.sort(key = lambda x: x[1], reverse=True)
        Y = []

        #gather results and interpret them into decimal form
        for k, v in lAnswer: 
          Y.append([ int(c) for c in k if c != ' '])
          print(Y)
        colorVal = ''
        for i in range(2):
          colorVal += str(Y[0][i])
        colorVal = int(colorVal, 2)
        print("interpreted color value is " + str(colorVal))
        typeVal = ''
        for i in range(2, 6):
          typeVal += str(Y[0][i])
        typeVal = int(typeVal, 2)
        print("interpreted type value is " + str(typeVal))
        print(typeVal)

        #add to knownColor
        if colorVal == Color.RED.value:
          self.knownColor.append(Color.RED)
          print("we now know it's red")
        elif colorVal == Color.BLUE.value:
          self.knownColor.append(Color.BLUE)
          print("we now know it's blue")
        elif colorVal == Color.YELLOW.value:
          self.knownColor.append(Color.YELLOW)
          print("we now know it's yellow")
        else:
          self.knownColor.append(Color.GREEN)
          print("we now know it's green")

        #add to knownType
        if typeVal == Type.NUMBER.value:
          self.knownType.append(Type.NUMBER)
          print("we now know it's number")
        elif typeVal == Type.SKIP.value:
          self.knownType.append(Type.SKIP)
          print("we now know it's skip")
        elif typeVal == Type.REVERSE.value:
          self.knownType.append(Type.REVERSE)
          print("we now know it's reverse")
        elif typeVal == Type.DRAW_2.value:
          self.knownType.append(Type.DRAW_2)
          print("we now know it's draw_2")
        elif typeVal == Type.WILD_DRAW_4.value:
          self.knownType.append(Type.WILD_DRAW_4)
          print("we now know it's wild_draw_4")
        elif typeVal == Type.WILD.value:
          self.knownType.append(Type.WILD)
          print("we now know it's wild")
        elif typeVal == Type.MAKE_ENTANGLED.value:
          self.knownType.append(Type.MAKE_ENTANGLED)
          print("we now know it's make_entangled")
        elif typeVal == Type.ENTANGLED.value:
          self.knownType.append(Type.ENTANGLED)
          print("we now know it's entangled")
        else:
          self.knownType.append(Type.INTERFERENCE)
          print("we now know it's interference")
        self.wasMeasured = True
        

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
        
        #TODO: I think I'll have a better idea of what actions to take after 
        # I examine the deck & player class lol
        if len(self.knownType) == 1:
          print("single type card")
          if self.knownType[0] == Type.SKIP:
            print("it's skip")
            #TODO: do something involving skipping next player
          elif self.knownType[0] == Type.REVERSE:
            print("it's reverse")
            #TODO: do something involving reversing the order
          elif self.knownType[0] == Type.DRAW_2:
            print("it's draw 2")
            #TODO: do something involving increasing adding 2 from deck
          elif self.knownType[0] == Type.WILD_DRAW_4:
            print("it's wild draw 4")
            #TODO: do something involving increasing adding 2 from deck + apply gates to them
          elif self.knownType[0] == Type.WILD:
            print("it's wild")
            #TODO: for wild cards, should this just be a player measuring cards in superposition to put them out of s.p.? or is this us putting a color in superposition?
          elif self.knownType[0] == Type.MAKE_ENTANGLED:
            print("it's make entangled")
            #TODO: entangle the cards
          elif self.knownType[0] == Type.ENTANGLED:
            print("it's entangled")
            #TODO: measure one card 
          elif self.knownType[0] == Type.INTERFERENCE:
            print("it's interference")
            #TODO: do something involving interference (adding right gates for this)
          else:
            print("it's number")
            # do nothing

    def show_card(self):
        """ Prints out a representation of the current card to the console
        
        """
        self.qc.draw() #TODO why won't stuff print :/ compiles fine, but no output for this.
