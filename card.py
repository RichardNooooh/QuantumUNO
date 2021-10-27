from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.visualization import plot_histogram, plot_state_qsphere, plot_bloch_multivector, plot_bloch_vector
from enum import Enum, auto

import player, quno
import numpy as np


class Color(Enum):
    """ Represents the color of the card

    We encode the color with two qubits

    """
    RED     = 0     # 00
    BLUE    = 1     # 01
    YELLOW  = 2     # 10
    GREEN   = 3     # 11

class Type(Enum):
    """ Represents the type of the card

    We encode the type with five qubits.

    """
    # Standard Normal Number Cards
    NUM_ONE         = 0      # 0000
    NUM_TWO         = 1      # 0001
    NUM_THREE       = 2      # 0010
    NUM_FOUR        = 3      # 0011
    NUM_FIVE        = 4      # 0100
    NUM_SIX         = 5      # 0101
    NUM_SEVEN       = 6      # 0110
    NUM_EIGHT       = 7      # 0111
    NUM_NINE        = 8      # 1000
    
    # Special Quantum Cards
    MAKE_ENTANGLED  = 9      # 1000
    ADD_PHASE       = 10     # 1010

    # "Super Special" Quantum Card
    ENTANGLED       = 11     # 1001


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
        If the length of knownColor is 1, this card is a single-colored card.
        If the length of knownColor is 2, this is a superposition card. The length should
        never be larger than 2.
    knownType : Type[]
        A list that represents the type(s) of the card that the Player knows.
        The length of knownType must be the same as the length of knownColor.
    """

    def initialize_qc(self):
        """ Initializes the internal quantum circuit to the knownColors/knownTypes
        
        Abstractly, this circuit implements an oracle for Grover's algorithm.
        For every card "state" (one state for a non-superposition card, two states
        for a superposition card) we want this object to represent, we use a
        multi-qubit Toffoli gate, filtering it out based on the bit representations
        of the color and type of the card state.

        """
        pass #TODO 


    def __init__(self, colors, types, isEntangled=False): #TODO allow for an empty constructor for Entangled cards
        # Parameter checks
        assert type(colors) is list and type(colors[0]) is Color, \
              "ERROR in Card.__init__() - The type of 'colors' is wrong: " \
              + str(type(colors[0])) + " instead of Color."
        assert type(types) is list and type(types[0]) is Type, \
              "ERROR in Card.__init__() - The type of 'types' is wrong: " \
              + str(type(types[0])) + " instead of Type."
        assert len(colors) == len(types), \
              "ERROR in Card.__init__() - The length of 'colors' and 'types' must be the same."
        assert len(colors) > 0, \
              "ERROR in Card.__init__() - The length of 'colors' and 'types' must be greater than 0."
        
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
        self.isEntangled = isEntangled
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
        had the most number of hits.
        Before this method returns:
            Returns a tuple (Color, Type) of the result,
            Sets the knownCard and knownType fields to the result, and
            Sets wasMeasured to True.
        """ # TODO use grover's algo
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
        assert type(nextPlayer) is player.Player, \
              "ERROR in Card.action() - nextPlayer parameter is not a Player."
        assert type(game) is quno.Game, \
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
        returnString = ""
        for i in range(len(self.knownColor)):
            returnString += str(self.knownColor[i]) + "\n"
        for i in range(len(self.knownType)):
            returnString += str(self.knownType[i]) + "\n"

        return returnString
