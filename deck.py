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
        newColors, newTypes = self.newCard()

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


    def addType(self, typeArray):
        type = randint(0, 9) # 0-10 inclusive
        typeArray.append(card.Type(type))


    def newCard(self):
        """ Creates a new random card for self.topOfDeckColor.
        The Card() constructor will generate the internal quantum
        circuit. This method must simply specify the various colors
        and types the new Deck card will have.

        Returns the tuple (colors, types) for the new card.

        See Card class for the specifications on knownColors and knownTypes.
        """
        # Is this going to be a new superposition card?
        probOfSuperposition = 0.5
        probOfMakeEntangled = 0.2
        isMakeEntangled = random() < probOfMakeEntangled #TODO
        isSuperposition = random() < probOfSuperposition #only going to do a max of 2

        knownColors = []
        knownTypes = []
        self.addColor(knownColors)
        self.addType(knownTypes)

        if (isSuperposition):
            self.addColor(knownColors)
            temporaryTypes = []
            self.addType(temporaryTypes)
            while temporaryTypes[0] in knownTypes:
                temporaryTypes = []
                self.addType(temporaryTypes)
            knownTypes.append(temporaryTypes[0])

        return (knownColors, knownTypes)


    def newEntangled(self, color): # TODO
        """ Creates a new entangled card for the caller

        Creates a random new card for the caller.
        len(knownColors[]) == 0 and len(knownTypes[]) == 0

        This method will directly manipulate the internal quantum circuit
        See Card class for the specifications on knownColors and knownTypes.
        """
        knownColor = [color]
        knownType = [self.getType()]
        return card.Card(knownColor, knownType, isEntangled=True)
