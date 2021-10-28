from random import random, randint
import heapq
from operator import itemgetter
from qiskit import QuantumCircuit, Aer, execute
import numpy as np
import card

class Deck:
    """ Generates random cards for the players to have

    Unlike normal UNO, the color of the top card of the deck is 
    always revealed to the players. This is to accommodate the Add Phase card.

    The top of the deck is a special kind of "card object", and
    is entirely different from the Card class. Since players
    need to be able to add RY(pi/2) gates to the color[0] qubit,
    storing the quantum state as a single recursive toffoli gate
    will not work with the Grover's algorithm measurement.

    If the top card is a superposition card (len(deckColors) > 1), we
    store the quantum circuit of the first color in deckColors. We
    also create a mapping from the possible first colors to the second
    colors.
    """

    def initColorCircuit(self):
        firstColor = self.deckColors[0]
        if firstColor == card.Color.RED:
            self.colorQC.i((0, 1))
        elif firstColor == card.Color.BLUE:
            self.colorQC.x(0)
        elif firstColor == card.Color.YELLOW:
            self.colorQC.x(1)
        elif firstColor == card.Color.GREEN:
            self.colorQC.x((0, 1)) 

    
    # FOR MEASUREMENT
    def initColorDictionary(self):
        self.colorDict = {}
        if len(self.deckColors) > 1:
            self.colorDict[self.deckColors[0]] = self.deckColors[1]
            self.colorDict[self.deckColors[0].getOppositeColor()] = self.deckColors[1].getOppositeColor()

    
    def resetTopCard(self):
        newColors, newTypes, isMakeEntangled = self.newCard()

        # stores the "true state" of the top card
        self.deckColors = newColors
        self.deckTypes = newTypes
        
        assert len(self.deckColors) == len(self.deckTypes)

        self.colorQC = QuantumCircuit(2, 2)
        self.initColorCircuit()


        self.initColorDictionary()
        # stores each potential color in a tuple, one for each state.
        # example: Red/Green superposition card with RY phase pi/2
        #           topOfDeckColor should store (Red, Green), (Blue, Yellow)
        self.ryGateCount = 0 #for printing purposes
        self.topOfDeckColor = []
        if len(self.deckColors) > 1:
            self.topOfDeckColor = [(self.deckColors[0], self.deckColors[1])]
        else:
            self.topOfDeckColor = [(self.deckColors[0], None)]



    def __init__(self):
        self.resetTopCard()

    
    def addRYPhase(self):
        self.ryGateCount += 1
        self.colorQC.ry(np.pi / 2, 0)

        if self.ryGateCount % 4 == 0:
            if len(self.deckColors) > 1:
                self.topOfDeckColor = [(self.deckColors[0], self.deckColors[1])]
            else:
                self.topOfDeckColor = [(self.deckColors[0], None)]

        elif self.ryGateCount % 4 == 1 or self.ryGateCount % 4 == 3:
            if len(self.deckColors) > 1:
                self.topOfDeckColor = [(self.deckColors[0], self.deckColors[1]), \
                                    (self.deckColors[0].getOppositeColor(), self.deckColors[1].getOppositeColor())]
            else:
                self.topOfDeckColor = [(self.deckColors[0], None), \
                                    (self.deckColors[0].getOppositeColor(), None)]
        elif self.ryGateCount % 4 == 2:
            if len(self.deckColors) > 1:
                self.topOfDeckColor = [(self.deckColors[0].getOppositeColor(), self.deckColors[1].getOppositeColor())]
            else:
                self.topOfDeckColor = [(self.deckColors[0].getOppositeColor(), None)]


    def getTopCard(self):
        # measure the color circuit
        self.colorQC.measure(0, 0)
        self.colorQC.measure(1, 1)

        backend = Aer.get_backend('aer_simulator')
        counts = execute(self.colorQC, backend, shots=1024).result().get_counts(self.colorQC) # takes a hot second

        topBitString = heapq.nlargest(1, counts.items(), key=itemgetter(1))[0][0]
        measuredColor = [card.Color(int(topBitString, 2))]

        if len(self.deckColors) > 1:
            measuredColor.append(self.colorDict[measuredColor[0]])

        topCard = card.Card(measuredColor, self.deckTypes)

        # reset top card
        self.resetTopCard()

        return topCard


    def addColor(self, colorArray):
        color = randint(0, 3)
        colorArray.append(card.Color(color))


    def addType(self, typeArray, isMakeEntangled):
        if not isMakeEntangled:
            type = randint(0, 9) # 0-10 inclusive
        else:
            type = randint(10, 15) # 10-15 inclusive

        typeArray.append(card.Type(type))


    def newCard(self): #TODO reconsider if I need to send isMakeEntangled a part of the return tuple
        """ Creates a new random card for self.topOfDeckColor.
        The Card() constructor will generate the internal quantum
        circuit. This method must simply specify the various colors
        and types the new Deck card will have.

        Returns the tuple (colors, types, isMakeEntangled) for the new card.

        See Card class for the specifications on knownColors and knownTypes.
        """

        probOfMakeEntangled = 1
        probOfSuperposition = 0.5
        isMakeEntangled = random() < probOfMakeEntangled
        isSuperposition = random() < probOfSuperposition

        knownColors = []
        knownTypes = []
        self.addColor(knownColors)
        self.addType(knownTypes, isMakeEntangled)

        # I do not want superposition cards to be make entangled cards
        if isSuperposition and not isMakeEntangled:
            self.addColor(knownColors)
            temporaryTypes = []
            self.addType(temporaryTypes, False)

            # Ensure that a card is not a duplicate of itself
            while temporaryTypes[0] in knownTypes:
                temporaryTypes = []
                self.addType(temporaryTypes, False)
            knownTypes.append(temporaryTypes[0])

        return (knownColors, knownTypes, isMakeEntangled)


    def newEntangled(self, cardColor):
        """ Creates an entangled pair of cards for the caller

        This function returns a tuple of two elements:
            [0] - A tuple of Color/Type, representing the output
                  of an entanglement measurement done by the first player
            [1] - An "isEntangled" card, representing an unmeasured entangled
                  card for the next player.

        We use a quantum circuit to emulate the process of entangling the
        two cards, by creating a 2-qubit quantum circuit that represents
        the bell state (|01> + |10>)/sqrt(2). Qubit 0 represents
        the original player and qubit 1 represents the next player.
        Let the bit value 0 represent cardColor[0], while the bit value 
        1 represents cardColor[1]. 
        
        If we measure qubit 0 and read the bit 0, we know that qubit 1 must
        have the bit value 1. This is analogous to the original player 
        receiving a card with cardColor[0], and then knowing that the
        next player must have a card with cardColor[1].
        
        Similarly, if we measure qubit 0 and read 1, qubit 1 must have the
        bit 0: the original player receives cardColor[1] and then knows that
        the next player has cardColor[0].
        """
        # use entanglement to emulate card color entanglement
        qc = QuantumCircuit(2, 1)
        qc.h(0)
        qc.x(1)
        qc.cx(0, 1)
        qc.measure(0, 0)
        backend = Aer.get_backend('aer_simulator')
        counts = execute(qc, backend, shots=1024).result().get_counts(qc)
        topBitString = heapq.nlargest(1, counts.items(), key=itemgetter(1))[0][0]

        currCardColor = None
        nextCardColor = None
        if topBitString == '0':
            currCardColor = cardColor[0]
            nextCardColor = cardColor[1]
        elif topBitString == '1':
            currCardColor = cardColor[1]
            nextCardColor = cardColor[0]
        else:
            assert False

        # the first player already "measured" their card
        currCardType = []
        self.addType(currCardType, False)

        # the next player has not "measured" their card yet
        nextCardType = []
        self.addType(nextCardType, False)
        
        return ((currCardColor, currCardType), \
            card.Card([nextCardColor], nextCardType, isEntangled=True))
