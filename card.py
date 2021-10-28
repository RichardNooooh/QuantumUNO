from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.visualization import plot_histogram, plot_state_qsphere, plot_bloch_multivector, plot_bloch_vector
from enum import Enum, auto
import heapq
from operator import itemgetter

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
    MAKE_ENTANGLED  = 9      # 1001
    ADD_PHASE       = 10     # 1010

    # "Super Special" Quantum Card
    ENTANGLED       = 11     # 1011


class Card:
    """ Represents a card in the game
    Attributes
    ----------------
    qc : QuantumCircuit
        The 7-qubit circuit that represents the underlying color and type of the
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

    @classmethod
    def recCZa(self, qc, a, Cr, Tr): # TODO add documentation here
        if len(Cr)<=1:
            if len(Cr)==1:          #if only 1 control bit, apply the C-gate
                qc.cu1(np.pi*a,Cr[0],Tr)
            else:                   #if no control bits, just apply the gate
                qc.u1(np.pi*a,Tr)
        else:
            nn=len(Cr)
            #apply C-sqrt(U)
            Card.recCZa(qc,a/2,[Cr[nn-1]],Tr)
        
            #recursively apply CCNot
            qc.h(Cr[nn-1])
            Card.recCZa(qc,1,Cr[0:nn-1],Cr[nn-1])
            qc.h(Cr[nn-1])
            
            #apply C-sqrt(U dg)
            Card.recCZa(qc,-a/2,[Cr[nn-1]],Tr)
            
            #recursively apply CCNot
            qc.h(Cr[nn-1])
            Card.recCZa(qc,1,Cr[0:nn-1],Cr[nn-1])
            qc.h(Cr[nn-1])
            
            #recursivle apply CC-sqrt(U)
            Card.recCZa(qc,a/2,Cr[0:nn-1],Tr)

    @classmethod
    def recTof(self, qc, Cr, Tr):
        qc.h(Tr)
        Card.recCZa(qc,1,Cr,Tr)
        qc.h(Tr)

    def initialize_qc(self):
        """ Initializes the internal quantum circuit to the knownColors/knownTypes
        
        Abstractly, this circuit implements an oracle for Grover's algorithm.
        For every card "state" (one state for a non-superposition card, two states
        for a superposition card) we want this object to represent, we use a
        multi-qubit Toffoli gate, filtering it out based on the bit representations
        of the color and type of the card state.

        """
        M = len(self.knownColor)
        toffoliQC = QuantumCircuit(7)
        Card.recTof(toffoliQC, toffoliQC.qubits[1:7], toffoliQC.qubits[0])

        for i in range(M):
            stateColor = self.knownColor[i]
            stateType = self.knownType[i]
            stateBinaryStr = np.binary_repr(stateColor.value, width=2) + np.binary_repr(stateType.value, width=4)
            xGateIndices = []
            for j in range(len(stateBinaryStr)):
                if stateBinaryStr[j] == '0':
                    xGateIndices.append(j+1)
            
            if (len(xGateIndices) > 0):
                self.qc.x(xGateIndices)

            self.qc += toffoliQC

            if (len(xGateIndices) > 0):
                self.qc.x(xGateIndices)


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
        self.qc = QuantumCircuit(7) # 1 output + 2 color + 4 type
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
        color and type. This card's quantum circuit stores an oracle.
        In order to find the true values of the card, we must use
        Grover's algorithm for M = 'len(self.knownColor)' solutions.

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
        """
        # W Circuit
        W = QuantumCircuit(7)

        W.h(W.qubits[1:7])
        W.x(W.qubits[1:7])

        Card.recCZa(W, 1, W.qubits[2:7], W.qubits[1])

        W.x(W.qubits[1:7])
        W.h(W.qubits[1:7])
        
        # Looping constant R
        M = len(self.knownColor)
        R = int(np.floor(np.pi * (np.sqrt(2**6/M)) / 4))

        # Grover's Algorithm
        measureQC = QuantumCircuit(7, 6)

        measureQC.x(0)
        measureQC.h(range(7))

        for _ in range(R):
            measureQC += self.qc
            measureQC += W

        measureQC.h(0)
        measureQC.x(0)

        for i in range(6):
            measureQC.measure(i+1,i)

        # Run it through the Aer Simulator
        print("   Please wait, our Grover monkeys are doing a lot of quantum magic...")
        backend = Aer.get_backend('aer_simulator')
        counts = execute(measureQC, backend, shots=1024).result().get_counts(measureQC) # takes a hot second

        # Look at the top M results
        topBitStrings = dict(heapq.nlargest(M, counts.items(), key=itemgetter(1))).keys()
        flippedBitStrings = []
        for bitString in topBitStrings:
            flippedBitStrings.append(bitString[::-1])

        # Interpret Results
        colors = []
        types = []
        for bitString in flippedBitStrings:
            measuredColor = (int(bitString, 2) & 0b110000) >> 4
            measuredType = int(bitString, 2) & 0b001111
            
            colors.append(Color(measuredColor))
            types.append(Type(measuredType))
        
        return (colors, types)
        

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
        
        pass


    def __str__(self):
        """ Prints out a representation of the current card to the console
        
        """
        returnString = ""
        for i in range(len(self.knownColor)):
            returnString += str(self.knownColor[i]) + "\n"
        for i in range(len(self.knownType)):
            returnString += str(self.knownType[i]) + "\n"

        return returnString
