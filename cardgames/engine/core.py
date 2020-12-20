# %%
from cards import Deck, Card, Stack
from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections import namedtuple

class Game(ABC):
    pass


class Player:
    def __init__(self, name, hand: Stack = None, wallet=100):
        if hand is not None:
            self.hand = hand
        else:
            self.hand = Stack.new_empty()
        self.name = name
        self.wallet = wallet

    def __str__(self):
        return f'{self.name}: {str(self.hand)}'

    def __repr__(self):
        return str(self)

    def check_hand(self):
        value= sum([card.pip.value for card in self.hand])
        return value


@dataclass
class PokDeng(Game):
    players: list[Player]
    player_bets: list[float]
    dealer: Player

    @classmethod
    def init_state(self, n_player=3):
        return


num_player = 1
dealer = Player(name='dealer')
players = [Player(name=f'p{i}') for i in range(num_player)]

# Game session
# each player place bet
player_bets = [10]

# shuffle deck
deck = Deck(is_shuffle=True)

# deal 1 card each player including dealer
hands = 2

for i in range(hands):
    for p in players:
        deck.deal(p.hand, 1)
    deck.deal(dealer.hand, 1)

# check for player and dealer pokdeng

# session end if dealer pokdeng
# ask whether player will add one more card
# dealer decide to take one more cards
# check all cards and play bet
# %%

# %%
