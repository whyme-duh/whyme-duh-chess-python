import pygame as p

class Pieces():
    def __init__(self):
        self.board = [
            ['bR', 'bN','bB','bQ','bK','bB','bN','bR'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.moveFnc = {'p' : self.getPawnMoves,
                        'R': self.getRookMoves,
                        'N' : self.getKnightMoves,
                        'Q' : self.getQueenMoves,
                        'B' : self.getBishopMoves ,
                        'K' : self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.elpassantMove = False     # for the elpassant sound
        self.castling = False          # for the castling sound
        self.enpassantPossible = ()   # coordinates of the sqaure where en passant capture is possible
        self.currentcastlingRights = Castle(True, True, True, True)
        self.castleRightLogs = [Castle(self.currentcastlingRights.wks, self.currentcastlingRights.bks, self.currentcastlingRights.wqs,self.currentcastlingRights.bqs )]

    """
    Takes a move as a parameter and execute it(this will not work for castling , pawn promotion and el passant"""
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "-"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)   # log the move so we can change it later
        self.whiteToMove = not self.whiteToMove   # it switched the player
        # updates the location of the king if it is moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        # for pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'  # gets the color and adds  the Q for queen

        # enpassant move
        if move.isElpassantMove:
            self.elpassantMove = True
            self.board[move.startRow][move.endCol] = '-'  # capturing the pawn

        # update the enpassant possible tuple
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:   # starting row and ending row will be two row apart, only on two sqaure advance
            self.enpassantPossible = ((move.startRow + move.endRow) //2, move.startCol)
        else:
            self.enpassantPossible = ()

        # FOR CASTLING
        if move.isCastleMove:
            self.castling = True
            if move.endCol - move.startCol == 2:    # king side
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol+1]         # moves the rook into the new sqaure
                self.board[move.endRow][move.endCol + 1] = '-'   # erase the previous place of rook
            else:                                   # queen side
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol - 2]  = '-'

        """update castling rights -> whenever a rook or king  moves"""
        self.updateCastleRights(move)
        self.castleRightLogs.append(Castle(self.currentcastlingRights.wks, self.currentcastlingRights.bks ,self.currentcastlingRights.wqs,self.currentcastlingRights.bqs))

    """
    updates the castle rights"""
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentcastlingRights.wks = False
            self.currentcastlingRights.wqs = False
        elif move.pieceMoved == "bK":
            self.currentcastlingRights.bks = False
            self.currentcastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:   #left rook
                    self.currentcastlingRights.wqs = False
                elif move.startCol == 7:        # right rook
                    self.currentcastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentcastlingRights.bqs = False
                elif move.startCol == 7:  # right rook
                    self.currentcastlingRights.bks = False

    """
    Undo the last move"""

    def undoMove(self):
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] =  move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            # undo the enpassant move
            if move.isElpassantMove:
                self.board[move.endRow][move.endCol] = '-'  # leave the landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)

            # undo a 2 sqaure pawn move
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()


            # undoing the castle rights
            self.castleRightLogs.pop()   # getting rid of new castle right
            self.currentcastlingRights = self.castleRightLogs[-1]   # setting the current castle rights to the last one of the list

            #undoing the castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:   # kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '-'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '-'


    """
    Reset Board  """
    def reset_board(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.moveFnc = {'p': self.getPawnMoves,
                        'R': self.getRookMoves,
                        'N': self.getKnightMoves,
                        'Q': self.getQueenMoves,
                        'B': self.getBishopMoves,
                        'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()  # coordinates of the sqaure where en passant capture is possible
        self.currentcastlingRights = Castle(True, True, True, True)
        self.castleRightLogs = [
            Castle(self.currentcastlingRights.wks, self.currentcastlingRights.bks, self.currentcastlingRights.wqs,
                   self.currentcastlingRights.bqs)]



    '''
    All move considering checks
    '''
    def getValidMoves(self):
        """
        1. Generate all the possible moves
        2. for each move , make a move
        3. generate all the opp moves
        4. check if any move attacks you king
        5. and if they do then that is not a legal move
        """
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = Castle(self.currentcastlingRights.wks, self.currentcastlingRights.bks, self.currentcastlingRights.wqs, self.currentcastlingRights.bqs)    # copy the current castling rights
        moves = self.getAllPossibleMoves()               # for now we wil not worry about checks
        if self.whiteToMove:
            self.getCastlingMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastlingMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        for i in range(len(moves)-1, -1, -1):            # when removing from the list go backward through that list
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove      # switched the turn as makeMove switch the turns
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:                               #either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        self.currentcastlingRights = tempCastleRights
        return moves
    """
    all moves considering checks
    """

    def inCheck(self):
        if self.whiteToMove:
            return self.sqUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.sqUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    def sqUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove   # switch the turn to opponent
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove   # switch it back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False


    """
    All moves without considering checks"""
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):   # no. of rows
            for c in range(len(self.board[r])):    # no. of cols in given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFnc[piece](r, c, moves)       # calls the appropriate move function ase on peice type

        return moves

    '''
    Get all the pawn moves for the pawn located row, col amd add these moves to the list and so on for other peices'''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:   # white turn to move
            if self.board[r-1][c] == "-":   # one square pawn advance
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "-":                # 2 square advance
                    moves.append(Move((r,c), (r-2, c), self.board))
            if c-1 >= 0:    # not to let the piece to go offboard to he left, these are capture to the left
                if self.board[r-1][c-1][0] == 'b': # if there is enemy move to capture
                    moves.append(Move((r, c), (r - 1, c-1), self.board))
                if (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantPossible = True))

            if c+1 <= 7:   # capture to the right
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c+ 1), self.board))
                if (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantPossible = True))
        """
        
        For a black turn    
        """

        if not self.whiteToMove:   # white turn to move
            if self.board[r + 1][c] == "-":   # one square pawn advance
                moves.append(Move((r,c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "-":                # 2 square advance
                    moves.append(Move((r,c), (r+2, c), self.board))
            if c-1 >= 0:    # not to let the piece to go offboard to he left, these are capture to the left
                if self.board[r+1][c-1][0] == 'w':       # if there is enemy move to capture
                    moves.append(Move((r, c), (r + 1, c-1), self.board))
                if (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantPossible = True))
            if c+1 <= 7:   # capture to the right
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c+ 1), self.board))
                if (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantPossible = True))
                    

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0 ), (0, -1), (1, 0), (0, 1))   # up left down right
        enemycolor = 'b' if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:     # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "-" :
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemycolor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:    # friendly piece available
                        break
                else:    # off board
                    break

    def getKnightMoves(self, r, c, moves):
        knight_moves = ((-2, 1), (-2, -1), (2, -1), (2, 1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        allycolor = "w" if self.whiteToMove else "b"
        for m in knight_moves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allycolor:     # not an ally piece (empty or enemy piece)
                    moves.append(Move((r,c ), (endRow, endCol), self.board))


    def getKingMoves(self, r, c, moves):
        king_moves = ((1, 0), (1, -1), (-1, -1), (-1, 1), (0,1), (-1, 0), (0,-1),(1, 1))
        allycolor = "w" if self.whiteToMove else "b"
        for k in king_moves :
            endRow = r + k[0]
            endCol = c + k[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allycolor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))



    """
    generate all the valid moves for the castling moves for king"""

    def getCastlingMoves(self, r, c ,moves):
        if self.sqUnderAttack(r, c):
            return    # cant castle
        if (self.whiteToMove and self.currentcastlingRights.wks == True) or (not self.whiteToMove and self.currentcastlingRights.bks == True):
            self.KingSideCastleMoves(r, c , moves)
        if (self.whiteToMove and self.currentcastlingRights.wqs == True) or (not self.whiteToMove and self.currentcastlingRights.bqs == True):
            self.QueenSideCastleMoves(r,c , moves)


    def KingSideCastleMoves(self,r ,c , moves):
        if self.board[r][c + 1] == '-' and self.board[r][c+ 2] == '-':
            if not self.sqUnderAttack(r, c + 1) and not self.sqUnderAttack(r, c +2):
                moves.append(Move((r,c), (r,c + 2), self.board, isCastleMove = True))


    def QueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '-' and self.board[r][c - 2] == '-':
            if not self.sqUnderAttack(r, c - 1) and not self.sqUnderAttack(r, c - 2):
                moves.append(Move((r, c),(r, c - 2), self.board, isCastleMove=True))


    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemycolor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '-':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemycolor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def getQueenMoves(self, r, c, moves):
        # done by using abstraction method
        self.getRookMoves(r,c, moves)
        self.getBishopMoves(r,c ,moves)


"""
CLASS FOR CASTLING"""
class Castle:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs




class Move():

    # maps keys to values
    #key ; value
    rankToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in rankToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4,
                   "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSquare, endSquare, board, isEnpassantPossible = False, isCastleMove = False):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7)
        # enpassant
        self.isElpassantMove = isEnpassantPossible
        if self.isElpassantMove:
            self.pieceCaptured = 'bp' if self.pieceMoved == 'wp' else 'wp'

        # for castling
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    '''
    Overriding the eqauls methods'''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.filesToCols[r]































