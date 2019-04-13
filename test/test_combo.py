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
        hand.add(Card("ten", "hearts"))
        hand.add(Card("jack", "spades"))
        hand.add(Card("queen", "diamonds"))
        hand.add(Card("king", "clubs"))
        hand.add(Card("ace", "hearts"))
        c = ComboList()
        self.assertEqual(Combo.STRAIGHT, c.match_any(hand).combo_type)

    def test_full_house(self):
        pygame.image = unittest.mock.Mock()
        pygame.image.load.return_value = None

        hand = Hand()
        hand.add(Card("ten", "hearts"))
        hand.add(Card("ten", "spades"))
        hand.add(Card("jack", "diamonds"))
        hand.add(Card("jack", "clubs"))
        hand.add(Card("jack", "hearts"))
        c = ComboList()
        self.assertEqual(Combo.FULL_HOUSE, c.match_any(hand).combo_type)


if __name__ == '__main__':
    unittest.main()
