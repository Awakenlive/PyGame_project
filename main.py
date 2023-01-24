import pygame
from numpy import roll
import os
import sys

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
    fullname = 'images//' + fullname
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
    'green_line': load_image('right_click.jpg'),
    'blue_line': load_image('left_click.jpg'),
    'finish_line': load_image('finish.jpg')
}
player_image = load_image('player.jpg')
tile_width = 125
tile_height = 270

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


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


class Player(Sprite): # Невидимый игрок для камеры
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            125 * pos_x, 1080 * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y, flag=None):
        global play_game
        camera.dx -= 125
        self.pos = (x, y)
        if flag is True:
            camera.dx = 0
            play_game.flag_live = True
        for sprite in sprite_group:
            camera.apply(sprite)


class Camera:
    def __init__(self):
        self.dx = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx


    def update(self, target):
        self.dx = 0


def move(hero, flag=None):
    x, y = hero.pos
    if flag is True:
        hero.move(x, y)
    elif flag is False:
        hero.move(x, y, True)


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
speed = 1  # Скорость игрока, чем меньше, тем больше


class Game:
    def __init__(self, color, level, screen_size=(1920,1080)):
        global speed
        self.color = color  # Цвет игрока
        self.level = load_level('ананас.txt') # загрузить уровень
        self.actual_pos = 2
        self.health = int(self.level[1].split()[-1])
        self.all_lines = []
        self.flag_live = True
        self.screen_size = screen_size
        self.flag_game = True # В конце игры что бы выключить и показать заставку
        # self.play_music(self.level)

    def play_music(self, level_inf):  # Воспроизведение музыки
        pygame.mixer.music.load('songs/' + ''.join(level_inf[0]))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

    def mouse_click(self, button):
        global flag_mouse_click, hero
        flag_mouse_click = True
        if 'f' in self.level[self.actual_pos]:
            self.flag_game = False
        elif not(button == 'left' and '1' in self.level[self.actual_pos]
        or button == 'right' and '2' in self.level[self.actual_pos]): # если неправильно нажата кнопка мыши:
            self.health -= 1
            self.check_health()
            # Если персонаж мёртв игра начинается с начала

    def new_pos(self):
        self.actual_pos += 1

    # Обновление позиции

    def mouse_dont_clicked(self):
        self.health -= 1
        self.check_health()

    # Если не успели кликнуть

    def check_health(self):
        if self.health <= 0:
            self.health = int(self.level[1][-1])
            self.actual_pos = 2
            screen.fill('black')
            # self.play_music(self.level)
            self.flag_live = False
        # Проверка количества жизней у игрока

    # Для заливки фона (в том числе все спрайтов)
    def generate_level(self, level_inf):
        new_player, x, y = None, None, None
        for x in range(2, len(level_inf)):
            for y in range(len(level_inf[x])):
                if level_inf[x][y] == '1':
                    Tile('green_line', x, y)
                elif level_inf[x][y] == '2':
                    Tile('blue_line', x, y)
                elif level_inf[x][y] == 'f':
                    Tile('finish_line', x, y)
                elif level_inf[x][y] == '@':
                    new_player = Player(x, y)
        return new_player, x, y
    # Генерация уровня


class LevelEditor:
    def __init__(self, level, flag):
        self.level = level
        self.pos_mouse = pygame.mouse.get_pos()
        if flag is False:
            self.make_new_level()
        else:
            self.edit_old_level()

    def make_new_level(self):
        pass

    def edit_old_level(self):
        pass

    def get_pos_mouse(self):
        self.pos_mouse = pygame.mouse.get_pos()


clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
level_map = load_level('ананас.txt')


def test_level_editor():
    running = True
    screen_size = (1920, 1080)
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    FPS = 144
    level_editor = LevelEditor('ананас.txt', False)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Если кнопка мыши была нажата
                level_editor.get_pos_mouse()
        pygame.display.update()
        sprite_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


camera = Camera()
play_game = Game('red', level_map)
hero, max_x, max_y = play_game.generate_level(level_map)
camera.update(hero)

def test_game():
    global flag_mouse_click
    running = True
    screen_size = (1920, 1080)
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    FPS = 144
    time_start = pygame.time.get_ticks() # Таймер если человек не успел кликнуть
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Для комбинации ALT + F4
                running = False
                pygame.quit()
                sys.exit()
            time_end = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN and time_end - time_start <= 1000:
                if event.button == 1 or event.button == 3:
                    if event.button == 1:
                        play_game.mouse_click('left') #клик по левой кнопке
                    elif event.button == 3:
                        play_game.mouse_click('right') # клик по правой кнопку
                    play_game.new_pos()
                    flag_mouse_click = False
                    time_start = pygame.time.get_ticks()
                    move(hero, play_game.flag_live)
            elif 'f' in play_game.level[play_game.actual_pos]:
                running = False
            elif time_end - time_start >= 1000:
                time_start = pygame.time.get_ticks()
                if flag_mouse_click is False:  # Если клика не было произведено
                    play_game.health -= 1
                    play_game.new_pos()
                    play_game.check_health()
                    move(hero, play_game.flag_live)
                    # Если персонаж умер возвращение на старую позицию, если здоровье есть, то игра продолжается
        screen.fill(pygame.Color("black"))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Для комбинации ALT + F4
                running = False
                pygame.quit()
                sys.exit()
            background = pygame.image.load('images/You_win.jpg')
            background = pygame.transform.scale(background, (1920, 1080))
            screen.blit(background, (0, 0))
            pygame.display.flip()


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
                            running = False
                        elif y_pos_btn + y_pos_move * 2 <= y <= y_pos_btn + y_pos_move * 2 + 100:  # Нажатие по третей кнопке
                            Settings_start.make_new_level()
                        elif y_pos_btn + y_pos_move * 3 <= y <= y_pos_btn + y_pos_move * 3 + 100:  # Нажатие по четвёртой кнопке
                            Settings_start.edit_level()
                        elif y_pos_btn + y_pos_move * 4 <= y <= y_pos_btn + y_pos_move * 4 + 100:  # Нажатие по пятой кнопке
                            Settings_start.change_color()
            elif flag_game is True:
                pass
            elif flag_leveleditor is True:
                pass
            clock.tick(FPS)
            pygame.display.flip()
    test_game()


if __name__ == '__main__':
    main()
