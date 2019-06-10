import sys
import pygame
from core import Core
from combo import Combo, ComboList
from translate import t, changeLanguage
from sound import sound


class PP:

    def __init__(self):

        self.screen = pygame.display.set_mode((1024, 600))

        pygame.display.set_caption("PPoker")
        icon = pygame.image.load("assets/img/icon.png").convert_alpha()
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
        font = pygame.font.SysFont("Tahoma", 28)
        font.set_bold(True)
        font_small = pygame.font.SysFont("Tahoma", 18)

        while True:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    changeLanguage()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.phase == 1:
                        self.core.change()
                        if self.core.combo is not None:
                            sound("win")
                        else:
                            sound("flip1")
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
                        sound("roll")
                        self.core.roll()
                        self.phase = 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.core.changeMultiplier(1)
                    elif event.key == pygame.K_2:
                        self.core.changeMultiplier(2)
                    elif event.key == pygame.K_3:
                        self.core.changeMultiplier(3)
                    elif event.key == pygame.K_4:
                        self.core.changeMultiplier(4)
                    elif event.key == pygame.K_5:
                        self.core.changeMultiplier(5)

                elif self.phase == 1 and self.core.hand.cards and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in range(len(self.card_rects)):
                        if self.card_rects[i].collidepoint(event.pos[0], event.pos[1]):
                            sound("flip2")
                            self.core.hand.cards[i].flip()
                            break

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            if self.core.hand.is_empty():
                for i in range(5):
                    self.screen.blit(self.slot_sprite, (i * 180 + 75, 320))
            else:
                i = 0
                for card in self.core.hand.cards:
                    self.screen.blit(card.get_sprite() if card.flipped else self.card_back_sprite, (i * 180 + 75, 320))
                    i += 1

            self.screen.blit(font.render(t("balance") + str(self.core.balance), -1, (255, 255, 255)), (650, 30))

            cmd = None
            if self.phase == 0:
                cmd = t("game.state.start")
            else:
                if self.phase == 1:
                    cmd = t("game.state.change")
                elif self.phase == -1:
                    cmd = t("game.state.roll")

            win_sum = 0
            if self.core.combo is not None:
                if self.core.combo == Combo.INITIAL:
                    win_sum = self.core.combo.rate
                else:
                    win_sum = self.core.combo.rate * self.core.stake * self.core.multiplier

            self.screen.blit(font_small.render(t("space") + cmd, -1, (255, 255, 255)), (650, 70))
            self.screen.blit(font_small.render(t("language.change"), -1, (255, 255, 255)), (650, 100))
            self.screen.blit(font_small.render(t("multiplier.change"), -1, (255, 255, 255)), (650, 130))
           
            self.draw_table()
            
            pygame.display.update()
            
    def draw_table(self):
        font = pygame.font.SysFont("Tahoma", 18)
        # highlight multiplier
        pygame.draw.rect(self.screen, (2, 137, 92), pygame.Rect(210+self.core.multiplier*70, 30, 69, 207))
        if self.core.combo is not None:
            # highlight win
            pygame.draw.rect(self.screen, (200, 0, 0), pygame.Rect(70, 30+(list(self.core.combos.combos.values()).index(self.core.combo)-1)*23, 555, 24))
        for i, c in enumerate(self.core.combos.combos.values()):
            if i == 0: continue
            for x in range(5):
                # draw number cells
                pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(279 + x*69, 30+(i-1)*23, 70, 24), 1)
                self.screen.blit(font.render(str(c.rate*self.core.stake*(x+1)), -1, (255, 255, 0)), (285 + x * 70, 30+(i-1)*23))
            # draw combo names cells
            pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(70, 30+(i-1)*23, 210, 24), 1)
            self.screen.blit(font.render(t(c.display_name), -1, (255, 255, 0)), (74, 30 + (i-1)*23))
        

if __name__ == "__main__":
    PP().run()
