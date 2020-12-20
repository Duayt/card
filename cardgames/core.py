# %%
from cardgames.cards import Deck, Card, Stack
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



