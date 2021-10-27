from card import Color, Type, Card
from random import randint
class Deck:
    """ Generates random cards for the players to have
    """
    
    @staticmethod
    def newCard():
        """ Creates a new random card for the caller
        The Card() constructor will generate the internal quantum
        circuit. This method must simply specify the various colors
        and types the new card will have.
        See Card class for the specifications on knownColors and knownTypes.
        """
        knownColors = []
        colorNum = randint(0, 2)
        for i in range(colorNum):
            color = randint(0, 4)
            if color == Color.RED.value:
                knownColors.append(Color.RED)
            elif color == Color.BLUE.value:
                knownColors.append(Color.BLUE)
            elif color == Color.GREEN.value:
                knownColors.append(Color.GREEN)
            else:
                knownColors.append(Color.YELLOW)

        #TODO what to do for types? a little confused on len > 1 thing
        knownTypes = []
        type = randint(0, 9)
        if type == Type.NUMBER.value:
            knownTypes.append(Type.NUMBER)
        elif type == Type.SKIP.value:
            knownTypes.append(Type.SKIP)
        elif type == Type.REVERSE.value:
            knownTypes.append(Type.REVERSE)
        elif type == Type.DRAW_2.value:
            knownTypes.append(Type.DRAW_2)
        elif type == Type.WILD_DRAW_4.value:
            knownTypes.append(Type.WILD_DRAW_4)
        elif type == Type.WILD.value:
            knownTypes.append(Type.WILD)
        elif type == Type.MAKE_ENTANGLED.value:
            knownTypes.append(Type.MAKE_ENTANGLED)
        elif type == Type.ENTANGLED.value:
            knownTypes.append(Type.ENTANGLED)
        else:
            knownTypes.append(Color.INTERFERENCE)
        return Card(knownColors, knownTypes)

    @staticmethod
    def newEntangled():
        """ Creates a new entangled card for the caller
        TODO documentation
        See Card class for the specifications on knownColors and knownTypes.
        """
        pass
