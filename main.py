import pygame as pg
from piece import Piece
import numpy as np
import sys
import os
import time
pg.init()
pg.font.init()

os.environ['SDL_VIDEO_CENTRED'] = '1'

b_pawn0, b_pawn1, b_pawn2, b_pawn3, b_pawn4, b_pawn5, b_pawn6, b_pawn7 = Piece(), Piece(), Piece(), Piece(), Piece(),\
                                                                         Piece(), Piece(), Piece()
b_rook0, b_knight0, b_bishop0, b_queen, b_king, b_bishop1, b_knight1, b_rook1 = Piece(), Piece(), Piece(), Piece(), \
                                                                                Piece(), Piece(), Piece(), Piece()
w_pawn0, w_pawn1, w_pawn2, w_pawn3, w_pawn4, w_pawn5, w_pawn6, w_pawn7 = Piece(), Piece(), Piece(), Piece(), Piece(), \
                                                                          Piece(), Piece(), Piece()
w_rook0, w_knight0, w_bishop0, w_queen, w_king, w_bishop1, w_knight1, w_rook1 = Piece(), Piece(), Piece(), Piece(), \
                                                                                 Piece(), Piece(), Piece(), Piece()
board = [
        b_pawn0, b_pawn1, b_pawn2, b_pawn3, b_pawn4, b_pawn5, b_pawn6, b_pawn7,
        b_rook0, b_knight0, b_bishop0, b_queen, b_king, b_bishop1, b_knight1, b_rook1,
        w_pawn0, w_pawn1, w_pawn2, w_pawn3, w_pawn4, w_pawn5, w_pawn6, w_pawn7,
        w_rook0, w_knight0, w_bishop0, w_queen, w_king, w_bishop1, w_knight1, w_rook1,
        ]
# board contains the pieces, eachn individual piece will contain its own x, y coords , eg x =0, y = 1
# asset paths
assets = [
    "chess_assets/b_pawn.png", "chess_assets/b_rook.png", "chess_assets/b_knight.png", "chess_assets/b_bishop.png",
    "chess_assets/b_queen.png", "chess_assets/b_king.png",
    "chess_assets/w_pawn.png", "chess_assets/w_rook.png", "chess_assets/w_knight.png", "chess_assets/w_bishop.png",
    "chess_assets/w_queen.png", "chess_assets/w_king.png",
    ]

boardfilled = np.zeros((8, 8)) - 1  # 0 is empty square, 1 if filled
# these will be used to index the squarecoords array and draw the pieces
border = 30
board_dim = 800
SURFACE = pg.display.set_mode((board_dim + border, board_dim + border))
pg.display.set_caption("Chess")
grey = 47, 79, 79
white = 255, 255, 255
black = 0, 0, 0
colouter = (255, 100, 50)
colinner = (161, 159, 16)
squarecoords = np.zeros((8, 8, 2), dtype=int)

# x axis offsets for pieces
# offsets for corresponding piece types
offset = [18, 19, 19, 20, 17, 21]

# board conditions
gameover = False
PLAYER_BLACK = True
PLAYER_WHITE = False
CURR_PLAYER = PLAYER_WHITE
clicked = False
xc, yc = 0, 0
colorshift = 0
s_piece = Piece()  # piece selected to be moved by the player
s_moves = []


def init():
    global board, squarecoords, boardfilled
    line = np.arange(border/2, board_dim - border/2, board_dim/8)
    for x in range(0, 8):
        for y in range(0, 8):
            squarecoords[y][x][0] = line[x]  # x pos
            squarecoords[y][x][1] = line[y]  # y pos

            if y < 2:
                boardfilled[y][x] = 1
            elif y > 5:
                boardfilled[y][x] = 0

        # init pieces
        board[x].owner = board[x+8].owner = True
        board[x + 16].owner = board[x+24].owner = False
        board[x + 8].type = x+1 if x < 5 else 8-x
        board[x + 24].type = x+1 if x < 5 else 8-x
        # init pawns
        # board[x].subindex = board[x+16].subindex = x

        # init coords
        board[x+8].y = 0
        board[x].y = 1
        board[x + 16].y = 6
        board[x + 24].y = 7
        board[x].x = board[x+8].x = x
        board[x+16].x = board[x+24].x = x


def drawboard():
    SURFACE.fill(grey)

    # draw squares
    for x in range(0, 8):
        for y in range(0, 8):
            colour = black
            if (x + y) % 2 == 0:
                colour = white
            pg.draw.rect(SURFACE, colour, (squarecoords[x][y][0], squarecoords[x][y][1], board_dim/8, board_dim/8))
    # draw pieces
    for x in range(0, 8):
        for m in range(0, 4):
            if board[x+m*8].alive:
                im = pg.image.load(assets[board[x + m*8].type]) if m < 2 else pg.image.load(assets[board[x + m*8].type + 6])
                SURFACE.blit(im, (squarecoords[board[x + m*8].y][board[x+m*8].x][0] + offset[board[x+m*8].type],
                                  squarecoords[board[x + m*8].y][board[x+m*8].x][1] - 1))

    SURFACE.blit(SURFACE, (0, 0))
    # pg.display.flip()


def selectsquare(x, y, colorchange):
    # draw changing color around square, clicktime is time the square was clicked on
    if x != -1 and y != -1:
        global squarecoords
        # col = (255-colorchange, 100, 50+colorchange) colchange max = 205
        col = (180, 200 - colorchange, 50+colorchange)
        pg.draw.rect(SURFACE, col, (squarecoords[y][x][0], squarecoords[y][x][1], board_dim/8, board_dim/8), 4)
        SURFACE.blit(SURFACE, (0, 0))


def findclicked(x, y):
    xguess, yguess = board_dim/8, board_dim/8
    insideflag = False
    for r in range(0, 8):
        if abs(y - squarecoords[r][0][1]) < yguess:
            yguess = int(r)
        if abs(x - squarecoords[0][r][0]) < xguess:
            xguess = int(r)
        if xguess < 9 and yguess < 9:
            insideflag = True
            break
    return (xguess, yguess) if insideflag else (-1, -1)


def movepiece(pxc, pyc, pxn, pyn):
    global board, s_piece, gameover
    for p in board:
        if p.alive:
            if p.x == pxn and p.y == pyn and p.owner != CURR_PLAYER:
                p.alive = False
                if p.type == 5:
                    gameover = True
            elif p.x == pxc and p.y == pyc and p.owner == CURR_PLAYER:
                p.x = pxn
                p.y = pyn
            if not p.type:
                if p.owner and p.y == 7 or not p.owner and p.y == 0:
                    p.type = 4  # peice promtion to a queen (any rational player would do this)



def findspiece(pxc, pyc):
    global board, s_piece
    for p in board:
        if p.alive:
            if p.x == pxc and p.y == pyc:  # and p.owner == CURR_PLAYER:
                s_piece = p


def highlightpossible(mov):
    global squarecoords, colinner, colouter
    for mo in mov:
        # col = (255-colorchange, 100, 50+colorchange) colchange max = 205
        y, x = mo[0], mo[1]
        pg.draw.rect(SURFACE, colouter,
                     (squarecoords[x][y][0], squarecoords[x][y][1], (board_dim / 8), (board_dim / 8)), 2)
        pg.draw.rect(SURFACE, colinner,
                     (squarecoords[x][y][0]+2, squarecoords[x][y][1]+2, (board_dim / 8)-4, (board_dim / 8)-4), 2)
        pg.draw.rect(SURFACE, colouter,
                     (squarecoords[x][y][0]+4, squarecoords[x][y][1]+4, (board_dim / 8)-8, (board_dim / 8)-8), 2)
        SURFACE.blit(SURFACE, (0, 0))


def checktest():
    # test if you have put the other player into check, then test if your own piece are in check
    global CURR_PLAYER, boardfilled, board
    opponent = 0 if CURR_PLAYER else 16
    currp = abs(opponent - 16)
    # testing if my moves have put the other player in check
    kingop = board[12+opponent]
    mkingop = [[kingop.x, kingop.y]]  # kingop.getpossiblemoves(boardfilled)
    kingc = board[12+currp]
    mkingc = [[kingc.x, kingc.y]]  # kingc.getpossiblemoves(boardfilled)

    for x in range(0, 16):
        if x % 12 != 0:
            movec = board[x + currp].getpossiblemoves(boardfilled)
            for mc in movec:
                mask = mkingop == mc
                copies = np.array(mask.all(axis=1))
                if np.any(copies, axis=0):
                    writetext(0)  # opponent in check
            moveop = board[x + opponent].getpossiblemoves(boardfilled)
            for mop in moveop:
                mask = mkingc == mop
                copies = np.array(mask.all(axis=1))
                if np.any(copies, axis=0):
                    writetext(2)  # curr player in check


def writetext(call):
    startTime = t = int(round(time.time()))
    if call == 1:
        winstring = 'white is the winner' if CURR_PLAYER else 'black is the winner'
    else:
        startTime = t = int(round(time.time()))
        winstring = 'you are in check' if call == 2 else 'opponent in check'
    while t - startTime < 3 or call:
        font = pg.font.SysFont('Calibri', 100)
        font2 = pg.font.SysFont('Calibri', 101)
        text = font.render(winstring, True, colinner)
        text2 = font2.render(winstring, True, colouter)
        SURFACE.blit(text, (50, 50))
        SURFACE.blit(text2, (47, 49))
        t = int(round(time.time()))
        call = False
        pg.display.flip()


init()
while True:
    drawboard()
    if not clicked and not gameover:
        pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            # get which button was clicked:
            (b1, b2, b3) = pg.mouse.get_pressed()
            colorshift = 0
            if b1:
                if clicked:
                    # move the piece from xc yc to xn yn (new positions)
                    (xn, yn) = pg.mouse.get_pos()
                    xn, yn = findclicked(xn, yn)
                    # if (xn, yn) is in the np array of all possible moves,
                    # which is returned from getpossible(Piece), then move piece
                    # findspiece(xc, yc)
                    if CURR_PLAYER == s_piece.owner:
                        s_moves = s_piece.getpossiblemoves(boardfilled)
                        for m in s_moves:
                            if m[0] == xn and m[1] == yn:
                                clicked = False
                                movepiece(xc, yc, xn, yn)
                                boardfilled[yc][xc] = -1
                                boardfilled[yn][xn] = CURR_PLAYER
                                # test for check
                                checktest()
                                CURR_PLAYER = not CURR_PLAYER
                                moves = []
                                break

                else:
                    clicked = True
                    s_moves = []
                    (xc, yc) = pg.mouse.get_pos()
                    xc, yc = findclicked(xc, yc)  # clicked coords
                    if boardfilled[yc][xc] == -1:
                        clicked = False
                    findspiece(xc, yc)
                    if CURR_PLAYER == s_piece.owner:
                        s_moves = s_piece.getpossiblemoves(boardfilled)
            elif b3:
                clicked = False
                s_moves = []
            elif b2:
                # click middle mouse button to restore board to previous state ( undo move)
                pass
    if clicked:
        if colorshift < 200:
            colorshift += 1
            highlightpossible(s_moves)
            selectsquare(xc, yc, colorshift)
            if not gameover:
                pg.display.flip()

    if gameover:
        writetext(1)

