from cardgames.core import Player
from cardgames.cards import Card
from cardgames.games import PokDengHand, PokDengRules, PokDeng, OUTCOME


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

    # JQK
    PokDengRules.set_rules()
    PokDengRules.all_rules == True
    hand = PokDengHand(
        cards=[Card.new(11, 1), Card.new(12, 1), Card.new(13, 2)])

    assert hand.value == 0
    assert hand.bet_multipler == 3

    # ORDER
    hand = PokDengHand(
        cards=[Card.new(7, 1), Card.new(8, 1), Card.new(9, 2)])

    assert hand.value == 4
    assert hand.bet_multipler == 3

    # Tripple
    hand = PokDengHand(
        cards=[Card.new(3, 1), Card.new(3, 2), Card.new(3, 3)])

    assert hand.value == 9
    assert hand.bet_multipler == 5

    # JQK same suit
    hand = PokDengHand(
        cards=[Card.new(11, 1), Card.new(12, 1), Card.new(13, 1)])

    assert hand.value == 0
    assert hand.bet_multipler == 3

    # ORDER flush
    hand = PokDengHand(
        cards=[Card.new(7, 1), Card.new(8, 1), Card.new(9, 1)])

    assert hand.value == 4
    assert hand.bet_multipler == 3


def test_pokdeng_case():
    hand1 = PokDengHand(
        cards=[Card.new(7, 1), Card.new(1, 1)])

    hand2 = PokDengHand(
        cards=[Card.new(11, 1), Card.new(9, 1)])

    hand3 = PokDengHand(
        cards=[Card.new(1, 1), Card.new(9, 1)])

    hand4 = PokDengHand(
        cards=[Card.new(3, 1), Card.new(3, 2), Card.new(3, 3)])

    hand5 = PokDengHand(
        cards=[Card.new(1, 2), Card.new(9, 3), Card.new(12, 4)])

    assert hand1.pokdeng == True
    assert hand2.pokdeng == True
    assert hand3.pokdeng == False
    assert hand4.pokdeng == False

    assert PokDeng.compare_hand(hand1, hand2) == OUTCOME.LOSE
    assert PokDeng.compare_hand(hand1, hand3) == OUTCOME.WIN
    assert PokDeng.compare_hand(hand1, hand4) == OUTCOME.WIN
    assert PokDeng.compare_hand(hand2, hand4) == OUTCOME.WIN
    assert PokDeng.compare_hand(hand3, hand5) == OUTCOME.DRAW