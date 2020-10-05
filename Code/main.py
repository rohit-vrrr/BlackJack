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
        single_card = self.deck.pop()
        return single_card


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
        except ValueError:
            print('Sorry please provide an integer')
        else:
            if chips.bet > chips.total:
                print(f'Sorry, you do not have enough chips! \n You have {chips.total}')
            else:
                break


def hit(deck_this, hand):
    hand.add_card(deck_this.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck_this, hand):
    global playing

    while True:
        n = input('Hit or Stand? Enter h or s: ')
        if n[0].lower() == 'h':
            hit(deck_this, hand)
        elif n[0].lower() == 's':
            print('Player Stands! Dealer\'s Turn')
            playing = False
        else:
            print('Please enter h or s only!')
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


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


# Game Manager
while True:

    print('\t\t\t\t\t\tWelcome to BlackJack')

    # Create & Shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up player chips
    player_chips = Chip()

    # Prompt player for their bet
    take_bet(player_chips)

    # Show cards
    show_some(player_hand, dealer_hand)

    while playing:

        # Prompt player to Hit or Stand
        hit_or_stand(deck, player_hand)

        show_some(player_hand, dealer_hand)

        # if player_hand exceeds 21, run player_bust
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # if player hasn't busted, play dealer's hand until dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # All different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    # Inform player of their remaining chips
    print(f'Player total chips are: {player_chips.total}')

    # Play again
    new_game = input('Would you like to play another hand? y/n:  ')
    if new_game[0] == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing!')
        break
