import sys
import pygame
from core import Core
from combo import Combo


class PP:

    def __init__(self):

        self.screen = pygame.display.set_mode((1024, 600))

        pygame.display.set_caption("PPoker")
        icon = pygame.image.load("assets/img/icon.png").convert()
        pygame.display.set_icon(icon)

        self.core = Core()
        self.background = pygame.image.load("assets/img/background.png").convert()
        self.slot_sprite = pygame.image.load("assets/img/card_slot.png").convert_alpha()
        self.card_back_sprite = pygame.image.load("assets/img/card_back.png").convert_alpha()
        self.phase = 0
        self.card_rects = []
        for i in range(5):
            self.card_rects.append(pygame.Rect(i * 180 + 75, 320, 150, 225))

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Courier New", 28)
        font.set_bold(True)
        font_small = pygame.font.SysFont("Courier New", 18)
        # self.core.roll()

        while True:
            clock.tick(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.phase == 1:
                        self.core.change()
                        self.phase = -1
                    elif self.phase != 0 and self.core.balance < self.core.stake:
                            self.core.balance = 0
                            self.core.hand.give_all(self.core.deck)
                            self.phase = 0
                    elif self.phase == 0:
                            self.core.balance = Core.START_BALANCE
                            self.core.set_initial_combo()
                            self.phase = -1
                    elif self.phase == -1:
                        self.core.roll()
                        self.phase = 1

                elif self.phase == 1 and self.core.hand.cards and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in range(len(self.card_rects)):
                        if self.card_rects[i].collidepoint(event.pos[0], event.pos[1]):
                            self.core.hand.cards[i].flip()
                            break

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))

            if self.core.hand.is_empty():
                for i in range(5):
                    self.screen.blit(self.slot_sprite, (i * 180 + 75, 320))
            else:
                i = 0
                for card in self.core.hand.cards:
                    self.screen.blit(card.get_sprite() if card.flipped else self.card_back_sprite, (i * 180 + 75, 320))
                    i += 1

            self.screen.blit(font.render("Balance: " + str(self.core.balance), -1, (255, 255, 255)), (750, 30))

            cmd = None
            if self.phase == 0:
                cmd = "start"
            else:
                if self.phase == 1:
                    cmd = "change"
                elif self.phase == -1:
                    cmd = "roll"

            win_sum = 0
            if self.core.combo is not None:
                if self.core.combo.comboType == Combo.INITIAL:
                    win_sum = self.core.combo.rate
                else:
                    win_sum = self.core.combo.rate * self.core.stake * self.core.multiplier

            self.screen.blit(font_small.render("Press <Space> to " + cmd, -1, (255, 255, 255)), (750, 70))
            self.screen.blit(font.render("" if self.core.combo is None else self.core.combo.display_name + ": +" + str(win_sum),
                                         -1, (255, 255, 255)), (300, 50))
            pygame.display.update()


if __name__ == "__main__":
    PP().run()
