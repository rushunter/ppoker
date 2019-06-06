from card import Card


class Hand:

    def __init__(self):
        self.cards = []

    def is_empty(self):
        return not self.cards

    def group_by_rank(self):
        ranks = {}
        for rank in Card.RANKS:
            ranks[rank] = len([x for x in self.cards if x.rank == rank])
        return ranks

    def group_by_suit(self):
        suits = {}
        for suit in Card.SUITS:
            suits[suit] = len([x for x in self.cards if x.suit == suit])
        return suits

    def add(self, card):
        card.flipped = True
        self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

    def give(self, card, hand):
        self.cards.remove(card)
        hand.add(card)

    def give_all(self, hand):
        hand.cards += self.cards
        self.cards.clear()
