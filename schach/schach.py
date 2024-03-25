import pygame
import sys
import os
from pygame.locals import *

pygame.init()
WIDTH = 1024
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.FULLSCREEN)
pygame.display.set_caption('Schachspiel')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 30)
timer = pygame.time.Clock()
fps = 60

# Initialisieren des Gamepads
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

#path
python_file_path = os.path.abspath(__file__)
python_file_directory = os.path.dirname(python_file_path)
os.chdir(python_file_directory)


white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations =  [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7),(6,7), (7,7), 
                  (0,6), (1,6), (2,6), (3,6), (4,6), (5,6),(6,6), (7,6)]

black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0),(6,0), (7,0), 
                  (0,1), (1,1), (2,1), (3,1), (4,1), (5,1),(6,1), (7,1)]
captured_pieces_white = []
captured_pieces_black = []

turn_step = 0
selection = 100
valid_moves = []
x_select = 225
y_select = 450
menu_open = 0

black_queen = pygame.image.load('images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (60, 60))
black_queen_small = pygame.transform.scale(black_queen, (40, 40))
black_king = pygame.image.load('images/black king.png')
black_king = pygame.transform.scale(black_king, (60, 60))
black_king_small = pygame.transform.scale(black_king, (40, 40))
black_rook = pygame.image.load('images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (60, 60))
black_rook_small = pygame.transform.scale(black_rook, (40, 40))
black_bishop = pygame.image.load('images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (60, 60))
black_bishop_small = pygame.transform.scale(black_bishop, (40, 40))
black_knight = pygame.image.load('images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (60, 60))
black_knight_small = pygame.transform.scale(black_knight, (40, 40))
black_pawn = pygame.image.load('images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (45, 45))
black_pawn_small = pygame.transform.scale(black_pawn, (40, 40))
white_queen = pygame.image.load('images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (60, 60))
white_queen_small = pygame.transform.scale(white_queen, (40, 40))
white_king = pygame.image.load('images/white king.png')
white_king = pygame.transform.scale(white_king, (60, 60))
white_king_small = pygame.transform.scale(white_king, (40, 40))
white_rook = pygame.image.load('images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (60, 60))
white_rook_small = pygame.transform.scale(white_rook, (40, 40))
white_bishop = pygame.image.load('images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (60, 60))
white_bishop_small = pygame.transform.scale(white_bishop, (40, 40))
white_knight = pygame.image.load('images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (60, 60))
white_knight_small = pygame.transform.scale(white_knight, (40, 40))
white_pawn = pygame.image.load('images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (45, 45))
white_pawn_small = pygame.transform.scale(white_pawn, (40, 40))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

counter = 0
winner = ''
game_over = False



def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [450 - (column * 150), row * 75, 75, 75])
        else:
            pygame.draw.rect(screen, 'light gray', [525 - (column * 150), row * 75, 75, 75])
        pygame.draw.rect(screen, 'black', [600, 0, 424, HEIGHT], 5)
        pygame.draw.rect(screen, 'black', [600, 0, 424, 455], 5)
        status_text = ['Weiß: Wähle eine Figur!', 'Weiß: Ziehe deine Figur!',
                       'Schwarz: Wähle eine Figur!', 'Schwarz: Ziehe deine Figur!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (620, 510))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 75 * i), (600, 75 * i), 2)
            pygame.draw.line(screen, 'black', (75 * i, 0), (75 * i, 600), 2)



def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_images[index], (white_locations[i][0] * 75 + 15, white_locations[i][1] * 75 + 15))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 75 + 7, white_locations[i][1] * 75 + 7))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 75 + 1, white_locations[i][1] * 75 + 1,
                                                 75, 75], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_images[index], (black_locations[i][0] * 75 + 15, black_locations[i][1] * 75 + 15))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 75 + 7, black_locations[i][1] * 75 + 7))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 75 + 1, black_locations[i][1] * 75 + 1,
                                                  75, 75], 2)


def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list



def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
   
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list



def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


def check_pawn(position, color):
    moves_list = []
    if color == 'black':
        if (position[0], position[1] + 1) not in black_locations and \
                (position[0], position[1] + 1) not in white_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in black_locations and \
                    (position[0], position[1] + 2) not in white_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in black_locations and \
                (position[0], position[1] - 1) not in white_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in black_locations and \
                    (position[0], position[1] - 2) not in white_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list



def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
   
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options



def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 75 + 38, moves[i][1] * 75 + 38), 5)



def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (620, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (820, 5 + 50 * i))


def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'red', [white_locations[king_index][0] * 75 + 1,
                                                              white_locations[king_index][1] * 75 + 1, 75, 75], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'blue', [black_locations[king_index][0] * 75 + 1,
                                                               black_locations[king_index][1] * 75 + 1, 75, 75], 5)


def menu():
    pygame.draw.rect(screen, 'black', [200, 200, 500, 70])
    screen.blit(font.render(f'Drücke SPACE um ins Hauptmenü zu gelangen!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Drücke ENTER um Weiterzuspielen!', True, 'white'), (210, 240))


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 500, 110])
    screen.blit(font.render(f'{winner} hat das Spiel gewonnen!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Drücke SPACE zum Neustart!', True, 'white'), (210, 240))
    screen.blit(font.render(f'Drücke ENTER um ins Hauptmenü zu gelangen!', True, 'white'), (210, 270))


black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill((64, 64, 64))
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if menu_open == 1:
        menu()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if menu_open == 0:
            if event.type == JOYAXISMOTION:
                axis = event.axis
                value = event.value
                if axis == 0 and abs(value) > 0.5:
                    if value < 0:
                        if x_select < 525:
                            x_select += 75
                    elif value > 0:
                         if x_select > 0:
                            x_select -= 75
                if axis ==1 and abs(value) > 0.5:
                    if value < 0:
                        if y_select < 525:
                            y_select += 75
                    elif value > 0:
                         if y_select > 0:
                            y_select -= 75    
        elif not game_over:
            if menu_open == 1:
                if joystick.get_button(0):
                    menu_open = 0
                if joystick.get_button(3):
                    run = False
            else:
                print ("test")
                if joystick.get_button(0):
                    menu_open = 1
                
                elif joystick.get_button(1):
                    x_coord = x_select // 75
                    y_coord = y_select // 75
                    click_coords = (x_coord, y_coord)
                    if turn_step <= 1:
                        if click_coords == (8, 8) or click_coords == (9, 8):
                            winner = 'Schwarz'
                        if click_coords in white_locations:
                            selection = white_locations.index(click_coords)
                            if turn_step == 0:
                                turn_step = 1
                        if click_coords in valid_moves and selection != 100:
                            white_locations[selection] = click_coords
                            if click_coords in black_locations:
                                black_piece = black_locations.index(click_coords)
                                captured_pieces_white.append(black_pieces[black_piece])
                                if black_pieces[black_piece] == 'king':
                                    winner = 'Weiß'
                                black_pieces.pop(black_piece)
                                black_locations.pop(black_piece)
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 2
                            x_select = 300
                            y_select = 75
                            selection = 100
                            valid_moves = []
                    if turn_step > 1:
                        if click_coords == (8, 8) or click_coords == (9, 8):
                            winner = 'Weiß'
                        if click_coords in black_locations:
                            selection = black_locations.index(click_coords)
                            if turn_step == 2:
                                turn_step = 3
                        if click_coords in valid_moves and selection != 100:
                            black_locations[selection] = click_coords
                            if click_coords in white_locations:
                                white_piece = white_locations.index(click_coords)
                                captured_pieces_black.append(white_pieces[white_piece])
                                if white_pieces[white_piece] == 'king':
                                    winner = 'Schwarz'
                                white_pieces.pop(white_piece)
                                white_locations.pop(white_piece)
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 0
                            x_select = 225
                            y_select = 450
                            selection = 100
                            valid_moves = []         
        if event.type == pygame.JOYBUTTONDOWN and game_over:
            if event.button == 3:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations =  [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7),(6,7), (7,7), 
                  (0,6), (1,6), (2,6), (3,6), (4,6), (5,6),(6,6), (7,6)]

                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0),(6,0), (7,0), 
                  (0,1), (1,1), (2,1), (3,1), (4,1), (5,1),(6,1), (7,1)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
            if event.button == 0:
                run = False
    if turn_step < 2:
        pygame.draw.rect(screen, "red", (x_select, y_select, 75, 75), 5)
    else:
        pygame.draw.rect(screen, "blue", (x_select, y_select, 75, 75), 5)

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()
