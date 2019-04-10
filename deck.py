import random
from hand import Hand
from card import Card


class Deck(Hand):

    def __init__(self):
        Hand.__init__(self)
        for rank in Card.RANKS:
            for suit in Card.SUITS:
                self.add(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def get_top(self, flipped=True):
        card = self.cards[0]
        card.flipped = flipped
        self.cards.remove(card)
        return card

    def give_top(self, hand, flipped=True):
        hand.add(self.get_top(flipped))
