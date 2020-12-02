# %%
from collections import namedtuple
import itertools
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union
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
    def __init__(self, cards: Union[None, List[Card]]):
        self.cards = cards

    def shuffle(self, seed=None):
        random.shuffle(self.cards, seed)

    def __str__(self):
        return f'Stack {len(self)} cards: \n {self.cards}'

    @classmethod
    def new_stack(cls,cards: Union[None, List[Card]]):
        return Stack(cards=cards)

    @classmethod
    def new_empty(cls):
        return cls.new_stack(cards=[])

    @classmethod
    def merge_new(cls,stack_a:Stack,stack_b:Stack):
        return cls.new_stack(cards=stack_a.cards+stack_b.cards)

    def __len__(self):
        return len(self.cards)

    def pop(self, index: int):
        return self.cards.pop(index)

    def top(self, n_cards=1):
        return Stack.new_stack(cards=[self.pop(index=0) for i in range(n_cards)])

    def remove(self, index_list: Union[int, List[int]] = [0]):
        if isinstance(index_list, int):
            index_list = list(range(index_list))
        index_list.sort(reverse=True)
        return Stack.new_stack(cards=[self.pop(index=index) for index in index_list])

    def add(self, card_list: Union[List[Card], Card] = []):
        if isinstance(card_list, Card):
            self.cards.append(card_list)
        else:
            self.cards.extend(card_list)



    # def deal_to(target_stack:Stack,n_cards=1,index=0):
    #     card_dealt=self.top(n_cards)


class Deck(Stack):
    def __init__(self, is_shuffle=False, seed=None):
        self.cards = [
            Card(pip, suit) for suit in Suit for pip in Pip
        ]
        if is_shuffle:
            self.shuffle(seed=seed)

    def __str__(self):
        return f'Decks {len(self)} cards: \n {self.cards}'

    @classmethod
    def new(cls):
        return Deck(is_shuffle=True)

    @classmethod
    def new_sorted(cls):
        return Deck(is_shuffle=False)


a_deck = Deck.new()
a_card = Card(pip=Pip.Ace, suit=Suit.Spade)
b_deck= Deck.new_sorted()
c_stacks=Deck.merge_new(a_deck,b_deck)
print(a_deck)
print(a_card)
a_deck.add(a_card)
print(a_deck)

a_deck.add([a_card,a_card])
print(a_deck)
# %%
