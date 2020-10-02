import random
def is_string_integer(string):
    try: int(string)
    except ValueError: return False
    else: return True
def is_integer_natural(integer):
    if integer < 1: return False
    else: return True

def get_card_value_from_card_number(cardNumber):
    if cardNumber == 0: value = 11
    elif cardNumber >= 1:
        value = cardNumber + 1
        if value > 10:
            value = 10
    
    return value

def get_card_from_id(id):
    decknumber = id = id % 51
    suitNumber = id = id % 12
    cardNumber = id
    return decks[decknumber][suitNumber][cardNumber]

suitList = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
cardList = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
class Card:
    def __init__(self, deckNumber, suitNumber, cardNumber):
        self.deckNumber = deckNumber
        self.suitNumber = suitNumber
        self.cardNumber = cardNumber

        self.suitName = suitList[suitNumber]
        self.cardName = cardList[cardNumber]
        self.cardFullName = '{} of {}'.format(self.cardName, self.suitName)

        self.cardID = (deckNumber * 51) + (suitNumber * 12) + cardNumber
        self.worth = get_card_value_from_card_number(cardNumber)
    def softify(self):
        if self.suitNumber != 0: raise Exception('Tried to make a card that wasn\'t an ace soft')
        else:
            self.worth = 1

class Player:
    def __init__(self):
        self.hand = []
        self.isSoft = False
    def check_soft(self):
        tempSoft = False
        for card in self.hand:
            if card.worth == 11: tempSoft = True
        self.isSoft = tempSoft

numberOfPlayers = 0
while numberOfPlayers < 1:
    numberOfPlayers = 0
    numberOfPlayers = input('Number of players: ')
    if is_string_integer(numberOfPlayers): numberOfPlayers = int(numberOfPlayers)
    else:
        print('Has to be a natural number')
        numberOfPlayers = 0
        continue
    if is_integer_natural(numberOfPlayers) == False:
        print('Has to be a natural number')
        numberOfPlayers = 0


numberOfDecks = 0
while numberOfDecks < 1:
    numberOfDecks = 0
    numberOfDecks = input('Number of decks: ')
    if is_string_integer(numberOfDecks): numberOfDecks = int(numberOfDecks)
    else:
        print('Has to be a natural number')
        numberOfDecks = 0
        continue
    if is_integer_natural(numberOfPlayers) == False:
        print('Has to be a natural number')
        numberOfDecks = 0

decks = []
for deck in range(numberOfDecks):
    decks.append(list(()))
    for suit in range(4):
        decks[deck].append(list(()))
        for card in range(13):
            decks[deck][suit].append(Card(deck, suit, card))

numberOfAllOfTheCards = numberOfDecks * 52
shuffledDeck = list(range(numberOfAllOfTheCards))
random.shuffle(shuffledDeck)