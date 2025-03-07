import os

import pygame
import random
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.stat = 0

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, 'black', self.rect, 3)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, 'black')
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


FPS = 50


class Bear(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("bear.png"), (100, 100))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bear.image
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 450
        self.stat = 0
        self.hp = 4

    def update(self):
        if self.stat == 0:
            self.rect.x -= 1


class BigBear(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("bigbear.png"), (100, 178))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = BigBear.image
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 390
        self.stat = 0
        self.hp = 7

    def update(self):
        if self.stat == 0:
            self.rect.x -= 1


class Enemy(Bear):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.flip(pygame.transform.scale(load_image("enemy.png"), (100, 100)), True, False)
        self.rect.x = 85
        self.rect.y = 450
        self.stat = 0
        self.hp = 3

    def update(self):
        if self.stat == 0:
            self.rect.x += 1


class BigEnemy(BigBear):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.flip(pygame.transform.scale(load_image("bigenemy.png"), (100, 178)), True, False)
        self.rect.x = 85
        self.rect.y = 390
        self.stat = 0
        self.hp = 6

    def update(self):
        if self.stat == 0:
            self.rect.x += 1


def terminate():
    pygame.quit()
    sys.exit()


def lvl1_game():
    screen.fill((255, 255, 255))
    fon = pygame.transform.scale(load_image('game_fon.png'), (1000, 800))
    screen.blit(fon, (0, 0))
    all_sprites = pygame.sprite.Group()
    bears = []
    enemy = []
    buttons = [Button("1", 215, 682, 100, 100, "grey", "green"),
               Button("X", 950, 0, 50, 50, "grey", "red")]
    buttons[1].stat = -1
    bear_image = pygame.transform.scale(load_image("bear.png"), (100, 100))
    enemy_birth = 0
    enemy_tower_hp = 10
    self_tower_hp = 10
    running = True
    while running:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for el in buttons:
                    if el.rect.collidepoint(event.pos) and el.stat == 0 and el.text == '1':
                        bears.append(Bear(all_sprites))
                        el.stat = 300
                    elif el.rect.collidepoint(event.pos) and el.text == "X":
                        start_screen()
        if enemy_birth == 0:
            enemy.append(Enemy(all_sprites))
            enemy_birth = random.randint(250, 350)
        enemy_birth -= 1
        for el in bears:
            el.update()
        for el in enemy:
            el.update()
        if len(bears) > 0 and len(enemy) > 0 and bears[0].rect.x <= enemy[0].rect.x + 100:
            for el in bears:
                if el.rect.x == bears[0].rect.x and el.stat == 0:
                    el.stat = 60
                if el.rect.x == bears[0].rect.x:
                    el.stat -= 1
                    if el.stat == 0:
                        enemy[0].hp -= 1
                    if len(enemy) > 0 and enemy[0].hp == 0:
                        for t in bears:
                            t.stat = 0
                        enemy[0].image = load_image("none.png")
                        enemy = enemy[1:]
            for el in enemy:
                if el.rect.x == enemy[0].rect.x and el.stat == 0:
                    el.stat = 60
                if el.rect.x == enemy[0].rect.x:
                    el.stat -= 1
                    if el.stat == 0:
                        bears[0].hp -= 1
                    if len(bears) > 0 and bears[0].hp == 0:
                        for t in enemy:
                            t.stat = 0
                        bears[0].image = load_image("none.png")
                        bears = bears[1:]
        for el in bears:
            if el.rect.x <= 185 and el.stat == 0:
                el.stat = 60
            if el.rect.x <= 185:
                el.stat -= 1
                if el.stat == 0:
                    enemy_tower_hp -= 1
        for el in enemy:
            if el.rect.x >= 800 and el.stat == 0:
                el.stat = 60
            if el.rect.x >= 800:
                el.stat -= 1
                if el.stat == 0:
                    self_tower_hp -= 1
        if enemy_tower_hp == 0:
            return
        elif self_tower_hp == 0:
            return
        for button in buttons:
            button.draw(screen)
            screen.blit(bear_image, (215, 682))
            if button.stat != 0:
                button.stat -= 1
            if button.stat == 0:
                button.hover_color = 'green'
            else:
                button.hover_color = 'red'
        all_sprites.draw(screen)
        pygame.display.update()


def lvl2_game():
    screen.fill((255, 255, 255))
    fon = pygame.transform.scale(load_image('game_fon.png'), (1000, 800))
    screen.blit(fon, (0, 0))
    all_sprites = pygame.sprite.Group()
    bears = []
    enemy = []
    buttons = [Button("1", 215, 682, 100, 100, "grey", "green"),
               Button("2", 330, 682, 100, 100, "grey", "green"),
               Button("X", 950, 0, 50, 50, "gray", "red")]
    buttons[2].stat = -1
    bear_image = pygame.transform.scale(load_image("bear.png"), (100, 100))
    big_bear_image = pygame.transform.scale(load_image("bigbear.png"), (56, 100))
    enemy_birth = 0
    enemy_type = random.randint(1, 3)
    enemy_tower_hp = 20
    self_tower_hp = 10
    running = True
    while running:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for el in buttons:
                    if el.rect.collidepoint(event.pos) and el.stat == 0 and el.text == '1':
                        bears.append(Bear(all_sprites))
                        el.stat = 350
                    elif el.rect.collidepoint(event.pos) and el.stat == 0 and el.text == '2':
                        bears.append(BigBear(all_sprites))
                        el.stat = 500
                    elif el.rect.collidepoint(event.pos) and el.text == "X":
                        start_screen()
        if enemy_birth == 0 and enemy_type < 3:
            enemy.append(Enemy(all_sprites))
            enemy_birth = random.randint(250, 350)
            enemy_type = random.randint(1, 3)
        elif enemy_birth == 0 and enemy_type == 3:
            enemy.append(BigEnemy(all_sprites))
            enemy_birth = random.randint(150, 250)
            enemy_type = random.randint(1, 3)
        enemy_birth -= 1
        for el in bears:
            el.update()
        for el in enemy:
            el.update()
        if len(bears) > 0 and len(enemy) > 0 and bears[0].rect.x <= enemy[0].rect.x + 100:
            for el in bears:
                if el.rect.x == bears[0].rect.x and el.stat == 0:
                    el.stat = 60
                if el.rect.x == bears[0].rect.x:
                    el.stat -= 1
                    if el.stat == 0:
                        enemy[0].hp -= 1
                    if len(enemy) > 0 and enemy[0].hp == 0:
                        for t in bears:
                            t.stat = 0
                        enemy[0].image = load_image("none.png")
                        enemy = enemy[1:]
            for el in enemy:
                if el.rect.x == enemy[0].rect.x and el.stat == 0:
                    el.stat = 60
                if el.rect.x == enemy[0].rect.x:
                    el.stat -= 1
                    if el.stat == 0:
                        bears[0].hp -= 1
                    if len(bears) > 0 and bears[0].hp == 0:
                        for t in enemy:
                            t.stat = 0
                        bears[0].image = load_image("none.png")
                        bears = bears[1:]
        for el in bears:
            if el.rect.x <= 185 and el.stat == 0:
                el.stat = 60
            if el.rect.x <= 185:
                el.stat -= 1
                if el.stat == 0:
                    enemy_tower_hp -= 1
        for el in enemy:
            if el.rect.x >= 800 and el.stat == 0:
                el.stat = 60
            if el.rect.x >= 800:
                el.stat -= 1
                if el.stat == 0:
                    self_tower_hp -= 1
        if enemy_tower_hp == 0:
            return
        elif self_tower_hp == 0:
            return
        for button in buttons:
            button.draw(screen)
            screen.blit(bear_image, (215, 682))
            screen.blit(big_bear_image, (350, 682))
            if button.stat != 0:
                button.stat -= 1
            if button.stat == 0:
                button.hover_color = 'green'
            else:
                button.hover_color = 'red'
        all_sprites.draw(screen)
        pygame.display.update()


def start_screen():
    screen.fill((255, 255, 255))
    status = 0
    game_satus = {0: "Изначальное меню",
                  1: "Выбор уровня",
                  2: "Уровень 1",
                  3: "Уровень 2", }
    fon = pygame.transform.scale(load_image('fon.png'), (794, 1200))
    play_button = Button("Играть", 300, 500, 100, 100, "grey", "green")
    exit_button = Button("Выход", 600, 500, 100, 100, "grey", "red")
    screen.blit(fon, (125, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect(600, 500, 100, 100).collidepoint(
                    event.pos) and status == 0:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect(300, 500, 100, 100).collidepoint(
                    event.pos) and status == 0:
                status = 1
                screen.fill((255, 255, 255))
                lvl1_button = Button("Уровень 1", 300, 500, 150, 100, "grey", "orange")
                lvl2_button = Button("Уровень 2", 600, 500, 150, 100, "grey", "orange")
                lvl1_button.draw(screen)
                lvl2_button.draw(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN and lvl1_button.rect.collidepoint(event.pos) and status == 1:
                status = 2
            elif event.type == pygame.MOUSEBUTTONDOWN and lvl2_button.rect.collidepoint(event.pos) and status == 1:
                status = 3
        if status == 0:
            play_button.draw(screen)
            exit_button.draw(screen)
        if status == 1:
            lvl1_button.draw(screen)
            lvl2_button.draw(screen)
        if status == 2:
            lvl1_game()
            status = 0
            screen.fill((255, 255, 255))
            fon = pygame.transform.scale(load_image('fon.png'), (794, 1200))
            play_button = Button("Играть", 300, 500, 100, 100, "grey", "green")
            exit_button = Button("Выход", 600, 500, 100, 100, "grey", "red")
            screen.blit(fon, (125, 0))
        if status == 3:
            lvl2_game()
            status = 0
            screen.fill((255, 255, 255))
            fon = pygame.transform.scale(load_image('fon.png'), (794, 1200))
            play_button = Button("Играть", 300, 500, 100, 100, "grey", "green")
            exit_button = Button("Выход", 600, 500, 100, 100, "grey", "red")
            screen.blit(fon, (125, 0))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.display.set_caption("TheBattleBears")
    pygame.init()
    size = width, height = 1000, 800
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    start_screen()
