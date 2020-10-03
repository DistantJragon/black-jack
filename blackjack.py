import random
import math
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
    decknumber = math.floor(id / 52)
    id = id % 52
    suitNumber = math.floor(id / 13)
    id = id % 13
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
        self.textureName = ''

        self.cardID = (deckNumber * 52) + (suitNumber * 13) + cardNumber
        self.worth = get_card_value_from_card_number(cardNumber)
        self.isFaceDown = False
    def softify(self):
        if self.cardNumber != 0: raise Exception('Tried to make a card that wasn\'t an ace soft')
        else:
            self.worth = 1
    def full_name(self):
        if self.cardNumber == 0:
            if self.worth == 11: self.textureName = ' (Soft)'
            elif self.worth == 1: self.textureName = ' (Hard)' 
        tempCardFullName = '{} of {}{}'.format(self.cardName, self.suitName, self.textureName)
        return tempCardFullName

class Player:
    def __init__(self, isDealer = False):
        self.isDealer = isDealer

        self.hand = []
        self.handIsSoft = False
        self.handWorth = 0

        self.choice = ''
        self.canChooseNow = True
        self.hasAbilityToChoose = True
        if self.isDealer:
            self.hasAbilityToChoose = False
    def check_soft(self):
        tempSoft = False
        for card in self.hand:
            if card.worth == 11: 
                tempSoft = True
                break
        self.handIsSoft = tempSoft
    def check_worth_of_hand(self):
        totalWorth = 0
        for card in self.hand: totalWorth += card.worth
        self.worth = totalWorth

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

players = []
for player in range(numberOfPlayers):
    players.append(Player())
players.append(Player(isDealer = True))

numberOfAllOfTheCards = numberOfDecks * 52
shuffledDeck = list(range(numberOfAllOfTheCards))
random.shuffle(shuffledDeck)

for i in range(2):
    for player in players:
        tempCard = get_card_from_id(shuffledDeck[-1])
        player.hand.append(tempCard)
        shuffledDeck.pop()
players[-1].hand[0].isFaceDown = True

gameTime = True
roundNumber = 0
while gameTime:
    for player in players:
        player.check_soft()
        player.check_worth_of_hand()

        if player.isDealer == False:
            print('Dealer\'s Hand:')
            for card in players[-1].hand:
                if card.isFaceDown == True: print('*Face Down*')
                else: print(card.full_name())
            print('')

            print('Your Hand:')
            for card in player.hand: print(card.full_name())
            print('')

        while player.handWorth > 21 and player.handIsSoft:
            for card in player.hand:
                if card.worth == 11:
                    card.worth = 1
                    if player.isDealer == False: print('Your first soft ace must harden to keep you in the game')
                    player.check_soft()
                    player.check_worth_of_hand()

                    if player.isDealer == False:
                        print('Your Hand:')
                        for card in player.hand: print(card.full_name())
                        print('')
        if player.handWorth > 21 and player.handIsSoft == False:
            if player.isDealer == False: print('Your hand exceeds 21 and you don\'t have a soft ace. You are bust')
            player.hasAbilityToChoose = False
    roundNumber += 1