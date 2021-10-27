from random import random, randint
import card

class Deck:
    """ Generates random cards for the players to have
    """
    
    @staticmethod
    def addColor(colorArray): #TODO make an enum classmethod to handle this better
        color = randint(0, 4)
        if color == card.Color.RED.value:
            colorArray.append(card.Color.RED)
        elif color == card.Color.BLUE.value:
            colorArray.append(card.Color.BLUE)
        elif color == card.Color.GREEN.value:
            colorArray.append(card.Color.GREEN)
        else:
            colorArray.append(card.Color.YELLOW)

    @staticmethod
    def addType(typeArray): #TODO make an enum classmethod to handle this better
        type = randint(0, 10) # 0-10 inclusive
        if   type == card.Type.NUM_ONE.value:
            typeArray.append(card.Type.NUM_ONE)
        elif type == card.Type.NUM_TWO.value:
            typeArray.append(card.Type.NUM_TWO)
        elif type == card.Type.NUM_THREE.value:
            typeArray.append(card.Type.NUM_THREE)
        elif type == card.Type.NUM_FOUR.value:
            typeArray.append(card.Type.NUM_FOUR)
        elif type == card.Type.NUM_FIVE.value:
            typeArray.append(card.Type.NUM_FIVE)
        elif type == card.Type.NUM_SIX.value:
            typeArray.append(card.Type.NUM_SIX)
        elif type == card.Type.NUM_SEVEN.value:
            typeArray.append(card.Type.NUM_SEVEN)
        elif type == card.Type.NUM_EIGHT.value:
            typeArray.append(card.Type.NUM_EIGHT)
        elif type == card.Type.NUM_NINE.value:
            typeArray.append(card.Type.NUM_NINE)
        elif type == card.Type.MAKE_ENTANGLED.value:
            typeArray.append(card.Type.MAKE_ENTANGLED)
        elif type == card.Type.ADD_PHASE.value:
            typeArray.append(card.Type.ADD_PHASE)
        else:
            print("Something messed up in getType(): type=" + str(type))

    @staticmethod
    def newCard():
        """ Creates a new random card for the caller
        The Card() constructor will generate the internal quantum
        circuit. This method must simply specify the various colors
        and types the new card will have.
        See Card class for the specifications on knownColors and knownTypes.
        """
        # Is this going to be a new superposition card?
        probOfSuperposition = 0.5 #TODO receive input from console here
        isSuperposition = random() < probOfSuperposition #only going to do a max of 2

        knownColors = []
        knownTypes = []
        Deck.addColor(knownColors)
        Deck.addType(knownTypes)

        if (isSuperposition): #TODO handle the case where both cards are the same in the superposition
            Deck.addColor(knownColors)
            Deck.addType(knownTypes)

        return card.Card(knownColors, knownTypes)

    @staticmethod
    def newEntangled():
        """ Creates a new entangled card for the caller

        Creates a random new card for the caller.
        len(knownColors[]) == 0 and len(knownTypes[]) == 0

        This method will directly manipulate the internal quantum circuit
        See Card class for the specifications on knownColors and knownTypes.
        """
        pass #TODO implement
