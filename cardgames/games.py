# %%
from dataclasses import dataclass
from cardgames.core import Player, Deck, Game, Stack, Card, Dealer
from cardgames.cards import Pip, Suit
from enum import Enum
import logging
logger = logging.getLogger(__name__)


class OUTCOME(Enum):
    WIN = 1
    DRAW = 0
    LOSE = -1

    def __lt__(self, other):
        return self.value < other.value


class ACTIONS(Enum):
    DRAW = 1
    STAY = 2


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
        elif PokDengRules.all_rules:
            if self.rule_tripple:
                return PokDengHandType.TRIPPLE
            elif self.rule_order_flush:
                return PokDengHandType.ORDER_FLUSH
            elif self.rule_order_normal:
                return PokDengHandType.ORDER
            elif self.rule_JQK:
                return PokDengHandType.JQK

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
        return super().__str__() + f' | ({self.value,self.bet_multipler, self.rank.name})'


@ dataclass
class PokDeng(Game):
    players: list[Player]
    dealer: Player

    @ classmethod
    def init_state(self, n_player=3, wallet=None):
        dealer = Dealer(name='dealer', hand=PokDengHand())
        players = [Player(name=f'player_{i}', hand=PokDengHand(
        ), wallet=wallet) for i in range(n_player)]

        return PokDeng(players=players, dealer=dealer)

    @ property
    def all_players(self):
        all_players = self.players+[self.dealer]
        return all_players

    @ property
    def active_players(self):
        active_players = [player for player in self.players if player.active]
        return active_players

    @ property
    def players_bets(self, bet_dict=dict()):
        players_bets = {players.name: players.bet()
                        for players in self.players}
        players_bets.update(bet_dict)
        return players_bets

    @ property
    def all_hands(self):
        text = ''
        for player in self.all_players:
            text = text + f'{player.name}:{str(player.hand)} \n'

        return text

    @staticmethod
    def compare_hand(hand: PokDengHand, other_hand: PokDengHand):

        if hand == other_hand:
            return OUTCOME.DRAW
        elif hand > other_hand:
            return OUTCOME.WIN
        else:
            return OUTCOME.LOSE

    def activate_all_players(self):
        for player in self.players:
            player.active = True

    def deactivate_all_players(self):
        for player in self.players:
            player.active = False

    def reset_all_hands(self):
        for player in self.all_players:
            player.hand = PokDengHand()

    def play(self, seed=None):
        # Activate players
        self.activate_all_players()
        PokDengRules.set_rules()
        deck = Deck(is_shuffle=True, seed=seed)
        # each player place bet
        players_bets = self.players_bets
        player_result = {}
        # deal 1 card each player including dealer
        hands = 2
        logger.info(f'n players: {len(self.players)}')
        logger.info('Dealing cards')
        for i in range(hands):
            for p in self.all_players:
                deck.deal(p.hand, 1)

        # session end if dealer pokdeng
        if self.dealer.hand.pokdeng:
            logger.info('Dealer Pok!')
            self.deactivate_all_players()
        else:
            logger.info('Dealer Not Pok, continue')

        # check all pokdeng
        for player in self.active_players:
            if player.hand.pokdeng and player.active:
                logger.info(f'{player.name} Pok!: {player.hand}')
                player.active = False

        if len(self.active_players) > 0:
            # player's Actions
            action_msg = 'Player actions\n'
            for i, action in enumerate(ACTIONS):
                action_msg = action_msg+f'\t{i+1}:{ACTIONS(i+1)}'
            logger.info(action_msg)

            for player in self.active_players:
                logger.info(f'{player.name} | {player.hand}')
                action_input = int(input(f'{player.name} action'))
                action_input = ACTIONS(action_input)
                logger.info(f'{player.name}:{action_input}')
                if action_input == ACTIONS.DRAW:
                    deck.deal(player.hand, 1)
                    logger.info(f'{player.name}|{player.hand}')

        if len(self.active_players) > 0:
            # Dealer actions
            action_msg = 'Dealer actions\n'
            for i, action in enumerate(ACTIONS):
                action_msg = action_msg+f'\t{i+1}:{ACTIONS(i+1)}'
            logger.info(action_msg)
            logger.info(f'Dealer | {self.dealer.hand}')
            action_input = int(input(f'dealer action'))
            action_input = ACTIONS(action_input)
            if action_input == ACTIONS.DRAW:
                deck.deal(self.dealer.hand, 1)
                logger.info(f'Dealer | {self.dealer.hand}')

        self.deactivate_all_players()

        # compare hands
        logger.info('Comparing all hands')
        player_results = {}
        bets_results = {}
        for player in self.players:
            hand_result = self.compare_hand(player.hand, self.dealer.hand)
            bet_multipler = hand_result.value * \
                (player.hand.bet_multipler if hand_result ==
                 OUTCOME.WIN else self.dealer.hand.bet_multipler)
            player_results[player.name] = hand_result
            bets_result = bet_multipler * players_bets[player.name]
            bets_results[player.name] = bets_result
            player.logs.append({'player': player.hand,
                                'dealer': self.dealer.hand,
                                'bet': players_bets[player.name],
                                'bet_result': bets_results[player.name]})
            # resolve money
            player.update_wallet(bets_result)
            self.dealer.update_wallet(-bets_result)
        logger.info(self.all_hands)
        self.reset_all_hands()
        
        logger.info(bets_result)
        return bets_result


logging.basicConfig(level=logging.INFO)
seed = 1234
n_player = 1
PokDengRules.set_rules()
game = PokDeng.init_state(n_player=n_player, wallet=100)
n_games = 10
for i in range(n_games):
    game.play()
# # new shuffle deck
# deck = Deck(is_shuffle=True, seed=seed)

# # each player place bet
# players_bets = game.players_bets
# player_result = {}
# # deal 1 card each player including dealer
# hands = 2
# logger.info(f'n players: {n_player}')
# logger.info('Dealing cards')
# for i in range(hands):
#     for p in game.all_players:
#         deck.deal(p.hand, 1)

# # session end if dealer pokdeng
# if game.dealer.hand.pokdeng:
#     logger.info('Dealer Pok!')
#     game.deactivate_all_players()
# else:
#     logger.info('Dealer Not Pok, continue')

# # check all pokdeng
# for player in game.active_players:
#     if player.hand.pokdeng and player.active:
#         logger.info(f'{player.name} Pok!: {player.hand}')
#         player.active == False

# if len(game.active_players) > 0:
#     # player's Actions
#     action_msg = 'Player actions\n'
#     for i, action in enumerate(ACTIONS):
#         action_msg = action_msg+f'\t{i+1}:{ACTIONS(i+1)}'
#     logger.info(action_msg)

#     for player in game.active_players:
#         logger.info(f'{player.name} | {player.hand}')
#         action_input = int(input(f'{player.name} action'))
#         action_input = ACTIONS(action_input)
#         logger.info(f'{player.name}:{action_input}')
#         if action_input == ACTIONS.DRAW:
#             deck.deal(player.hand, 1)
#             logger.info(f'{player.name}|{player.hand}')


# if len(game.active_players) > 0:
#     # Dealer actions
#     action_msg = 'Dealer actions\n'
#     for i, action in enumerate(ACTIONS):
#         action_msg = action_msg+f'\t{i+1}:{ACTIONS(i+1)}'
#     logger.info(action_msg)
#     logger.info(f'Dealer | {game.dealer.hand}')
#     action_input = int(input(f'dealer action'))
#     action_input = ACTIONS(action_input)
#     if action_input == ACTIONS.DRAW:
#         deck.deal(game.dealer.hand, 1)
#         logger.info(f'Dealer | {game.dealer.hand}')

# game.deactivate_all_players()

# # compare hands
# logger.info('Comparing all hands')
# player_results = {}
# bets_results = {}
# for player in game.players:
#     hand_result = game.compare_hand(player.hand, game.dealer.hand)
#     bet_multipler = hand_result.value * \
#         (player.hand.bet_multipler if hand_result ==
#          OUTCOME.WIN else game.dealer.hand.bet_multipler)
#     player_results[player.name] = hand_result
#     bets_result = bet_multipler * players_bets[player.name]
#     bets_results[player.name] = bets_result
#     player.logs.append({'player': player.hand,
#                         'dealer': game.dealer.hand,
#                         'bet': players_bets[player.name],
#                         'bet_result': bets_results[player.name]})
#     # resolve money
#     player.update_wallet(bets_result)
#     dealer.update_wallet(-bets_result)


# %%
