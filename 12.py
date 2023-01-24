import pygame
if event.type == pygame.MOUSEBUTTONDOWN and time_end - time_start <= 1000:
    if event.button == 1 or event.button == 3:
         # Клик по левой кнопки мышки (зелёная линия)
        if event.button == 1 and pygame.key.get_mods() & pygame.K_a:
            play_game.mouse_click('left', 'a')
        elif event.button == 1 and pygame.key.get_mods() & pygame.K_s:
            play_game.mouse_click('left', 's')
        elif event.button == 1 and pygame.key.get_mods() & pygame.K_d:
            play_game.mouse_click('left', 'd')
        elif event.button == 1 and pygame.key.get_mods() & pygame.K_f:
            play_game.mouse_click('left', 'f')
        if event.button == 3 and pygame.key.get_mods() & pygame.K_a:
            play_game.mouse_click('right', 'a')
        elif event.button == 3 and pygame.key.get_mods() & pygame.K_s:
            play_game.mouse_click('right', 's')
        elif event.button == 3 and pygame.key.get_mods() & pygame.K_d:
            play_game.mouse_click('right', 'd')
        elif event.button == 3 and pygame.key.get_mods() & pygame.K_f:
            play_game.mouse_click('right', 'f')
        # Клик по правой кнопки мышки (голубая линия)
        play_game.new_pos()
        flag_mouse_click = False
        time_start = pygame.time.get_ticks()
        move(hero, play_game.flag_live)
  def mouse_click(self, button, key):
        global flag_mouse_click, hero
        flag_mouse_click = True
        if not(button == 'left' and '1' in self.level[self.actual_pos]): # если неправильно нажата кнопка мыши
            if not(key == 'a' and self.level[self.actual_pos][0] == 1 or
            key == 's' and self.level[self.actual_pos][1] == 1 or
            key == 'd' and self.level[self.actual_pos][2] == 1 or
            key == 'f' and self.level[self.actual_pos][3] == 1):
                self.health -= 1
                self.check_health()
        elif not(button == 'right' and '2' in self.level[self.actual_pos]):
            if not(key == 'a' and self.level[self.actual_pos][0] == 2 or
            key == 's' and self.level[self.actual_pos][1] == 2 or
            key == 'd' and self.level[self.actual_pos][2] == 2 or
            key == 'f' and self.level[self.actual_pos][3] == 2):
                self.health -= 1
                self.check_health()
            # Если персонаж мёртв игра начинается с начала
