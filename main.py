import pygame
from numpy import roll
import os
from time import time

flag_mainwindow = True
flag_game = False
flag_leveleditor = False
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)


def load_level(filename):
    filename = "levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


tile_images = {
    'red_orb_1': load_image('images//r_cl1.png'),
    'blue_orb_1': load_image('images//b_cl1.png')
}


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass

tile_width = tile_height = 125
class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()

images = {
    'red_orb_cl1': pygame.image.load('images//r_cl1.png'),
    'red_orb_cl2': pygame.image.load('images//r_cl2.png'),
    'blue_orb_cl1': pygame.image.load('images//b_cl1.png'),
    'blue_orb_cl2': pygame.image.load('images//b_cl2.png'),
}


class MainWindow:
    def __init__(self, screen_size=(1920, 1080)):
        global flag_mainwindow, flag_game, flag_leveleditor
        self.screen_size = screen_size
        self.all_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'white', 'black']  # Для выбора цвета игрока
        self.levels = os.listdir('levels')  # Все уровни
        self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        background = pygame.image.load('images/background.png')
        self.background = pygame.transform.scale(background, screen_size)
        self.screen.blit(self.background, (0, 0))
        # Заливка фона
        self.button_names = [f'Текущий уровень: {self.levels[0]}',
                             'Играть',
                             'Строить новый уровень',
                             'Редактировать уровень',
                             f'Цвет игрока: {self.all_colors[0]}']
        self.font = pygame.font.SysFont("Verdana", screen_size[1] // 25)
        self.new_level = False
        self.draw_buttons()

    def draw_buttons(self):
        self.screen.blit(self.background, (0, 0))
        self.x, self.y = self.screen_size[0] // 2.9, self.screen_size[1] // 4
        for i in self.button_names:
            text = self.font.render(i, True, '#A044C1')
            button = pygame.draw.rect(self.screen, 'White',
                                      (self.x - 10, self.y, self.screen_size[1] // 1.5, 100), 6)
            self.screen.blit(text, (self.x, self.y + 15))
            self.y += self.screen_size[1] // 7
        # Отрисовка кнопок

    def current_color(self):  # Текущий цвет
        return self.all_colors[0]

    def current_level(self):  # Текущий уровень
        return self.levels[0]

    def change_level(self):  # Циклический сдвиг списка уровней на 1
        self.levels = roll(self.levels, 1)
        print(self.levels)

    def change_color(self):  # Циклический сдвиг списка уровней на 1
        self.all_colors = roll(self.all_colors, 1)
        self.button_names[-1] = f'Текущий цвет: {self.all_colors[0]}'
        self.draw_buttons()

    def start_game(self):
        flag_game = True
        flag_mainwindow = False

    def make_new_level(self):
        flag_leveleditor = True
        flag_mainwindow = False

    def edit_level(self):
        flag_leveleditor = True
        flag_mainwindow = False
        self.new_level = True


flag_mouse_click = False  # Если было произведено нажатие на мышку


class Game:
    def __init__(self, color, level):
        self.color = color  # Цвет игрока
        self.level = load_level('ананас.txt')
        self.actual_pos = 2
        self.health = int(self.level[1][-1])
        self.generate_level(self.level)

    def play_music(self, level_inf):  # Воспроизведение музыки
        pygame.mixer.music.load('songs/' + ''.join(level_inf[0]))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

    def mouse_click(self, button):
        global flag_mouse_click
        flag_mouse_click = True
        if not (button == 'left' and '1' in self.level[self.actual_pos] or button == 'right' and '2' in self.level[
            self.actual_pos]):
            self.health -= 1
            self.check_health()
            # Если персонаж мёртв игра начинается с начала

    def mouse_dont_clicked(self):
        self.health -= 1
        self.check_health()

    def check_health(self):
        if self.health == 0:
            self.health = int(self.level[1][-1])
            self.actual_pos = 2
            self.play_music(self.level)

    def generate_level(self, level_inf):
        new_player, x, y = None, None, None
        for y in range(2, len(level_inf)):
            for x in range(len(level_inf[y])):
                if level_inf[y][x] == '1':
                    Tile('red_orb_1', x, y)
                elif level_inf[y][x] == '2':
                    Tile('blue_orb_1', x, y)
        return new_player, x, y
    # Загрузка карты уровня


class LevelEditor:
    def __init__(self, level):
        self.level = level


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0


def test_game():
    global flag_mouse_click

    running = True
    screen_size = (1920, 1080)
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    FPS = 144
    clock = pygame.time.Clock()
    sprite_group = SpriteGroup()
    hero_group = SpriteGroup()
    level_map = load_level('ананас.txt')
    play_game = Game('red', level_map)
    hero, max_x, max_y = play_game.generate_level(level_map)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # левая кнопка мыши
                        play_game.mouse_click('left')
                    if event.button == 3:  # правая кнопка мыши
                        play_game.mouse_click('right')
            if flag_mouse_click is True:
                flag_mouse_click = False
        sprite_group.draw(screen)
        hero_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


def main():
    pygame.init()
    pygame.display.set_caption('The Line')
    running = True
    # screen_size = list(map(int, input().split()))
    # Settings_start = MainWindow((screen_size[0], screen_size[1]))
    screen_size = (1920, 1080)
    Settings_start = MainWindow()
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    FPS = 144
    clock = pygame.time.Clock()
    sprite_group = SpriteGroup()
    hero_group = SpriteGroup()
    level_map = 'ye.txt'
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if flag_mainwindow is True:
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    y_pos_move = screen_size[1] // 7
                    y_pos_btn = screen_size[1] // 4
                    if screen_size[0] // 2.9 <= x <= screen_size[0] // 2.9 + screen_size[1] // 1.5:
                        # Если нажатие мыши в области кнопок по x
                        if y_pos_btn <= y <= y_pos_btn + 100:  # Нажатие по первой кнопки
                            Settings_start.change_level()
                            level_map = Settings_start.current_level()
                        elif y_pos_btn + y_pos_move <= y <= y_pos_btn + y_pos_move + 100:  # Нажатие по второй кнопке
                            Settings_start.start_game()
                        elif y_pos_btn + y_pos_move * 2 <= y <= y_pos_btn + y_pos_move * 2 + 100:  # Нажатие по третей кнопке
                            Settings_start.make_new_level()
                        elif y_pos_btn + y_pos_move * 3 <= y <= y_pos_btn + y_pos_move * 3 + 100:  # Нажатие по четвёртой кнопке
                            Settings_start.edit_level()
                        elif y_pos_btn + y_pos_move * 4 <= y <= y_pos_btn + y_pos_move * 4 + 100:  # Нажатие по пятой кнопке
                            Settings_start.change_color()
            elif flag_game is True:
                test_game()
            elif flag_leveleditor is True:
                pass
            clock.tick(FPS)
            pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    test_game()
