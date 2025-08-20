import copy
import random
import pygame
import sys
pygame.init()

# @todo Выяснить что такое loop
# @todo Разобраться с корректным перезапуском программы (сворачиванием)
# @todo Разные типы ячеек - как классы с наследованием

def main_game_loop():
    SIDE = 64
    def load_scaled_image(path, size):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (size, size))

    def check_win(qurrent, win, type_of_quad, freez):
        for y in range(len(qurrent)):
            for x in range(len(qurrent[0])):
                if type_of_quad[y][x] != 1 and freez[y][x] != 2:
                    if qurrent[y][x] != win[y][x]:
                        return False
        return True

    def reload_win(type_of_quad, win):
        match type_of_quad:
            case 1: return pygame.image.load('items/empty.png')
            case 2: img = pygame.image.load('items/battery_active.png')
            case 3: img = pygame.image.load('items/light_active.png')
            case 4: img = pygame.image.load('items/straight_active.png')
            case 5: img = pygame.image.load('items/corner_active.png')
            case 6: img = pygame.image.load('items/cross_active.png')

        rotation_state = win
        if rotation_state == 2: img = pygame.transform.rotate(img, -90)
        elif rotation_state == 3: img = pygame.transform.rotate(img, 180)
        elif rotation_state == 4: img = pygame.transform.rotate(img, 90)
        return img

    def reload(type_of_quad, qurrent):
        match type_of_quad:
            case 1: img = pygame.image.load('items/empty.png')
            case 2: img = pygame.image.load('./items/battery.png')
            case 3: img = pygame.image.load('items/light.png')
            case 4: img = pygame.image.load('items/straight.png')
            case 5: img = pygame.image.load('items/corner.png')
            case 6: img = pygame.image.load('items/cross.png')
        
        rotation_state = qurrent
        if rotation_state == 2: img = pygame.transform.rotate(img, -90)
        elif rotation_state == 3: img = pygame.transform.rotate(img, 180)
        elif rotation_state == 4: img = pygame.transform.rotate(img, 90)
        return img

    def read_matrix_from_txt(file_path):
        with open(file_path, 'r') as file:
            return [[int(x) for x in line.strip().split()] for line in file]

    lvl = random.randint(1, 10)
    file_path = f'уровни/lvl-{lvl}.txt'
    matrix = read_matrix_from_txt(file_path)

    qurrent = copy.deepcopy(matrix)
    win = copy.deepcopy(matrix)
    type_of_quad = copy.deepcopy(matrix)
    freez = copy.deepcopy(matrix)

    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            type_of_quad[y][x] = int(str(matrix[y][x])[0])
            win[y][x] = int(str(matrix[y][x])[3])
            qurrent[y][x] = int(str(matrix[y][x])[1])
            freez[y][x] = int(str(matrix[y][x])[2])

    W = len(matrix[0]) * SIDE
    H = len(matrix) * SIDE
    sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    pygame.display.set_caption(f'Электропроводка v. 1.0 - уровень {lvl}')
    pygame.display.set_icon(pygame.image.load('items/light_active.png'))

    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if type_of_quad[y][x] == 1 or freez[y][x] == 2:
                sc.blit(load_scaled_image('items/empty.png', SIDE), (SIDE * x, SIDE * y))
            else:
                sc.blit(load_scaled_image('items/filled.png', SIDE), (SIDE * x, SIDE * y))
    
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if type_of_quad[y][x] not in [1, 0]:
                cell_img = reload(type_of_quad[y][x], qurrent[y][x])
                sc.blit(pygame.transform.scale(cell_img, (SIDE, SIDE)), (SIDE * x, SIDE * y))

    pygame.display.update()

    FPS = 60
    clock = pygame.time.Clock()
    game_won = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                mouse_X, mouse_Y = event.pos
            
            elif event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.size
                cell_size_x = new_width // len(matrix[0])
                cell_size_y = new_height // len(matrix)
                SIDE = max(min(cell_size_x, cell_size_y), 50)
                
                W = len(matrix[0]) * SIDE
                H = len(matrix) * SIDE
                sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
                
                for y in range(len(matrix)):
                    for x in range(len(matrix[0])):
                        if type_of_quad[y][x] == 1 or freez[y][x] == 2:
                            img = load_scaled_image('items/empty.png', SIDE)
                        else:
                            img = load_scaled_image('items/filled.png', SIDE)
                        sc.blit(img, (SIDE * x, SIDE * y))
                        
                        if type_of_quad[y][x] not in [1, 0]:
                            cell_img = reload(type_of_quad[y][x], qurrent[y][x])
                            scaled_cell = pygame.transform.scale(cell_img, (SIDE, SIDE))
                            sc.blit(scaled_cell, (SIDE * x, SIDE * y))
                
                if game_won:
                    restart_img = load_scaled_image('items/перезапуск.png', SIDE*2)
                    x_corner = (W - SIDE*2) // 2
                    y_corner = (H - SIDE*2) // 2
                    sc.blit(restart_img, (x_corner, y_corner))
                
                pygame.display.flip()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_won and event.button == 1:
                    X_quad = int(mouse_X) // SIDE
                    Y_quad = int(mouse_Y) // SIDE
                    if freez[Y_quad][X_quad] != 2 and type_of_quad[Y_quad][X_quad] != 1:
                        if type_of_quad[Y_quad][X_quad] == 4 and qurrent[Y_quad][X_quad] >= 2:
                            qurrent[Y_quad][X_quad] = 1
                        elif type_of_quad[Y_quad][X_quad] == 6:
                            qurrent[Y_quad][X_quad] = 1
                        else:
                            qurrent[Y_quad][X_quad] = qurrent[Y_quad][X_quad] % 4 + 1
                        
                        bg = load_scaled_image('items/filled.png', SIDE)
                        sc.blit(bg, (SIDE * X_quad, SIDE * Y_quad))
                        
                        cell_img = reload(type_of_quad[Y_quad][X_quad], qurrent[Y_quad][X_quad])
                        scaled_cell = pygame.transform.scale(cell_img, (SIDE, SIDE))
                        sc.blit(scaled_cell, (SIDE * X_quad, SIDE * Y_quad))
                        
                        pygame.display.update((SIDE * X_quad, SIDE * Y_quad, SIDE, SIDE))
                        
                        if check_win(qurrent, win, type_of_quad, freez):
                            game_won = True
                            for y in range(len(matrix)):
                                for x in range(len(matrix[0])):
                                    if type_of_quad[y][x] == 1 or freez[y][x] == 2:
                                        img = load_scaled_image('items/empty.png', SIDE)
                                    else:
                                        img = load_scaled_image('items/filled.png', SIDE)
                                    sc.blit(img, (SIDE * x, SIDE * y))
                                    
                                    if type_of_quad[y][x] not in [1, 0]:
                                        cell_img = reload_win(type_of_quad[y][x], win[y][x])
                                        scaled_cell = pygame.transform.scale(cell_img, (SIDE, SIDE))
                                        sc.blit(scaled_cell, (SIDE * x, SIDE * y))
                            
                            restart_img = load_scaled_image('items/перезапуск.png', SIDE*2)
                            x_corner = (W - SIDE*2) // 2
                            y_corner = (H - SIDE*2) // 2
                            sc.blit(restart_img, (x_corner, y_corner))
                            pygame.display.flip()
                
                elif game_won and event.button == 1:
                    btn_size = SIDE * 2
                    x_corner = (W - btn_size) // 2
                    y_corner = (H - btn_size) // 2
                    
                    if (x_corner <= mouse_X <= x_corner + btn_size and 
                        y_corner <= mouse_Y <= y_corner + btn_size):
                        return True

        clock.tick(FPS)
    
    return False

while True:
    should_restart = main_game_loop()
    if not should_restart:
        break