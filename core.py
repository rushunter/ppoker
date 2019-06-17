from hand import Hand
from deck import Deck
from combo import ComboList, Combo


class Core:
    MAX_MULTIPLIER = 5
    DEFAULT_STAKE = 10
    START_BALANCE = 500

    def __init__(self):
        self.deck = Deck()
        self.hand = Hand()
        self.balance = 0
        self.stake = Core.DEFAULT_STAKE
        self.multiplier = 1
        self.combo = None
        self.combos = ComboList()
        self.combos.set_initial_balance(Core.START_BALANCE)

    def set_initial_combo(self):
        self.combo = self.combos.combos[Combo.INITIAL]

    def roll(self):
        self.combo = None
        if self.balance < self.stake:
            self.multiplier = 1
            return

        # return cards to deck
        self.hand.give_all(self.deck)
        # shuffle cards
        self.deck.shuffle()
        # decrease balance
        self.balance -= self.stake * self.multiplier
        # take 5 cards
        for i in range(5):
            self.deck.give_top(self.hand)

    def change(self):
        # drop discarded cards
        for i, card in enumerate(self.hand.cards):
            if not card.flipped:
                # take cards instead
                self.hand.cards[i] = self.deck.get_top()
                self.deck.add(card)
        # check combinations
        self.matchAny()

    def matchAny(self):
        self.combo = self.combos.match_any(self.hand)
        if self.combo is not None:
            self.balance += self.stake * self.combo.rate * self.multiplier

    def changeMultiplier(self, m):

        prev = self.multiplier
        # increase multiplier or set to 1 if max
        self.multiplier = m
        # modify balance considering new multiplier
        self.balance += self.stake * (prev - self.multiplier)
