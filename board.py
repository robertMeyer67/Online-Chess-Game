from piece import Bishop
from piece import King
from piece import Rook
from piece import Pawn
from piece import Queen
from piece import Knight
import time
import pygame


class Board:
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols

        self._ready = False

        self._last = None

        self._copy = True

        self._board = [[0 for x in range(8)] for _ in range(rows)]

        self._board[0][0] = Rook(0, 0, "b")
        self._board[0][1] = Knight(0, 1, "b")
        self._board[0][2] = Bishop(0, 2, "b")
        self._board[0][3] = Queen(0, 3, "b")
        self._board[0][4] = King(0, 4, "b")
        self._board[0][5] = Bishop(0, 5, "b")
        self._board[0][6] = Knight(0, 6, "b")
        self._board[0][7] = Rook(0, 7, "b")

        self._board[1][0] = Pawn(1, 0, "b")
        self._board[1][1] = Pawn(1, 1, "b")
        self._board[1][2] = Pawn(1, 2, "b")
        self._board[1][3] = Pawn(1, 3, "b")
        self._board[1][4] = Pawn(1, 4, "b")
        self._board[1][5] = Pawn(1, 5, "b")
        self._board[1][6] = Pawn(1, 6, "b")
        self._board[1][7] = Pawn(1, 7, "b")

        self._board[7][0] = Rook(7, 0, "w")
        self._board[7][1] = Knight(7, 1, "w")
        self._board[7][2] = Bishop(7, 2, "w")
        self._board[7][3] = Queen(7, 3, "w")
        self._board[7][4] = King(7, 4, "w")
        self._board[7][5] = Bishop(7, 5, "w")
        self._board[7][6] = Knight(7, 6, "w")
        self._board[7][7] = Rook(7, 7, "w")

        self._board[6][0] = Pawn(6, 0, "w")
        self._board[6][1] = Pawn(6, 1, "w")
        self._board[6][2] = Pawn(6, 2, "w")
        self._board[6][3] = Pawn(6, 3, "w")
        self._board[6][4] = Pawn(6, 4, "w")
        self._board[6][5] = Pawn(6, 5, "w")
        self._board[6][6] = Pawn(6, 6, "w")
        self._board[6][7] = Pawn(6, 7, "w")

        self._p1Name = "Player 1"
        self._p2Name = "Player 2"

        self._turn = "w"

        self._time1 = 900
        self._time2 = 900

        self._storedtime1 = 0
        self._storedtime2 = 0

        self._winner = None

        self._startTime = time.time()

    # Getters
    def get_rows(self):
        return self._rows

    def get_cols(self):
        return self._cols

    def is_ready(self):
        return self._ready

    def get_last(self):
        return self._last

    def is_copy(self):
        return self._copy

    def get_board(self):
        return self._board

    def get_p1Name(self):
        return self._p1Name

    def get_p2Name(self):
        return self._p2Name

    def get_turn(self):
        return self._turn

    def get_time1(self):
        return self._time1

    def get_time2(self):
        return self._time2

    def get_storedtime1(self):
        return self._storedtime1

    def get_storedtime2(self):
        return self._storedtime2

    def get_winner(self):
        return self._winner

    def get_startTime(self):
        return self._startTime

    # Setters
    def set_rows(self, rows):
        self._rows = rows

    def set_cols(self, cols):
        self._cols = cols

    def set_ready(self, ready):
        self._ready = ready

    def set_last(self, last):
        self._last = last

    def set_copy(self, copy):
        self._copy = copy

    def set_board(self, board):
        self._board = board

    def set_p1Name(self, name):
        self._p1Name = name

    def set_p2Name(self, name):
        self._p2Name = name

    def set_turn(self, turn):
        self._turn = turn

    def set_time1(self, time1):
        self._time1 = time1

    def set_time2(self, time2):
        self._time2 = time2

    def set_storedtime1(self, storedtime1):
        self._storedtime1 = storedtime1

    def set_storedtime2(self, storedtime2):
        self._storedtime2 = storedtime2

    def set_winner(self, winner):
        self._winner = winner

    def set_startTime(self, startTime):
        self._startTime = startTime

    def update_moves(self):
        """
        :param none
        :return: none
        """

        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    self._board[i][j].update_valid_moves(self._board)

    def draw(self, win, color):
        """
        :param win: str, color: tuple
        :return: void
        """
        if self.last and color == self._turn:
            yLastStart, xLastStart = self.last[0]
            yLastEnd, xLastEnd = self.last[1]

            xLastStartCoord = (4 - xLastStart) +round(self.startX + (xLastStart * self.rect[2] / 8))
            yLastStartCoord = 3 + round(self.startY + (yLastStart * self.rect[3] / 8))
            pygame.draw.circle(win, (0,0,255), (xLastStartCoord+32, yLastStartCoord+30), 34, 4)
            xLastEndCoord = (4 - xLastStart) + round(self.startX + (xLastEnd * self.rect[2] / 8))
            yLastEndCoord = 3+ round(self.startY + (yLastEnd * self.rect[3] / 8))
            pygame.draw.circle(win, (0, 0, 255), (xLastEndCoord + 32, yLastEndCoord + 30), 34, 4)

        s = None
        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    self._board[i][j].draw(win, color)
                    if self._board[i][j].isSelected:
                        s = (i, j)


    def get_dangerMoves(self, color):
        """
        :param color: tuple
        :return: dangerMoves: list
        """

        dangerMoves = []
        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    if self._board[i][j].get_color() != color:
                        for move in self._board[i][j].get_moveList():
                            dangerMoves.append(move)

        return dangerMoves

    def is_checked(self, color):
        """
        :param color: tuple
        :return: bool
        """

        self.update_moves()
        dangerMoves = self.get_dangerMoves(color)
        king_pos = (-1, -1)
        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    if self._board[i][j].is_king() and self._board[i][j].get_color() == color:
                        king_pos = (j, i)

        if king_pos in dangerMoves:
            return True

        return False

    def select(self, col, row, color):
        """
        :param col: int, row: int, color: tuple
        :return: None
        """
        
        changed = False
        prev = (-1, -1)
        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    if self._board[i][j].is_selected():
                        prev = (i, j)

        # if piece
        if self._board[row][col] == 0 and prev!=(-1,-1):
            moves = self._board[prev[0]][prev[1]].get_moveList()
            if (col, row) in moves:
                changed = self.move(prev, (row, col), color)

        else:
            if prev == (-1,-1):
                self.reset_selected()
                if self._board[row][col] != 0:
                    self._board[row][col].set_selected(True)
            else:
                if self._board[prev[0]][prev[1]].get_color() != self._board[row][col].get_color():
                    moves = self._board[prev[0]][prev[1]].get_moveList()
                    if (col, row) in moves:
                        changed = self.move(prev, (row, col), color)

                    if self._board[row][col].get_color == color:
                        self._board[row][col].set_selected(True)

                else:
                    if self._board[row][col].get_color == color:
                        #castling
                        self.reset_selected()
                        if self._board[prev[0]][prev[1]].moved == False and self._board[prev[0]][prev[1]].rook and self._board[row][col].is_king() and col != prev[1] and prev!=(-1,-1):
                            castle = True
                            if prev[1] < col:
                                for j in range(prev[1]+1, col):
                                    if self._board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed = self.move(prev, (row, 3), color)
                                    changed = self.move((row,col), (row, 2), color)
                                if not changed:
                                    self._board[row][col].set_selected(True)

                            else:
                                for j in range(col+1,prev[1]):
                                    if self._board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed = self.move(prev, (row, 6), color)
                                    changed = self.move((row,col), (row, 5), color)
                                if not changed:
                                    self._board[row][col].set_selected(True)
                            
                        else:
                            self._board[row][col].set_selected(True)

        if changed:
            if self._turn == "w":
                self._turn = "b"
                self.reset_selected()
            else:
                self._turn = "w"
                self.reset_selected()

    def reset_selected(self):
        """
        :param None
        :return: None
        """
        
        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    self._board[i][j].set_selected(False)

    def check_mate(self, color):
        """
        :param color: tuple
        :return: bool
        """
        
        '''if self.is_checked(color):
            king = None
            for i in range(self._rows):
                for j in range(self._cols):
                    if self._board[i][j] != 0:
                        if self._board[i][j].king and self._board[i][j].color == color:
                            king = self._board[i][j]
            if king is not None:
                valid_moves = king.valid_moves(self._board)

                dangerMoves = self.get_dangerMoves(color)

                danger_count = 0

                for move in valid_moves:
                    if move in dangerMoves:
                        danger_count += 1
                return danger_count == len(valid_moves)'''

        return False

    def move(self, start, end, color):
        """
        :param start: list, end: list, color: tuple
        :return: bool
        """
        
        checkedBefore = self.is_checked(color)
        changed = True
        nBoard = self._board[:]
        if nBoard[start[0]][start[1]].is_pawn():
            nBoard[start[0]][start[1]].set_first(False)

        nBoard[start[0]][start[1]].change_pos((end[0], end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self._board = nBoard

        if self.is_checked(color) or (checkedBefore and self.is_checked(color)):
            changed = False
            nBoard = self._board[:]
            if nBoard[end[0]][end[1]].is_pawn():
                nBoard[end[0]][end[1]].set_first(True)

            nBoard[end[0]][end[1]].change_pos((start[0], start[1]))
            nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
            nBoard[end[0]][end[1]] = 0
            self._board = nBoard
        else:
            self.reset_selected()

        self.update_moves()
        if changed:
            self.last = [start, end]
            if self._turn == "w":
                self._storedtime1 += (time.time() - self._startTime)
            else:
                self._storedtime2 += (time.time() - self._startTime)
            self._startTime = time.time()

        return changed
