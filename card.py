from pygame import image


class Card:
    RANKS = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace']
    SUITS = ['hearts', 'spades', 'diamonds', 'clubs']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.flipped = True
        self.__sprite = image.load("assets/img/cards/%s-%s.png" % (rank, suit)).convert_alpha()

    def flip(self):
        self.flipped = not self.flipped

    def get_sprite(self):
        return self.__sprite

    def __str__(self):
        return self.rank + '-' + self.suit
