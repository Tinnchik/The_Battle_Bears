import os
import sys

import pygame


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None, argv=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.argv = argv

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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                if self.argv is not None:
                    self.action(self.argv)
                else:
                    self.action()


FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fl = 0
    fon = pygame.transform.scale(load_image('fon.jpg'), (600, 270))
    play_button = Button("Играть", 100, 300, 100, 100, "grey", "green")
    exit_button = Button("Выход", 400, 300, 100, 100, "grey", "red")
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect(400, 300, 100, 100).collidepoint(
                    event.pos) and not fl:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect(100, 300, 100, 100).collidepoint(event.pos):
                fl = 1
                screen.fill((255, 255, 255))
            if not fl:
                play_button.draw(screen)
                exit_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    start_screen()
