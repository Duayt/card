from cardgames.engine.cards import Pip, Suit, Card, Stack, Deck


def test_card_attributes():
    a_card = Card(pip=Pip.Ace, suit=Suit.Spade)

    assert str(a_card.pip) == 'A'
    assert str(a_card.suit) == '♠'


def test_pip():
    a_card = Card(pip=Pip.Ace, suit=Suit.Spade)
    b_card = Card(pip=Pip.Ace, suit=Suit.Heart)
    c_card = Card(pip=Pip.Deuce, suit=Suit.Spade)
    d_card = Card(pip=Pip.Deuce, suit=Suit.Heart)

    assert a_card.pip <= b_card.pip
    assert a_card.pip < c_card.pip
    assert a_card.suit > b_card.suit
    assert a_card.pip == b_card.pip
    assert a_card.suit != b_card.suit

    assert a_card > b_card
    assert c_card > a_card
    assert a_card < c_card
    assert c_card > b_card
    assert d_card > a_card
    assert a_card < d_card
