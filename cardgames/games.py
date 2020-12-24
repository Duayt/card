# %%
from dataclasses import dataclass
from cardgames.core import Player, Deck, Game, Stack, Card, Dealer
from cardgames.cards import Pip, Suit
from enum import Enum


class OUTCOME(Enum):
    WIN = 1
    DRAW = 0
    LOSE = -1

    def __lt__(self, other):
        return self.value < other.value


class PokDengHandType(Enum):
    POKDENG = 10
    TRIPPLE = 9
    ORDER_FLUSH = 8
    ORDER = 7
    JQK = 6
    NORMAL = 5

    def __lt__(self, other):
        return self.value < other.value


class PokDengRules:
    # https://en.wikipedia.org/wiki/Pok_Deng
    rule_JQK: bool = False
    rule_order: bool = False
    rule_tripple: bool = False

    @classmethod
    @property
    def rules(cls):
        return (cls.rule_JQK, cls.rule_order, cls.rule_tripple)

    @classmethod
    @property
    def all_rules(cls):
        return all([cls.rule_JQK, cls.rule_order, cls.rule_tripple])

    @classmethod
    def set_rules(cls, rules: tuple[bool, bool, bool] = (True, True, True)):
        cls.rule_JQK = rules[0]
        cls.rule_order = rules[1]
        cls.rule_tripple = rules[2]


class PokDengHand(Stack):

    @property
    def pokdeng(self) -> bool:
        return self.value in [8, 9] and len(self) == 2

    @property
    def rule_tripple(self) -> bool:
        return self.same_pips == 3 and len(self) == 3

    @property
    def rule_order(self) -> bool:
        if len(self) < 3:
            return False
        else:
            return self.pips[2].value - self.pips[1].value == self.pips[1].value - self.pips[0].value == 1

    @property
    def rule_order_flush(self) -> bool:
        return self.rule_order and self.same_suits == 3

    @property
    def rule_order_normal(self) -> bool:
        return self.rule_order and self.same_suits != 3

    @property
    def rule_JQK(self) -> bool:
        return set(self.pips).issubset([Pip.Jack, Pip.Queen, Pip.King]) and len(self) == 3

    @ property
    def bet_multipler(self):
        if len(self) <= 2:
            return max(self.same_suits, self.same_pips)
        elif len(self) == 3:
            if PokDengRules.rule_JQK and self.rule_JQK:
                return 3
            elif PokDengRules.rule_order and self.rule_order:
                return 3
            elif PokDengRules.rule_tripple and self.rule_tripple:
                return 5
            elif self.same_suits == 3:
                return self.same_suits
            else:
                return 1
        else:
            raise ValueError('Hand more than 2')

    @property
    def rank(self):
        if self.pokdeng:
            return PokDengHandType.POKDENG
        elif self.rule_tripple:
            return PokDengHandType.TRIPPLE
        elif self.rule_order_flush:
            return PokDengHandType.ORDER_FLUSH
        elif self.rule_order_normal:
            return PokDengHandType.ORDER
        elif self.rule_JQK:
            return PokDengHandType.JQK
        else:
            return PokDengHandType.NORMAL

    @ property
    def value(self):
        last_card_value = int(
            str(sum(card.pip.value if card.pip.value < 10 else 10 for card in self.cards))[-1])
        return last_card_value

    def __eq__(self, other):
        return ((self.rank, self.value) == (other.rank, other.value))

    def __lt__(self, other):
        # return self.value < other.value
        return ((self.rank, self.value) < (other.rank, other.value))

    def __str__(self):
        return super().__str__() + f'|({self.value},{self.bet_multipler})'


@ dataclass
class PokDeng(Game):
    players: list[Player]
    dealer: Player

    @ classmethod
    def init_state(self, n_player=3, wallet=None):
        num_player = 1
        dealer = Dealer(name='dealer', hand=PokDengHand())
        players = [Player(name=f'player_{i}', hand=PokDengHand(
        ), wallet=wallet) for i in range(n_player)]

        return PokDeng(players=players, dealer=dealer)

    @ property
    def all_players(self):
        all_players = self.players+[self.dealer]
        return all_players

    @ property
    def players_bets(self, bet_dict=dict()):
        players_bets = {players.name: players.bet()
                        for players in self.players}
        players_bets.update(bet_dict)
        return players_bets

    @staticmethod
    def compare_hand(hand: PokDengHand, other_hand: PokDengHand):
        if hand == other_hand:
            return OUTCOME.DRAW
        elif hand > other_hand:
            return OUTCOME.WIN
        else:
            return OUTCOME.LOSE

    def play(self, seed=None):

        # new shuffle deck
        deck = Deck(is_shuffle=True, seed=seed)

        # each player place bet
        player_bets = self.players_bets

        # deal 1 card each player including dealer
        hands = 2

        for i in range(hands):
            for p in self.all_players:
                deck.deal(p.hand, 1)
        # session end if dealer pokdeng
        if self.dealer.hand.pokdeng:
            print('games end')

        # check for player and dealer pokdeng

        # ask whether player will add one more card
        # dealer decide to take one more cards
        # check all cards and play bet

        return


game = PokDeng.init_state(n_player=2, wallet=100)
# %%
