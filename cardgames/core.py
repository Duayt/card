# %%
from cardgames.cards import Deck, Card, Stack
from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections import namedtuple
import numpy as np


class Game(ABC):
    pass


class Player:
    def __init__(self, name, hand: Stack = None, wallet=100, default_bet=10):
        if hand is not None:
            self.hand = hand
        else:
            self.hand = Stack.new_empty()
        self.name = name
        self.wallet = wallet
        self.logs = []
        self.default_bet = default_bet

    def __str__(self):
        return f'{self.name}: {str(self.wallet)}'

    def __repr__(self):
        return str(self)

    def check_hand(self):
        value = sum([card.pip.value for card in self.hand])
        return value

    def bet(self, bet=None):
        if bet is None:
            bet = self.default_bet
        return min(bet, self.wallet)


class Dealer(Player):
    def __init__(self, name='dealer', hand: Stack = None):
        super(Dealer, self).__init__(name=name, hand=hand,
                                     wallet=0, default_bet=None)

# %%
