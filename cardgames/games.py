# %%
from dataclasses import dataclass
from cardgames.core import Player, Deck, Game, Stack, Card
from cardgames.cards import Pip, Suit
from collections import Counter


class PokDengRules:
    rule_JKQ: bool = False
    rule_order: bool = False
    rule_tripple: bool = False

    @classmethod
    @property
    def rules(cls):
        return (cls.rule_JKQ, cls.rule_order, cls.rule_tripple)

    @classmethod
    def set_rules(cls, rules: tuple[bool, bool, bool] = (True, True, True)):
        cls.rule_JKQ = rules[0]
        cls.rule_order = rules[1]
        cls.rule_tripple = rules[2]


class PokDengHand(Stack):

    @property
    def bet_multipler(self):
        suits = [card.suit for card in self]
        suits.sort()
        pips = [card.pip for card in self]
        pips.sort()
        same_suits = min(v for k, v in Counter(suits).items())
        same_pips = min(v for k, v in Counter(pips).items())
        if len(self) <= 2:
            return max(same_suits, same_pips)
        elif len(self) == 3:
            if PokDengRules.rule_JKQ and set(pips).issubset([Pip.Jack, Pip.Queen, Pip.King]):
                # 9 deng if same suit
                print('jkq')
                return 3 * same_suits
            elif PokDengRules.rule_order and pips[2].value - pips[1].value == pips[1].value - pips[0].value == 1:
                return 3 *same_suits
            elif PokDengRules.rule_tripple and same_pips == 3:
                return 5
            elif same_suits == 3:
                return same_suits
            else:
                return 1
        else:
            raise ValueError('Hand more than 2')

    @property
    def value(self):
        last_card_value = int(
            str(sum(card.pip.value if card.pip.value < 10 else 10 for card in self.cards))[-1])
        return last_card_value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        return super().__str__() + f'|({self.value},{self.bet_multipler})'


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
