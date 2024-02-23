import pygame

pygame.init()
WIDTH = 1024
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')
screen.fill((64, 64, 64))
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_location = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0),(6,0), (7,0), 
                  (0,1), (1,1), (2,1), (3,1), (4,1), (5,1),(6,1), (7,1)]

black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_location = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7),(6,7), (7,7), 
                  (0,6), (1,6), (2,6), (3,6), (4,6), (5,6),(6,6), (7,6)]

caputures_pieces_white = []
caputures_pieces_black = []

turn_step = 0
selection = 100
valid_moves = []

black_queen = pygame.image.load('images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (60, 60))

black_king = pygame.image.load('images/black king.png')
black_king = pygame.transform.scale(black_king, (60, 60))

black_knight = pygame.image.load('images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (60, 60))

black_rook = pygame.image.load('images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (60, 60))

black_bishop = pygame.image.load('images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (60, 60))

black_pawn = pygame.image.load('images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (60, 60))

black_images = [black_bishop, black_king, black_pawn, black_knight, black_rook, black_queen]


white_queen = pygame.image.load('images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (60, 60))

white_king = pygame.image.load('images/white king.png')
white_king = pygame.transform.scale(white_king, (60, 60))

white_knight = pygame.image.load('images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (60, 60))

white_rook = pygame.image.load('images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (60, 60))

white_bishop = pygame.image.load('images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (60, 60))

white_pawn = pygame.image.load('images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (60, 60))

white_images = [white_bishop, white_king, white_pawn, white_knight, white_rook, white_queen]


piece_list = ['bishop', 'king', 'pawn', 'knight', 'rook', 'queen']


def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [450 - (column * 150), row * 75, 75, 75])
        else:
            pygame.draw.rect(screen, 'light gray', [525 - (column * 150), row * 75, 75, 75])
        pygame.draw.rect(screen, 'black', [600, 0, 424, HEIGHT], 5)
        pygame.draw.rect(screen, 'black', [600, 0, 424, 450], 5)
        pygame.draw.rect(screen, 'red', [912, 450, 112, 150], 5)
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 75 * i), (600, 75 * i), 2)
            pygame.draw.line(screen, 'black', (75 * i, 0), (75 * i, 600), 2)
        status_text = ['Weiß: Wähle eine Figur aus!', 'Weiß: Mach einen Schritt!', 'Schwarz: Wähle eine Figur aus!', 'Schwarz: Mach einen Schritt!']

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        screen.blit(white_images[index], (white_location[i][0] * 75 + 7, white_location[i][1] * 75 + 7))

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        screen.blit(black_images[index], (black_location[i][0] * 75 + 7, black_location[i][1] * 75 + 7))


 
run = True
while run:
    timer.tick(fps)
    screen.fill((64, 64, 64))
    draw_board()
    draw_pieces()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
