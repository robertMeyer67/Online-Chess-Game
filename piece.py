import pygame
import os

bBishop = pygame.image.load(os.path.join("img", "black_bishop.png"))
bKing = pygame.image.load(os.path.join("img", "black_king.png"))
bKnight = pygame.image.load(os.path.join("img", "black_knight.png"))
bPawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
bQueen = pygame.image.load(os.path.join("img", "black_queen.png"))
bRook = pygame.image.load(os.path.join("img", "black_rook.png"))

wBishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
wKing = pygame.image.load(os.path.join("img", "white_king.png"))
wKnight = pygame.image.load(os.path.join("img", "white_knight.png"))
wPawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
wQueen = pygame.image.load(os.path.join("img", "white_queen.png"))
wRook = pygame.image.load(os.path.join("img", "white_rook.png"))

blackImages = [bBishop, bKing, bKnight, bPawn, bQueen, bRook]
whiteImages= [wBishop, wKing, wKnight, wPawn, wQueen, wRook]

transformedBlackImages = []
transformedWhiteImages = []

for img in blackImages:
    transformedBlackImages.append(pygame.transform.scale(img, (55, 55)))

for img in whiteImages:
    transformedWhiteImages.append(pygame.transform.scale(img, (55, 55)))


class Piece:
    img = -1
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, row, col, color):
        self._row = row
        self._col = col
        self._color = color
        self._selected = False
        self._moveList = []
        self._king = False
        self._pawn = False
    
    # Getters
    def get_row(self):
        return self._row

    def get_col(self):
        return self._col

    def get_color(self):
        return self._color

    def is_selected(self):
        return self._selected

    def get_moveList(self):
        return self._moveList

    def is_king(self):
        return self._king

    def is_pawn(self):
        return self._pawn

    # Setters
    def set_row(self, row):
        self._row = row

    def set_col(self, col):
        self._col = col

    def set_color(self, color):
        self._color = color

    def set_selected(self, selected):
        self._selected = selected

    def set_moveList(self, moveList):
        self._moveList = moveList

    def set_king(self, king):
        self._king = king

    def set_pawn(self, pawn):
        self._pawn = pawn

    def isSelected(self):
        return self._selected

    def update_valid_moves(self, board):
        self._moveList = self.valid_moves(board)

    def draw(self, win, color):
        """
        :param win: canvas, color: tuple
        :return: None
        """
        
        if self._color == "w":
            drawThis = W[self.img]
        else:
            drawThis = B[self.img]

        xCoordinate = (4 - self._col) + round(self.startX + (self._col * self.rect[2] / 8))
        yCoordinate = 3 + round(self.startY + (self._row * self.rect[3] / 8))

        if self._selected and self._color == color:
            pygame.draw.rect(win, (255, 0, 0), (xCoordinage, yCoordinate, 62, 62), 4)

        win.blit(drawThis, (xCoordinate, yCoordinate))

        '''if self._selected and self._color == color:  # Remove false to draw dots
            moves = self._moveList

            for move in moves:
                x = 33 + round(self.startX + (move[0] * self.rect[2] / 8))
                y = 33 + round(self.startY + (move[1] * self.rect[3] / 8))
                pygame.draw.circle(win, (255, 0, 0), (x, y), 10)'''

    def change_pos(self, pos):
        """
        :param pos: list
        :return: None
        """
        
        self._row = pos[0]
        self._col = pos[1]

    def __str__(self):
        """
        :return: str
        """
        
        return str(self._col) + " " + str(self._row)


class Bishop(Piece):
    img = 0

    def valid_moves(self, board):
        """
        :param board: Board
        :return: list
        """
        
        i = self._row
        j = self._col

        moves = []

        # TOP RIGHT
        diagonalJumpLeft = j + 1
        diagonalJumpRight = j - 1
        for di in range(i - 1, -1, -1):
            if diagonalJumpLeft < 8:
                possibleMove = board[di][diagonalJumpLeft]
                if possibleMove == 0:
                    moves.append((diagonalJumpLeft, di))
                elif possibleMove.color != self._color:
                    moves.append((diagonalJumpLeft, di))
                    break
                else:
                    break
            else:
                break

            diagonalJumpLeft += 1

        for di in range(i - 1, -1, -1):
            if diagonalJumpRight > -1:
                possibleMove = board[di][diagonalJumpRight]
                if possibleMove == 0:
                    moves.append((diagonalJumpRight, di))
                elif possibleMove.color != self._color:
                    moves.append((diagonalJumpRight, di))
                    break
                else:
                    break
            else:
                break

            diagonalJumpRight -= 1

        # TOP LEFT
        diagonalJumpLeft = j + 1
        diagonalJumpRight = j - 1
        for di in range(i + 1, 8):
            if diagonalJumpLeft < 8:
                possibleMove = board[di][diagonalJumpLeft]
                if possibleMove == 0:
                    moves.append((diagonalJumpLeft, di))
                elif possibleMove.color != self._color:
                    moves.append((diagonalJumpLeft, di))
                    break
                else:
                    break
            else:
                break
            diagonalJumpLeft += 1
        for di in range(i + 1, 8):
            if diagonalJumpRight > -1:
                possibleMove = board[di][diagonalJumpRight]
                if possibleMove == 0:
                    moves.append((diagonalJumpRight, di))
                elif possibleMove.color != self._color:
                    moves.append((diagonalJumpRight, di))
                    break
                else:
                    break
            else:
                break

            diagonalJumpRight -= 1

        return moves


class King(Piece):
    img = 1

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self._king = True

    def valid_moves(self, board):
        """
        :param board: Board
        :return: list
        """
        
        i = self._row
        j = self._col

        moves = []

        if i > 0:
            # TOP LEFT
            if j > 0:
                possibleMove = board[i - 1][j - 1]
                if possibleMove == 0:
                    moves.append((j - 1, i - 1,))
                elif possibleMove.color != self._color:
                    moves.append((j - 1, i - 1,))

            # TOP MIDDLE
            possibleMove = board[i - 1][j]
            if possibleMove == 0:
                moves.append((j, i - 1))
            elif possibleMove.color != self._color:
                moves.append((j, i - 1))

            # TOP RIGHT
            if j < 7:
                possibleMove = board[i - 1][j + 1]
                if possibleMove == 0:
                    moves.append((j + 1, i - 1,))
                elif possibleMove.color != self._color:
                    moves.append((j + 1, i - 1,))

        if i < 7:
            # BOTTOM LEFT
            if j > 0:
                possibleMove = board[i + 1][j - 1]
                if possibleMove == 0:
                    moves.append((j - 1, i + 1,))
                elif possibleMove.color != self._color:
                    moves.append((j - 1, i + 1,))

            # BOTTOM MIDDLE
            possibleMove = board[i + 1][j]
            if possibleMove == 0:
                moves.append((j, i + 1))
            elif possibleMove.color != self._color:
                moves.append((j, i + 1))

            # BOTTOM RIGHT
            if j < 7:
                possibleMove = board[i + 1][j + 1]
                if possibleMove == 0:
                    moves.append((j + 1, i + 1))
                elif possibleMove.color != self._color:
                    moves.append((j + 1, i + 1))

        # MIDDLE LEFT
        if j > 0:
            possibleMove = board[i][j - 1]
            if possibleMove == 0:
                moves.append((j - 1, i))
            elif possibleMove.color != self._color:
                moves.append((j - 1, i))

        # MIDDLE RIGHT
        if j < 7:
            possibleMove = board[i][j + 1]
            if possibleMove == 0:
                moves.append((j + 1, i))
            elif possibleMove.color != self._color:
                moves.append((j + 1, i))

        return moves


class Knight(Piece):
    img = 2

    def valid_moves(self, board):
        """
        :param board: Board
        :return: list
        """
        
        i = self._row
        j = self._col

        moves = []

        # DOWN LEFT
        if i < 6 and j > 0:
            possibleMove = board[i + 2][j - 1]
            if possibleMove == 0:
                moves.append((j - 1, i + 2))
            elif possibleMove.color != self._color:
                moves.append((j - 1, i + 2))

        # UP LEFT
        if i > 1 and j > 0:
            possibleMove = board[i - 2][j - 1]
            if possibleMove == 0:
                moves.append((j - 1, i - 2))
            elif possibleMove.color != self._color:
                moves.append((j - 1, i - 2))

        # DOWN RIGHT
        if i < 6 and j < 7:
            possibleMove = board[i + 2][j + 1]
            if possibleMove == 0:
                moves.append((j + 1, i + 2))
            elif possibleMove.color != self._color:
                moves.append((j + 1, i + 2))

        # UP RIGHT
        if i > 1 and j < 7:
            possibleMove = board[i - 2][j + 1]
            if possibleMove == 0:
                moves.append((j + 1, i - 2))
            elif possibleMove.color != self._color:
                moves.append((j + 1, i - 2))

        if i > 0 and j > 1:
            possibleMove = board[i - 1][j - 2]
            if possibleMove == 0:
                moves.append((j - 2, i - 1))
            elif possibleMove.color != self._color:
                moves.append((j - 2, i - 1))

        if i > 0 and j < 6:
            possibleMove = board[i - 1][j + 2]
            if possibleMove == 0:
                moves.append((j + 2, i - 1))
            elif possibleMove.color != self._color:
                moves.append((j + 2, i - 1))

        if i < 7 and j > 1:
            possibleMove = board[i + 1][j - 2]
            if possibleMove == 0:
                moves.append((j - 2, i + 1))
            elif possibleMove.color != self._color:
                moves.append((j - 2, i + 1))

        if i < 7 and j < 6:
            possibleMove = board[i + 1][j + 2]
            if possibleMove == 0:
                moves.append((j + 2, i + 1))
            elif possibleMove.color != self._color:
                moves.append((j + 2, i + 1))

        return moves


class Pawn(Piece):
    img = 3

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self._first = True
        self._queen = False
        self._pawn = True

    # Getters
    def is_first(self):
        return self._first

    def is_queen(self):
        return self._queen

    # Setters
    def set_first(self, first):
        self._first = first

    def set_queen(self, queen):
        self._queen = queen


    def valid_moves(self, board):
        """
        :param board: Board
        :return: list
        """
        
        i = self._row
        j = self._col

        moves = []
        try:
            if self._color == "b":
                if i < 7:
                    possibleMove = board[i + 1][j]
                    if possibleMove == 0:
                        moves.append((j, i + 1))

                    # DIAGONAL
                    if j < 7:
                        possibleMove = board[i + 1][j + 1]
                        if possibleMove != 0:
                            if possibleMove.color != self._color:
                                moves.append((j + 1, i + 1))

                    if j > 0:
                        possibleMove = board[i + 1][j - 1]
                        if possibleMove != 0:
                            if possibleMove.color != self._color:
                                moves.append((j - 1, i + 1))

                if self._first:
                    if i < 6:
                        possibleMove = board[i + 2][j]
                        if possibleMove == 0:
                            if board[i + 1][j] == 0:
                                moves.append((j, i + 2))
                        elif possibleMove.color != self._color:
                            moves.append((j, i + 2))
            # WHITE
            else:

                if i > 0:
                    possibleMove = board[i - 1][j]
                    if possibleMove == 0:
                        moves.append((j, i - 1))

                if j < 7:
                    possibleMove = board[i - 1][j + 1]
                    if possibleMove != 0:
                        if possibleMove.color != self._color:
                            moves.append((j + 1, i - 1))

                if j > 0:
                    possibleMove = board[i - 1][j - 1]
                    if possibleMove != 0:
                        if possibleMove.color != self._color:
                            moves.append((j - 1, i - 1))

                if self._first:
                    if i > 1:
                        possibleMove = board[i - 2][j]
                        if possibleMove == 0:
                            if board[i - 1][j] == 0:
                                moves.append((j, i - 2))
                        elif possibleMove.color != self._color:
                            moves.append((j, i - 2))
        except Exception as e:
            print(f'Error while finding valid moves for pawn at row {self._row} column {self._col}: {e}')
            pass

        return moves


class Queen(Piece):
    img = 4

    def valid_moves(self, board):
        """
        :param board: Board
        :return: list
        """
        
        i = self._row
        j = self._col

        moves = []

        # TOP RIGHT
        diagonalJumpLeft = j + 1
        diagonalJumpRight = j - 1
        for di in range(i - 1, -1, -1):
            if diagonalJumpLeft < 8:
                possibleMove = board[di][diagonalJumpLeft]
                if possibleMove == 0:
                    moves.append((diagonalJumpLeft, di))
                elif possibleMove.color != self._color:
                    moves.append((diagonalJumpLeft, di))
                    break
                else:
                    diagonalJumpLeft = 9

            diagonalJumpLeft += 1

        for di in range(i - 1, -1, -1):
            if diagonalJumpRight > -1:
                possibleMove = board[di][diagonalJumpRight]
                if possibleMove == 0:
                    moves.append((diagonalJumpRight, di))
                elif possibleMove.color != self._color:
                    moves.append((diagonalJumpRight, di))
                    break
                else:
                    diagonalJumpRight = -1

            diagonalJumpRight -= 1

        # TOP LEFT
        diagonalJumpLeft = j + 1
        diagonalJumpRight = j - 1
        for di in range(i + 1, 8):
            if diagonalJumpLeft < 8:
                possibleMove = board[di][diagonalJumpLeft]
                if possibleMove == 0:
                    moves.append((diagonalJumpLeft, di))
                elif possibleMove.color != self._color:
                    moves.append((diagonalJumpLeft, di))
                    break
                else:
                    diagonalJumpLeft = 9
            diagonalJumpLeft += 1
        for di in range(i + 1, 8):
            if diagonalJumpRight > -1:
                possibleMove = board[di][diagonalJumpRight]
                if possibleMove == 0:
                    moves.append((diagonalJumpRight, di))
                elif possibleMove.color != self._color:
                    moves.append((diagonalJumpRight, di))
                    break
                else:
                    diagonalJumpRight = -1

            diagonalJumpRight -= 1

        # UP
        for x in range(i - 1, -1, -1):
            possibleMove = board[x][j]
            if possibleMove == 0:
                moves.append((j, x))
            elif possibleMove.color != self._color:
                moves.append((j, x))
                break
            else:
                break

        # DOWN
        for x in range(i + 1, 8, 1):
            possibleMove = board[x][j]
            if possibleMove == 0:
                moves.append((j, x))
            elif possibleMove.color != self._color:
                moves.append((j, x))
                break
            else:
                break

        # LEFT
        for x in range(j - 1, -1, -1):
            possibleMove = board[i][x]
            if possibleMove == 0:
                moves.append((x, i))
            elif possibleMove.color != self._color:
                moves.append((x, i))
                break
            else:
                break

        # RIGHT
        for x in range(j + 1, 8, 1):
            possibleMove = board[i][x]
            if possibleMove == 0:
                moves.append((x, i))
            elif possibleMove.color != self._color:
                moves.append((x, i))
                break
            else:
                break

        return moves


class Rook(Piece):
    img = 5

    def valid_moves(self, board):
        """
        :param board: Board
        :return: list
        """
        
        i = self._row
        j = self._col

        moves = []

        # UP
        for x in range(i - 1, -1, -1):
            possibleMove = board[x][j]
            if possibleMove == 0:
                moves.append((j, x))
            elif possibleMove.color != self._color:
                moves.append((j, x))
                break
            else:
                break

        # DOWN
        for x in range(i + 1, 8, 1):
            possibleMove = board[x][j]
            if possibleMove == 0:
                moves.append((j, x))
            elif possibleMove.color != self._color:
                moves.append((j, x))
                break
            else:
                break

        # LEFT
        for x in range(j - 1, -1, -1):
            possibleMove = board[i][x]
            if possibleMove == 0:
                moves.append((x, i))
            elif possibleMove.color != self._color:
                moves.append((x, i))
                break
            else:
                break

        # RIGHT
        for x in range(j + 1, 8, 1):
            possibleMove = board[i][x]
            if possibleMove == 0:
                moves.append((x, i))
            elif possibleMove.color != self._color:
                moves.append((x, i))
                break
            else:
                break

        return moves

