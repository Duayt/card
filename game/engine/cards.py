# %%
from dataclasses import dataclass
from enum import Enum


class Pip(Enum):
    def __init__(self, id, code, display, unicode=None):
        self.id = id
        self.code = code
        self.display = display

        if unicode is None:
            self.unicode = str(self.id)
        else:
            self.unicode = unicode

    Ace = 1, 'ace', 'A'
    Deuce = 2, 'deuce', '2'
    Three = 3, 'three', '3'
    Four = 4, 'fourt', '4'
    Five = 5, 'five', '5'
    Six = 6, 'six', '6'
    Seven = 7, 'seven', '7'
    Eight = 8, 'eight', '8'
    Nine = 9, 'nine', '9'
    Ten = 10, 'ten', '10', 'A'
    Jack = 11, 'jack', 'J', 'B'
    Queen = 12, 'queen', 'Q', 'C'
    King = 13, 'king', 'K', 'D'


class Suit(Enum):
    def __init__(self, id, code, display, unicode):
        self.id = id
        self.code = code
        self.display = display

        if unicode is None:
            self.unicode = str(self.id)
        else:
            self.unicode = unicode

    Club = 1, 'club', '♣', 'A'
    Heart = 2, 'heart', '♥', 'B'
    Diamond = 3, 'diamond', '♦', 'C'
    Spade = 4, 'spade', '♠', 'D'


@dataclass
class Card:
    pip: Pip
    suit: Suit

    def __str__(self):
        return f'{self.pip.display}{self.suit.display}'

    def unicode(self):
        code= f'\\U0001F0{self.suit.unicode}{self.pip.unicode}'
        return code.encode().decode('unicode_escape')
        
# %%
