# %%
from collections import namedtuple
import itertools
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import random


class EnumWithAttrs(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, label, abv, unicode):
        self.label = label
        self.abv = abv
        if unicode is None:
            self.unicode = self.value
        else:
            self.unicode = unicode


class Pip(EnumWithAttrs):
    Ace = 'ace', 'A', None
    Deuce = 'deuce', '2', None
    Three = 'three', '3', None
    Four = 'fourt', '4', None
    Five = 'five', '5', None
    Six = 'six', '6', None
    Seven = 'seven', '7', None
    Eight = 'eight', '8', None
    Nine = 'nine', '9', None
    Ten = 'ten', '10', 'A'
    Jack = 'jack', 'J', 'B'
    Queen = 'queen', 'Q', 'C'
    King = 'king', 'K', 'D'


class Suit(EnumWithAttrs):
    Club = 'club', '♣', 'A'
    Heart = 'heart', '♥', 'B'
    Diamond = 'diamond', '♦', 'C'
    Spade = 'spade', '♠', 'D'


@dataclass
class Card:
    pip: Pip
    suit: Suit

    def __str__(self):
        return f'{self.pip.abv}{self.suit.abv}'

    def __hash__(self):
        return hash((self.pip.label, self.suit.label))

    def __repr__(self):
        # return str((self.pip.abv,self.suit.abv))
        return self.__str__()

    def unicode(self):
        code = f'\\U0001F0{self.suit.unicode}{self.pip.unicode}'
        return code.encode().decode('unicode_escape')


class Stack:
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def shuffle(self, seed=None):
        random.shuffle(self.cards, seed)


class Deck(Stack):
    def __init__(self, is_shuffle=False, seed=None):
        self.cards = [
            Card(pip, suit) for suit in Suit for pip in Pip
        ]
        if is_shuffle:
            self.shuffle(seed=seed)

    @classmethod
    def new(self) -> 'Deck':
        return Deck(is_shuffle=True)

    @classmethod
    def new_sorted(self) -> 'Deck':
        return Deck(is_shuffle=False)


sample_deck = Deck.new()
sample_deck.cards
# %%
