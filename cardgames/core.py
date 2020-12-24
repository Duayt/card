# %%
from cardgames.cards import Deck, Card, Stack
from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections import namedtuple
import numpy as np


class Player:
    def __init__(self, name, hand: Stack = None, wallet=100, default_bet=10):
        if hand is not None:
            self.hand = hand
        else:
            self.hand = Stack.new_empty()
        self.name = name
        self.wallet = wallet
        self.logs = []
        self.default_bet = default_bet
        self.active = True

    def __str__(self):
        return f'{self.name}: {str(self.wallet)}'

    def __repr__(self):
        return str(self)

    def check_hand(self):
        value = sum([card.pip.value for card in self.hand])
        return value

    def bet(self, bet=None):
        if bet is None:
            bet = self.default_bet
        return min(bet, self.wallet)

    def update_wallet(self, value):
        self.wallet += value


class Dealer(Player):
    def __init__(self, name='dealer', hand: Stack = None):
        super(Dealer, self).__init__(name=name, hand=hand,
                                     wallet=0, default_bet=None)


@dataclass
class Game:
    players: list[Player]
    dealer: Player

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
        text = 'All Hands: \n'
        for player in self.all_players:
            text = text + f'\t{player.name}:{str(player.hand)} \n'

        return text
# %%
