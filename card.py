from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.visualization import plot_histogram, plot_state_qsphere, plot_bloch_multivector, plot_bloch_vector
from enum import Enum, auto
import numpy as np
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
    # Special Quantum Cards
    NORMAL = 0
    MAKE_ENTANGLED  = 1
    ENTANGLED       = 2
    INTERFERENCE    = 3
    #WILD = 4 
    #TODO should wild be a card? or is it more of a concept?
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
    interferenceCount = 0
    #TODO prints are just my notes when testing, lol. def delete later
    def initialize_qc(self):
        """ Initializes the internal quantum circuit to the knownColors/knownTypes
        This method will add the appropriate gates to obtain the correct colors/types
        """
        if len(self.knownColor) > 1: #initially put the card in superposition. Interference cards played will continue to manipulate until measure
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
            if self.knownType[0] == Type.MAKE_ENTANGLED:
                print("it's make entangled")
                self.qc.x(self.qTypeRegister[0])
            elif self.knownType[0] == Type.ENTANGLED:
                print("it's entangled")
                self.qc.x(self.qTypeRegister[1])
            elif self.knownType[0] == Type.INTERFERENCE:
                print("it's interference")
                self.qc.x(self.qTypeRegister[0])
                self.qc.x(self.qTypeRegister[1])
            else:
                print("it's normal")

          # I still don't really know what it would mean to have more than 1 type cards? do we really need type cards > 1?

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
        self.qTypeRegister = QuantumRegister(3)
        self.cColorRegister = ClassicalRegister(2)
        self.cTypeRegister = ClassicalRegister(3)
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
        lAnswer = [(k[::-1],v) for k,v in counts.items()]
        lAnswer.sort(key = lambda x: x[1], reverse=True)
        Y = []

        #gather results and interpret them into decimal form
        for k, v in lAnswer: 
            Y.append([ int(c) for c in k if c != ' '])
        colorVal = ''
        for i in range(2):
            colorVal = str(Y[0][i]) + colorVal
        colorVal = int(colorVal, 2)
        typeVal = ''
        for i in range(2, 5):
            typeVal = str(Y[0][i]) + typeVal
        typeVal = int(typeVal, 2)
        
        if colorVal == Color.RED.value:
            self.knownColor[0] = (Color.RED)
            measuredColor = Color.RED
            print("we now know it's red")
        elif colorVal == Color.BLUE.value:
            print(Color.BLUE)
            self.knownColor[0] = (Color.BLUE)
            measuredColor = Color.BLUE
            print("we now know it's blue")
        elif colorVal == Color.YELLOW.value:
            self.knownColor[0] = (Color.YELLOW)
            measuredColor = Color.YELLOW
            print("we now know it's yellow")
        else:
            self.knownColor[0] = (Color.GREEN)
            measuredColor = Color.GREEN
            print("we now know it's green")

        if typeVal == Type.NORMAL.value:
            self.knownType[0] = (Type.NORMAL)
            measuredType = Type.NORMAL
            print("we now know it's normal")
        elif typeVal == Type.MAKE_ENTANGLED.value:
            self.knownType[0] = (Type.MAKE_ENTANGLED)
            measuredType = Type.NORMAL
            print("we now know it's make_entangled")
        elif typeVal == Type.ENTANGLED.value:
            self.knownType[0] = (Type.ENTANGLED)
            measuredType = Type.NORMAL
            print("we now know it's entangled")
        else:
            self.knownType[0] = (Type.INTERFERENCE)
            measuredType = Type.NORMAL
            print("we now know it's interference")
        self.wasMeasured = True
        return (measuredColor, measuredType)
        

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
        
        if len(self.knownType) == 1:
            if self.knownType[0] == Type.MAKE_ENTANGLED:
                print("it's make entangled")
                #TODO: how to entangle this card object w/ other card?
            elif self.knownType[0] == Type.ENTANGLED:
                print("it's entangled")
                self.qc.measure()
            elif self.knownType[0] == Type.INTERFERENCE:
                self.qc.ry(np.pi/2,self.qColorRegister[0])  

            # INCOMPLETE BS DOWN HERE, EITHER FIX OR REMOVE
            #calculate applyNum = floor(interferenceCount / 4)
            #interferenceCount += 1;
            #applyNum = np.floor(interferenceCount/4)
            # apply ry(pi/4) to q[1] applyNum times
            #self.qc.ry(np.pi/4, qColorRegister[1])


    def __str__(self):
        """ Prints out a representation of the current card to the console
        
        """
        for i in range(len(self.knownColor)):
            print(self.knownColor[i])
        for i in range(len(self.knownType)):
            print(self.knownType[i])
####QUESTIONS/CONCERNS I HAD (there may be more i'm forgetting but if so i forgot them lol#########

#-> Is there a need to even have the circuit represent a normal card? maybe so depending on player/deck 
#implementation, but idk
#-> what exactly does it mean for knownTypes length to be bigger than 1? saw something about superposition of colors,
#but how would we handle this for types (e.g. what exactly do we need to do to type if we have type length > 2?)
#-> how to handle make entangled? bc each card is its own circuit, right? how can we entangle someone else's card if it's
#on a diff circuit?
#-> should wild be a card? or is it more of a concept? bc we use the length of knownColors for superposition...
#-> I had to dip so i didn't finish/correct my logic for the interference card plis fix
