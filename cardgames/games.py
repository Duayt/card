# %%
from dataclasses import dataclass
from cardgames.core import Player, Dealer, Deck, Game, Stack, Card
from cardgames.cards import Pip, Suit


class PokDengRules:
    #https://en.wikipedia.org/wiki/Pok_Deng
    rule_JKQ: bool = False
    rule_order: bool = False
    rule_tripple: bool = False

    @classmethod
    @property
    def rules(cls):
        return (cls.rule_JKQ, cls.rule_order, cls.rule_tripple)

    @classmethod
    @property
    def all_rules(cls):
        return all([cls.rule_JKQ, cls.rule_order, cls.rule_tripple])

    @classmethod
    def set_rules(cls, rules: tuple[bool, bool, bool] = (True, True, True)):
        cls.rule_JKQ = rules[0]
        cls.rule_order = rules[1]
        cls.rule_tripple = rules[2]


class PokDengHand(Stack):

    @property
    def is_pok(self) ->:
        return (len(self) ==2) and self.value
    @property
    def check_rule_JKQ(self) -> bool:
        return set(self.pips).issubset([Pip.Jack, Pip.Queen, Pip.King])

    @property
    def check_rule_order(self) -> bool:
        return self.pips[2].value - self.pips[1].value == self.pips[1].value - self.pips[0].value == 1

    @property
    def check_rule_tripple(self) -> bool:
        return hand.pips[2].value - hand.pips[1].value == hand.pips[1].value - hand.pips[0].value == 1

    @property
    def check_any_rule(self) -> bool:
        return any([self.check_rule_JKQ, self.check_rule_order, self.check_rule_tripple])

    @ property
    def bet_multipler(self):
        if len(self) <= 2:
            return max(self.same_suits, self.same_pips)
        elif len(self) == 3:
            if PokDengRules.rule_JKQ and self.check_rule_JKQ:
                # 9 deng if same suit
                print('jkq')
                return 3 * self.same_suits
            elif PokDengRules.rule_order and self.check_rule_order:
                return 3 * self.same_suits
            elif PokDengRules.rule_tripple and self.same_pips == 3:
                return 5
            elif self.same_suits == 3:
                return self.same_suits
            else:
                return 1
        else:
            raise ValueError('Hand more than 2')

    @ property
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


@ dataclass
class PokDeng(Game):
    players: list[Player]
    dealer: Player
    n_players:

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
        # %%

        return


# %%
