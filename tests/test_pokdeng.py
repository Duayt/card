from cardgames.core import Player
from cardgames.cards import Card
from cardgames.games import PokDengHand, PokDengRules


def test_pokdenghand():
    player = Player('test', hand=PokDengHand(
        cards=[Card.new(1, 1), Card.new(7, 1)]))

    assert player.hand.value == 8
    assert player.hand.bet_multipler == 2

    assert PokDengRules.rules == (False, False, False)

    # Nomal check
    PokDengRules.all_rules == False
    hand = PokDengHand(
        cards=[Card.new(1, 1), Card.new(11, 1), Card.new(12, 2)])

    assert hand.value == 1
    assert hand.bet_multipler == 1

    hand = PokDengHand(
        cards=[Card.new(10, 1), Card.new(11, 1), Card.new(12, 2)])

    assert hand.value == 0
    assert hand.bet_multipler == 1

    hand = PokDengHand(
        cards=[Card.new(10, 1), Card.new(11, 1), Card.new(12, 1)])

    assert hand.value == 0
    assert hand.bet_multipler == 3

    hand = PokDengHand(
        cards=[Card.new(4, 2), Card.new(4, 1)])

    assert hand.value == 8
    assert hand.bet_multipler == 2

    # All rules

    # JKQ
    PokDengRules.set_rules()
    PokDengRules.all_rules == True
    hand = PokDengHand(
        cards=[Card.new(11, 1), Card.new(12, 1), Card.new(13, 2)])

    assert hand.value == 0
    assert hand.bet_multipler == 3

    # ORDER
    PokDengRules.set_rules()
    hand = PokDengHand(
        cards=[Card.new(7, 1), Card.new(8, 1), Card.new(9, 2)])

    assert hand.value == 4
    assert hand.bet_multipler == 3
    # Tripple
    hand = PokDengHand(
        cards=[Card.new(3, 1), Card.new(3, 2), Card.new(3, 3)])

    assert hand.value == 9
    assert hand.bet_multipler == 5

    # JKQ same suit
    PokDengRules.set_rules()
    hand = PokDengHand(
        cards=[Card.new(11, 1), Card.new(12, 1), Card.new(13, 1)])

    assert hand.value == 0
    assert hand.bet_multipler == 9

    # ORDER same suit
    PokDengRules.set_rules()
    hand = PokDengHand(
        cards=[Card.new(7, 1), Card.new(8, 1), Card.new(9, 1)])

    assert hand.value == 4
    assert hand.bet_multipler == 9
