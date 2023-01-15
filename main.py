import pygame
from numpy import roll
import os

# воспроизведение фоновой музыки
#pygame.mixer.music.play(-1)
#pygame.mixer.music.stop()

class MainWindow:
    def __init__(self, screen_size=(1920, 1080)):
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
        pass

    def make_new_level(self):
        pass

    def edit_level(self):
        self.new_level = True


class Game:
    def __init__(self, color, level):
        self.color = color
        self.level = level


    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '1':
                    Tile('red_orb_cl1', x, y)
                elif level[y][x] == '2':
                    Tile('blue_orb_cl1', x, y)
        return new_player, x, y


class LevelEditor:
    def __init__(self, level):
        self.level = level


images = {
    'red_orb_cl1': pygame.image.load('images/r_cl1.png'),
    'red_orb_cl2': pygame.image.load('images/r_cl2.png'),
    'blue_orb_cl1': pygame.image.load('images/b_cl1.png'),
    'blue_orb_cl2': pygame.image.load('images/b_cl2.png'),
}
def game():
    pygame.init()
    pygame.display.set_caption('The Line')
    clock = pygame.time.Clock()
    time_on = False
    speed = 10
    ticks = 0
    running = True
    # screen_size = list(map(int, input().split()))
    # Settings_start = MainWindow((screen_size[0], screen_size[1]))
    screen_size = (1920, 1080)
    Settings_start = MainWindow()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                y_pos_move = screen_size[1] // 7
                y_pos_btn = screen_size[1] // 4
                if screen_size[0] // 2.9 <= x <= screen_size[0] // 2.9 + screen_size[
                    1] // 1.5:  # Если нажатие мыши в области кнопок по x
                    if y_pos_btn <= y <= y_pos_btn + 100:  # Нажатие по первой кнопки
                        Settings_start.change_level()
                    elif y_pos_btn + y_pos_move <= y <= y_pos_btn + y_pos_move + 100:  # Нажатие по второй кнопке
                        Settings_start.start_game()
                    elif y_pos_btn + y_pos_move * 2 <= y <= y_pos_btn + y_pos_move * 2 + 100:  # Нажатие по третей кнопке
                        Settings_start.make_new_level()
                    elif y_pos_btn + y_pos_move * 3 <= y <= y_pos_btn + y_pos_move * 3 + 100:  # Нажатие по четвёртой кнопке
                        Settings_start.edit_level()
                    elif y_pos_btn + y_pos_move * 4 <= y <= y_pos_btn + y_pos_move * 4 + 100:  # Нажатие по пятой кнопке
                        Settings_start.change_color()

        pygame.display.flip()
    pygame.quit()
def main():
    pygame.init()
    pygame.display.set_caption('The Line')
    clock = pygame.time.Clock()
    time_on = False
    speed = 10
    ticks = 0
    running = True
    # screen_size = list(map(int, input().split()))
    # Settings_start = MainWindow((screen_size[0], screen_size[1]))
    screen_size = (1920, 1080)
    Settings_start = MainWindow()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                y_pos_move = screen_size[1] // 7
                y_pos_btn = screen_size[1] // 4
                if screen_size[0] // 2.9 <= x <= screen_size[0] // 2.9 + screen_size[
                    1] // 1.5:  # Если нажатие мыши в области кнопок по x
                    if y_pos_btn <= y <= y_pos_btn + 100:  # Нажатие по первой кнопки
                        Settings_start.change_level()
                    elif y_pos_btn + y_pos_move <= y <= y_pos_btn + y_pos_move + 100:  # Нажатие по второй кнопке
                        Settings_start.start_game()
                    elif y_pos_btn + y_pos_move * 2 <= y <= y_pos_btn + y_pos_move * 2 + 100:  # Нажатие по третей кнопке
                        Settings_start.make_new_level()
                    elif y_pos_btn + y_pos_move * 3 <= y <= y_pos_btn + y_pos_move * 3 + 100:  # Нажатие по четвёртой кнопке
                        Settings_start.edit_level()
                    elif y_pos_btn + y_pos_move * 4 <= y <= y_pos_btn + y_pos_move * 4 + 100:  # Нажатие по пятой кнопке
                        Settings_start.change_color()

        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    game()
