import numpy as np


class Piece:

    owner = False  # piece is owned by player White # white  = False, black = True
    type = 0    # piece is of type {0:pawn, 1:rook, 2:knight, 3: bishop, 4:queen, 5:king}
    subindex = 0  # piece's subindex from right to left
    #  0 by default, 1 for dulicate (e.g 0 for right rook, 1 for left rook),cap at 7 for pawns
    alive = True

    # subindexmax = 0  # max number of these pieces, used for looping through in  -- is this needed?
    # row col coords
    y = 0
    x = 0

    def getpossiblemoves(self, boardfilled):
        moves = np.array([[-1, -1]])
        sx, sy = self.x, self.y   # search x y
        if not self.type:   # true if pawn
            a = 1 if self.owner else -1
            if boardfilled[self.y+a][self.x] == -1:
                moves = np.concatenate((np.array([[self.x, self.y+a]]), moves))
            if self.x != 0 and boardfilled[self.y+a][self.x-1] == (not self.owner):
                moves = np.concatenate((np.array([[self.x-1, self.y+a]]), moves))
            if self.x != 7 and boardfilled[self.y+a][self.x+1] == (not self.owner):
                moves = np.concatenate((np.array([[self.x+1, self.y+a]]), moves))
            if (not self.owner and self.y == 6) or (self.owner and self.y == 1):
                moves = np.concatenate((np.array([[self.x, self.y+2*a]]), moves))
            moves = moves[:-1]

        elif self.type == 1:  # rook
            rangesize = 4
            dxy_dict = np.array([1, -1, 0, 0, 0, 0, 1, -1])
            moves = self.n_linefinding(dxy_dict, rangesize, moves, boardfilled, sx, sy)
        elif self.type == 2:  # knight
            dxy_dict = np.array([1, 2, 2, 1, -1, -2, 2, 1])
            for r in range(0, 4):
                dx, dy = dxy_dict[r], dxy_dict[r + 2]
                for m in [1, -1]:
                    sx = self.x + m * dx
                    sy = self.y + m * dy
                    if 0 <= sx < 8 and 0 <= sy < 8 and boardfilled[sy][sx] != self.owner:
                        moves = np.concatenate((np.array([[sx, sy]]), moves))
            return moves[:-1]
        elif self.type == 3:  # bishop
            rangesize = 4
            dxy_dict = np.array([1, 1, -1, -1, 1, -1, 1, -1])
            moves = self.n_linefinding(dxy_dict, rangesize, moves, boardfilled, sx, sy)
        elif self.type == 4:  # queen
            dxy_dict = np.array([1, -1, 0, 0, 1, 1, -1, -1, 0, 0, 1, -1, 1, -1, 1, -1])
            rangesize = 8
            moves = self.n_linefinding(dxy_dict, rangesize, moves, boardfilled, sx, sy)
        elif self.type == 5:  # king
            for sx in [self.x-1, self.x, self.x+1]:
                for sy in [self.y-1, self.y, self.y+1]:
                    if 0 <= sx < 8 and 0 <= sy < 8 and (sx+sy != 0):
                        moves = np.concatenate((np.array([[sx, sy]]), moves))
            moves = moves[:-1]

        return self.trimmoves(boardfilled, moves)

    def trimmoves(self, boardfilled, moves):  # removes the moves that would be blocked by the players own pieces
        loop = 0
        for m in moves:
            if boardfilled[m[1]][m[0]] == self.owner:
                moves = np.delete(moves, loop, 0)
                loop = loop-1
            loop = loop+1
        return moves

    def n_linefinding(self, dxy_dict, rangesize, moves, boardfilled, sx, sy):
        for r in range(0, rangesize):
            dx, dy, stop, start = dxy_dict[r], dxy_dict[r + rangesize], False, True
            sx += dx
            sy += dy
            if not (sx >= 8 or sy >= 8 or sx <= -1 or sy <= -1):
                while not stop and 0 <= sx <= 7 and 0 <= sy <= 7:
                    try:
                        if boardfilled[sy][sx] == -1:
                            moves = np.concatenate((np.array([[sx, sy]]), moves))
                            sx += dx
                            sy += dy
                        else:
                            moves = np.concatenate((np.array([[sx, sy]]), moves))
                            sx, sy = self.x, self.y
                            stop = True
                    except IndexError:
                        print(IndexError)
                        break
            sx, sy = self.x, self.y
        return moves[:-1]
