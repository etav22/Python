# Imports
import numpy as np
import random

# Initial Setup
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9,
          'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


# Class Instantiation
class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]
        self.name = rank + ' of ' + suit

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:

    def __init__(self):

        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal(self):
        return self.all_cards.pop()


class Player:

    def __init__(self):
        self.name = input("What's your name? ")
        while True:
            try:
                self.balance = int(input("How many chips do you have? "))
            except ValueError or TypeError:
                print("HEY! That's not a numeric value. Try again :)")
            else:
                break

    def add_balance(self, amount):
        self.balance += amount
        print('New Balance: ', self.balance)

    def deduct_balance(self, amount):
        self.balance -= amount
        print('New Balance: ', self.balance)

    def __str__(self):
        return f'Elias has {str(self.balance)} chips left!'


def bet(player_balance):
    while True:
        try:
            bet_amount = int(input("How much would you like to bet? "))
            if bet_amount > player_balance:
                print('>:( Fool, you cannot bet more than you have. Try again.')
                continue
        except ValueError or TypeError:
            print("Please try entering the amount in a numeric format.")
        else:
            print("Thank you. Now prepare to lose that amount to the almighty dealer, muahahaha!")
            return bet_amount


def hit_or_stand():
    choice = None

    while choice not in ['h', 's']:
        choice = input("Would you like to hit or stand (H/S)? ").lower()

    return choice


def check_bust(hand_value):
    return hand_value > 21


def play_again():
    choice = None

    while choice not in ['y', 'n']:
        choice = input("Would you like to play again (Y/N)? ").lower()

    return choice == 'y'


def ace_check(hand, used=None):
    ace_counter = 0
    for card in hand:
        if card.rank == 'Ace':
            ace_counter += 1 - used
    return ace_counter


if __name__ == '__main__':

    game_on = True
    round_on = True
    print("Welcome to the blackjack table!")

    player = Player()
    while game_on:

        # Creating and shuffling the cards
        deck = Deck()
        deck.shuffle()

        # Get the player's initial bet
        bet_amount = bet(player.balance)

        # Creating the player's hand
        player_cards = [deck.deal() for i in range(2)]

        print(f"{player.name}, here are your two cards: {player_cards[0].name} + {player_cards[1].name}")

        # Setting aces used to zero
        aces_used = 0

        # Player's turn
        player_turn = True
        while player_turn:
            # Player's turn
            choice = hit_or_stand()
            if choice == 'h':
                new_card = deck.deal()
                print(f"You got the {new_card.rank} of {new_card.suit} ")
                player_cards.append(new_card)
                player_cards_total = sum([player_cards[i].value for i in range(len(player_cards))])
                aces = ace_check(player_cards, aces_used)
                player_bust = check_bust(player_cards_total)
                if player_bust and aces == 0:
                    print(f"You went bust at {player_cards_total} :(")
                    player_turn = False
                elif player_bust and aces > 0:
                    player_cards_total -= 10
                    aces_used += 1
            else:
                player_cards_total = sum([player_cards[i].value for i in range(len(player_cards))])
                print(f"You have stayed with a total of: {player_cards_total}.")
                player_turn = False
                player_bust = False

        # If player busted, then skip the dealer's turn
        if player_bust:
            player.deduct_balance(bet_amount)
            print(f"Your new total balance is {player.balance}.")
            continue
        else:
            dealer_turn = True
            dealer_cards = [deck.deal() for i in range(2)]

            # Resetting the aces used
            aces_used = 0

            while dealer_turn:
                dealer_cards_total = sum([dealer_cards[i].value for i in range(len(dealer_cards))])

                if dealer_cards_total <= player_cards_total:
                    dealer_cards.append(deck.deal())
                    dealer_cards_total = sum([dealer_cards[i].value for i in range(len(dealer_cards))])
                    dealer_bust = check_bust(dealer_cards_total)
                    aces = ace_check(dealer_cards, aces_used)
                    if dealer_bust and aces == 0:
                        print(f"The dealer has gone bust at {dealer_cards_total}!")
                        dealer_turn = False
                    elif dealer_bust and aces > 0:
                        dealer_cards_total -= 10
                        aces_used += 1
                else:
                    dealer_turn = False
                    dealer_bust = False
                    print(f"The dealer has a total of: {dealer_cards_total}, you have lost.")

        if player_cards_total > dealer_cards_total or dealer_bust is True:
            player.add_balance(bet_amount)
        else:
            player.deduct_balance(bet_amount)

        print(f"Your new total balance is {player.balance}.")

        if player.balance == 0:
            print("Get your broke ass out of my casino.")
            break

        game_on = play_again()

    print('Thanks for playing, come again soon!')



