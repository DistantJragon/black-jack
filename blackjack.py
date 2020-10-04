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
    decknumber = id // 52
    id = id % 52
    suitNumber = id // 13
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
    def __init__(self, playerNumber, isDealer = False):
        self.isDealer = isDealer
        self.playerNumber = playerNumber

        self.hand = []
        self.handIsSoft = False
        self.handWorth = 0
        self.hasBlackjack = False

        self.choice = ''
        self.isBust = False
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
        self.handWorth = totalWorth

numberOfPlayers = 0
while numberOfPlayers < 1:
    numberOfPlayers = input('Number of players: ')
    if is_string_integer(numberOfPlayers): numberOfPlayers = int(numberOfPlayers)
    else:
        print('Has to be a natural number')
        numberOfPlayers = 0
        continue
    if not(is_integer_natural(numberOfPlayers)):
        print('Has to be a natural number')
        numberOfPlayers = 0


numberOfDecks = 0
while numberOfDecks < 1:
    numberOfDecks = input('Number of decks: ')
    if is_string_integer(numberOfDecks): numberOfDecks = int(numberOfDecks)
    else:
        print('Has to be a natural number')
        numberOfDecks = 0
        continue
    if not(is_integer_natural(numberOfPlayers)):
        print('Has to be a natural number')
        numberOfDecks = 0
print('')

decks = []
for deck in range(numberOfDecks):
    decks.append(list(()))
    for suit in range(4):
        decks[deck].append(list(()))
        for card in range(13):
            decks[deck][suit].append(Card(deck, suit, card))

players = []
for playerNumber in range(numberOfPlayers):
    players.append(Player(playerNumber = playerNumber))
players.append(Player(playerNumber = playerNumber, isDealer = True))
dealer = players[-1]

numberOfAllOfTheCards = numberOfDecks * 52
shuffledDeck = list(range(numberOfAllOfTheCards))
random.shuffle(shuffledDeck)

for i in range(2):
    for player in players:
        tempCard = get_card_from_id(shuffledDeck[-1])
        player.hand.append(tempCard)
        shuffledDeck.pop()
dealer.hand[0].isFaceDown = True

gameTime = True
roundNumber = 0
while gameTime:
    choiceList = []

    print('Round #{}'.format(roundNumber + 1))
    for player in players:
        player.check_soft()
        player.check_worth_of_hand()

        if roundNumber == 0 and player.handWorth == 21: player.hasBlackjack = True
        if roundNumber == 1: dealer.hand[0].isFaceDown = False

        if not(player.isDealer):
            print('-------------------')
            print('Player {}\'s turn'.format(player.playerNumber + 1))
            print('-------------------')
            print('Dealer\'s Hand:')
            for card in dealer.hand:
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
                    if not(player.isDealer): print('Your first soft ace must harden to keep you in the game')
                    player.check_soft()
                    player.check_worth_of_hand()

                    if not(player.isDealer):
                        print('Your Hand:')
                        for card in player.hand: print(card.full_name())
                        print('')
                    break

        if player.handWorth > 21 and not(player.handIsSoft):
            if not(player.isDealer): print('Your hand exceeds 21 and you don\'t have a soft ace. You are bust')
            player.isBust = True

        if not(player.isDealer) and not(player.isBust):
            while not(player.choice == 'stand') and not(player.choice == 'hit'):
                player.choice = input('Hit or stand: ').lower()
                if not(player.choice == 'stand') and not(player.choice == 'hit'): print('Invalid input')

        if player.isBust == True:
            player.choice = 'stand'

        if player.isDealer:
            if player.handWorth < 17 or (player.handWorth == 17 and player.handIsSoft):
                player.choice = 'hit'
            elif player.handWorth >= 17 and not(player.handIsSoft):
                player.choice = 'stand'

        if player.choice == 'hit':
            tempCard = get_card_from_id(shuffledDeck[-1])
            player.hand.append(tempCard)
            shuffledDeck.pop()
            if player.isDealer: print('Dealer draws a(n) {}'.format(tempCard.full_name()))
            else: print('Player {} hits'.format(player.playerNumber + 1))
            player.hasBlackjack = False

        if player.choice == 'stand':
            if player.isDealer: print('Dealer stands')
            else: print('Player {} stands'.format(player.playerNumber + 1))
        print('')

        choiceList.append(player.choice)
        player.choice = ''

    allPlayersStand = True
    for choice in choiceList:
        if choice == 'hit':
            allPlayersStand = False

    if allPlayersStand:
        gameTime = False

    if gameTime: roundNumber += 1

print('Dealer ended with a hand totaling {}'.format(dealer.handWorth))
for player in players:
    if not(player.isDealer):
        currentPlayerString = 'Player {} '.format(player.playerNumber + 1)
        currentPlayerHandWorthString = ' {}'.format(player.handWorth)
        if player.isBust:
            print(currentPlayerString + 'loses with' + currentPlayerHandWorthString)
            continue
        if player.handWorth == 21:
            if dealer.handWorth == 21:
                print(currentPlayerString + 'pushes')
            elif player.hasBlackjack:
                print(currentPlayerString + 'wins and gets a bonus for having a blackjack')
            else:
                print(currentPlayerString + 'wins with' + currentPlayerHandWorthString)
            continue
        elif player.handWorth < 21:
            if player.handWorth > dealer.handWorth or dealer.handWorth > 21:
                print(currentPlayerString + 'wins with' + currentPlayerHandWorthString)
            elif player.handWorth == dealer.handWorth:
                print(currentPlayerString + 'pushes')
            elif player.handWorth < dealer.handWorth:
                print(currentPlayerString + 'loses with' + currentPlayerHandWorthString)
print('The game lasted {} rounds'.format(roundNumber + 1))