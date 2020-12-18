from cardgames.engine.cards import Pip,Suit,Card,Stack,Deck

def test_card():
    a_card=Card(pip=Pip.Ace,suit=Suit.Spade)

    assert str(a_card.pip)=='A'
    assert str(a_card.suit)=='♠'