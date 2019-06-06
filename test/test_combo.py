import unittest
import unittest.mock
from combo import ComboList, Combo
from hand import Hand
from card import Card
import pygame


class TestCombo(unittest.TestCase):

    def test_straight(self):
        pygame.image = unittest.mock.Mock()
        pygame.image.load.return_value = None

        hand = Hand()
        hand.add(Card("ten", "hearts", False))
        hand.add(Card("six", "spades", False))
        hand.add(Card("eight", "diamonds", False))
        hand.add(Card("seven", "clubs", False))
        hand.add(Card("nine", "hearts", False))
        c = ComboList()
        self.assertEqual(Combo.STRAIGHT, c.match_any(hand).combo_type)

    def test_full_house(self):
        pygame.image = unittest.mock.Mock()
        pygame.image.load.return_value = None

        hand = Hand()
        hand.add(Card("ten", "hearts", False))
        hand.add(Card("ten", "spades", False))
        hand.add(Card("jack", "diamonds", False))
        hand.add(Card("jack", "clubs", False))
        hand.add(Card("jack", "hearts", False))
        c = ComboList()
        self.assertEqual(Combo.FULL_HOUSE, c.match_any(hand).combo_type)


if __name__ == '__main__':
    unittest.main()
