import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
         'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        return f'{self.deck}'

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        # from Deck.deal() --> single Card(suit, rank)
        self.cards.append(card)
        self.value = values[card.rank]

        # track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        # if total value > 21 and i still have an ace
        # then change my ace to be 1, instead of 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chip:
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet?  '))
        except TypeError:
            print('Sorry please provide an integer')
        else:
            if chips.bet > chips.total:
                print(f'Sorry, you do not have enough chips! \n You have {chips.total}')
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        n = input('Hit or Stand? Enter h or s: ')
        if n[0].lower() == 'h':
            hit(deck, hand)
        elif n[0].lower() == 's':
            print('Player Stands! Dealer\'s Turn')
            playing = False
        else:
            print('Please enter h or s only!')
            continue
        break


def player_busts(player, dealer, chips):
    print('BUST PLAYER!')
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print('PLAYER WINS!')
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print('PLAYER WINS! DEALER BUSTED')
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print('DEALER WINS!')
    chips.lose_bet()


def push(player, dealer):
    print('Dealer and Player tie! PUSH')


test_deck = Deck()
test_deck.shuffle()

# Player
test_player = Hand()
# Deal 1 card from the deck Card(suit, rank)
pulled_card = test_deck.deal()
print(pulled_card)
test_player.add_card(pulled_card)
print(test_player.value)
