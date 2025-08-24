import copy 
import random
import pygame
pygame.init()

# Узнать что такое loop()
#   loop -> с англ. 'петля', в контексте программы
#   обозначает основной код в виде функции, который как бы идет по петле

side = 64

class Cell:
    def __init__(self, cell_type, rotation, frozen, win_pos):
        self.cell_type = cell_type
        self.rotation = rotation
        self.frozen = frozen
        self.win_pos = win_pos

    def can_rotate(self):
        if self.frozen != 2 and self.cell_type != 1 and self.cell_type != 6:
            return True
        else:
            return False

    def rotate(self):
        if self.can_rotate() and self.cell_type != 4:
            self.rotation = self.rotation % 4 + 1
        elif self.can_rotate() and self.cell_type == 4:
            self.rotation = self. rotation % 2 + 1

    def is_win(self):
        return self.rotation == self.win_pos

    def draw(self, surface, x, y, side, all_active):
        image = self.get_image(all_active)
        image = pygame.transform.scale(image, (side, side))
        surface.blit(image, (x * side, y * side))

    def rotate_image(image, rotation):
        if rotation == 2:
            return pygame.transform.rotate(image, -90)
        elif rotation == 3:
            return pygame.transform.rotate(image, 180)
        elif rotation == 4:
            return pygame.transform.rotate(image, 90)
        return image

class EmptyCell(Cell):
    def get_image(self, all_active=False):
        return pygame.image.load('items/empty.png')

class BatteryCell(Cell):
    def get_image(self, all_active=False):
        if all_active:
            image = pygame.image.load('items/battery_active.png')
        else:
            image = pygame.image.load('items/battery.png')
        return Cell.rotate_image(image, self.rotation)

class LightCell(Cell):
    def get_image(self, all_active=False):
        if all_active:
            image = pygame.image.load('items/light_active.png')
        else:
            image = pygame.image.load('items/light.png')
        return Cell.rotate_image(image, self.rotation)

class StraightCell(Cell):
    def get_image(self, all_active=False):
        if all_active:
            image = pygame.image.load('items/straight_active.png')
        else:
            image = pygame.image.load('items/straight.png')
        if self.rotation == 2:
            image = pygame.transform.rotate(image, -90)
        return image

class CornerCell(Cell):
    def get_image(self, all_active=False):
        if all_active:
            image = pygame.image.load('items/corner_active.png')
        else:
            image = pygame.image.load('items/corner.png')
        return Cell.rotate_image(image, self.rotation)

class CrossCell(Cell):
    def get_image(self, all_active=False):
        if all_active:
            image = pygame.image.load('items/cross_active.png')
        else:
            image = pygame.image.load('items/cross.png')
        return image

def create_cell(cell_type, rotation, frozen, win):
    if cell_type == 1:
        return EmptyCell(cell_type, rotation, frozen, win)
    elif cell_type == 2:
        return BatteryCell(cell_type, rotation, frozen, win)
    elif cell_type == 3:
        return LightCell(cell_type, rotation, frozen, win)
    elif cell_type == 4:
        return StraightCell(cell_type, rotation, frozen, win)
    elif cell_type == 5:
        return CornerCell(cell_type, rotation, frozen, win)
    elif cell_type == 6:
        return CrossCell(cell_type, rotation, frozen, win)

def read_matrix_from_txt(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        for line in file:
            row = []
            for cell_str in line.strip().split():
                cell_type = int(cell_str[0])
                rotation = int(cell_str[1])
                frozen = int(cell_str[2])
                win = int(cell_str[3])
                row.append(create_cell(cell_type, rotation, frozen, win))
            matrix.append(row)
    return matrix

def inspect_win(matrix):
    for row in matrix:
        for cell in row:
            if cell.cell_type != 1 and cell.cell_type !=6 and cell.frozen != 2:
                if not cell.is_win():
                    return False
    return True

def choice_next_lvl(lvls):
    if not lvls:
        lvls = list(range(1, 11))
    lvl = random.choice(lvls)
    lvls.remove(lvl)
    return lvl, lvls

def draw_field(scene, matrix, side, all_active=False):
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell.cell_type == 1 or cell.frozen == 2:
                image = pygame.image.load('items/empty.png')
            else:
                image = pygame.image.load('items/filled.png')
            image = pygame.transform.scale(image, (side, side))
            scene.blit(image, (side * x, side * y))
            if cell.cell_type != 1:
                cell.draw(scene, x, y, side, all_active)
    pygame.display.update()


def main_game_loop(file_path, side):
    matrix = read_matrix_from_txt(file_path)

    W = len(matrix[0]) * side
    H = len(matrix) * side
    sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    pygame.display.set_caption(f'GameElectro - level {lvl}')
    pygame.display.set_icon(pygame.image.load('items/light_active.png'))

    draw_field(sc, matrix, side)
    FPS = 10
    clock = pygame.time.Clock()
    game_won = False
    mouse_X, mouse_Y = 0, 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_X, mouse_Y = event.pos
            elif event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.size
                cell_size_x = new_width // len(matrix[0])
                cell_size_y = new_height // len(matrix)
                side = max(min(cell_size_x, cell_size_y), 50)
                W = len(matrix[0]) * side
                H = len(matrix) * side
                sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
                draw_field(sc, matrix, side, game_won)
                if game_won:
                    restart_image = pygame.image.load('items/перезапуск.png')
                    restart_image = pygame.transform.scale(restart_image, (side*2, side*2))
                    x_corner = (W - side*2) // 2
                    y_corner = (H - side*2) // 2
                    sc.blit(restart_image, (x_corner, y_corner))
                    pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_won and event.button == 1:
                    X_quad = int(mouse_X) // side
                    Y_quad = int(mouse_Y) // side
                    if 0 <= Y_quad < len(matrix) and 0 <= X_quad < len(matrix[0]):
                        cell = matrix[Y_quad][X_quad]
                        if cell.can_rotate():
                            cell.rotate()
                            game_won = inspect_win(matrix)
                            draw_field(sc, matrix, side, game_won)
                            if game_won:
                                restart_image = pygame.image.load('items/перезапуск.png')
                                restart_image = pygame.transform.scale(restart_image, (side*2, side*2))
                                x_corner = (W - side*2) // 2
                                y_corner = (H - side*2) // 2
                                sc.blit(restart_image, (x_corner, y_corner))
                                pygame.display.flip()
                elif game_won and event.button == 1:
                    btn_size = side * 2
                    x_corner = (W - btn_size) // 2
                    y_corner = (H - btn_size) // 2
                    if (x_corner <= mouse_X <= x_corner + btn_size and
                        y_corner <= mouse_Y <= y_corner + btn_size):
                        return True, side
        clock.tick(FPS)
    return False, side

lvls = list(range(1, 11))

while True:
    lvl, lvls = choice_next_lvl(lvls)
    file_path = f'levels/lvl-{lvl}.txt'
    should_restart, side = main_game_loop(file_path, side)
    if not should_restart:
        break