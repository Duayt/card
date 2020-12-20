# %%
from dataclasses import dataclass
from .core import Player, Deck, Game, Stack,Card
from collections import Counter
# >>> mylist = [20, 30, 25, 20, 30]
# >>> max(k for k,v in Counter(mylist).items() if v>1)
# 30


class PokDengHand(Stack):

    def get_bet_multipler(self):
        suits = [card.suit for card in self]
        if 1 <= len(self) <= 3:
            return max(v for k, v in Counter(suits).items())
        else:
            raise ValueError('Hand more than 2')

    def get_value(self):
        return int(str(sum(card.pip.value for card in self.cards))[-1])


@dataclass
class PokDeng(Game):
    players: list[Player]
    player_bets: list[float]
    dealer: Player

    @classmethod
    def init_state(self, n_player=3):
        return


num_player = 1
dealer = Player(name='dealer', hand=PokDengHand())
players = [Player(name=f'p{i}', hand=PokDengHand()) for i in range(num_player)]

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
