# %%
from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import List, Union


@total_ordering
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

    def __str__(self):
        return self.abv

    def __lt__(self, other):
        return self.value < other.value


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


@total_ordering
@dataclass
class Card:
    pip: Pip
    suit: Suit

    @classmethod
    def new(cls, pip: int, suit: int):
        return cls(pip=Pip(pip), suit=Suit(suit))

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

    def __eq__(self, other):
        return ((self.pip.value, self.suit.value) == (other.pip.value, other.suit.value))

    def __lt__(self, other):
        return ((self.pip.value, self.suit.value) < (other.pip.value, other.suit.value))


class Stack:
    def __init__(self, cards: Union[None, List[Card]] = None):
        if cards is not None:
            self.cards = cards
        else:
            self.cards = []

    @property
    def suits(self):
        suits = [card.suit for card in self]
        suits.sort()
        return suits

    @property
    def pips(self):
        pips = [card.pip for card in self]
        pips.sort()
        return pips

    @property
    def same_suits(self):
        if len(self) == 0:
            return 0
        else:
            return min(v for k, v in Counter(self.suits).items())

    @property
    def same_pips(self):
        if len(self) == 0:
            return 0
        else:
            return min(v for k, v in Counter(self.pips).items())

    def shuffle(self, seed=None):
        random.seed(seed)
        random.shuffle(self.cards)

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f'{self.cards}'

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.cards)

    @classmethod
    def new_stack(cls, cards: Union[None, List[Card]]):
        return Stack(cards=cards)

    @classmethod
    def new_empty(cls):
        return cls.new_stack(cards=None)

    @classmethod
    def merge_new(cls, stack_a: Stack, stack_b: Stack):
        return cls.new_stack(cards=stack_a.cards+stack_b.cards)

    def pop(self, index: int):
        return self.cards.pop(index)

    def top(self, n=1):
        return Stack.new_stack(cards=[self.pop(index=0) for i in range(n)])

    def remove(self, index_list: Union[int, List[int]] = [0]):
        if isinstance(index_list, int):
            index_list = list(range(index_list))
        index_list.sort(reverse=True)
        return Stack.new_stack(cards=[self.pop(index=index) for index in index_list])

    def add(self, cards: Union[List[Card], Card, Stack] = []):
        if isinstance(cards, Card):
            self.cards.append(cards)
        elif isinstance(cards, (Stack, Deck)):
            self.cards.extend(cards.cards)
        else:
            self.cards.extend(cards)


class Deck(Stack):
    def __init__(self, is_shuffle=False, seed=None):
        self.cards = [
            Card(pip, suit) for suit in Suit for pip in Pip
        ]
        if is_shuffle:
            self.shuffle(seed=seed)

    def deal(self, other: Union[Stack, None] = None, n=1):
        assert (other is None) or isinstance(other, Stack)
        cards = self.top(n=n)
        if other is None:
            return Stack.new_stack(cards=cards.cards)
        else:
            other.add(cards=cards)

    @classmethod
    def new(cls):
        return Deck(is_shuffle=True)

    @classmethod
    def new_sorted(cls):
        return Deck(is_shuffle=False)

# %%
