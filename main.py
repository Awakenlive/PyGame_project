import pygame
from numpy import roll
import os
import sys

with open("settings/settings.txt", encoding="cp1251") as f:
    text = f.readlines()
screen_size = (int(text[0].strip().split()[-2]), int(text[0].strip().split()[-1])) # Размер экрана
speed = text[1].strip().split()[-1] # Скорость игрока
actual_level = text[2].strip().split()[-1] # Текущий уровень
f.close()

pygame.init()
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)



def load_level(filename):
    filename = "levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map
    # Для загрузки уровней


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
    # Для загрузки изображений


tile_images = {
    'green_line': load_image('right_click.jpg'),
    'blue_line': load_image('left_click.jpg'),
    'finish_line': load_image('finish.jpg')
}

player_image = [load_image('red.jpg'), load_image('orange.jpg'), load_image('yellow.jpg'), load_image('green.jpg'),
                load_image('blue.jpg'), load_image('white.jpg')]
# Загрузка всех объектов в игре
tile_width = 125
tile_height = 270


# Длина и высота плиточек в игре (зелёных и голубых)

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


class Player(Sprite):  # Невидимый игрок для камеры
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image[0]
        self.rect = self.image.get_rect().move(
            125 * pos_x, 1080 * pos_y)
        self.pos = (pos_x, pos_y)

    def new_img(self, pos_x, pos_y):  # Для загрузки картинки игрока после изменений
        self.image = player_image[0]
        self.rect = self.image.get_rect().move(
            125 * pos_x, 1080 * pos_y)

    def move(self, x, y, flag=None):
        global play_game
        camera.dx -= 125
        self.pos = (x, y)
        if flag is True:
            play_game.flag_live = True
            camera.dx = 0
        for sprite in sprite_group:
            camera.apply(sprite)
    # Для работы камеры


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
    # Для дальнейшего работы с классом player


class MainWindow:
    def __init__(self):
        global flag_mainwindow, flag_game, flag_leveleditor, screen_size
        self.screen_size = screen_size
        self.all_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'white']  # Для выбора цвета игрока
        self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        background = pygame.image.load('images/background.png')
        self.background = pygame.transform.scale(background, screen_size)
        self.screen.blit(self.background, (0, 0))
        # Заливка фона
        self.button_names = ['Играть',
                             f'Цвет игрока: {self.current_color()}']
        self.text = ['Правила:', 'Зелёная плитка - правый клик', 'Голубая плитка - левый клик']
        # Название всех кнопок
        self.font = pygame.font.SysFont("Verdana", screen_size[1] // 25)
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
        for j in range(3):
            text = self.font.render(self.text[j], True, '#A044C1')
            self.screen.blit(text, (self.x, self.y))
            self.y += self.screen_size[1] // 10
        # Отрисовка кнопок и текста

    def current_color(self):  # Текущий цвет
        return self.all_colors[0]

    def change_color(self):  # Циклический сдвиг списка цветов на 1
        global player_image
        player_image = roll(player_image, 1)
        self.all_colors = roll(self.all_colors, 1)
        self.button_names[-1] = f'Текущий цвет: {self.current_color()}'
        self.draw_buttons()


flag_mouse_click = False  # Если было произведено нажатие на мышку


class Game:
    def __init__(self):
        global screen_size, actual_level
        self.level = load_level(actual_level)  # загрузить уровень
        self.actual_pos = 2
        self.health = int(self.level[1].split()[-1])  # Количество жизней
        self.screen_size = screen_size
        self.flag_live = True  # Если персонаж жив

    def play_music(self, level_inf):
        pygame.mixer.music.load('songs/' + ''.join(level_inf[0]))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        # Загрузка музыки

    def mouse_click(self, button):  # Обработка событий мыши и сравнение их с тем, что должно быть нажато (см карту)
        global flag_mouse_click, hero
        flag_mouse_click = True
        if 'f' in self.level[self.actual_pos]:
            self.flag_game = False
        elif '1' in self.level[self.actual_pos] or '2' in self.level[self.actual_pos]:
            if not (button == 'left' and '1' in self.level[self.actual_pos]
                    or button == 'right' and '2' in self.level[
                        self.actual_pos]):  # если неправильно нажата кнопка мыши:
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
            self.health = int(self.level[1].split()[-1])
            self.actual_pos = 2
            self.play_music(self.level)
            self.flag_live = False
        # Проверка количества жизней у игрока

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


clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
current_level = 'ананас.txt'


def main():
    global current_level, screen_size
    pygame.init()
    running = True
    Settings_start = MainWindow()
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    FPS = 144
    clock = pygame.time.Clock()
    flag_game = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:  # Проверка место клика мыши, вдруг оно поподает по площади кнопки
                x, y = pygame.mouse.get_pos()
                y_pos_move = screen_size[1] // 7
                y_pos_btn = screen_size[1] // 4
                if screen_size[0] // 2.9 <= x <= screen_size[0] // 2.9 + screen_size[1] // 1.5:
                    # Если нажатие мыши в области кнопок по x
                    if y_pos_btn <= y <= y_pos_btn + 100:  # Нажатие по первой кнопки
                        running = False
                    elif y_pos_btn + y_pos_move <= y <= y_pos_btn + y_pos_move + 100:  # Нажатие по второй кнопке
                        Settings_start.change_color()
            clock.tick(FPS)
            pygame.display.flip()
    game()

camera = Camera()
play_game = Game()
level_map = load_level(actual_level)
hero, max_x, max_y = play_game.generate_level(level_map)
camera.update(hero)
# Загрузка уровня

def game():
    global flag_mouse_click, camera, screen_size, speed
    running = True
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    screen.fill('black')
    FPS = 144
    time_start = pygame.time.get_ticks()  # Таймер если человек не успел кликнуть
    player = Player(2, 0)
    player.new_img(player.pos[0], player.pos[1])
    play_game.play_music(play_game.level)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Для комбинации ALT + F4
                running = False
                pygame.quit()
                sys.exit()
            time_end = pygame.time.get_ticks()  # Количество миллисекунд с начала игры
            if event.type == pygame.MOUSEBUTTONDOWN and time_end - time_start <= int(speed):  # Если количество
                if event.button == 1 or event.button == 3:
                    if event.button == 1:
                        play_game.mouse_click('left')  # клик по левой кнопке
                    elif event.button == 3:
                        play_game.mouse_click('right')  # клик по правой кнопку
                    play_game.new_pos()
                    flag_mouse_click = False
                    time_start = pygame.time.get_ticks()  # Обновляем количество секунд для таймера
                    move(hero, play_game.flag_live)
                    screen.fill(pygame.Color("black"))
            elif 'f' in play_game.level[play_game.actual_pos]:  # Если это конец игры
                running = False
            elif time_end - time_start >= int(speed):
                time_start = pygame.time.get_ticks()  # Обновляем количество секунд для таймера
                if flag_mouse_click is False:  # Если клика не было произведено
                    play_game.health -= 1
                    play_game.new_pos()
                    play_game.check_health()
                    move(hero, play_game.flag_live)
                    screen.fill(pygame.Color("black"))
                    # Если персонаж умер возвращение на старую позицию, если здоровье есть, то игра продолжается
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
            background = pygame.transform.scale(background, screen_size)
            screen.blit(background, (0, 0))
            pygame.display.flip()
            # Заставка с победой


if __name__ == '__main__':
    main()
