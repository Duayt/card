from cardgames.core import Player
from cardgames.cards import Card
from cardgames.games import PokDengHand


def test_pokdenghand():
    player =Player('test',hand=PokDengHand(cards=[Card.new(1,1),Card.new(7,1)]))

    assert player.hand.get_value() ==8
    assert player.hand.get_bet_multipler() ==2