from .game.engine.cards import Pip,Suit,Card,Stack,Deck

def test_card():
    a_card=Card(pip=Pip.Ace,suit=Suit.Spade)
    print(a_card)